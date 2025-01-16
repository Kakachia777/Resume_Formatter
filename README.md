# Resume Formatter

A simple tool that formats your resume to match company standards with just one click!

## First Time Setup (Mac Users)

1. **Install Python**
   - Visit [Python's Download Page](https://www.python.org/downloads/macos/)
   - Download the latest version
   - Double click the downloaded file
   - Follow the installation wizard

2. **Get the Resume Formatter**
   - Open Terminal
     * Click the magnifying glass (🔍) in top-right corner of your screen
     * Type "Terminal"
     * Click the Terminal app
   - Copy and paste these commands one by one:
     ```
     cd Downloads
     git clone https://github.com/kakachia777/resume_formatter.git
     cd resume_formatter
     python -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

## How to Use (Every Time)

1. **Start the Program**
   - Open Terminal
   - Copy and paste these commands one by one:
     ```
     cd resume_formatter
     source venv/bin/activate
     streamlit run resume_formatter.py
     ```
   - A webpage will open automatically in your browser

2. **Format Your Resume**
   - Click "Browse files" 
   - Select your resume (Word or PDF)
   - Wait a few seconds
   - Click "Download Formatted Resume" when it appears
   - Find your formatted resume in your Downloads folder

## What You'll Get
- Your resume formatted with:
  * Company logo at the top
  * Professional font and spacing
  * Organized sections
  * Clean, consistent look

## Need Help?
If something's not working:
1. Close Terminal
2. Close your browser
3. Start fresh with the "How to Use" steps
4. Still stuck? Contact [support contact]

Note: Make sure you have `optomi_logo.png` in the same folder as the program for the company logo to appear.
