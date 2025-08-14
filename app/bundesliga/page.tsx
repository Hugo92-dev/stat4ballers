import Link from 'next/link';

const clubs = [
  { id: 'augsburg', name: 'Augsburg', ville: 'Augsbourg' },
  { id: 'leverkusen', name: 'Leverkusen', ville: 'Leverkusen' },
  { id: 'bayern', name: 'Bayern', ville: 'Munich' },
  { id: 'dortmund', name: 'Dortmund', ville: 'Dortmund' },
  { id: 'monchengladbach', name: 'Mönchengladbach', ville: 'Mönchengladbach' },
  { id: 'eintracht-frankfurt', name: 'Eintracht Frankfurt', ville: 'Francfort' },
  { id: 'cologne', name: 'Cologne', ville: 'Cologne' },
  { id: 'fribourg', name: 'Fribourg', ville: 'Fribourg' },
  { id: 'hambourg', name: 'Hambourg', ville: 'Hambourg' },
  { id: 'heidenheim', name: 'Heidenheim', ville: 'Heidenheim' },
  { id: 'hoffenheim', name: 'Hoffenheim', ville: 'Hoffenheim' },
  { id: 'mainz-05', name: 'Mainz 05', ville: 'Mayence' },
  { id: 'rb-leipzig', name: 'RB Leipzig', ville: 'Leipzig' },
  { id: 'sankt-pauli', name: 'Sankt Pauli', ville: 'Hambourg' },
  { id: 'stuttgart', name: 'Stuttgart', ville: 'Stuttgart' },
  { id: 'union-berlin', name: 'Union Berlin', ville: 'Berlin' },
  { id: 'werder', name: 'Werder', ville: 'Brême' },
  { id: 'wolfsbourg', name: 'Wolfsbourg', ville: 'Wolfsbourg' }
];

export default function BundesligaPage() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l&apos;accueil
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">Bundesliga - Saison 2025/26</h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clubs.map(club => (
            <Link 
              key={club.id}
              href={`/bundesliga/${club.id}`}
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