# Resume Formatter

A Python-based tool that automatically formats Word document and PDF resumes to a standardized company template using Streamlit and python-docx.

## Features

- Web interface for easy resume uploading and formatting
- Supports both PDF and DOCX file formats
- Standardized formatting:
  - Cambria font throughout
  - Name: 14pt bold, centered at top
  - Section headers: 12pt bold, underlined
  - Body text: 11pt normal
  - Skills section: Two-column layout
  - Dates: Right-aligned
  - Margins: Narrow (0.5" all sides)
- Preserves original content while applying consistent styling
- Exports formatted document with "_formatted" suffix

## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kakachia777/resume-formatter.git
cd resume-formatter
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Web Interface (Recommended)

1. Start the Streamlit app:
```bash
streamlit resume_formatter.py
```

2. Access the interface:
   - Open the URL shown in your terminal (typically http://localhost:8501)
   - Upload your resume (PDF or DOCX)
   - Click "Format Resume" to process
   - Download the formatted version when complete

## File Structure

```
resume-formatter/
├── resume_formatter.py # Main application file with Streamlit interface
├── requirements.txt   # Project dependencies
└── README.md         # This file
```

## Dependencies

- streamlit==1.32.0
- google-generativeai==0.3.2
- python-docx==1.1.0
- pdfminer.six==20231228
- python-dotenv==1.0.1 

## Known Limitations

- Output is always in DOCX format, even for PDF inputs
- May require manual adjustment for complex layouts
- Tables and images may need manual formatting
- PDF conversion may not preserve all formatting perfectly

## Required Files

- `optomi_logo.png` - Place this in the root directory for the header image
