from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    texte_complet = ""
    for page in reader.pages:
        texte_complet += page.extract_text() or ""
    return texte_complet