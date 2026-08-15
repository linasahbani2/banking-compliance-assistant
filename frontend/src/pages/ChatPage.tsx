import { useState } from "react";

interface Source {
  document_id: number;
  extrait: string;
}

interface Message {
  question: string;
  reponse: string;
  sources: Source[];
}

const API_URL = "http://localhost:8000";

function ChatPage() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(
        `${API_URL}/api/ask?question=${encodeURIComponent(question)}`
      );
      if (!response.ok) throw new Error("Erreur serveur");
      const data = await response.json();

      setMessages((prev) => [...prev, data]);
      setQuestion("");
    } catch {
      setError("Impossible d'obtenir une réponse. Vérifie que le backend et Ollama tournent bien.");
    } finally {
      setLoading(false);
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
        <h2 className="text-lg font-semibold mb-4">Assistant IA</h2>
        <div className="flex gap-3">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && !loading && handleAsk()}
            placeholder="Pose une question sur tes documents..."
            disabled={loading}
            className="flex-1 border rounded px-3 py-2 disabled:bg-gray-100"
          />
          <button
            onClick={handleAsk}
            disabled={loading || !question.trim()}
            className="bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50 flex items-center gap-2 whitespace-nowrap"
          >
            {loading && (
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
            )}
            {loading ? "Réflexion..." : "Envoyer"}
          </button>
        </div>
        {loading && (
          <p className="text-sm text-gray-400 mt-2">
            L'assistant lit tes documents, ça peut prendre jusqu'à 30 secondes...
          </p>
        )}
      </div>

      <div className="space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6">
            <p className="font-semibold text-blue-900 mb-2">{msg.question}</p>
            <p className="text-gray-700 mb-3">{msg.reponse}</p>
            <div className="text-xs text-gray-400">
              {msg.sources.length} source(s) trouvée(s)
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ChatPage;