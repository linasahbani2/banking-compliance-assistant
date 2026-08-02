from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import shutil
import os
from text_extraction import extract_text_from_pdf, split_text_into_chunks, generate_embedding

import models
import schemas
from database import get_db, engine

app = FastAPI(title="Banking Compliance & Audit Assistant API")

@app.get("/")
def read_root():
    return {"message": "L'API fonctionne correctement"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"db_connection": "ok", "result": result.scalar()}

@app.get("/api/documents", response_model=List[schemas.DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).all()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/documents", response_model=schemas.DocumentOut)
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    nouveau_document = models.Document(
        nom=file.filename,
        type=file.content_type,
        chemin_fichier=file_path
    )
    db.add(nouveau_document)
    db.commit()
    db.refresh(nouveau_document)

    return nouveau_document

@app.get("/api/documents/{document_id}/extract-text")
def extract_text(document_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return {"error": "Document non trouvé"}

    texte = extract_text_from_pdf(document.chemin_fichier)
    return {"document_id": document_id, "texte_extrait": texte[:500]}

@app.get("/api/documents/{document_id}/chunks")
def get_document_chunks(document_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return {"error": "Document non trouvé"}

    texte = extract_text_from_pdf(document.chemin_fichier)
    chunks = split_text_into_chunks(texte)

    return {
        "document_id": document_id,
        "nombre_de_chunks": len(chunks),
        "premiers_chunks": chunks[:3]
    }

@app.get("/api/test-embedding")
def test_embedding():
    texte_exemple = "Le contrôle KYC est obligatoire avant validation."
    vecteur = generate_embedding(texte_exemple)
    return {
        "texte": texte_exemple,
        "taille_du_vecteur": len(vecteur),
        "premiers_nombres": vecteur[:5]
    }