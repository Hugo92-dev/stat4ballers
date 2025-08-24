import PlayerPageRouter from '@/components/PlayerPageRouter';
import { ligaTeams } from '@/data/ligaTeams';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  return (
    <PlayerPageRouter 
      params={params}
      teams={ligaTeams}
      leagueSlug="liga"
    />
  );
}