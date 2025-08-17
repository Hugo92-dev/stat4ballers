'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useState } from 'react';
import SearchBar from '@/components/SearchBar';
import { leagueLogos } from '@/data/logos';
import { getClubLogoPath } from '@/data/clubLogosMapping';

interface Team {
  id: string;
  name: string;
  logo?: string;
  stadium: string;
  founded: number;
  colors: string[];
  stats?: {
    position: number;
    points: number;
    played: number;
    wins: number;
    draws: number;
    losses: number;
  };
}

interface LeaguePageProps {
  leagueId: string;
  leagueName: string;
  leagueFlag: string;
  teams: Team[];
  gradient: string;
}

export default function LeaguePage({ leagueId, leagueName, leagueFlag, teams, gradient }: LeaguePageProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'name' | 'position'>('name');

  const filteredTeams = teams
    .filter(team => team.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      return (a.stats?.position || 999) - (b.stats?.position || 999);
    });

  return (
    <main className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className={`relative overflow-hidden bg-gradient-to-br ${gradient}`}>
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative container mx-auto px-4 py-16 md:py-24">
          <div className="text-center">
            <div className="flex flex-col items-center justify-center mb-6">
              <div className="mb-6">
                <Image
                  src={leagueLogos[leagueId]}
                  alt={leagueName}
                  width={120}
                  height={120}
                  className="drop-shadow-2xl"
                />
              </div>
              <h1 className="text-4xl md:text-6xl font-bold text-white">
                {leagueName}
              </h1>
            </div>
            <p className="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
              Explorez les statistiques détaillées de tous les clubs et joueurs
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <div className="bg-white/20 backdrop-blur-md px-6 py-3 rounded-full text-white">
                <span className="font-bold text-lg">{teams.length}</span> Clubs
              </div>
              <div className="bg-white/20 backdrop-blur-md px-6 py-3 rounded-full text-white">
                <span className="font-bold text-lg">500+</span> Joueurs
              </div>
              <div className="bg-white/20 backdrop-blur-md px-6 py-3 rounded-full text-white">
                <span className="font-bold text-lg">4</span> Catégories de stats
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Filters Section */}
      <section className="sticky top-16 z-40 bg-white shadow-md">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <div className="flex-1 w-full md:max-w-md">
              <input
                type="text"
                placeholder="Rechercher un club..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
              />
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => setSortBy('name')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  sortBy === 'name' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Par nom
              </button>
              <button
                onClick={() => setSortBy('position')}
                className={`px-4 py-2 rounded-lg transition-colors ${
                  sortBy === 'position' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                Par classement
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Teams Grid */}
      <section className="py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredTeams.map((team) => (
              <Link
                key={team.id}
                href={`/${leagueId}/${team.id}`}
                className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden transform hover:-translate-y-1"
              >
                <div className="relative h-32 bg-gradient-to-br from-gray-50 via-white to-gray-100">
                  <div className="absolute inset-0 flex items-center justify-center p-4">
                    <Image
                      src={getClubLogoPath(leagueId, team.id)}
                      alt={team.name}
                      width={80}
                      height={80}
                      className="object-contain drop-shadow-lg"
                      onError={(e) => {
                        const img = e.target as HTMLImageElement;
                        img.style.display = 'none';
                        const fallback = img.nextElementSibling as HTMLElement;
                        if (fallback) fallback.style.display = 'flex';
                      }}
                    />
                    <div className="w-20 h-20 bg-gradient-to-br from-gray-200 to-gray-300 rounded-full items-center justify-center hidden">
                      <span className="text-2xl font-bold text-gray-600">
                        {team.name.substring(0, 2).toUpperCase()}
                      </span>
                    </div>
                  </div>
                  {team.stats?.position && (
                    <div className="absolute top-2 right-2 bg-black/70 text-white px-2 py-1 rounded-full text-sm font-bold">
                      #{team.stats.position}
                    </div>
                  )}
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-bold mb-2 text-gray-900 group-hover:text-blue-600 transition-colors">
                    {team.name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3">{team.stadium}</p>
                  {team.stats && (
                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div className="bg-gray-50 rounded-lg p-2">
                        <div className="text-lg font-bold text-gray-900">{team.stats.points}</div>
                        <div className="text-xs text-gray-500">Points</div>
                      </div>
                      <div className="bg-gray-50 rounded-lg p-2">
                        <div className="text-lg font-bold text-green-600">{team.stats.wins}</div>
                        <div className="text-xs text-gray-500">Victoires</div>
                      </div>
                      <div className="bg-gray-50 rounded-lg p-2">
                        <div className="text-lg font-bold text-gray-900">{team.stats.played}</div>
                        <div className="text-xs text-gray-500">Matchs</div>
                      </div>
                    </div>
                  )}
                  <div className="mt-4 flex items-center justify-between">
                    <div className="flex gap-1">
                      {team.colors.map((color, index) => (
                        <div
                          key={index}
                          className="w-6 h-6 rounded-full border border-gray-300"
                          style={{ backgroundColor: color }}
                        />
                      ))}
                    </div>
                    <svg className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transform group-hover:translate-x-1 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}