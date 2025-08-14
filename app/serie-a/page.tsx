import Link from 'next/link';

const clubs = [
  { id: 'ac-milan', name: 'AC Milan', ville: 'Milan' },
  { id: 'atalanta', name: 'Atalanta', ville: 'Bergame' },
  { id: 'bologne', name: 'Bologne', ville: 'Bologne' },
  { id: 'cagliari', name: 'Cagliari', ville: 'Cagliari' },
  { id: 'come', name: 'Côme', ville: 'Côme' },
  { id: 'cremonese', name: 'Cremonese', ville: 'Crémone' },
  { id: 'fiorentina', name: 'Fiorentina', ville: 'Florence' },
  { id: 'genoa', name: 'Genoa', ville: 'Gênes' },
  { id: 'inter', name: 'Inter', ville: 'Milan' },
  { id: 'juventus', name: 'Juventus', ville: 'Turin' },
  { id: 'lazio', name: 'Lazio', ville: 'Rome' },
  { id: 'lecce', name: 'Lecce', ville: 'Lecce' },
  { id: 'naples', name: 'Naples', ville: 'Naples' },
  { id: 'parme', name: 'Parme', ville: 'Parme' },
  { id: 'pise', name: 'Pise', ville: 'Pise' },
  { id: 'roma', name: 'Roma', ville: 'Rome' },
  { id: 'sassuolo', name: 'Sassuolo', ville: 'Sassuolo' },
  { id: 'torino', name: 'Torino', ville: 'Turin' },
  { id: 'udinese', name: 'Udinese', ville: 'Udine' },
  { id: 'hellas-verone', name: 'Hellas Vérone', ville: 'Vérone' }
];

export default function SerieAPage() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l&apos;accueil
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">Serie A - Saison 2025/26</h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clubs.map(club => (
            <Link 
              key={club.id}
              href={`/serie-a/${club.id}`}
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