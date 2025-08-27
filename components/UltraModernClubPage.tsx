'use client';

import { useState } from 'react';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import { slugifyPlayer } from '@/utils/slugify';
import { teamDetails } from '@/data/teamDetailsFromAPI';
import { getClubColors } from '@/data/clubColors';
import UltraModernClubHeader from '@/components/UltraModernClubHeader';
import UltraModernSearchBar from '@/components/UltraModernSearchBar';
import UltraModernPlayerCard from '@/components/UltraModernPlayerCard';

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

interface UltraModernClubPageProps {
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
  
  if (isGK) return { 
    label: 'Gardiens', 
    emoji: '🧤', 
    gradient: 'from-amber-400 via-yellow-500 to-orange-500',
    count: 0,
    order: 1
  };
  if (isDF) return { 
    label: 'Défenseurs', 
    emoji: '🛡️', 
    gradient: 'from-blue-400 via-indigo-500 to-purple-500',
    count: 0,
    order: 2
  };
  if (isMF) return { 
    label: 'Milieux', 
    emoji: '⚡', 
    gradient: 'from-emerald-400 via-teal-500 to-cyan-500',
    count: 0,
    order: 3
  };
  if (isFW) return { 
    label: 'Attaquants', 
    emoji: '🎯', 
    gradient: 'from-red-400 via-pink-500 to-rose-500',
    count: 0,
    order: 4
  };
  return { 
    label: 'Autres', 
    emoji: '👤', 
    gradient: 'from-gray-400 via-gray-500 to-gray-600',
    count: 0,
    order: 5
  };
};

export default function UltraModernClubPage({ 
  clubId, 
  clubName, 
  leagueId, 
  leagueName,
  teams
}: UltraModernClubPageProps) {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Trouver l'équipe dans les données
  const team = teams.find(t => t.slug === clubId);
  const details = teamDetails[clubId];
  const clubColors = getClubColors(clubId);
  
  if (!team) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black flex items-center justify-center">
        <div className="text-center">
          <div className="w-24 h-24 mx-auto mb-8 bg-gradient-to-br from-red-500/20 to-red-600/20 rounded-full flex items-center justify-center">
            <svg className="w-12 h-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <h1 className="text-3xl font-bold text-white mb-4">Équipe non trouvée</h1>
          <p className="text-gray-400 mb-8">L'équipe demandée n'existe pas ou n'est pas disponible.</p>
          <a 
            href={`/${leagueId}`}
            className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-full font-medium hover:scale-105 transition-transform duration-300"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
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
  
  // Grouper les joueurs par position avec informations enrichies
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
    acc[key].count = acc[key].players.length;
    
    return acc;
  }, {} as Record<string, any>);

  // Trier les groupes par ordre logique
  const sortedGroups = Object.entries(positionGroups).sort(([,a], [,b]) => a.order - b.order);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-950 via-gray-900 to-black">
      {/* Ultra-modern header */}
      <UltraModernClubHeader
        clubId={clubId}
        clubName={team.nom || team.name}
        leagueId={leagueId}
        leagueName={leagueName}
        playerCount={team.players.length}
        logoPath={getClubLogoPath(leagueId, clubId)}
        colors={clubColors}
        details={details}
      />

      {/* Main content with search and players */}
      <div className="relative pb-32">
        {/* Ultra-modern search bar */}
        <div className="max-w-7xl mx-auto px-8 pt-16">
          <UltraModernSearchBar
            searchTerm={searchTerm}
            onSearchChange={setSearchTerm}
            colors={clubColors}
            resultCount={filteredPlayers.length}
          />
        </div>

        {/* Players section */}
        <div className="max-w-7xl mx-auto px-8">
          {sortedGroups.length > 0 ? (
            <div className="space-y-20">
              {sortedGroups.map(([positionName, groupData], groupIndex) => (
                <div key={positionName} className="group/position">
                  {/* Position header with modern design */}
                  <div className="flex items-center justify-between mb-12">
                    <div className="flex items-center gap-6">
                      <div className={`
                        w-16 h-16 rounded-2xl bg-gradient-to-br ${groupData.gradient}
                        flex items-center justify-center text-2xl
                        group-hover/position:scale-110 group-hover/position:rotate-12
                        transition-all duration-500
                      `}>
                        {groupData.emoji}
                      </div>
                      <div>
                        <h2 className={`
                          text-4xl font-black text-transparent bg-clip-text
                          bg-gradient-to-r ${groupData.gradient}
                          mb-2
                        `}>
                          {positionName}
                        </h2>
                        <p className="text-gray-400 text-lg">
                          {groupData.count} joueur{groupData.count > 1 ? 's' : ''}
                        </p>
                      </div>
                    </div>
                    
                    <div className={`
                      w-12 h-12 rounded-xl bg-gradient-to-br ${groupData.gradient} opacity-20
                      group-hover/position:opacity-40 group-hover/position:scale-110
                      transition-all duration-500
                    `} />
                  </div>
                  
                  {/* Players grid with staggered animations */}
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                    {groupData.players.map((player: Player, index: number) => {
                      const playerName = player.displayName || player.nom || player.name || 'Unknown';
                      const playerSlug = player.playerSlug || slugifyPlayer(playerName);
                      
                      return (
                        <div
                          key={player.id}
                          className="animate-fade-in-up"
                          style={{
                            animationDelay: `${(groupIndex * 200) + (index * 100)}ms`,
                            animationFillMode: 'both'
                          }}
                        >
                          <UltraModernPlayerCard
                            player={player}
                            clubId={clubId}
                            leagueId={leagueId}
                            playerSlug={playerSlug}
                            colors={clubColors}
                          />
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          ) : searchTerm ? (
            /* No results state */
            <div className="text-center py-24">
              <div className={`
                w-32 h-32 mx-auto mb-8 rounded-3xl
                bg-gradient-to-br ${clubColors.gradient} opacity-10
                flex items-center justify-center
                animate-pulse-glow
              `}>
                <svg className="w-16 h-16 text-white/50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
              
              <h3 className="text-4xl font-black text-white mb-4">
                Aucun joueur trouvé
              </h3>
              <p className="text-xl text-gray-400 mb-8 max-w-md mx-auto">
                Aucun joueur ne correspond à votre recherche 
                <span className={`
                  font-bold text-transparent bg-clip-text
                  bg-gradient-to-r ${clubColors.gradient}
                `}>
                  "{searchTerm}"
                </span>
              </p>
              
              <button
                onClick={() => setSearchTerm('')}
                className={`
                  inline-flex items-center gap-3 px-8 py-4 rounded-2xl
                  bg-gradient-to-r ${clubColors.gradient} text-white font-bold
                  hover:scale-105 hover:shadow-xl
                  transition-all duration-300 transform
                `}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                Réinitialiser la recherche
              </button>
            </div>
          ) : null}
        </div>
      </div>
    </div>
  );
}