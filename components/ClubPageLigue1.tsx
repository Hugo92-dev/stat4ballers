'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import { ligue1Teams } from '@/data/ligue1Teams';
import { slugifyPlayer } from '@/utils/slugify';
import { teamDetails } from '@/data/teamDetailsFromAPI';

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
          
          <div className="flex-1">
            <h1 className="text-5xl font-bold text-white mb-2">{team.nom}</h1>
            <p className="text-gray-300 text-lg">Effectif complet • Saison 2025/2026</p>
            <div className="flex flex-wrap gap-6 mt-4">
              <p className="text-gray-400">
                <span className="text-gray-500">Effectif:</span> {team.players.length} joueurs
              </p>
              {teamDetails[clubId]?.stadium && (
                <p className="text-gray-400">
                  <span className="text-gray-500">Stade:</span> {teamDetails[clubId].stadium}
                </p>
              )}
              {teamDetails[clubId]?.coach && (
                <p className="text-gray-400">
                  <span className="text-gray-500">Entraîneur:</span> {teamDetails[clubId].coach}
                </p>
              )}
              {teamDetails[clubId]?.founded && (
                <p className="text-gray-400">
                  <span className="text-gray-500">Fondé en:</span> {teamDetails[clubId].founded}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Infos du club et Palmarès */}
      {teamDetails[clubId]?.trophies && Object.keys(teamDetails[clubId].trophies!).length > 0 && (
        <div className="max-w-7xl mx-auto px-8 py-6">
          <div className="bg-gradient-to-r from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <span className="text-3xl mr-3">🏆</span> Palmarès
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {Object.entries(teamDetails[clubId].trophies!).map(([trophy, count]) => (
                <div key={trophy} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                  <span className="text-gray-300 text-sm">{trophy}</span>
                  <span className="text-yellow-400 font-bold text-lg">{count}x</span>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-gray-700">
              <p className="text-gray-400">
                Total: <span className="text-yellow-400 font-bold">
                  {Object.values(teamDetails[clubId].trophies!).reduce((a, b) => a + b, 0)}
                </span> trophées
              </p>
            </div>
          </div>
        </div>
      )}

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
                            <div className="relative w-12 h-12">
                              {player.image ? (
                                <img
                                  src={player.image}
                                  alt={playerDisplayName}
                                  className="w-12 h-12 rounded-full object-cover border-2 border-gray-600"
                                  onError={(e) => {
                                    e.currentTarget.style.display = 'none';
                                    const fallback = e.currentTarget.nextElementSibling as HTMLElement;
                                    if (fallback) fallback.style.display = 'flex';
                                  }}
                                />
                              ) : null}
                              <div 
                                className={`w-12 h-12 bg-gradient-to-br from-gray-600 to-gray-800 rounded-full flex items-center justify-center text-white font-bold ${player.image ? 'hidden' : ''}`}
                                style={player.image ? { display: 'none' } : {}}
                              >
                                {player.jersey || player.name.charAt(0)}
                              </div>
                              {player.jersey && (
                                <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-black rounded-full flex items-center justify-center text-white text-xs font-bold border border-gray-600">
                                  {player.jersey}
                                </div>
                              )}
                            </div>
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