import PlayerPageRouter from '@/components/PlayerPageRouter';
import { ligue1Teams } from '@/data/ligue1Teams';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  return (
    <PlayerPageRouter 
      params={params}
      teams={ligue1Teams}
      leagueSlug="ligue1"
    />
  );
}