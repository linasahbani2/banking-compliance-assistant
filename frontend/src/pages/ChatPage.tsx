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

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    const response = await fetch(
      `${API_URL}/api/ask?question=${encodeURIComponent(question)}`
    );
    const data = await response.json();

    setMessages((prev) => [...prev, data]);
    setQuestion("");
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Assistant IA</h2>
        <div className="flex gap-3">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="Pose une question sur tes documents..."
            className="flex-1 border rounded px-3 py-2"
          />
          <button
            onClick={handleAsk}
            disabled={loading}
            className="bg-blue-700 text-white px-4 py-2 rounded disabled:opacity-50"
          >
            {loading ? "..." : "Envoyer"}
          </button>
        </div>
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