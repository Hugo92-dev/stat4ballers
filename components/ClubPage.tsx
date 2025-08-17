'use client';

import Link from 'next/link';
import Image from 'next/image';
import { generatePlayers } from '@/utils/playerGenerator';
import { getClubLogoPath } from '@/data/clubLogosMapping';

interface ClubPageProps {
  clubId: string;
  clubName: string;
  leagueId: string;
  leagueName: string;
  primaryColor?: string;
  secondaryColor?: string;
}

export default function ClubPage({ 
  clubId, 
  clubName, 
  leagueId, 
  leagueName,
  primaryColor = '#1e3a8a',
  secondaryColor = '#ffffff'
}: ClubPageProps) {
  const joueurs = generatePlayers(clubName, 15);

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Hero Section avec Logo */}
      <section 
        className="relative py-16 mb-8"
        style={{
          background: `linear-gradient(135deg, ${primaryColor} 0%, ${primaryColor}dd 100%)`
        }}
      >
        <div className="container mx-auto px-4">
          <Link 
            href={`/${leagueId}`} 
            className="inline-flex items-center text-white/90 hover:text-white mb-6 transition-colors"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Retour à {leagueName}
          </Link>
          
          <div className="flex items-center gap-8">
            <div className="bg-white p-6 rounded-2xl shadow-2xl">
              <Image
                src={getClubLogoPath(leagueId, clubId)}
                alt={clubName}
                width={120}
                height={120}
                className="object-contain"
              />
            </div>
            
            <div className="text-white">
              <h1 className="text-5xl font-bold mb-2">{clubName}</h1>
              <p className="text-xl opacity-90">Effectif Saison 2025-2026</p>
              <div className="flex gap-4 mt-4">
                <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
                  <span className="font-bold text-2xl">{joueurs.length}</span>
                  <span className="ml-2">Joueurs</span>
                </div>
                <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-lg">
                  <span className="font-bold text-2xl">4</span>
                  <span className="ml-2">Catégories de stats</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Grille des joueurs */}
      <section className="container mx-auto px-4 pb-12">
        <h2 className="text-3xl font-bold text-gray-900 mb-8">Effectif professionnel</h2>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {joueurs.map(joueur => (
            <div key={joueur.id} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group">
              <div 
                className="h-2"
                style={{
                  background: `linear-gradient(90deg, ${primaryColor} 0%, ${secondaryColor} 100%)`
                }}
              />
              
              <div className="p-6">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {joueur.nom}
                    </h3>
                    <p className="text-sm text-gray-600 font-medium">{joueur.poste}</p>
                  </div>
                  <span 
                    className="text-3xl font-bold opacity-20"
                    style={{ color: primaryColor }}
                  >
                    #{joueur.numero}
                  </span>
                </div>
                
                <div className="space-y-2 mt-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Buts</span>
                    <span className="font-semibold">{joueur.buts}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Passes décisives</span>
                    <span className="font-semibold">{joueur.passes_decisives}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600">Minutes jouées</span>
                    <span className="font-semibold">{joueur.minutes}</span>
                  </div>
                </div>
                
                <Link 
                  href={`/${leagueId}/${clubId}/${joueur.id}`}
                  className="mt-4 inline-flex items-center text-blue-600 hover:text-blue-700 font-medium group"
                >
                  <span>Voir les stats</span>
                  <svg className="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </Link>
              </div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}