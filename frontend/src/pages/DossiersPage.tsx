import { useEffect, useState } from "react";

interface Dossier {
  id: number;
  nom: string;
  type_dossier: string;
  date_creation: string;
}

interface Analyse {
  conforme: boolean;
  documents_presents: string[];
  documents_manquants: string[];
}

const API_URL = "http://localhost:8000";

const TYPES_DOSSIER = ["ouverture_compte_entreprise", "demande_credit"];

function DossiersPage() {
  const [dossiers, setDossiers] = useState<Dossier[]>([]);
  const [nom, setNom] = useState("");
  const [typeDossier, setTypeDossier] = useState(TYPES_DOSSIER[0]);
  const [selectedDossier, setSelectedDossier] = useState<number | null>(null);
  const [analyse, setAnalyse] = useState<Analyse | null>(null);

  const fetchDossiers = async () => {
    const response = await fetch(`${API_URL}/api/dossiers`);
    const data = await response.json();
    setDossiers(data);
  };

  useEffect(() => {
    fetchDossiers();
  }, []);

  const handleCreateDossier = async () => {
    if (!nom.trim()) return;

    await fetch(`${API_URL}/api/dossiers`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nom, type_dossier: typeDossier }),
    });

    setNom("");
    fetchDossiers();
  };

  const handleAnalyser = async (dossierId: number) => {
    setSelectedDossier(dossierId);
    const response = await fetch(`${API_URL}/api/dossiers/${dossierId}/analyse`);
    const data = await response.json();
    setAnalyse(data);
  };

  return (
    <div className="max-w-2xl mx-auto p-8">
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-lg font-semibold mb-4">Créer un dossier</h2>
        <div className="flex gap-3 mb-3">
          <input
            type="text"
            value={nom}
            onChange={(e) => setNom(e.target.value)}
            placeholder="Nom du dossier"
            className="flex-1 border rounded px-3 py-2"
          />
        </div>
        <div className="flex gap-3">
          <select
            value={typeDossier}
            onChange={(e) => setTypeDossier(e.target.value)}
            className="flex-1 border rounded px-3 py-2"
          >
            {TYPES_DOSSIER.map((t) => (
              <option key={t} value={t}>{t}</option>
            ))}
          </select>
          <button
            onClick={handleCreateDossier}
            className="bg-blue-700 text-white px-4 py-2 rounded"
          >
            Créer
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold mb-4">Dossiers</h2>
        {dossiers.length === 0 ? (
          <p className="text-gray-500">Aucun dossier pour l'instant.</p>
        ) : (
          <ul className="divide-y">
            {dossiers.map((d) => (
              <li key={d.id} className="py-3">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-medium">{d.nom}</p>
                    <p className="text-sm text-gray-400">{d.type_dossier}</p>
                  </div>
                  <button
                    onClick={() => handleAnalyser(d.id)}
                    className="text-blue-700 text-sm hover:underline"
                  >
                    Analyser
                  </button>
                </div>

                {selectedDossier === d.id && analyse && (
                  <div className="mt-3 p-3 bg-gray-50 rounded">
                    <p className={analyse.conforme ? "text-green-700 font-semibold" : "text-red-700 font-semibold"}>
                      {analyse.conforme ? "✅ Dossier conforme" : "⚠️ Dossier incomplet"}
                    </p>
                    {analyse.documents_manquants.length > 0 && (
                      <p className="text-sm text-gray-600 mt-1">
                        Documents manquants : {analyse.documents_manquants.join(", ")}
                      </p>
                    )}
                  </div>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}

export default DossiersPage;