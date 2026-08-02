from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    texte_complet = ""
    for page in reader.pages:
        texte_complet += page.extract_text() or ""
    return texte_complet

from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_into_chunks(texte: str) -> list[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_text(texte)
    return chunks