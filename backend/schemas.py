from pydantic import BaseModel
from datetime import datetime

class DocumentOut(BaseModel):
    id: int
    nom: str
    type: str | None = None
    chemin_fichier: str | None = None
    date_upload: datetime

    class Config:
        from_attributes = True


class DossierCreate(BaseModel):
    nom: str
    type_dossier: str


class DossierOut(BaseModel):
    id: int
    nom: str
    type_dossier: str
    date_creation: datetime

    class Config:
        from_attributes = True


class DossierDocumentCreate(BaseModel):
    document_id: int
    type_document: str