'use client';

import Link from 'next/link';
import Image from 'next/image';
import { ClubColors } from '@/data/clubColors';

interface MinimalistPlayerCardProps {
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

export default function MinimalistPlayerCard({ 
  player, 
  clubId, 
  leagueId, 
  playerSlug,
  colors 
}: MinimalistPlayerCardProps) {
  const playerName = player.displayName || player.nom || player.name || 'Unknown';
  const jerseyNumber = player.numero ?? player.jersey_number;
  const nationality = player.nationalite || player.nationality;
  const height = player.taille ?? player.height;
  
  return (
    <Link
      href={`/${leagueId}/${clubId}/${playerSlug}`}
      className="group block"
    >
      <div className="relative bg-white rounded-lg border border-gray-100 hover:border-gray-200 transition-all duration-200 hover:shadow-sm">
        {/* Subtle club accent */}
        <div className={`absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r ${colors.gradient} opacity-60`} />
        
        <div className="p-4">
          {/* Header avec photo et numéro */}
          <div className="flex items-center gap-3 mb-3">
            {/* Photo joueur */}
            <div className="relative w-12 h-12 rounded-full overflow-hidden bg-gray-50 border border-gray-100 flex-shrink-0">
              {player.image ? (
                <Image
                  src={player.image}
                  alt={playerName}
                  fill
                  className="object-cover"
                />
              ) : (
                <div className="w-full h-full flex items-center justify-center text-gray-300">
                  <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                  </svg>
                </div>
              )}
            </div>
            
            {/* Nom et numéro */}
            <div className="flex-1 min-w-0">
              <h3 className="font-medium text-gray-900 truncate text-sm group-hover:text-gray-700 transition-colors">
                {playerName}
              </h3>
              <div className="flex items-center gap-2 mt-0.5">
                {jerseyNumber && (
                  <span className={`
                    inline-flex items-center justify-center w-5 h-5 rounded text-xs font-medium text-white
                    bg-gradient-to-r ${colors.gradient}
                  `}>
                    {jerseyNumber}
                  </span>
                )}
                <span className="text-xs text-gray-500 font-medium">{player.position}</span>
              </div>
            </div>
          </div>
          
          {/* Infos compactes */}
          <div className="space-y-2 text-xs text-gray-600">
            {nationality && (
              <div className="flex justify-between">
                <span className="text-gray-400">Nationalité</span>
                <span className="font-medium truncate ml-2">{nationality}</span>
              </div>
            )}
            
            <div className="flex justify-between">
              {player.age && (
                <div className="flex justify-between w-full">
                  <span className="text-gray-400">Âge</span>
                  <span className="font-medium">{player.age} ans</span>
                </div>
              )}
            </div>
            
            {height && (
              <div className="flex justify-between">
                <span className="text-gray-400">Taille</span>
                <span className="font-medium">{height} cm</span>
              </div>
            )}
          </div>
        </div>
        
        {/* Hover indicator */}
        <div className="absolute inset-x-0 bottom-0 h-0.5 bg-gradient-to-r from-transparent via-gray-200 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
      </div>
    </Link>
  );
}