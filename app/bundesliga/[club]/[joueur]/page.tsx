import PlayerPageRouter from '@/components/PlayerPageRouter';
import { bundesligaTeams } from '@/data/bundesligaTeams';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  return (
    <PlayerPageRouter 
      params={params}
      teams={bundesligaTeams}
      leagueSlug="bundesliga"
    />
  );
}