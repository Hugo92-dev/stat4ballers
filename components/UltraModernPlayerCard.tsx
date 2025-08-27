'use client';

import Link from 'next/link';
import Image from 'next/image';
import { ClubColors } from '@/data/clubColors';
import { useState } from 'react';
import { translateNationality, translatePosition } from '@/utils/translations';

interface UltraModernPlayerCardProps {
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
  clubPattern?: string;
}

const getPositionInfo = (position: string) => {
  const isGK = position === 'GK' || position === 'Goalkeeper';
  const isDF = ['DF', 'CB', 'LB', 'RB', 'Defender'].includes(position);
  const isMF = ['MF', 'DM', 'CM', 'AM', 'LM', 'RM', 'Midfielder'].includes(position);
  const isFW = ['FW', 'ST', 'CF', 'LW', 'RW', 'Attacker'].includes(position);
  
  if (isGK) return { emoji: '🧤', color: 'from-amber-400 to-yellow-500', bgColor: 'bg-amber-500/10' };
  if (isDF) return { emoji: '🛡️', color: 'from-blue-400 to-indigo-500', bgColor: 'bg-blue-500/10' };
  if (isMF) return { emoji: '⚡', color: 'from-emerald-400 to-teal-500', bgColor: 'bg-emerald-500/10' };
  if (isFW) return { emoji: '🎯', color: 'from-red-400 to-pink-500', bgColor: 'bg-red-500/10' };
  return { emoji: '👤', color: 'from-gray-400 to-gray-500', bgColor: 'bg-gray-500/10' };
};

const getClubPattern = (clubId: string) => {
  const patterns = {
    'olympique-marseille': (
      <div className="absolute inset-0 opacity-5">
        <svg viewBox="0 0 100 100" className="w-full h-full">
          <defs>
            <pattern id="om-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <circle cx="10" cy="10" r="2" fill="currentColor" opacity="0.3"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#om-pattern)" />
        </svg>
      </div>
    ),
    'paris-saint-germain': (
      <div className="absolute inset-0 opacity-5">
        <svg viewBox="0 0 100 100" className="w-full h-full">
          <defs>
            <pattern id="psg-pattern" x="0" y="0" width="25" height="25" patternUnits="userSpaceOnUse">
              <polygon points="12.5,2 22,20 3,20" fill="currentColor" opacity="0.4"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#psg-pattern)" />
        </svg>
      </div>
    ),
    'default': null
  };
  return patterns[clubId as keyof typeof patterns] || patterns.default;
};

