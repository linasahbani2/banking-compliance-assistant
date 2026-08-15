import { useEffect, useState } from "react";

interface Document {
  id: number;
  nom: string;
  type: string;
  chemin_fichier: string;
  date_upload: string;
}

const API_URL = "http://localhost:8000";

function DocumentsPage() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchDocuments = async () => {
    setError(null);
    try {
      const response = await fetch(`${API_URL}/api/documents`);
      if (!response.ok) throw new Error("Erreur serveur");
      const data = await response.json();
      setDocuments(data);
    } catch {
      setError("Impossible de contacter le serveur. Vérifie que le backend est bien lancé.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/api/documents`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Échec de l'upload");

      setSelectedFile(null);
      await fetchDocuments();
    } catch {
      setError("L'upload a échoué. Réessaie ou vérifie ta connexion au serveur.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-6">
          ⚠️ {error}
        </div>
      )}

      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Uploader un document</h2>
        <div className="flex gap-3">
          <input
            type="file"
            onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
            className="flex-1 border rounded px-3 py-2"
          />
          <button
            onClick={handleUpload}
            disabled={!selectedFile || uploading}
            className="bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50 flex items-center gap-2"
          >
            {uploading && (
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            )}
            {uploading ? "Envoi..." : "Uploader"}
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Documents</h2>
        {loading ? (
          <p className="text-gray-500">Chargement...</p>
        ) : documents.length === 0 ? (
          <p className="text-gray-500">Aucun document pour l'instant.</p>
        ) : (
          <ul className="divide-y">
            {documents.map((doc) => (
              <li key={doc.id} className="py-3 flex justify-between">
                <span>{doc.nom}</span>
                <span className="text-sm text-gray-400">
                  {new Date(doc.date_upload).toLocaleDateString()}
                </span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default DocumentsPage;