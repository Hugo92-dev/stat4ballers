import Link from 'next/link';

const clubs = [
  { id: 'psg', name: 'Paris Saint-Germain', ville: 'Paris' },
  { id: 'om', name: 'Olympique de Marseille', ville: 'Marseille' },
  { id: 'monaco', name: 'AS Monaco', ville: 'Monaco' },
  { id: 'lille', name: 'LOSC Lille', ville: 'Lille' },
  { id: 'lyon', name: 'Olympique Lyonnais', ville: 'Lyon' },
  { id: 'nice', name: 'OGC Nice', ville: 'Nice' },
  { id: 'lens', name: 'RC Lens', ville: 'Lens' },
  { id: 'rennes', name: 'Stade Rennais', ville: 'Rennes' },
];

export default function Ligue1Page() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l'accueil
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">Ligue 1 - Saison 2024/25</h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clubs.map(club => (
            <Link 
              key={club.id}
              href={`/ligue1/${club.id}`}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition"
            >
              <h2 className="text-2xl font-semibold text-blue-900">{club.name}</h2>
              <p className="text-gray-600 mt-2">📍 {club.ville}</p>
              <p className="text-blue-600 mt-4">Voir l'effectif →</p>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}