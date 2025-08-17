export function generateClubPageContent(clubName: string, clubId: string, league: string) {
  return `import Link from 'next/link';
import { generatePlayers } from '@/utils/playerGenerator';

export default function ${clubId.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join('')}Page() {
  const joueurs = generatePlayers('${clubName}', 15);

  return (
    <main className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <Link href="/${league}" className="text-blue-900 hover:underline mb-4 inline-block">
          ← Retour à la ${league === 'ligue1' ? 'Ligue 1' : 
            league === 'premier-league' ? 'Premier League' :
            league === 'liga' ? 'Liga' :
            league === 'serie-a' ? 'Serie A' :
            'Bundesliga'}
        </Link>
        <h1 className="text-4xl font-bold text-blue-900 mb-8">
          Effectif ${clubName}
        </h1>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {joueurs.map(joueur => (
            <div key={joueur.id} className="bg-white p-6 rounded-lg shadow-md">
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-xl font-semibold text-blue-900">{joueur.nom}</h3>
                <span className="text-2xl font-bold text-gray-400">#{joueur.numero}</span>
              </div>
              <p className="text-gray-600">{joueur.poste}</p>
              <div className="mt-4 text-sm text-gray-500">
                <p>⚽ {joueur.buts} buts • 🅰️ {joueur.passes_decisives} assists</p>
                <p>⏱️ {joueur.minutes} minutes jouées</p>
              </div>
              <Link 
                href={\`/${league}/${clubId}/\${joueur.id}\`}
                className="mt-4 text-blue-600 hover:underline inline-block"
              >
                Voir les stats complètes →
              </Link>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}`;
}