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

from sentence_transformers import SentenceTransformer

modele_embedding = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(texte: str) -> list[float]:
    vecteur = modele_embedding.encode(texte)
    return vecteur.tolist()

import ollama

def generate_answer(question: str, contexte: str) -> str:
    prompt = f"""Tu es un assistant qui répond aux questions en te basant uniquement sur le contexte fourni ci-dessous.

Contexte :
{contexte}

Question : {question}

Réponds en français, de manière claire et concise, en te basant uniquement sur le contexte donné."""

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]