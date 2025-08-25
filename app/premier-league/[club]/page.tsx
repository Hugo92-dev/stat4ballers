import ClubPageEnhanced from '@/components/ClubPageEnhanced';
import { premierLeagueTeams } from '@/data/premierLeagueTeams';

export default function ClubPage({ params }: { params: { club: string } }) {
  // Gérer les alias d'URLs
  const slugAliases: Record<string, string> = {
    'west-ham': 'west-ham-united',
    'brighton': 'brighton-hove-albion',
    'brighton-&-hove-albion': 'brighton-hove-albion',
    'man-city': 'manchester-city',
    'man-united': 'manchester-united',
    'newcastle': 'newcastle-united',
  };
  
  const actualSlug = slugAliases[params.club] || params.club;
  
  // Trouver le club dans les données
  const club = premierLeagueTeams.find(c => c.slug === actualSlug);
  
  if (!club) {
    return (
      <main className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Club non trouvé</h1>
          <a href="/premier-league" className="text-blue-400 hover:underline">
            Retour à la Premier League
          </a>
        </div>
      </main>
    );
  }

  return (
    <ClubPageEnhanced
      clubId={actualSlug}
      clubName={club.nom}
      leagueId="premier-league"
      leagueName="Premier League"
      teams={premierLeagueTeams}
      primaryColor="#38003c"
      secondaryColor="#ffffff"
    />
  );
}