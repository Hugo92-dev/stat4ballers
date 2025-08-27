'use client';

import MinimalistClubPage from '@/components/MinimalistClubPage';

interface Player {
  id: string | number;
  name?: string;
  nom?: string;
  displayName?: string;
  position: string;
  nationality?: string;
  nationalite?: string;
  jersey_number?: number | null;
  numero?: number | null;
  age?: string;
  height?: number | null;
  taille?: number | null;
  weight?: number | null;
  poids?: number | null;
  image?: string;
  playerSlug?: string;
}

interface Team {
  id: string | number;
  name: string;
  slug: string;
  players: Player[];
}

interface ClubPageEnhancedProps {
  clubId: string;
  clubName: string;
  leagueId: string;
  leagueName: string;
  teams: Team[];
  primaryColor?: string;
  secondaryColor?: string;
}

export default function ClubPageEnhanced({ 
  clubId, 
  clubName, 
  leagueId, 
  leagueName,
  teams,
  primaryColor = '#1e3a8a',
  secondaryColor = '#ffffff'
}: ClubPageEnhancedProps) {
  return (
    <MinimalistClubPage
      clubId={clubId}
      clubName={clubName}
      leagueId={leagueId}
      leagueName={leagueName}
      teams={teams}
    />
  );
}