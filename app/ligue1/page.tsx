import Link from 'next/link';

const clubs = [
  { id: 'angers', name: 'Angers', ville: 'Angers' },
  { id: 'auxerre', name: 'Auxerre', ville: 'Auxerre' },
  { id: 'brest', name: 'Brest', ville: 'Brest' },
  { id: 'le-havre', name: 'Le Havre', ville: 'Le Havre' },
  { id: 'lens', name: 'Lens', ville: 'Lens' },
  { id: 'lille', name: 'Lille', ville: 'Lille' },
  { id: 'lorient', name: 'Lorient', ville: 'Lorient' },
  { id: 'lyon', name: 'Lyon', ville: 'Lyon' },
  { id: 'marseille', name: 'Marseille', ville: 'Marseille' },
  { id: 'metz', name: 'Metz', ville: 'Metz' },
  { id: 'monaco', name: 'Monaco', ville: 'Monaco' },
  { id: 'nantes', name: 'Nantes', ville: 'Nantes' },
  { id: 'nice', name: 'Nice', ville: 'Nice' },
  { id: 'paris-saint-germain', name: 'Paris-Saint-Germain', ville: 'Paris' },
  { id: 'paris-fc', name: 'Paris FC', ville: 'Paris' },
  { id: 'rennes', name: 'Rennes', ville: 'Rennes' },
  { id: 'strasbourg', name: 'Strasbourg', ville: 'Strasbourg' },
  { id: 'toulouse', name: 'Toulouse', ville: 'Toulouse' }
];

export default function Ligue1Page() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l'accueil
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">Ligue 1 - Saison 2025/26</h1>
        
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