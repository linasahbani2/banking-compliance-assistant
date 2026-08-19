CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    type VARCHAR(150),
    chemin_fichier VARCHAR(500),
    date_upload TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    texte TEXT NOT NULL,
    embedding VECTOR(384)
);

CREATE TABLE IF NOT EXISTS dossiers (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    type_dossier VARCHAR(100) NOT NULL,
    date_creation TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS dossier_documents (
    id SERIAL PRIMARY KEY,
    dossier_id INTEGER REFERENCES dossiers(id),
    type_document VARCHAR(100) NOT NULL,
    document_id INTEGER REFERENCES documents(id)
);