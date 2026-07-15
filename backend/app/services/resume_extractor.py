import pypdf
from docx import Document
from typing import Optional
import io


class ResumeExtractor:
    """Extract text from PDF and DOCX resume files."""
    
    @staticmethod
    def extract_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file content."""
        try:
            pdf_reader = pypdf.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def extract_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file content."""
        try:
            doc = Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Failed to extract text from DOCX: {str(e)}")
    
    @staticmethod
    def extract_text(file_content: bytes, file_type: str) -> str:
        """
        Extract text from resume file based on file type.
        
        Args:
            file_content: Binary content of the file
            file_type: Either 'pdf' or 'docx'
        
        Returns:
            Extracted text as string
        """
        file_type = file_type.lower()
        
        if file_type == 'pdf':
            return ResumeExtractor.extract_from_pdf(file_content)
        elif file_type == 'docx':
            return ResumeExtractor.extract_from_docx(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}. Only PDF and DOCX are supported.")
