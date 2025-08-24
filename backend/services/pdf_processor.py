import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import base64
import io
import re
import os
from typing import Dict, List, Any, Optional
import json
import cv2
import numpy as np

class PDFProcessor:
    def __init__(self):
        """Initialize PDF processor with two processing modes"""
        self.processing_mode = "text_only"  # Options: "text_only", "full_pdf"
        self._load_math_detection_model()
        
    def set_processing_mode(self, mode: str):
        """Set processing mode: 'text_only' or 'full_pdf'"""
        if mode in ["text_only", "full_pdf"]:
            self.processing_mode = mode
        else:
            raise ValueError("Mode must be 'text_only' or 'full_pdf'")
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Task 1: PDF Ingestion & OCR
        Process PDF and extract text, headings, tables, math, and images
        """
        try:
            if self.processing_mode == "text_only":
                return self._process_pdf_text_only(pdf_path)
            else:
                return self._process_pdf_full(pdf_path)
        except Exception as e:
            # Fallback to text-only mode if full processing fails
            try:
                print(f"Full PDF processing failed, falling back to text-only: {e}")
                return self._process_pdf_text_only(pdf_path)
            except Exception as fallback_error:
                raise Exception(f"PDF processing failed completely: {str(fallback_error)}")
    
    def _process_pdf_text_only(self, pdf_path: str) -> Dict[str, Any]:
        """Simple text-only PDF processing (Option 1)"""
        try:
            doc = fitz.open(pdf_path)
            extracted_data = {
                "page": 1,
                "heading": "",
                "paragraphs": [],
                "equations": [],
                "images": [],
                "extracted_text": "",
                "confidence_score": 0.0,
                "processing_mode": "text_only"
            }
            
            all_text = ""
            all_paragraphs = []
            
            # Process first 3 pages for text extraction
            for page_num in range(min(3, len(doc))):
                page = doc.load_page(page_num)
                
                # Extract text
                text = page.get_text()
                all_text += text + "\n"
                
                # Extract paragraphs
                paragraphs = self._extract_paragraphs(text)
                all_paragraphs.extend(paragraphs)
                
                # Extract heading from first page
                if page_num == 0:
                    heading = self._extract_heading(text)
                    extracted_data["heading"] = heading
            
            # Extract math expressions from text
            equations = self._extract_math_expressions(all_text)
            
            extracted_data.update({
                "paragraphs": all_paragraphs[:15],  # Limit to first 15 paragraphs
                "equations": equations[:10],  # Limit to first 10 equations
                "extracted_text": all_text,
                "confidence_score": self._calculate_confidence(all_text, len(all_paragraphs))
            })
            
            doc.close()
            return extracted_data
            
        except Exception as e:
            raise Exception(f"Text-only PDF processing failed: {str(e)}")
    
    def _process_pdf_full(self, pdf_path: str) -> Dict[str, Any]:
        """Full PDF processing with OCR and image extraction (Option 2)"""
        try:
            doc = fitz.open(pdf_path)
            extracted_data = {
                "page": 1,
                "heading": "",
                "paragraphs": [],
                "equations": [],
                "images": [],
                "extracted_text": "",
                "confidence_score": 0.0,
                "processing_mode": "full_pdf"
            }
            
            all_text = ""
            all_paragraphs = []
            all_equations = []
            all_images = []
            
            # Process all pages
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Extract text
                text = page.get_text()
                all_text += text + "\n"
                
                # Extract paragraphs
                paragraphs = self._extract_paragraphs(text)
                all_paragraphs.extend(paragraphs)
                
                # Extract images and process with OCR if needed
                images = self._extract_images(page)
                all_images.extend(images)
                
                # Extract math expressions
                equations = self._extract_math_expressions(text)
                all_equations.extend(equations)
                
                # Extract headings (from first page)
                if page_num == 0:
                    heading = self._extract_heading(text)
                    extracted_data["heading"] = heading
            
            # Process images with OCR if they contain text
            ocr_text = self._process_images_with_ocr(all_images)
            if ocr_text:
                all_text += "\n" + ocr_text
                all_paragraphs.extend(self._extract_paragraphs(ocr_text))
            
            # Process math expressions
            processed_equations = self._process_math_with_free_ocr(all_equations)
            
            extracted_data.update({
                "paragraphs": all_paragraphs[:20],  # Limit to first 20 paragraphs
                "equations": processed_equations,
                "images": [img[:100] + "..." if len(img) > 100 else img for img in all_images[:5]],  # Limit to 5 images
                "extracted_text": all_text,
                "confidence_score": self._calculate_confidence(all_text, len(all_paragraphs))
            })
            
            doc.close()
            return extracted_data
            
        except Exception as e:
            raise Exception(f"Full PDF processing failed: {str(e)}")
    
    def process_text_input(self, text: str) -> Dict[str, Any]:
        """Process plain text input (alternative to PDF)"""
        try:
            extracted_data = {
                "page": 1,
                "heading": self._extract_heading(text),
                "paragraphs": self._extract_paragraphs(text),
                "equations": self._extract_math_expressions(text),
                "images": [],
                "extracted_text": text,
                "confidence_score": self._calculate_confidence(text, len(text.split('\n\n'))),
                "processing_mode": "text_input"
            }
            
            return extracted_data
        except Exception as e:
            raise Exception(f"Text processing failed: {str(e)}")
    
    def _extract_paragraphs(self, text: str) -> List[str]:
        """Extract paragraphs from text"""
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        return [p for p in paragraphs if len(p) > 10]  # Filter out very short paragraphs
    
    def _extract_heading(self, text: str) -> str:
        """Extract main heading from text"""
        lines = text.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip()
            if line and len(line) < 100 and not line.isdigit():
                return line
        return "Untitled Document"
    
    def _extract_images(self, page) -> List[str]:
        """Extract images from page and convert to base64"""
        images = []
        try:
            image_list = page.get_images()
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    pix = fitz.Pixmap(page.parent, xref)
                    
                    if pix.n - pix.alpha < 4:  # GRAY or RGB
                        img_data = pix.tobytes("png")
                        base64_img = base64.b64encode(img_data).decode()
                        images.append(base64_img)
                    
                    pix = None
                except Exception as e:
                    continue
        except Exception as e:
            print(f"Image extraction failed: {e}")
        
        return images
    
    def _extract_math_expressions(self, text: str) -> List[str]:
        """Extract potential math expressions from text"""
        # Common math patterns
        math_patterns = [
            r'\$[^$]+\$',  # LaTeX inline math
            r'\\\[[^\]]+\\\]',  # LaTeX display math
            r'[a-zA-Z]\s*[+\-*/=]\s*[a-zA-Z0-9]',  # Simple equations
            r'[0-9]+\s*[+\-*/]\s*[0-9]+',  # Basic arithmetic
            r'[a-zA-Z]+\s*=\s*[a-zA-Z0-9+\-*/()]+',  # Variable assignments
            r'[a-zA-Z]+\s*\+\s*[a-zA-Z0-9]',  # Addition expressions
            r'[a-zA-Z]+\s*\-\s*[a-zA-Z0-9]',  # Subtraction expressions
            r'[a-zA-Z]+\s*\*\s*[a-zA-Z0-9]',  # Multiplication expressions
            r'[a-zA-Z]+\s*/\s*[a-zA-Z0-9]',  # Division expressions
        ]
        
        equations = []
        for pattern in math_patterns:
            matches = re.findall(pattern, text)
            equations.extend(matches)
        
        return list(set(equations))  # Remove duplicates
    
    def _process_images_with_ocr(self, images: List[str]) -> str:
        """Process images with OCR to extract text"""
        ocr_text = ""
        
        for img_base64 in images[:3]:  # Limit to first 3 images
            try:
                # Decode base64 image
                img_data = base64.b64decode(img_base64)
                img = Image.open(io.BytesIO(img_data))
                
                # Run OCR
                text = pytesseract.image_to_string(img)
                if text.strip():
                    ocr_text += text + "\n"
                    
            except Exception as e:
                continue
        
        return ocr_text
    
    def _load_math_detection_model(self):
        """Load free math detection model (placeholder for future implementation)"""
        # This is a placeholder for future implementation
        # Could use open-source models like:
        # - EasyOCR for general OCR
        # - PaddleOCR for better math recognition
        # - Custom trained models on math datasets
        pass
    
    def _process_math_with_free_ocr(self, equations: List[str]) -> List[str]:
        """Process math expressions with free OCR alternatives"""
        processed_equations = []
        
        for equation in equations[:10]:  # Limit to first 10 equations
            try:
                # Enhanced math pattern recognition
                processed_equation = self._enhance_math_expression(equation)
                processed_equations.append(processed_equation)
                    
            except Exception as e:
                processed_equations.append(equation)
        
        return processed_equations
    
    def _enhance_math_expression(self, equation: str) -> str:
        """Enhance math expression using free tools"""
        # Clean up common OCR artifacts
        equation = re.sub(r'[|]', '1', equation)  # Common OCR mistake
        equation = re.sub(r'[O]', '0', equation)  # Common OCR mistake
        equation = re.sub(r'[l]', '1', equation)  # Common OCR mistake
        
        # Standardize math symbols
        math_replacements = {
            '×': '*',
            '÷': '/',
            '−': '-',
            '±': '+-',
            '≤': '<=',
            '≥': '>=',
            '≠': '!=',
            '≈': '~',
            '∞': 'inf',
            'π': 'pi',
            '√': 'sqrt',
            '²': '^2',
            '³': '^3',
            '⁴': '^4'
        }
        
        for old_symbol, new_symbol in math_replacements.items():
            equation = equation.replace(old_symbol, new_symbol)
        
        return equation
    
    def _calculate_confidence(self, text: str, paragraph_count: int) -> float:
        """Calculate confidence score for extraction quality"""
        if not text:
            return 0.0
        
        # Simple confidence calculation based on text length and paragraph count
        text_length = len(text)
        confidence = min(1.0, (text_length / 1000) * 0.5 + (paragraph_count / 10) * 0.5)
        return round(confidence, 2)
