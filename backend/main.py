from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db


app = FastAPI(title="Banking Compliance & Audit Assistant API")

@app.get("/")
def read_root():
    return {"message": "L'API fonctionne correctement"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

from database import engine
from sqlalchemy import text

@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {"db_connection": "ok", "result": result.scalar()}

@app.get("/api/documents", response_model=List[schemas.DocumentOut])
def list_documents(db: Session = Depends(get_db)):
    return db.query(models.Document).all()