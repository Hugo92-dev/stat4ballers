import ClubPagePremierLeague from '@/components/ClubPagePremierLeague';
import { premierLeagueTeams } from '@/data/premierLeagueTeams';

export default function ClubPage({ params }: { params: { club: string } }) {
  // Trouver le club dans les données
  const club = premierLeagueTeams.find(c => c.slug === params.club);
  
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
    <ClubPagePremierLeague
      clubId={params.club}
      clubName={club.name}
      leagueId="premier-league"
      leagueName="Premier League"
      primaryColor="#38003c"
      secondaryColor="#ffffff"
    />
  );
}