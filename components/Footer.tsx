import Link from 'next/link';

const leagues = [
  { id: 'ligue1', name: 'Ligue 1' },
  { id: 'premier-league', name: 'Premier League' },
  { id: 'liga', name: 'La Liga' },
  { id: 'serie-a', name: 'Serie A' },
  { id: 'bundesliga', name: 'Bundesliga' }
];

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <span className="text-2xl">⚽</span>
              <span className="font-bold text-xl text-white">Stat4Ballers</span>
            </div>
            <p className="text-sm">
              L'analyse complète des statistiques des joueurs des 5 grands championnats européens.
            </p>
          </div>
          
          <div>
            <h3 className="font-semibold text-white mb-4">Championnats</h3>
            <ul className="space-y-2">
              {leagues.map((league) => (
                <li key={league.id}>
                  <Link href={`/${league.id}`} className="hover:text-white transition-colors">
                    {league.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold text-white mb-4">Statistiques</h3>
            <ul className="space-y-2">
              <li>Stats Générales</li>
              <li>Performance Offensive</li>
              <li>Impact Défensif</li>
              <li>Créativité</li>
            </ul>
          </div>
          
          <div>
            <h3 className="font-semibold text-white mb-4">Données</h3>
            <p className="text-sm">
              Données automatiquement mises à jour par notre système API. Garantissant des données à jour et fiables.
            </p>
          </div>
        </div>
        
        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-sm">
          <p>&copy; 2025 Stat4Ballers. Tous droits réservés.</p>
        </div>
      </div>
    </footer>
  );
}