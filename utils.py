# utils.py
import io
import os
import re
from xhtml2pdf import pisa
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def convert_html_to_pdf(html_string: str) -> io.BytesIO | None:
    """Takes an HTML string, registers Indic fonts dynamically, and returns a PDF Byte stream."""
    pdf_buffer = io.BytesIO()

    # --- THE DEVANAGARI FONT REGISTRATION PATCH ---
    font_path = "NotoSansDevanagari-Regular.ttf"
    if os.path.exists(font_path):
        try:
            pdfmetrics.registerFont(TTFont('Noto Sans Devanagari', font_path))
        except Exception as e:
            print(f"Warning: Failed to bind Devanagari TTF: {e}")
    # ----------------------------------------------

    pisa_status = pisa.CreatePDF(html_string.encode('utf-8'), dest=pdf_buffer)
    if pisa_status.err:
        return None
        
    pdf_buffer.seek(0)
    return pdf_buffer

def sanitize_html_output(raw_response: str) -> str:
    """Strips markdown codeblocks and returns raw HTML immune to LLM syntax quirks."""
    text = raw_response.strip()
    tblk = "`" * 3  

    if f"{tblk}html" in text:
        text = text.split(f"{tblk}html")[1]
        if tblk in text:
            text = text.split(tblk)[0]
    elif text.startswith(tblk) and text.endswith(tblk):
        text = text[3:-3]

    text = re.sub(r"^html\s*", "", text, flags=re.IGNORECASE).strip()
    return text

def generate_safe_filename(topic: str) -> str:
    """Converts English ('Ohm's Law') AND Indic ('संज्ञा') topics into safe OS filenames."""
    # \w matches alphanumeric characters in ANY script (Latin, Devanagari, etc.)
    safe_name = re.sub(r'[^\w\-]', '_', topic)
    # Collapse accidental double/triple underscores into a single clean underscore
    safe_name = re.sub(r'_+', '_', safe_name).strip('_')
    
    return f"{safe_name.lower()}_masterclass.pdf"