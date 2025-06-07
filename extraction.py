import pymupdf 


def extract_text_from_pdf(pdf_path): 
    text = "" 
    if not pdf_path.endswith('.pdf'): 
        raise ValueError("The provided file is not a PDF.") 
    try:
        doc = pymupdf.open(pdf_path) 
        for page in doc:
            text += page.get_text() + chr(12) + "\n"
    except Exception as e:
        raise RuntimeError(f"An error occurred while extracting text from the PDF: {e}")
    return text 


