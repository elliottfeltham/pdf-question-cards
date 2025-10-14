import fitz  # PyMuPDF

def extract_all_text(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()            
    doc.close()
    return text
