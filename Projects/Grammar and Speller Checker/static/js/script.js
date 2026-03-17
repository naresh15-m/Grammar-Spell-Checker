// Main JavaScript for Grammar & Spell Checker

document.addEventListener('DOMContentLoaded', function() {
    // Text form submission
    const textForm = document.getElementById('textForm');
    if (textForm) {
        textForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const textInput = document.getElementById('textInput');
            const text = textInput.value.trim();
            
            if (!text) {
                showError('Please enter some text to check');
                return;
            }
            
            // Show loading spinner
            showLoading(true);
            hideError();
            
            try {
                const formData = new FormData();
                formData.append('text', text);
                
                const response = await fetch('/check', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Save results to localStorage and redirect
                    localStorage.setItem('checkResults', JSON.stringify(data));
                    window.location.href = '/result';
                } else {
                    showError(data.error || 'An error occurred while checking the text');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                showLoading(false);
            }
        });
    }
    
    // File form submission
    const fileForm = document.getElementById('fileForm');
    if (fileForm) {
        fileForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const fileInput = document.getElementById('fileInput');
            const file = fileInput.files[0];
            
            if (!file) {
                showError('Please select a file to upload');
                return;
            }
            
            // Check file size (16MB max)
            if (file.size > 16 * 1024 * 1024) {
                showError('File size exceeds 16MB limit');
                return;
            }
            
            // Show loading spinner
            showLoading(true);
            hideError();
            
            try {
                const formData = new FormData();
                formData.append('file', file);
                
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    // Save results to localStorage and redirect
                    localStorage.setItem('checkResults', JSON.stringify(data));
                    window.location.href = '/result';
                } else {
                    showError(data.error || 'An error occurred while processing the file');
                }
            } catch (error) {
                showError('Network error: ' + error.message);
            } finally {
                showLoading(false);
            }
        });
    }
    
    // File input change event
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = this.files[0];
            if (file) {
                // Validate file type
                const validTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
                if (!validTypes.includes(file.type) && 
                    !file.name.endsWith('.txt') && 
                    !file.name.endsWith('.pdf') && 
                    !file.name.endsWith('.docx')) {
                    showError('Please upload a valid file (TXT, PDF, or DOCX)');
                    this.value = '';
                }
            }
        });
    }
    
    // Helper functions
    function showLoading(show) {
        const spinner = document.getElementById('loadingSpinner');
        if (spinner) {
            if (show) {
                spinner.classList.remove('d-none');
            } else {
                spinner.classList.add('d-none');
            }
        }
    }
    
    function showError(message) {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.classList.remove('d-none');
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                hideError();
            }, 5000);
        }
    }
    
    function hideError() {
        const errorDiv = document.getElementById('errorMessage');
        if (errorDiv) {
            errorDiv.classList.add('d-none');
        }
    }
    
    // Auto-resize textarea
    const textarea = document.getElementById('textInput');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }
    
    // Add drag and drop functionality for file upload
    const fileTab = document.getElementById('file');
    if (fileTab) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            fileTab.addEventListener(eventName, preventDefaults, false);
        });
        
        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }
        
        ['dragenter', 'dragover'].forEach(eventName => {
            fileTab.addEventListener(eventName, highlight, false);
        });
        
        ['dragleave', 'drop'].forEach(eventName => {
            fileTab.addEventListener(eventName, unhighlight, false);
        });
        
        function highlight(e) {
            fileTab.classList.add('bg-light');
        }
        
        function unhighlight(e) {
            fileTab.classList.remove('bg-light');
        }
        
        fileTab.addEventListener('drop', handleDrop, false);
        
        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            
            if (files.length > 0) {
                const fileInput = document.getElementById('fileInput');
                fileInput.files = files;
                
                // Trigger change event
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        }
    }
});