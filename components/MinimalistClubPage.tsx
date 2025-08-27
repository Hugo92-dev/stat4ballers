'use client';

import { useState } from 'react';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import { slugifyPlayer } from '@/utils/slugify';
import { teamDetails } from '@/data/teamDetailsFromAPI';
import { getClubColors } from '@/data/clubColors';
import MinimalistClubHeader from '@/components/MinimalistClubHeader';
import MinimalistSearchBar from '@/components/MinimalistSearchBar';
import MinimalistPlayerCard from '@/components/MinimalistPlayerCard';

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
  nom?: string;
}

interface MinimalistClubPageProps {
  clubId: string;
  clubName: string;
  leagueId: string;
  leagueName: string;
  teams: Team[];
}

const getPositionInfo = (position: string) => {
  const isGK = position === 'GK' || position === 'Goalkeeper';
  const isDF = ['DF', 'CB', 'LB', 'RB', 'Defender'].includes(position);
  const isMF = ['MF', 'DM', 'CM', 'AM', 'LM', 'RM', 'Midfielder'].includes(position);
  const isFW = ['FW', 'ST', 'CF', 'LW', 'RW', 'Attacker'].includes(position);
  
  if (isGK) return { label: 'Gardiens', order: 1 };
  if (isDF) return { label: 'Défenseurs', order: 2 };
  if (isMF) return { label: 'Milieux', order: 3 };
  if (isFW) return { label: 'Attaquants', order: 4 };
  return { label: 'Autres', order: 5 };
};

export default function MinimalistClubPage({ 
  clubId, 
  clubName, 
  leagueId, 
  leagueName,
  teams
}: MinimalistClubPageProps) {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Trouver l'équipe dans les données
  const team = teams.find(t => t.slug === clubId);
  const details = teamDetails[clubId];
  const clubColors = getClubColors(clubId);
  
  if (!team) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto p-8">
          <div className="w-16 h-16 mx-auto mb-4 bg-gray-200 rounded-lg flex items-center justify-center">
            <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h1 className="text-xl font-medium text-gray-900 mb-2">Équipe non trouvée</h1>
          <p className="text-gray-500 text-sm mb-6">L'équipe demandée n'existe pas ou n'est pas disponible.</p>
          <a 
            href={`/${leagueId}`}
            className="inline-flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 19l-7-7 7-7" />
            </svg>
            Retour à {leagueName}
          </a>
        </div>
      </div>
    );
  }
  
  // Filtrer les joueurs selon la recherche
  const filteredPlayers = team.players.filter(player => {
    const name = (player.nom || player.name || '').toLowerCase();
    const position = (player.position || '').toLowerCase();
    const nationality = (player.nationalite || player.nationality || '').toLowerCase();
    const term = searchTerm.toLowerCase();
    
    return name.includes(term) || position.includes(term) || nationality.includes(term);
  });
  
  // Grouper les joueurs par position
  const positionGroups = filteredPlayers.reduce((acc, player) => {
    const posInfo = getPositionInfo(player.position);
    const key = posInfo.label;
    
    if (!acc[key]) {
      acc[key] = {
        ...posInfo,
        players: []
      };
    }
    acc[key].players.push(player);
    
    return acc;
  }, {} as Record<string, any>);

  // Trier les groupes par ordre logique
  const sortedGroups = Object.entries(positionGroups).sort(([,a], [,b]) => a.order - b.order);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header minimaliste */}
      <MinimalistClubHeader
        clubId={clubId}
        clubName={team.nom || team.name}
        leagueId={leagueId}
        leagueName={leagueName}
        playerCount={team.players.length}
        logoPath={getClubLogoPath(leagueId, clubId)}
        colors={clubColors}
        details={details}
      />

      {/* Contenu principal */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Barre de recherche */}
        <MinimalistSearchBar
          searchTerm={searchTerm}
          onSearchChange={setSearchTerm}
          colors={clubColors}
          resultCount={filteredPlayers.length}
        />

        {/* Sections des joueurs */}
        {sortedGroups.length > 0 ? (
          <div className="space-y-8">
            {sortedGroups.map(([positionName, groupData]) => (
              <div key={positionName}>
                {/* Header de section */}
                <div className="flex items-center gap-4 mb-4">
                  <h2 className="text-lg font-medium text-gray-900">
                    {positionName}
                  </h2>
                  <div className={`w-1.5 h-1.5 rounded-full bg-gradient-to-r ${clubColors.gradient}`} />
                  <span className="text-sm text-gray-500">
                    {groupData.players.length} joueur{groupData.players.length > 1 ? 's' : ''}
                  </span>
                  <div className="flex-1 h-px bg-gray-200" />
                </div>
                
                {/* Grille de cartes compactes */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {groupData.players.map((player: Player) => {
                    const playerName = player.displayName || player.nom || player.name || 'Unknown';
                    const playerSlug = player.playerSlug || slugifyPlayer(playerName);
                    
                    return (
                      <MinimalistPlayerCard
                        key={player.id}
                        player={player}
                        clubId={clubId}
                        leagueId={leagueId}
                        playerSlug={playerSlug}
                        colors={clubColors}
                      />
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        ) : searchTerm ? (
          /* État sans résultats */
          <div className="text-center py-16">
            <div className="w-16 h-16 mx-auto mb-4 bg-gray-200 rounded-lg flex items-center justify-center">
              <svg className="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Aucun joueur trouvé
            </h3>
            <p className="text-gray-500 text-sm mb-6 max-w-sm mx-auto">
              Aucun joueur ne correspond à votre recherche 
              <span className="font-medium text-gray-900">"{searchTerm}"</span>
            </p>
            
            <button
              onClick={() => setSearchTerm('')}
              className="inline-flex items-center gap-2 px-4 py-2 bg-gray-900 text-white rounded-lg text-sm font-medium hover:bg-gray-800 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Effacer la recherche
            </button>
          </div>
        ) : null}
      </div>
    </div>
  );
}