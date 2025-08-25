import ClubPageEnhanced from '@/components/ClubPageEnhanced';
import { bundesligaTeams } from '@/data/bundesligaTeams';

export default function ClubPage({ params }: { params: { club: string } }) {
  // Trouver le club dans les données
  const club = bundesligaTeams.find(c => c.slug === params.club);
  
  if (!club) {
    return (
      <main className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Club non trouvé</h1>
          <a href="/bundesliga" className="text-blue-400 hover:underline">
            Retour à la Bundesliga
          </a>
        </div>
      </main>
    );
  }

  return (
    <ClubPageEnhanced
      clubId={params.club}
      clubName={club.nom}
      leagueId="bundesliga"
      leagueName="Bundesliga"
      teams={bundesligaTeams}
      primaryColor="#000000"
      secondaryColor="#ffffff"
    />
  );
}