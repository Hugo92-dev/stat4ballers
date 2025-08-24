import PlayerPageWithStats from '@/components/PlayerPageWithStats';
import { notFound } from 'next/navigation';
import { findPlayerBySlug, getLeagueColor } from '@/data/unifiedMapping';
import { Team } from '@/data/types';

interface PlayerPageRouterProps {
  params: { club: string; joueur: string };
  teams: Team[];
  leagueSlug: string;
}

export default function PlayerPageRouter({ 
  params, 
  teams, 
  leagueSlug 
}: PlayerPageRouterProps) {
  // Trouver le club
  const club = teams.find(t => t.slug === params.club);
  
  if (!club) {
    if (typeof window !== 'undefined') {
      console.error(`[PlayerPageRouter] Club non trouvé: ${params.club} dans ${leagueSlug}`);
      console.log('Clubs disponibles:', teams.map(t => t.slug));
    }
    notFound();
  }

  // Trouver le joueur avec la fonction unifiée
  const player = findPlayerBySlug(club.players, params.joueur);

  if (!player) {
    if (typeof window !== 'undefined') {
      console.error(`[PlayerPageRouter] Joueur non trouvé: ${params.joueur} dans ${club.name}`);
      console.log('Joueurs disponibles:', club.players.map(p => p.playerSlug || p.displayName || p.name));
    }
    notFound();
  }

  // Obtenir la couleur de la ligue
  const leagueColor = getLeagueColor(leagueSlug);

  return (
    <PlayerPageWithStats
      player={player}
      clubName={club.name}
      clubSlug={params.club}
      leagueSlug={leagueSlug}
      leagueColor={leagueColor}
    />
  );
}