```tsx
import Link from 'next/link';

// Données temporaires pour tester
const clubs = [
  { id: 'psg', name: 'Paris Saint-Germain', slug: 'psg' },
  { id: 'om', name: 'Olympique de Marseille', slug: 'om' },
  { id: 'ol', name: 'Olympique Lyonnais', slug: 'ol' },
  // On ajoutera les autres clubs après
];

export default function Ligue1Page() {
  return (
    <main className="min-h-screen bg-[--background] py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-[--primary] mb-8">Ligue 1 - Saison 2024/25</h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {clubs.map(club => (
            <Link 
              key={club.id}
              href={`/ligue1/${club.slug}`}
              className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition"
            >
              <h2 className="text-2xl font-semibold text-[--primary]">{club.name}</h2>
              <p className="text-gray-600 mt-2">Voir l'effectif →</p>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
```