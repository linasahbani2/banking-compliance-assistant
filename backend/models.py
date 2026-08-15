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

class Dossier(Base):
    __tablename__ = "dossiers"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(255), nullable=False)
    type_dossier = Column(String(100), nullable=False)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())


class DossierDocument(Base):
    __tablename__ = "dossier_documents"

    id = Column(Integer, primary_key=True, index=True)
    dossier_id = Column(Integer, ForeignKey("dossiers.id"))
    type_document = Column(String(100), nullable=False)
    document_id = Column(Integer, ForeignKey("documents.id"))