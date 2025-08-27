'use client';

import Link from 'next/link';
import Image from 'next/image';
import { ClubColors } from '@/data/clubColors';

interface MinimalistClubHeaderProps {
  clubId: string;
  clubName: string;
  leagueId: string;
  leagueName: string;
  playerCount: number;
  logoPath: string;
  colors: ClubColors;
  details?: {
    stadium?: string;
    capacity?: number;
    founded?: number;
  };
}

export default function MinimalistClubHeader({
  clubId,
  clubName,
  leagueId,
  leagueName,
  playerCount,
  logoPath,
  colors,
  details
}: MinimalistClubHeaderProps) {
  return (
    <div className="bg-white border-b border-gray-100">
      <div className="max-w-6xl mx-auto px-6 py-8">
        {/* Navigation */}
        <Link 
          href={`/${leagueId}`}
          className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-gray-700 transition-colors mb-6"
        >
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 19l-7-7 7-7" />
          </svg>
          {leagueName}
        </Link>
        
        {/* Main header */}
        <div className="flex items-start gap-8">
          {/* Logo */}
          <div className="relative">
            <div className="w-20 h-20 bg-gray-50 rounded-lg p-3 border border-gray-100">
              <Image
                src={logoPath}
                alt={clubName}
                fill
                className="object-contain p-1"
              />
            </div>
            {/* Subtle accent */}
            <div className={`absolute -bottom-1 -right-1 w-4 h-4 rounded-full bg-gradient-to-r ${colors.gradient} opacity-80`} />
          </div>
          
          {/* Club info */}
          <div className="flex-1">
            <div className="flex items-baseline gap-4 mb-2">
              <h1 className="text-3xl font-light text-gray-900 tracking-tight">
                {clubName}
              </h1>
              <div className={`px-2 py-0.5 rounded-full text-xs font-medium text-white bg-gradient-to-r ${colors.gradient}`}>
                2025/26
              </div>
            </div>
            
            {/* Stats en ligne */}
            <div className="flex items-center gap-8 text-sm text-gray-600 mt-4">
              <div className="flex items-center gap-2">
                <div className={`w-2 h-2 rounded-full bg-gradient-to-r ${colors.gradient}`} />
                <span className="font-medium text-gray-900">{playerCount}</span>
                <span>joueurs</span>
              </div>
              
              {details?.stadium && (
                <div className="flex items-center gap-2">
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                  <span>{details.stadium}</span>
                  {details.capacity && (
                    <span className="text-gray-400">
                      ({new Intl.NumberFormat('fr-FR').format(details.capacity)})
                    </span>
                  )}
                </div>
              )}
              
              {details?.founded && (
                <div className="flex items-center gap-2">
                  <svg className="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span>Fondé en {details.founded}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}