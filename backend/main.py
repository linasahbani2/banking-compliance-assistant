from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import shutil
import os
from text_extraction import extract_text_from_pdf, split_text_into_chunks, generate_embedding, generate_answer
import models
import schemas
from database import get_db, engine
from fastapi.middleware.cors import CORSMiddleware
from compliance_rules import REGLES_CONFORMITE
from database import Base, engine


app = FastAPI(title="Banking Compliance & Audit Assistant API")
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/api/documents/{document_id}/index")
def index_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()
    if not document:
        return {"error": "Document non trouvé"}

    texte = extract_text_from_pdf(document.chemin_fichier)
    chunks = split_text_into_chunks(texte)

    chunks_crees = 0
    for chunk_texte in chunks:
        embedding = generate_embedding(chunk_texte)
        nouveau_chunk = models.DocumentChunk(
            document_id=document_id,
            texte=chunk_texte,
            embedding=embedding
        )
        db.add(nouveau_chunk)
        chunks_crees += 1

    db.commit()

    return {
        "document_id": document_id,
        "chunks_indexes": chunks_crees
    }

@app.get("/api/search")
def search_chunks(question: str, db: Session = Depends(get_db)):
    embedding_question = generate_embedding(question)

    resultats = (
        db.query(models.DocumentChunk)
        .order_by(models.DocumentChunk.embedding.cosine_distance(embedding_question))
        .limit(3)
        .all()
    )

    return {
        "question": question,
        "resultats": [
            {"document_id": r.document_id, "texte": r.texte}
            for r in resultats
        ]
    }

@app.get("/api/ask")
def ask_question(question: str, db: Session = Depends(get_db)):
    embedding_question = generate_embedding(question)

    resultats = (
        db.query(models.DocumentChunk)
        .order_by(models.DocumentChunk.embedding.cosine_distance(embedding_question))
        .limit(3)
        .all()
    )

    contexte = "\n\n".join([r.texte for r in resultats])
    reponse = generate_answer(question, contexte)

    return {
        "question": question,
        "reponse": reponse,
        "sources": [{"document_id": r.document_id, "extrait": r.texte[:100]} for r in resultats]
    }


@app.post("/api/dossiers", response_model=schemas.DossierOut)
def create_dossier(dossier: schemas.DossierCreate, db: Session = Depends(get_db)):
    nouveau_dossier = models.Dossier(
        nom=dossier.nom,
        type_dossier=dossier.type_dossier
    )
    db.add(nouveau_dossier)
    db.commit()
    db.refresh(nouveau_dossier)
    return nouveau_dossier


@app.get("/api/dossiers", response_model=List[schemas.DossierOut])
def list_dossiers(db: Session = Depends(get_db)):
    return db.query(models.Dossier).all()


@app.post("/api/dossiers/{dossier_id}/documents")
def add_document_to_dossier(
    dossier_id: int,
    document: schemas.DossierDocumentCreate,
    db: Session = Depends(get_db)
):
    lien = models.DossierDocument(
        dossier_id=dossier_id,
        document_id=document.document_id,
        type_document=document.type_document
    )
    db.add(lien)
    db.commit()
    return {"message": "Document rattaché au dossier"}


@app.get("/api/dossiers/{dossier_id}/analyse")
def analyser_dossier(dossier_id: int, db: Session = Depends(get_db)):
    dossier = db.query(models.Dossier).filter(models.Dossier.id == dossier_id).first()
    if not dossier:
        return {"error": "Dossier non trouvé"}

    documents_requis = REGLES_CONFORMITE.get(dossier.type_dossier, [])

    documents_fournis = (
        db.query(models.DossierDocument)
        .filter(models.DossierDocument.dossier_id == dossier_id)
        .all()
    )
    types_fournis = [doc.type_document for doc in documents_fournis]

    documents_manquants = [t for t in documents_requis if t not in types_fournis]
    documents_presents = [t for t in documents_requis if t in types_fournis]

    conforme = len(documents_manquants) == 0

    return {
        "dossier_id": dossier_id,
        "type_dossier": dossier.type_dossier,
        "conforme": conforme,
        "documents_presents": documents_presents,
        "documents_manquants": documents_manquants
    }


@app.get("/api/dossiers/{dossier_id}/rapport")
def generer_rapport(dossier_id: int, db: Session = Depends(get_db)):
    dossier = db.query(models.Dossier).filter(models.Dossier.id == dossier_id).first()
    if not dossier:
        return {"error": "Dossier non trouvé"}

    documents_requis = REGLES_CONFORMITE.get(dossier.type_dossier, [])
    documents_fournis = (
        db.query(models.DossierDocument)
        .filter(models.DossierDocument.dossier_id == dossier_id)
        .all()
    )
    types_fournis = [doc.type_document for doc in documents_fournis]
    documents_manquants = [t for t in documents_requis if t not in types_fournis]

    prompt = f"""Tu es un assistant d'audit bancaire. Rédige un rapport court et structuré pour le dossier suivant.

Nom du dossier : {dossier.nom}
Type de dossier : {dossier.type_dossier}
Documents fournis : {", ".join(types_fournis) if types_fournis else "aucun"}
Documents manquants : {", ".join(documents_manquants) if documents_manquants else "aucun"}

Rédige le rapport avec 3 parties claires :
1. Résumé
2. Anomalies détectées (documents manquants, s'il y en a)
3. Recommandations

Réponds en français, de manière professionnelle et concise."""

    rapport = generate_answer(dossier.nom, prompt)

    return {
        "dossier_id": dossier_id,
        "nom": dossier.nom,
        "rapport": rapport
    }


@app.get("/api/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_documents = db.query(models.Document).count()
    total_dossiers = db.query(models.Dossier).count()

    dossiers = db.query(models.Dossier).all()

    dossiers_conformes = 0
    dossiers_non_conformes = 0

    for dossier in dossiers:
        documents_requis = REGLES_CONFORMITE.get(dossier.type_dossier, [])
        documents_fournis = (
            db.query(models.DossierDocument)
            .filter(models.DossierDocument.dossier_id == dossier.id)
            .all()
        )
        types_fournis = [doc.type_document for doc in documents_fournis]
        manquants = [t for t in documents_requis if t not in types_fournis]

        if len(manquants) == 0:
            dossiers_conformes += 1
        else:
            dossiers_non_conformes += 1

    repartition_types = {}
    for dossier in dossiers:
        repartition_types[dossier.type_dossier] = repartition_types.get(dossier.type_dossier, 0) + 1

    return {
        "total_documents": total_documents,
        "total_dossiers": total_dossiers,
        "dossiers_conformes": dossiers_conformes,
        "dossiers_non_conformes": dossiers_non_conformes,
        "repartition_types": repartition_types
    }