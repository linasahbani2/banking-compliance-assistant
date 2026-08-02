from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base
from sqlalchemy import ForeignKey

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    type = Column(String(50))
    chemin_fichier = Column(String(500))
    date_upload = Column(DateTime(timezone=True), server_default=func.now())

from pgvector.sqlalchemy import Vector

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    texte = Column(String)
    embedding = Column(Vector(384))