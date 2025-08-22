import PlayerPageWithStats from '@/components/PlayerPageWithStats';
import { ligue1Teams } from '@/data/ligue1Teams';
import { notFound } from 'next/navigation';
import { slugifyPlayer } from '@/utils/slugify';

export default function JoueurPage({ 
  params 
}: { 
  params: { club: string; joueur: string } 
}) {
  // Trouver le club
  const club = ligue1Teams.find(t => t.slug === params.club);
  
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
    <PlayerPageWithStats
      player={player}
      clubName={club.name}
      clubSlug={params.club}
      leagueSlug="ligue1"
      leagueColor="from-blue-600 to-blue-800"
    />
  );
}