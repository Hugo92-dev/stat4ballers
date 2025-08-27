'use client';

import Link from 'next/link';
import Image from 'next/image';
import { ClubColors } from '@/data/clubColors';
import { useState, useEffect } from 'react';

interface UltraModernClubHeaderProps {
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

const getClubHeroPattern = (clubId: string) => {
  const patterns = {
    'olympique-marseille': (
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-96 h-96 bg-gradient-to-br from-sky-400/20 to-blue-600/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-20 -left-20 w-72 h-72 bg-gradient-to-tr from-cyan-400/15 to-sky-500/15 rounded-full blur-2xl animate-pulse delay-1000" />
        <svg className="absolute inset-0 w-full h-full opacity-5" viewBox="0 0 100 100">
          <defs>
            <radialGradient id="om-radial" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="currentColor" stopOpacity="0.3" />
              <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
            </radialGradient>
          </defs>
          <circle cx="20" cy="30" r="8" fill="url(#om-radial)" />
          <circle cx="80" cy="20" r="6" fill="url(#om-radial)" />
          <circle cx="70" cy="70" r="10" fill="url(#om-radial)" />
          <circle cx="30" cy="80" r="7" fill="url(#om-radial)" />
        </svg>
      </div>
    ),
    'paris-saint-germain': (
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-32 -right-32 w-80 h-80 bg-gradient-to-br from-blue-600/20 to-red-600/20 rounded-full blur-3xl animate-pulse" />
        <div className="absolute -bottom-16 -left-16 w-64 h-64 bg-gradient-to-tr from-red-500/15 to-purple-500/15 rounded-full blur-2xl animate-pulse delay-700" />
        <svg className="absolute inset-0 w-full h-full opacity-5" viewBox="0 0 100 100">
          <defs>
            <pattern id="psg-pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <polygon points="10,2 18,18 2,18" fill="currentColor" opacity="0.4"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#psg-pattern)" />
        </svg>
      </div>
    )
  };
  return patterns[clubId as keyof typeof patterns] || patterns['olympique-marseille'];
};

export default function UltraModernClubHeader({
  clubId,
  clubName,
  leagueId,
  leagueName,
  playerCount,
  logoPath,
  colors,
  details
}: UltraModernClubHeaderProps) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);

  return (
    <div className="relative min-h-[60vh] flex items-center justify-center overflow-hidden">
      {/* Dynamic background with club-specific patterns */}
      <div className="absolute inset-0 bg-gradient-to-br from-gray-950 via-gray-900 to-black">
        <div className={`absolute inset-0 bg-gradient-to-br ${colors.cardGradient} opacity-40`} />
        {getClubHeroPattern(clubId)}
      </div>
      
      {/* Animated grid overlay */}
      <div className="absolute inset-0 opacity-5">
        <div className="absolute inset-0" style={{
          backgroundImage: `linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)`,
          backgroundSize: '50px 50px',
          animation: 'grid-move 20s linear infinite'
        }} />
      </div>
      
      {/* Content */}
      <div className="relative z-10 w-full max-w-7xl mx-auto px-8">
        {/* Back button */}
        <Link 
          href={`/${leagueId}`}
          className="group inline-flex items-center gap-3 mb-12 p-3 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 hover:bg-white/10 transition-all duration-300"
        >
          <div className="w-10 h-10 rounded-xl bg-gradient-to-r from-white/20 to-white/10 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
            <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </div>
          <span className="text-white font-medium group-hover:text-gray-200 transition-colors">
            Retour à {leagueName}
          </span>
        </Link>
        
        <div className="flex flex-col lg:flex-row items-center gap-12">
          
          {/* Club logo with modern styling */}
          <div className="relative group">
            <div className={`
              absolute inset-0 bg-gradient-to-br ${colors.gradient}
              rounded-3xl opacity-20 blur-2xl scale-110
              group-hover:opacity-40 group-hover:scale-125
              transition-all duration-700
            `} />
            
            <div className="relative">
              <div className={`
                w-40 h-40 bg-gradient-to-br ${colors.gradient} p-[3px] rounded-3xl
                group-hover:rotate-3 transform transition-all duration-500
              `}>
                <div className="w-full h-full bg-white rounded-3xl p-6 group-hover:scale-105 transition-transform duration-500">
                  <Image
                    src={logoPath}
                    alt={clubName}
                    fill
                    className="object-contain p-2"
                  />
                </div>
              </div>
              
              {/* Floating elements around logo */}
              {mounted && (
                <>
                  <div className="absolute -top-4 -right-4 w-8 h-8 bg-gradient-to-br from-white/20 to-white/5 rounded-full animate-float-1 opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
                  <div className="absolute -bottom-2 -left-6 w-6 h-6 bg-gradient-to-br from-white/15 to-white/5 rounded-full animate-float-2 opacity-0 group-hover:opacity-100 transition-opacity duration-700 delay-300" />
                  <div className="absolute top-1/2 -right-8 w-4 h-4 bg-gradient-to-br from-white/25 to-white/5 rounded-full animate-float-3 opacity-0 group-hover:opacity-100 transition-opacity duration-700 delay-600" />
                </>
              )}
            </div>
          </div>
          
          {/* Club info with modern typography */}
          <div className="flex-1 text-center lg:text-left space-y-8">
            <div>
              <h1 className={`
                text-6xl lg:text-8xl font-black text-transparent bg-clip-text
                bg-gradient-to-r ${colors.gradient}
                mb-4 leading-tight
                drop-shadow-2xl
                animate-gradient-x bg-300%
              `}>
                {clubName}
              </h1>
              
              <p className="text-xl text-gray-300 font-light tracking-wide">
                Effectif complet • Saison 2025/2026
              </p>
            </div>
            
            {/* Modern stats cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-2xl lg:max-w-none">
              
              {/* Players count */}
              <div className="group relative p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 hover:bg-white/10 transition-all duration-500 hover:scale-105">
                <div className={`absolute inset-0 bg-gradient-to-br ${colors.cardGradient} opacity-0 group-hover:opacity-30 rounded-2xl transition-opacity duration-500`} />
                <div className="relative">
                  <div className="flex items-center gap-3 mb-2">
                    <div className={`w-3 h-3 rounded-full bg-gradient-to-r ${colors.gradient} animate-pulse`} />
                    <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">Effectif</span>
                  </div>
                  <div className="text-3xl font-black text-white mb-1">{playerCount}</div>
                  <div className="text-sm text-gray-400">joueurs</div>
                </div>
              </div>
              
              {/* Stadium */}
              {details?.stadium && (
                <div className="group relative p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 hover:bg-white/10 transition-all duration-500 hover:scale-105">
                  <div className={`absolute inset-0 bg-gradient-to-br ${colors.cardGradient} opacity-0 group-hover:opacity-30 rounded-2xl transition-opacity duration-500`} />
                  <div className="relative">
                    <div className="flex items-center gap-3 mb-2">
                      <div className={`w-3 h-3 rounded-full bg-gradient-to-r ${colors.gradient} animate-pulse delay-200`} />
                      <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">Stade</span>
                    </div>
                    <div className="text-lg font-bold text-white mb-1 truncate">{details.stadium}</div>
                    {details.capacity && (
                      <div className="text-sm text-gray-400">
                        {new Intl.NumberFormat('fr-FR').format(details.capacity)} places
                      </div>
                    )}
                  </div>
                </div>
              )}
              
              {/* Founded */}
              {details?.founded && (
                <div className="group relative p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 hover:bg-white/10 transition-all duration-500 hover:scale-105">
                  <div className={`absolute inset-0 bg-gradient-to-br ${colors.cardGradient} opacity-0 group-hover:opacity-30 rounded-2xl transition-opacity duration-500`} />
                  <div className="relative">
                    <div className="flex items-center gap-3 mb-2">
                      <div className={`w-3 h-3 rounded-full bg-gradient-to-r ${colors.gradient} animate-pulse delay-500`} />
                      <span className="text-gray-400 text-sm font-medium uppercase tracking-wider">Fondé en</span>
                    </div>
                    <div className="text-3xl font-black text-white mb-1">{details.founded}</div>
                    <div className="text-sm text-gray-400">
                      {new Date().getFullYear() - details.founded} ans d'histoire
                    </div>
                  </div>
                </div>
              )}
              
            </div>
          </div>
        </div>
      </div>
      
      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-gray-900 to-transparent" />
    </div>
  );
}