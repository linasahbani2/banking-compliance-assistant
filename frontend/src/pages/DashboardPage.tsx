import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";

interface Stats {
  total_documents: number;
  total_dossiers: number;
  dossiers_conformes: number;
  dossiers_non_conformes: number;
  repartition_types: Record<string, number>;
}

const API_URL = "http://localhost:8000";
const COLORS = ["#1d4ed8", "#7c3aed", "#059669", "#d97706"];

function DashboardPage() {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    fetch(`${API_URL}/api/dashboard/stats`)
      .then((res) => res.json())
      .then((data) => setStats(data));
  }, []);

  if (!stats) return <div className="p-8">Chargement...</div>;

  const conformiteData = [
    { name: "Conformes", value: stats.dossiers_conformes },
    { name: "Non conformes", value: stats.dossiers_non_conformes },
  ];

  const typesData = Object.entries(stats.repartition_types).map(([name, value]) => ({
    name,
    value,
  }));

  return (
    <div className="max-w-4xl mx-auto p-8">
      <div className="grid grid-cols-2 gap-6 mb-6">
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <p className="text-3xl font-bold text-blue-900">{stats.total_documents}</p>
          <p className="text-gray-500">Documents</p>
        </div>
        <div className="bg-white rounded-lg shadow p-6 text-center">
          <p className="text-3xl font-bold text-blue-900">{stats.total_dossiers}</p>
          <p className="text-gray-500">Dossiers</p>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Conformité des dossiers</h2>
          {stats.total_dossiers === 0 ? (
            <p className="text-gray-500">Aucun dossier pour l'instant.</p>
          ) : (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={conformiteData} dataKey="value" nameKey="name" outerRadius={80} label>
                  {conformiteData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Répartition par type</h2>
          {typesData.length === 0 ? (
            <p className="text-gray-500">Aucun dossier pour l'instant.</p>
          ) : (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={typesData} dataKey="value" nameKey="name" outerRadius={80} label>
                  {typesData.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;