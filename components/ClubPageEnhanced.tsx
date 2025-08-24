'use client';

import { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { getClubLogoPath } from '@/data/clubLogosMapping';
import { slugifyPlayer } from '@/utils/slugify';
import { teamDetails } from '@/data/teamDetails';

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
}

interface ClubPageEnhancedProps {
  clubId: string;
  clubName: string;
  leagueId: string;
  leagueName: string;
  teams: Team[];
  primaryColor?: string;
  secondaryColor?: string;
}

export default function ClubPageEnhanced({ 
  clubId, 
  clubName, 
  leagueId, 
  leagueName,
  teams,
  primaryColor = '#1e3a8a',
  secondaryColor = '#ffffff'
}: ClubPageEnhancedProps) {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Trouver l'équipe dans les données
  const team = teams.find(t => t.slug === clubId);
  const details = teamDetails[clubId];
  
  if (!team) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 to-black p-8">
        <div className="max-w-7xl mx-auto text-center text-white">
          <h1 className="text-3xl font-bold mb-4">Équipe non trouvée</h1>
          <Link href={`/${leagueId}`} className="text-blue-400 hover:underline">
            Retour à {leagueName}
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
  const filteredPlayers = team.players.filter(player => {
    const name = player.nom || player.name || '';
    const position = player.position || '';
    const nationality = player.nationalite || player.nationality || '';
    
    return name.toLowerCase().includes(searchTerm.toLowerCase()) ||
           position.toLowerCase().includes(searchTerm.toLowerCase()) ||
           nationality.toLowerCase().includes(searchTerm.toLowerCase());
  });
  
  // Grouper les joueurs par position
  const playersByPosition = {
    GK: filteredPlayers.filter(p => p.position === 'GK' || p.position === 'Goalkeeper'),
    DF: filteredPlayers.filter(p => ['DF', 'CB', 'LB', 'RB', 'Defender'].includes(p.position)),
    MF: filteredPlayers.filter(p => ['MF', 'DM', 'CM', 'AM', 'LM', 'RM', 'Midfielder'].includes(p.position)),
    FW: filteredPlayers.filter(p => ['FW', 'ST', 'CF', 'LW', 'RW', 'Attacker'].includes(p.position)),
    Unknown: filteredPlayers.filter(p => p.position === 'Unknown' || !p.position)
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
            <h1 className="text-5xl font-bold text-white mb-2">{team.name}</h1>
            <p className="text-gray-300 text-lg">Effectif complet • Saison 2025/2026</p>
            <div className="flex flex-wrap gap-6 mt-4">
              <p className="text-gray-400">
                <span className="text-gray-500">Effectif:</span> {team.players.length} joueurs
              </p>
              {details?.stadium && (
                <p className="text-gray-400">
                  <span className="text-gray-500">Stade:</span> {details.stadium}
                  {details.capacity && ` (${details.capacity.toLocaleString()} places)`}
                </p>
              )}
              {details?.coach && (
                <p className="text-gray-400">
                  <span className="text-gray-500">Entraîneur:</span> {details.coach}
                </p>
              )}
              {details?.founded && (
                <p className="text-gray-400">
                  <span className="text-gray-500">Fondé en:</span> {details.founded}
                </p>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Infos du club et Palmarès */}
      {details?.trophies && Object.keys(details.trophies).length > 0 && (
        <div className="max-w-7xl mx-auto px-8 py-6">
          <div className="bg-gradient-to-r from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-700">
            <h2 className="text-2xl font-bold text-white mb-4 flex items-center">
              <span className="text-3xl mr-3">🏆</span> Palmarès
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {Object.entries(details.trophies).map(([trophy, count]) => (
                <div key={trophy} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                  <span className="text-gray-300 text-sm">{trophy}</span>
                  <span className="text-yellow-400 font-bold text-lg">{count}x</span>
                </div>
              ))}
            </div>
            <div className="mt-4 pt-4 border-t border-gray-700">
              <p className="text-gray-400">
                Total: <span className="text-yellow-400 font-bold">
                  {Object.values(details.trophies).reduce((a, b) => a + b, 0)}
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
              <h2 className={`text-xl font-bold mb-4 bg-gradient-to-r ${getPositionColor(position)} bg-clip-text text-transparent`}>
                {getPositionLabel(position)} ({players.length})
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {players.map((player) => {
                  const playerName = player.displayName || player.nom || player.name || 'Unknown';
                  const playerSlug = player.playerSlug || slugifyPlayer(playerName);
                  const jerseyNumber = player.numero ?? player.jersey_number;
                  const nationality = player.nationalite || player.nationality;
                  const height = player.taille ?? player.height;
                  const weight = player.poids ?? player.weight;
                  
                  return (
                    <Link
                      key={player.id}
                      href={`/${leagueId}/${clubId}/${playerSlug}`}
                      className="group bg-gradient-to-r from-gray-800 to-gray-900 rounded-xl p-4 hover:from-gray-700 hover:to-gray-800 transition-all duration-300 transform hover:scale-[1.02] border border-gray-700 hover:border-blue-500"
                    >
                      <div className="flex items-center gap-4">
                        <div className="relative w-16 h-16 bg-gray-700 rounded-full overflow-hidden flex-shrink-0">
                          {player.image ? (
                            <Image
                              src={player.image}
                              alt={playerName}
                              fill
                              className="object-cover"
                            />
                          ) : (
                            <div className="w-full h-full flex items-center justify-center text-gray-400">
                              <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                              </svg>
                            </div>
                          )}
                          {jerseyNumber && (
                            <div className="absolute -bottom-1 -right-1 w-6 h-6 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-bold">
                              {jerseyNumber}
                            </div>
                          )}
                        </div>
                        
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-white group-hover:text-blue-400 transition-colors truncate">
                            {playerName}
                          </h3>
                          <div className="flex items-center gap-3 text-sm text-gray-400 mt-1">
                            <span>{player.position}</span>
                            {nationality && (
                              <>
                                <span className="text-gray-600">•</span>
                                <span className="truncate">{nationality}</span>
                              </>
                            )}
                          </div>
                          <div className="flex items-center gap-3 text-xs text-gray-500 mt-1">
                            {player.age && <span>{player.age} ans</span>}
                            {height && (
                              <>
                                {player.age && <span className="text-gray-600">•</span>}
                                <span>{height} cm</span>
                              </>
                            )}
                          </div>
                        </div>
                        
                        <svg className="w-5 h-5 text-gray-600 group-hover:text-blue-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </Link>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}