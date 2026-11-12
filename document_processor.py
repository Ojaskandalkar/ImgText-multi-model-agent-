import fitz  # PyMuPDF
import docx
from google import genai
import os

def get_image_description(image_bytes: bytes) -> str:
    """Uses Gemini Vision to describe an image or OCR scanned text."""
    client = genai.Client()
    try:
        response = client.models.generate_content(
            model='gemini-3.5-flash-lite',
            contents=[
                "Describe this image in detail. If it contains text, extract it (OCR).",
                {"mime_type": "image/jpeg", "data": image_bytes}
            ]
        )
        return response.text
    except Exception as e:
        return f"[Image Processing Failed: {e}]"

def process_pdf(file_path: str) -> list:
    doc = fitz.open(file_path)
    content = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        page_image_descriptions = []
        
        # OCR Fallback: If no text is found, treat the page as a scanned image
        if not text:
            pix = page.get_pixmap()
            text = get_image_description(pix.tobytes("jpeg"))
            
        # Extract embedded images from the PDF page
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            desc = get_image_description(image_bytes)
            page_image_descriptions.append(desc)
            
        content.append({
            "page": page_num + 1,
            "text": text,
            "image_descriptions": page_image_descriptions
        })
    return content

def process_docx(file_path: str) -> list:
    doc = docx.Document(file_path)
    text_content = []
    
    # Extract paragraphs
    for para in doc.paragraphs:
        if para.text.strip():
            text_content.append(para.text.strip())
            
    # Extract tables
    for table in doc.tables:
        for row in table.rows:
            row_data = [cell.text.strip() for cell in row.cells]
            text_content.append(" | ".join(row_data))
            
    return [{"page": 1, "text": "\n".join(text_content), "image_descriptions": []}]

def process_txt(file_path: str) -> list:
    with open(file_path, 'r', encoding='utf-8') as f:
        return [{"page": 1, "text": f.read(), "image_descriptions": []}]

def process_image(file_path: str) -> list:
    with open(file_path, 'rb') as f:
        img_bytes = f.read()
    desc = get_image_description(img_bytes)
    return [{"page": 1, "text": "", "image_descriptions": [desc]}]

def process_file(file_path: str) -> list:
    ext = file_path.lower().split('.')[-1]
    if ext == 'pdf':
        return process_pdf(file_path)
    elif ext == 'docx':
        return process_docx(file_path)
    elif ext == 'txt':
        return process_txt(file_path)
    elif ext in ['png', 'jpg', 'jpeg']:
        return process_image(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")