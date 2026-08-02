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