import { useEffect, useState } from "react";

interface Document {
  id: number;
  nom: string;
  type: string;
  chemin_fichier: string;
  date_upload: string;
}

const API_URL = "http://localhost:8000";

function App() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);

  const fetchDocuments = async () => {
    const response = await fetch(`${API_URL}/api/documents`);
    const data = await response.json();
    setDocuments(data);
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append("file", selectedFile);

    await fetch(`${API_URL}/api/documents`, {
      method: "POST",
      body: formData,
    });

    setSelectedFile(null);
    setUploading(false);
    fetchDocuments();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-blue-900 mb-6">
          Banking Compliance & Audit Assistant
        </h1>

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
              className="bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50"
            >
              {uploading ? "Envoi..." : "Uploader"}
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Documents</h2>
          {documents.length === 0 ? (
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
    </div>
  );
}

export default App;