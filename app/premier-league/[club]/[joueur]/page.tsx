import PlayerPage from '@/components/PlayerPage';
import { premierLeagueTeams } from '@/data/premierLeagueTeams';
import { notFound } from 'next/navigation';
import { slugifyPlayer } from '@/utils/slugify';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  // Trouver le club
  const club = premierLeagueTeams.find(t => t.slug === params.club);
  
  if (!club) {
    notFound();
  }

  // Le paramètre joueur est déjà un slug
  const playerSlug = params.joueur;
  
  // Trouver le joueur en comparant les slugs
  const player = club.players.find(p => {
    const playerDisplayName = p.displayName || p.fullName || p.name;
    return slugifyPlayer(playerDisplayName) === playerSlug;
  });

  if (!player) {
    notFound();
  }

  return (
    <PlayerPage
      player={player}
      clubName={club.name}
      clubSlug={params.club}
      leagueSlug="premier-league"
      leagueColor="from-purple-600 to-purple-800"
    />
  );
}