from flask import Flask, render_template, request, jsonify
from textblob import TextBlob
from gingerit_local import GingerIt
import os
from werkzeug.utils import secure_filename
import PyPDF2
import docx

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_file(file_path, file_type):
    """Extract text from uploaded files"""
    text = ""
    
    if file_type == 'txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    
    elif file_type == 'pdf':
        with open(file_path, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
    
    elif file_type == 'docx':
        doc = docx.Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + '\n'
    
    return text

def check_grammar_spelling(text):
    """Check grammar and spelling using multiple libraries"""
    results = {
        'original_text': text,
        'corrected_text': '',
        'errors': [],
        'statistics': {}
    }
    
    # Method 1: TextBlob for spelling
    blob = TextBlob(text)
    spelling_corrections = []
    
    for word in blob.words:
        if len(word) > 1:  # Skip single characters
            corrected = str(word.correct())
            if corrected.lower() != word.lower():
                spelling_corrections.append({
                    'original': word,
                    'corrected': corrected,
                    'type': 'spelling'
                })
    
    # Method 2: GingerIt for grammar
    parser = GingerIt()
    try:
        ginger_result = parser.parse(text)
        grammar_corrections = []
        
        if ginger_result['corrections']:
            for correction in ginger_result['corrections']:
                grammar_corrections.append({
                    'original': correction['text'],
                    'corrected': correction['correct'],
                    'type': 'grammar',
                    'suggestion': correction.get('suggestion', '')
                })
        
        results['corrected_text'] = ginger_result['result']
    except:
        # Fallback to TextBlob if GingerIt fails
        results['corrected_text'] = str(blob.correct())
        grammar_corrections = []
    
    # Combine corrections
    results['errors'] = spelling_corrections + grammar_corrections
    
    # Calculate statistics
    results['statistics'] = {
        'total_words': len(text.split()),
        'total_errors': len(results['errors']),
        'spelling_errors': len(spelling_corrections),
        'grammar_errors': len(grammar_corrections)
    }
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_text():
    """Handle text input checking"""
    text = request.form.get('text', '')
    
    if not text.strip():
        return jsonify({'error': 'Please enter some text to check'}), 400
    
    results = check_grammar_spelling(text)
    return jsonify(results)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload checking"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        file_type = filename.rsplit('.', 1)[1].lower()
        text = extract_text_from_file(file_path, file_type)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        if not text.strip():
            return jsonify({'error': 'No text could be extracted from the file'}), 400
        
        results = check_grammar_spelling(text)
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500

@app.route('/result')
def result():
    """Render result page"""
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)