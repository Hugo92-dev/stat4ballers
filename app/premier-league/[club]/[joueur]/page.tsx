import PlayerPageRouter from '@/components/PlayerPageRouter';
import { premierLeagueTeams } from '@/data/premierLeagueTeams';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  return (
    <PlayerPageRouter 
      params={params}
      teams={premierLeagueTeams}
      leagueSlug="premier-league"
    />
  );
}