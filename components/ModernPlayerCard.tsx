'use client';

import Link from 'next/link';
import Image from 'next/image';
import { ClubColors } from '@/data/clubColors';
import { translateNationality, translatePosition } from '@/utils/translations';

interface ModernPlayerCardProps {
  player: {
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
  };
  clubId: string;
  leagueId: string;
  playerSlug: string;
  colors: ClubColors;
}

const getPositionStyle = (position: string) => {
  const isGK = position === 'GK' || position === 'Goalkeeper';
  const isDF = ['DF', 'CB', 'LB', 'RB', 'Defender'].includes(position);
  const isMF = ['MF', 'DM', 'CM', 'AM', 'LM', 'RM', 'Midfielder'].includes(position);
  const isFW = ['FW', 'ST', 'CF', 'LW', 'RW', 'Attacker'].includes(position);
  
  if (isGK) return 'from-amber-500/20 to-amber-600/20 border-amber-500/30';
  if (isDF) return 'from-blue-500/20 to-blue-600/20 border-blue-500/30';
  if (isMF) return 'from-green-500/20 to-green-600/20 border-green-500/30';
  if (isFW) return 'from-red-500/20 to-red-600/20 border-red-500/30';
  return 'from-gray-500/20 to-gray-600/20 border-gray-500/30';
};

const getPositionIcon = (position: string) => {
  const isGK = position === 'GK' || position === 'Goalkeeper';
  const isDF = ['DF', 'CB', 'LB', 'RB', 'Defender'].includes(position);
  const isMF = ['MF', 'DM', 'CM', 'AM', 'LM', 'RM', 'Midfielder'].includes(position);
  const isFW = ['FW', 'ST', 'CF', 'LW', 'RW', 'Attacker'].includes(position);
  
  if (isGK) return '🥅';
  if (isDF) return '🛡️';
  if (isMF) return '⚡';
  if (isFW) return '⚽';
  return '👤';
};

export default function ModernPlayerCard({ 
  player, 
  clubId, 
  leagueId, 
  playerSlug,
  colors 
}: ModernPlayerCardProps) {
  const playerName = player.displayName || player.nom || player.name || 'Unknown';
  const jerseyNumber = player.numero ?? player.jersey_number;
  const nationality = player.nationalite || player.nationality;
  const height = player.taille ?? player.height;
  const weight = player.poids ?? player.weight;
  const positionStyle = getPositionStyle(player.position);
  const positionIcon = getPositionIcon(player.position);
  
  return (
    <Link
      href={`/${leagueId}/${clubId}/${playerSlug}`}
      className="group relative block h-full"
    >
      <div className={`
        card-hover-glow relative h-full overflow-hidden rounded-2xl
        bg-gradient-to-br from-gray-900/90 via-gray-800/80 to-gray-900/90
        backdrop-blur-sm border border-gray-700/50
        transition-all duration-500 ease-out
        hover:scale-[1.03] hover:shadow-2xl
        hover:border-opacity-100
        ${colors.borderColor}
      `}>
        {/* Background gradient effect */}
        <div className={`
          absolute inset-0 opacity-0 group-hover:opacity-100
          bg-gradient-to-br ${colors.hoverGradient}
          transition-opacity duration-500
        `} />
        
        {/* Top section with jersey number */}
        <div className="relative p-5">
          <div className="flex items-start justify-between mb-3">
            {/* Jersey number with enhanced styling */}
            {jerseyNumber && (
              <div className={`
                relative w-14 h-14 flex items-center justify-center
                bg-gradient-to-br ${colors.gradient}
                rounded-xl shadow-lg transform transition-transform
                group-hover:scale-110 group-hover:rotate-3
              `}>
                <span className="text-white font-bold text-xl drop-shadow-lg">
                  {jerseyNumber}
                </span>
                <div className="absolute inset-0 bg-white/20 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              </div>
            )}
            
            {/* Position badge */}
            <div className={`
              px-3 py-1 rounded-full text-xs font-medium
              bg-gradient-to-r ${positionStyle}
              border backdrop-blur-sm
              transform transition-transform group-hover:scale-110
            `}>
              <span className="mr-1">{positionIcon}</span>
              <span className="text-white/90">{translatePosition(player.position)}</span>
            </div>
          </div>
          
          {/* Player photo with enhanced styling */}
          <div className="relative mx-auto w-24 h-24 mb-4">
            <div className={`
              absolute inset-0 bg-gradient-to-br ${colors.gradient}
              rounded-full opacity-30 blur-xl
              group-hover:opacity-50 transition-opacity duration-500
            `} />
            <div className="relative w-full h-full rounded-full overflow-hidden border-2 border-white/20 shadow-xl">
              {player.image ? (
                <Image
                  src={player.image}
                  alt={playerName}
                  fill
                  className="object-cover group-hover:scale-110 transition-transform duration-500"
                />
              ) : (
                <div className="w-full h-full bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center">
                  <svg className="w-12 h-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
          </div>
          
          {/* Player name with gradient effect */}
          <h3 className="text-center mb-3">
            <span className={`
              text-lg font-bold text-white
              group-hover:bg-gradient-to-r group-hover:${colors.gradient}
              group-hover:bg-clip-text group-hover:text-transparent
              transition-all duration-300
            `}>
              {playerName}
            </span>
          </h3>
          
          {/* Stats grid */}
          <div className="grid grid-cols-2 gap-2 text-xs">
            {nationality && (
              <div className="bg-white/5 rounded-lg p-2 backdrop-blur-sm">
                <span className="text-gray-400 block">Nationalité</span>
                <span className="text-white font-medium truncate block">{translateNationality(nationality)}</span>
              </div>
            )}
            {player.age && (
              <div className="bg-white/5 rounded-lg p-2 backdrop-blur-sm">
                <span className="text-gray-400 block">Âge</span>
                <span className="text-white font-medium">{player.age} ans</span>
              </div>
            )}
            {height && (
              <div className="bg-white/5 rounded-lg p-2 backdrop-blur-sm">
                <span className="text-gray-400 block">Taille</span>
                <span className="text-white font-medium">{height} cm</span>
              </div>
            )}
            {weight && (
              <div className="bg-white/5 rounded-lg p-2 backdrop-blur-sm">
                <span className="text-gray-400 block">Poids</span>
                <span className="text-white font-medium">{weight} kg</span>
              </div>
            )}
          </div>
        </div>
        
        {/* Bottom action bar */}
        <div className={`
          absolute bottom-0 left-0 right-0 h-12
          bg-gradient-to-t from-black/60 to-transparent
          opacity-0 group-hover:opacity-100
          transition-opacity duration-300
          flex items-center justify-center
        `}>
          <div className="flex items-center gap-2 text-white/90 text-sm font-medium">
            <span>Voir les stats</span>
            <svg className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          </div>
        </div>
      </div>
    </Link>
  );
}