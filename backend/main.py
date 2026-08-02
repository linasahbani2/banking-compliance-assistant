from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import shutil
import os

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