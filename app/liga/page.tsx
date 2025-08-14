import Link from 'next/link';

const clubs = [
  { id: 'deportivo-alaves', name: 'Deportivo Alavés', ville: 'Vitoria-Gasteiz' },
  { id: 'ath-bilbao', name: 'Ath. Bilbao', ville: 'Bilbao' },
  { id: 'atletico-madrid', name: 'Atlético Madrid', ville: 'Madrid' },
  { id: 'barcelone', name: 'Barcelone', ville: 'Barcelone' },
  { id: 'celta-vigo', name: 'Celta Vigo', ville: 'Vigo' },
  { id: 'elche', name: 'Elche', ville: 'Elche' },
  { id: 'espanyol', name: 'Espanyol', ville: 'Barcelone' },
  { id: 'getafe', name: 'Getafe', ville: 'Getafe' },
  { id: 'girona', name: 'Girona', ville: 'Girona' },
  { id: 'levante', name: 'Levante', ville: 'Valence' },
  { id: 'majorque', name: 'Majorque', ville: 'Palma' },
  { id: 'osasuna', name: 'Osasuna', ville: 'Pampelune' },
  { id: 'rayo', name: 'Rayo', ville: 'Madrid' },
  { id: 'betis', name: 'Betis', ville: 'Séville' },
  { id: 'real-madrid', name: 'Real Madrid', ville: 'Madrid' },
  { id: 'real-oviedo', name: 'Real Oviedo', ville: 'Oviedo' },
  { id: 'real-sociedad', name: 'Real Sociedad', ville: 'Saint-Sébastien' },
  { id: 'seville', name: 'Séville', ville: 'Séville' },
  { id: 'valence', name: 'Valence', ville: 'Valence' },
  { id: 'villarreal', name: 'Villarreal', ville: 'Villarreal' }
];

export default function LigaPage() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l&apos;accueil
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">Liga - Saison 2025/26</h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clubs.map(club => (
            <Link 
              key={club.id}
              href={`/liga/${club.id}`}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition"
            >
              <h2 className="text-2xl font-semibold text-blue-900">{club.name}</h2>
              <p className="text-gray-600 mt-2">📍 {club.ville}</p>
              <p className="text-blue-600 mt-4">Voir l&apos;effectif →</p>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}