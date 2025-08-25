import ClubPageEnhanced from '@/components/ClubPageEnhanced';
import { ligaTeams } from '@/data/ligaTeams';

export default function ClubPage({ params }: { params: { club: string } }) {
  // Trouver le club dans les données
  const club = ligaTeams.find(c => c.slug === params.club);
  
  if (!club) {
    return (
      <main className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Club non trouvé</h1>
          <a href="/liga" className="text-blue-400 hover:underline">
            Retour à La Liga
          </a>
        </div>
      </main>
    );
  }

  return (
    <ClubPageEnhanced
      clubId={params.club}
      clubName={club.nom}
      leagueId="liga"
      leagueName="La Liga"
      teams={ligaTeams}
      primaryColor="#ee8707"
      secondaryColor="#ffffff"
    />
  );
}