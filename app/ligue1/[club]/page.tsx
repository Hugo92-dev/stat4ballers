import ClubPageEnhanced from '@/components/ClubPageEnhanced';
import { ligue1Teams } from '@/data/ligue1Teams';

export default function ClubPage({ params }: { params: { club: string } }) {
  // Trouver le club dans les données
  const club = ligue1Teams.find(c => c.slug === params.club);
  
  if (!club) {
    return (
      <main className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Club non trouvé</h1>
          <a href="/ligue1" className="text-blue-400 hover:underline">
            Retour à la Ligue 1
          </a>
        </div>
      </main>
    );
  }

  return (
    <ClubPageEnhanced
      clubId={params.club}
      clubName={club.nom}
      leagueId="ligue1"
      leagueName="Ligue 1"
      teams={ligue1Teams}
      primaryColor="#1e3a8a"
      secondaryColor="#ffffff"
    />
  );
}