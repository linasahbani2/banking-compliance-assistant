import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import DocumentsPage from "./pages/DocumentsPage";
import ChatPage from "./pages/ChatPage";
import DossiersPage from "./pages/DossiersPage";

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-blue-900 text-white p-4">
          <div className="max-w-2xl mx-auto flex items-center justify-between">
            <h1 className="text-xl font-bold">Banking Compliance & Audit Assistant</h1>
            <nav className="flex gap-4">
              <Link to="/" className="hover:underline">Documents</Link>
              
              <Link to="/chat" className="hover:underline">Assistant IA</Link>
              <Link to="/dossiers" className="hover:underline">Dossiers</Link>            
            </nav>
          </div>
        </header>

        <Routes>
          <Route path="/" element={<DocumentsPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/dossiers" element={<DossiersPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;