export default function UltraModernPlayerCard({ 
  player, 
  clubId, 
  leagueId, 
  playerSlug,
  colors 
}: UltraModernPlayerCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  
  const playerName = player.displayName || player.nom || player.name || 'Unknown';
  const jerseyNumber = player.numero ?? player.jersey_number;
  const nationality = player.nationalite || player.nationality;
  const height = player.taille ?? player.height;
  const weight = player.poids ?? player.weight;
  const positionInfo = getPositionInfo(player.position);
  const clubPattern = getClubPattern(clubId);
  
  return (
    <Link
      href={`/${leagueId}/${clubId}/${playerSlug}`}
      className="group relative block h-full"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="relative h-full">
        {/* Main card with glassmorphism effect */}
        <div className={`
          relative h-full overflow-hidden rounded-3xl
          bg-gradient-to-br from-white/10 via-white/5 to-transparent
          backdrop-blur-xl border border-white/20
          transition-all duration-700 ease-out
          transform-gpu
          ${isHovered ? 'scale-[1.05] shadow-2xl shadow-black/20' : 'hover:scale-[1.02]'}
        `}>
          
          {/* Dynamic background with club colors */}
          <div className={`
            absolute inset-0 bg-gradient-to-br ${colors.cardGradient}
            opacity-20 group-hover:opacity-40
            transition-opacity duration-500
          `} />
          
          {/* Club pattern overlay */}
          <div className={`absolute inset-0 text-white group-hover:scale-110 transition-transform duration-700`}>
            {clubPattern}
          </div>
          
          {/* Animated border glow */}
          <div className={`
            absolute inset-0 rounded-3xl opacity-0 group-hover:opacity-100
            bg-gradient-to-r ${colors.gradient} p-[1px]
            transition-opacity duration-500
          `}>
            <div className="w-full h-full rounded-3xl bg-transparent" />
          </div>
          
          {/* Content */}
          <div className="relative p-6 h-full flex flex-col">
            
            {/* Top section with jersey and position */}
            <div className="flex items-start justify-between mb-4">
              {jerseyNumber && (
                <div className={`
                  relative w-16 h-16 flex items-center justify-center
                  bg-gradient-to-br ${colors.gradient}
                  rounded-2xl shadow-xl
                  transform transition-all duration-500
                  ${isHovered ? 'rotate-6 scale-110' : 'rotate-0'}
                `}>
                  <span className="text-white font-black text-2xl drop-shadow-lg">
                    {jerseyNumber}
                  </span>
                  <div className={`
                    absolute inset-0 rounded-2xl
                    bg-gradient-to-t from-black/20 to-transparent
                    opacity-0 group-hover:opacity-100
                    transition-opacity duration-300
                  `} />
                </div>
              )}
              
              <div className={`
                flex items-center gap-2 px-3 py-1.5 rounded-full
                ${positionInfo.bgColor} backdrop-blur-sm border border-white/20
                transform transition-all duration-300
                ${isHovered ? 'scale-110 -translate-y-1' : ''}
              `}>
                <span className="text-lg">{positionInfo.emoji}</span>
                <span className="text-white font-medium text-sm">{translatePosition(player.position)}</span>
              </div>
            </div>
            
            {/* Player photo with modern styling */}
            <div className="relative mx-auto mb-6">
              <div className={`
                absolute inset-0 bg-gradient-to-br ${colors.gradient}
                rounded-full opacity-30 blur-2xl scale-110
                group-hover:opacity-50 group-hover:scale-125
                transition-all duration-700
              `} />
              
              <div className="relative w-24 h-24">
                <div className={`
                  absolute inset-0 rounded-full
                  bg-gradient-to-br ${colors.gradient} p-[2px]
                  animate-pulse group-hover:animate-none
                `}>
                  <div className="w-full h-full rounded-full overflow-hidden bg-gray-900">
                    {player.image ? (
                      <Image
                        src={player.image}
                        alt={playerName}
                        fill
                        className={`
                          object-cover transition-transform duration-700
                          ${isHovered ? 'scale-110' : ''}
                        `}
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center">
                        <svg className="w-12 h-12 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                        </svg>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
            
            {/* Player name with modern typography */}
            <div className="text-center mb-4">
              <h3 className={`
                text-xl font-black text-white mb-1
                group-hover:bg-gradient-to-r group-hover:${colors.gradient}
                group-hover:bg-clip-text group-hover:text-transparent
                transition-all duration-500
                transform ${isHovered ? 'scale-105' : ''}
              `}>
                {playerName}
              </h3>
            </div>
            
            {/* Stats with modern design */}
            <div className="flex-1 space-y-3">
              {nationality && (
                <div className="group/stat flex items-center justify-between p-2 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300">
                  <span className="text-gray-300 text-sm">🌍 Nationalité</span>
                  <span className="text-white font-semibold text-sm truncate ml-2">{translateNationality(nationality)}</span>
                </div>
              )}
              
              {player.age && (
                <div className="group/stat flex items-center justify-between p-2 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300">
                  <span className="text-gray-300 text-sm">🎂 Âge</span>
                  <span className="text-white font-semibold text-sm">{player.age} ans</span>
                </div>
              )}
              
              <div className="grid grid-cols-2 gap-2">
                {height && (
                  <div className="group/stat p-2 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300 text-center">
                    <div className="text-gray-300 text-xs mb-1">📏 Taille</div>
                    <div className="text-white font-semibold text-sm">{height}cm</div>
                  </div>
                )}
                
                {weight && (
                  <div className="group/stat p-2 rounded-xl bg-white/5 backdrop-blur-sm border border-white/10 hover:bg-white/10 transition-all duration-300 text-center">
                    <div className="text-gray-300 text-xs mb-1">⚖️ Poids</div>
                    <div className="text-white font-semibold text-sm">{weight}kg</div>
                  </div>
                )}
              </div>
            </div>
            
            {/* Action indicator */}
            <div className={`
              mt-4 flex items-center justify-center gap-2 p-3 rounded-2xl
              bg-gradient-to-r ${colors.gradient} opacity-0 group-hover:opacity-100
              transform translate-y-4 group-hover:translate-y-0
              transition-all duration-500 ease-out
            `}>
              <span className="text-white font-semibold text-sm">Voir les stats</span>
              <svg className={`
                w-4 h-4 text-white transform transition-transform duration-300
                ${isHovered ? 'translate-x-1' : ''}
              `} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </div>
          </div>
          
          {/* Subtle floating particles effect */}
          <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-3xl">
            <div className={`
              absolute w-2 h-2 bg-white/20 rounded-full
              top-1/4 left-1/4 animate-float-1
              opacity-0 group-hover:opacity-100
              transition-opacity duration-700 delay-100
            `} />
            <div className={`
              absolute w-1 h-1 bg-white/30 rounded-full
              top-1/3 right-1/3 animate-float-2
              opacity-0 group-hover:opacity-100
              transition-opacity duration-700 delay-300
            `} />
            <div className={`
              absolute w-1.5 h-1.5 bg-white/25 rounded-full
              bottom-1/3 left-1/3 animate-float-3
              opacity-0 group-hover:opacity-100
              transition-opacity duration-700 delay-500
            `} />
          </div>
        </div>
      </div>
    </Link>
  );
}