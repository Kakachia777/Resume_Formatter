import streamlit as st
import google.generativeai as genai
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from pdf2docx import Converter
import io
import logging
from typing import List, Dict, Tuple
import re
import os
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Gemini API setup
genai.configure(api_key='AIzaSyDdXpU3bn57KJEbA58rqjdK5yHccpOEbWs')
model = genai.GenerativeModel('gemini-2.0-flash-exp')

class ResumeProcessor:
    def __init__(self, doc: Document):
        self.doc = doc
        self.sections_to_keep = ['EDUCATION', 'PROFESSIONAL EXPERIENCE']
        self.sections_map = {}

    def analyze_document_structure(self) -> Dict[str, List[int]]:
        """
        Analyzes document structure and maps sections to paragraph indices
        """
        current_section = None
        for i, para in enumerate(self.doc.paragraphs):
            text = para.text.strip().upper()
            
            if text and any(text.endswith(section) for section in self.sections_to_keep):
                current_section = text
                if current_section not in self.sections_map:
                    self.sections_map[current_section] = []
                self.sections_map[current_section].append(i)
            elif current_section:
                self.sections_map[current_section].append(i)
                
        logger.info(f"Identified sections: {list(self.sections_map.keys())}")
        return self.sections_map

    def identify_sections_to_remove(self) -> List[str]:
        """
        Uses Gemini to identify sections that should be removed
        """
        text_content = "\n".join([p.text for p in self.doc.paragraphs])
        
        prompt = """
        Analyze this resume and identify sections to remove.
        Keep only:
        1. Education section and its content
        2. Professional Experience section and its content
        
        Return ONLY the exact section names that should be removed (e.g., "SKILLS SUMMARY", "PROFESSIONAL SUMMARY").
        Do not include any explanations or additional text.
        """
        
        try:
            response = model.generate_content(prompt + text_content)
            sections = [section.strip().upper() for section in response.text.split('\n') 
                       if section.strip() and section.strip().upper() not in self.sections_to_keep]
            logger.info(f"Sections to remove: {sections}")
            return sections
        except Exception as e:
            logger.error(f"Error in Gemini API call: {str(e)}")
            raise

    def clean_document(self, sections_to_remove: List[str]) -> None:
        """
        Removes identified sections while preserving document structure and headers
        """
        paragraphs_to_remove = set()
        current_section = None
        in_removal_section = False

        # First pass: mark paragraphs for removal
        for i, para in enumerate(self.doc.paragraphs):
            text = para.text.strip().upper()
            
            if text in sections_to_remove:
                current_section = text
                in_removal_section = True
                paragraphs_to_remove.add(i)
            elif any(text.endswith(section) for section in self.sections_to_keep):
                in_removal_section = False
            elif in_removal_section:
                paragraphs_to_remove.add(i)

        # Remove marked paragraphs in reverse order
        for idx in sorted(paragraphs_to_remove, reverse=True):
            p = self.doc.paragraphs[idx]._element
            p.getparent().remove(p)
            
        logger.info(f"Removed {len(paragraphs_to_remove)} paragraphs")

    def preserve_formatting(self) -> None:
        """
        Ensures formatting is preserved after removal, without underline
        """
        for para in self.doc.paragraphs:
            if para.text.strip().upper() in self.sections_to_keep:
                for run in para.runs:
                    run.font.size = Pt(12)
                    run.font.bold = True
                    run.font.underline = False  # Remove underline
                para.space_after = Pt(12)

def convert_pdf_to_docx(pdf_file) -> Document:
    """
    Converts PDF file to DOCX format
    """
    try:
        # Create temporary files for conversion
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as pdf_temp:
            pdf_temp.write(pdf_file.read())
            pdf_path = pdf_temp.name

        docx_path = pdf_path.replace('.pdf', '.docx')
        
        # Convert PDF to DOCX
        cv = Converter(pdf_path)
        cv.convert(docx_path)
        cv.close()

        # Load the converted document
        doc = Document(docx_path)

        # Clean up temporary files
        os.unlink(pdf_path)
        os.unlink(docx_path)

        return doc

    except Exception as e:
        logger.error(f"Error converting PDF to DOCX: {str(e)}")
        raise

def process_resume(uploaded_file) -> Tuple[Document, str]:
    """
    Main processing function that handles both PDF and DOCX files
    """
    try:
        # Create a copy of the uploaded file in memory
        file_copy = io.BytesIO(uploaded_file.read())
        uploaded_file.seek(0)  # Reset file pointer for potential reuse
        
        # Determine file type and process accordingly
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            doc = convert_pdf_to_docx(file_copy)
        elif file_extension == 'docx':
            doc = Document(file_copy)
        else:
            return None, f"Unsupported file format: {file_extension}"
        
        processor = ResumeProcessor(doc)
        
        # Process the document
        processor.analyze_document_structure()
        sections_to_remove = processor.identify_sections_to_remove()
        processor.clean_document(sections_to_remove)
        processor.preserve_formatting()
        
        return doc, "Success"
        
    except Exception as e:
        logger.error(f"Error processing resume: {str(e)}")
        return None, f"Error: {str(e)}"

def create_streamlit_interface():
    """
    Creates Streamlit interface with support for PDF and DOCX
    """
    st.title('Resume Section Processor')
    st.write("Upload a resume (PDF or DOCX) to remove unnecessary sections while preserving formatting.")
    
    uploaded_file = st.file_uploader("Upload Resume", type=['docx', 'pdf'])
    
    if uploaded_file:
        with st.spinner('Processing document...'):
            doc, message = process_resume(uploaded_file)
            
            if doc:
                bio = io.BytesIO()
                doc.save(bio)
                
                st.success("Document processed successfully!")
                
                # Determine output filename with original extension
                original_name = uploaded_file.name
                output_filename = f"processed_{original_name.rsplit('.', 1)[0]}.docx"
                
                st.download_button(
                    label="Download Processed Resume",
                    data=bio.getvalue(),
                    file_name=output_filename,
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            else:
                st.error(message)

if __name__ == "__main__":
    create_streamlit_interface()