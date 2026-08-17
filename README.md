# Banking Compliance & Audit Assistant

Assistant intelligent basé sur l'IA (RAG) pour les équipes conformité et audit bancaire — recherche documentaire intelligente, analyse de conformité automatisée, et génération de rapports d'audit.

##  Contexte

Les équipes conformité et audit d'une banque doivent constamment consulter des procédures internes, circulaires réglementaires et normes qui évoluent régulièrement. Cette plateforme centralise ces documents et permet d'y poser des questions en langage naturel, d'analyser automatiquement la conformité d'un dossier, et de générer des rapports d'audit.

##  Fonctionnalités

- **Base documentaire intelligente** — upload et indexation automatique de documents (PDF, DOCX)
- **Assistant IA (RAG)** — pose une question, obtiens une réponse rédigée avec citation des sources
- **Analyse de conformité** — vérifie automatiquement si un dossier contient tous les documents requis
- **Génération de rapports d'audit** — résumé, anomalies et recommandations générés par IA
- **Risk Dashboard** — vue d'ensemble statistique (documents, dossiers, taux de conformité)

##  Stack technique

- **Frontend** : React, TypeScript, Tailwind CSS, Recharts
- **Backend** : FastAPI (Python), SQLAlchemy
- **Base de données** : PostgreSQL + pgvector (recherche vectorielle)
- **IA** : LangChain, sentence-transformers (embeddings), Ollama (LLM local — phi3)
- **DevOps** : Docker, Docker Compose

##  Confidentialité par conception

Le LLM (phi3) tourne **entièrement en local** via Ollama — aucune donnée sensible ne transite par une API externe, ce qui respecte les contraintes de confidentialité du secteur bancaire.
##  Installation

### Prérequis
- Docker Desktop
- [Ollama](https://ollama.com) installé, avec le modèle `phi3` téléchargé (`ollama pull phi3`)

### Lancer le projet

```bash
docker compose up --build
```

- Frontend : http://localhost:5173
- Backend (API) : http://localhost:8000
- Documentation API : http://localhost:8000/docs

##  Structure du projet

banking-compliance-assistant/
├── backend/ # API FastAPI + pipeline RAG
├── frontend/ # Interface React
└── docker-compose.yml


##  Aperçu

*(captures d'écran à ajouter)*

##  Auteur

Lina Sahbani