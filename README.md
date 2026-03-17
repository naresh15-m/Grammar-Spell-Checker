# Grammar-Spell-Checker
Grammar & Spell Checker Web Application
A powerful full-stack web application for real-time grammar and spell checking built with Python Flask. The application supports both direct text input and file uploads (TXT, PDF, DOCX), providing comprehensive error detection and correction.

📋 Features
Real-time Text Checking: Type or paste text directly for instant grammar and spell checking

File Upload Support: Upload and check TXT, PDF, and DOCX files (up to 16MB)

Dual Correction Methods:

TextBlob for spelling error detection

GingerIt API (with local fallback) for grammar checking

Comprehensive Statistics: View detailed error breakdown (total words, spelling errors, grammar errors)

Responsive Design: Works seamlessly on desktop, tablet, and mobile devices

User-Friendly Interface: Clean, modern UI with Bootstrap 5 and Font Awesome icons

Error Highlighting: Clearly displays original errors and their corrections

🛠️ Technology Stack
Backend: Python 3.x, Flask

Frontend: HTML5, CSS3, JavaScript, Bootstrap 5

Libraries:

TextBlob (spelling correction)

GingerIt API (grammar checking)

PyPDF2 (PDF text extraction)

python-docx (DOCX text extraction)

Cloudscraper (bypass Cloudflare)

📁 Project Structure
grammar-spell-checker/
│
├── app.py                    # Main Flask application
├── gingerit_local.py         # Local GingerIt implementation
├── requirements.txt          # Python dependencies
├── uploads/                  # Temporary file upload directory
│
├── static/
│   ├── css/
│   │   └── style.css        # Custom CSS styles
│   └── js/
│       └── script.js         # Frontend JavaScript
│
└── templates/
    ├── index.html            # Main input page
    └── result.html           # Results display page

