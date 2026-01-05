import pytesseract
import pdfplumber
from PIL import Image
import os


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class FileProcessorService:
    IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/jpg"]
    PDF_MIME_TYPE = "application/pdf"

    def extract_text(self, file_path: str, mime_type: str | None) -> str:
        if not mime_type:
            return ""

        if mime_type in self.IMAGE_MIME_TYPES:
            return self._extract_from_image(file_path)

        if mime_type == self.PDF_MIME_TYPE:
            return self._extract_from_pdf(file_path)

        return ""
    
    def _extract_from_image(self, file_path: str) -> str:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image, lang="por")
        return text.strip()
    
    def _extract_from_pdf(self, file_path: str) -> str:
        text = ""

        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        return text.strip()
    
file_processor_service = FileProcessorService()