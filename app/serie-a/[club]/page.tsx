import ClubPageSerieA from '@/components/ClubPageSerieA';
import { serieATeams } from '@/data/serieATeams';

export default function ClubPage({ params }: { params: { club: string } }) {
  // Trouver le club dans les données
  const club = serieATeams.find(c => c.slug === params.club);
  
  if (!club) {
    return (
      <main className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Club non trouvé</h1>
          <a href="/serie-a" className="text-blue-400 hover:underline">
            Retour à la Serie A
          </a>
        </div>
      </main>
    );
  }

  return (
    <ClubPageSerieA
      clubId={params.club}
      clubName={club.name}
      leagueId="serie-a"
      leagueName="Serie A"
      primaryColor="#00844A"
      secondaryColor="#ffffff"
    />
  );
}