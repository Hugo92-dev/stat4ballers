import Link from 'next/link';

const clubs = [
  { id: 'arsenal', name: 'Arsenal', ville: 'Londres' },
  { id: 'aston-villa', name: 'Aston Villa', ville: 'Birmingham' },
  { id: 'bournemouth', name: 'Bournemouth', ville: 'Bournemouth' },
  { id: 'brentford', name: 'Brentford', ville: 'Londres' },
  { id: 'brighton', name: 'Brighton', ville: 'Brighton' },
  { id: 'burnley', name: 'Burnley', ville: 'Burnley' },
  { id: 'chelsea', name: 'Chelsea', ville: 'Londres' },
  { id: 'crystal-palace', name: 'Crystal Palace', ville: 'Londres' },
  { id: 'everton', name: 'Everton', ville: 'Liverpool' },
  { id: 'fulham', name: 'Fulham', ville: 'Londres' },
  { id: 'leeds-united', name: 'Leeds United', ville: 'Leeds' },
  { id: 'liverpool', name: 'Liverpool', ville: 'Liverpool' },
  { id: 'manchester-city', name: 'Manchester City', ville: 'Manchester' },
  { id: 'manchester-united', name: 'Manchester United', ville: 'Manchester' },
  { id: 'newcastle', name: 'Newcastle', ville: 'Newcastle' },
  { id: 'nottm-forest', name: 'Nottm Forest', ville: 'Nottingham' },
  { id: 'sunderland', name: 'Sunderland', ville: 'Sunderland' },
  { id: 'tottenham', name: 'Tottenham', ville: 'Londres' },
  { id: 'west-ham', name: 'West Ham', ville: 'Londres' },
  { id: 'wolves', name: 'Wolves', ville: 'Wolverhampton' }
];

export default function PremierLeaguePage() {
  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à l&apos;accueil
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">Premier League - Saison 2025/26</h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clubs.map(club => (
            <Link 
              key={club.id}
              href={`/premier-league/${club.id}`}
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