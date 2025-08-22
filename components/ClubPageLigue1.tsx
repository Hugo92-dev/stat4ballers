'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import { ligue1Teams } from '@/data/ligue1Teams';
import { slugifyPlayer } from '@/utils/slugify';

interface ClubPageProps {
  clubId: string;
  clubName: string;
  leagueId: string;
  leagueName: string;
  primaryColor?: string;
  secondaryColor?: string;
}

export default function ClubPageLigue1({ 
  clubId, 
  clubName, 
  leagueId, 
  leagueName,
  primaryColor = '#1e3a8a',
  secondaryColor = '#ffffff'
}: ClubPageProps) {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Trouver l'équipe dans les données
  const team = ligue1Teams.find(t => t.slug === clubId);
  
  if (!team) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black p-8">
        <div className="max-w-7xl mx-auto text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Équipe non trouvée</h1>
          <Link href="/ligue1" className="text-blue-400 hover:underline">
            Retour à la Ligue 1
          </Link>
        </div>
      </div>
    );
  }
  
  // Calculer l'âge à partir de la date de naissance
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
  
  // Filtrer les joueurs selon la recherche
  const filteredPlayers = team.players.filter(player =>
    player.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    player.position.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (player.nationality && player.nationality.toLowerCase().includes(searchTerm.toLowerCase()))
  );
  
  // Grouper les joueurs par position
  const playersByPosition = {
    GK: filteredPlayers.filter(p => p.position === 'GK'),
    DF: filteredPlayers.filter(p => ['DF', 'CB', 'LB', 'RB'].includes(p.position)),
    MF: filteredPlayers.filter(p => ['MF', 'DM', 'CM', 'AM', 'LM', 'RM'].includes(p.position)),
    FW: filteredPlayers.filter(p => ['FW', 'ST', 'CF', 'LW', 'RW'].includes(p.position)),
    Unknown: filteredPlayers.filter(p => p.position === 'Unknown')
  };
  
  const getPositionLabel = (key: string) => {
    const labels: Record<string, string> = {
      GK: 'Gardiens',
      DF: 'Défenseurs',
      MF: 'Milieux',
      FW: 'Attaquants',
      Unknown: 'Non défini'
    };
    return labels[key] || key;
  };
  
  const getPositionColor = (key: string) => {
    const colors: Record<string, string> = {
      GK: 'from-yellow-500 to-yellow-600',
      DF: 'from-blue-500 to-blue-600',
      MF: 'from-green-500 to-green-600',
      FW: 'from-red-500 to-red-600',
      Unknown: 'from-gray-500 to-gray-600'
    };
    return colors[key] || 'from-gray-500 to-gray-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black">
      {/* Header */}
      <div className="relative bg-gradient-to-r from-gray-900 to-black p-8 shadow-2xl border-b border-gray-700">
        <Link 
          href={`/${leagueId}`}
          className="inline-flex items-center text-gray-300 hover:text-white transition-colors mb-6 group"
        >
          <svg className="w-5 h-5 mr-2 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Retour à {leagueName}
        </Link>
        
        <div className="flex items-center gap-8">
          <div className="relative w-32 h-32 bg-white rounded-2xl p-4 shadow-xl">
            <Image
              src={getClubLogoPath(leagueId, clubId)}
              alt={clubName}
              fill
              className="object-contain p-2"
            />
          </div>
          
          <div>
            <h1 className="text-5xl font-bold text-white mb-2">{team.name}</h1>
            <p className="text-gray-300 text-lg">Effectif complet • Saison 2024/2025</p>
            <p className="text-gray-400 mt-2">{team.players.length} joueurs</p>
          </div>
        </div>
      </div>

      {/* Barre de recherche */}
      <div className="max-w-7xl mx-auto px-8 py-6">
        <div className="relative max-w-md mx-auto">
          <input
            type="text"
            placeholder="Rechercher un joueur..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-6 py-3 bg-gray-800 text-white rounded-full border border-gray-700 focus:border-blue-500 focus:outline-none pl-12"
          />
          <svg className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>
      </div>

      {/* Liste des joueurs par position */}
      <div className="max-w-7xl mx-auto px-8 pb-12">
        {Object.entries(playersByPosition).map(([position, players]) => {
          if (players.length === 0) return null;
          
          return (
            <div key={position} className="mb-8">
              <div className={`bg-gradient-to-r ${getPositionColor(position)} text-white px-6 py-3 rounded-t-xl`}>
                <h2 className="text-xl font-bold">{getPositionLabel(position)} ({players.length})</h2>
              </div>
              
              <div className="bg-gray-800 rounded-b-xl overflow-hidden">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
                  {players.map((player) => {
                    const playerDisplayName = player.displayName || player.fullName || player.name;
                    const playerSlug = slugifyPlayer(playerDisplayName);
                    return (
                      <Link
                        key={player.id}
                        href={`/ligue1/${clubId}/${playerSlug}`}
                        className="bg-gray-700 rounded-xl p-4 hover:bg-gray-600 transition-all hover:scale-105 cursor-pointer block"
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div className="flex items-center gap-3">
                            {player.jersey && (
                              <div className="w-10 h-10 bg-gradient-to-br from-gray-600 to-gray-800 rounded-full flex items-center justify-center text-white font-bold">
                                {player.jersey}
                              </div>
                            )}
                            <div>
                              <h3 className="text-white font-semibold text-lg">{playerDisplayName}</h3>
                              <p className="text-gray-400 text-sm">{player.position}</p>
                            </div>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-2 gap-2 mt-3 text-sm">
                          {player.dateOfBirth && (
                            <div className="text-gray-400">
                              <span className="text-gray-500">Âge:</span> {calculateAge(player.dateOfBirth)} ans
                            </div>
                          )}
                          {player.nationality && player.nationality !== 'Unknown' && (
                            <div className="text-gray-400">
                              <span className="text-gray-500">Nationalité:</span> {player.nationality}
                            </div>
                          )}
                          {player.height && (
                            <div className="text-gray-400">
                              <span className="text-gray-500">Taille:</span> {player.height} cm
                            </div>
                          )}
                          {player.weight && (
                            <div className="text-gray-400">
                              <span className="text-gray-500">Poids:</span> {player.weight} kg
                            </div>
                          )}
                        </div>
                      </Link>
                    );
                  })}
                </div>
              </div>
            </div>
          );
        })}
        
        {filteredPlayers.length === 0 && (
          <div className="text-center py-12 text-gray-400">
            <p className="text-xl">Aucun joueur trouvé</p>
          </div>
        )}
      </div>
    </div>
  );
}