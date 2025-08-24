import PlayerPageRouter from '@/components/PlayerPageRouter';
import { serieATeams } from '@/data/serieATeams';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  return (
    <PlayerPageRouter 
      params={params}
      teams={serieATeams}
      leagueSlug="serie-a"
    />
  );
}