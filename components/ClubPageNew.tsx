'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import { ligue1Data } from '@/data/ligue1Data';

interface ClubPageProps {
  clubId: string;
  clubName: string;
  leagueId: string;
  leagueName: string;
  primaryColor?: string;
  secondaryColor?: string;
}

interface Player {
  id: number;
  nom: string;
  position: string;
  position_id: number;
  age: string; // Date de naissance
  nationalite: string;
  numero: number | null;
  taille: number | null;
  poids: number | null;
}

export default function ClubPageNew({ 
  clubId, 
  clubName, 
  leagueId, 
  leagueName,
  primaryColor = '#1e3a8a',
  secondaryColor = '#ffffff'
}: ClubPageProps) {
  // State pour la recherche
  const [searchTerm, setSearchTerm] = useState('');
  
  // Fonction pour calculer l'âge à partir de la date de naissance
  const calculateAge = (birthDate: string): number => {
    if (!birthDate) return 0;
    const today = new Date();
    const birth = new Date(birthDate);
    let age = today.getFullYear() - birth.getFullYear();
    const monthDiff = today.getMonth() - birth.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
      age--;
    }
    return age;
  };
  
  // Récupérer les joueurs depuis les données TypeScript générées
  const getPlayers = () => {
    if (leagueId === 'ligue1') {
      // Nouveau format : objet avec des clés basées sur les slugs d'équipes
      const clubData = ligue1Data[clubId as keyof typeof ligue1Data];
      return clubData?.players || [];
    }
    return [];
  };

  const joueurs = getPlayers();
  
  // Trier les joueurs par position
  const positionOrder: Record<string, number> = {
    'Gardien': 1,
    'Défenseur': 2,
    'Milieu': 3,
    'Attaquant': 4
  };
  
  const joueursTries = [...joueurs].sort((a, b) => {
    const orderA = positionOrder[a.position] || 5;
    const orderB = positionOrder[b.position] || 5;
    return orderA - orderB;
  });
  
  // Filtrer les joueurs selon la recherche
  const joueursFiltres = joueursTries.filter((joueur: Player) => {
    const search = searchTerm.toLowerCase();
    return (
      joueur.nom.toLowerCase().includes(search) ||
      joueur.position.toLowerCase().includes(search) ||
      joueur.nationalite.toLowerCase().includes(search) ||
      (joueur.numero && joueur.numero.toString().includes(search))
    );
  });

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
        <h2 className="text-3xl font-bold text-gray-900 mb-4">Effectif professionnel</h2>
        
        {/* Barre de recherche */}
        {joueurs.length > 0 && (
          <div className="mb-8">
            <div className="relative max-w-md">
              <input
                type="text"
                placeholder="Rechercher un joueur, position, nationalité..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 pl-10 pr-4 text-gray-700 bg-white border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-colors"
              />
              <svg
                className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
              {searchTerm && (
                <button
                  onClick={() => setSearchTerm('')}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
            {searchTerm && (
              <p className="mt-2 text-sm text-gray-600">
                {joueursFiltres.length} joueur{joueursFiltres.length > 1 ? 's' : ''} trouvé{joueursFiltres.length > 1 ? 's' : ''}
              </p>
            )}
          </div>
        )}
        
        {joueurs.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg">
            <p className="text-gray-600">Aucun joueur disponible pour ce club.</p>
            <p className="text-sm text-gray-500 mt-2">Les données seront ajoutées prochainement.</p>
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {joueursFiltres.map((joueur: Player, index: number) => (
              <div key={joueur.id || `player-${index}`} className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 overflow-hidden group">
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
                      <div className="flex items-center gap-2 mt-1">
                        <span className="text-sm text-gray-600 font-medium">{joueur.position}</span>
                        {joueur.nationalite && (
                          <span className="text-xs text-gray-500">• {joueur.nationalite}</span>
                        )}
                      </div>
                    </div>
                    <span 
                      className="text-3xl font-bold opacity-20"
                      style={{ color: primaryColor }}
                    >
                      #{joueur.numero || '?'}
                    </span>
                  </div>
                  
                  <div className="space-y-2 mt-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Nationalité</span>
                      <span className="font-semibold">{joueur.nationalite}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Âge</span>
                      <span className="font-semibold">{calculateAge(joueur.age)} ans</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Taille</span>
                      <span className="font-semibold">{joueur.taille ? `${joueur.taille} cm` : '-'}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Poids</span>
                      <span className="font-semibold">{joueur.poids ? `${joueur.poids} kg` : '-'}</span>
                    </div>
                  </div>
                  
                  <Link 
                    href={`/${leagueId}/${clubId}/${joueur.nom.toLowerCase().replace(/\s+/g, '-')}`}
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
        )}
      </section>
    </main>
  );
}