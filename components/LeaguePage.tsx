'use client';

import Link from 'next/link';
import Image from 'next/image';
import { useState } from 'react';
import SearchBar from '@/components/SearchBar';
import { leagueLogos } from '@/data/logos';
import { getClubLogoPath } from '@/data/clubLogosMapping';

interface Team {
  id: string | number;
  name: string;
  slug?: string;
  logo?: string;
  stadium?: string;
  founded?: number;
  colors?: string[];
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
  const [sortBy, setSortBy] = useState<'name' | 'position'>('position');

  // Classement Premier League 2025/2026
  const premierLeagueRanking: Record<string, number> = {
    'liverpool': 1,
    'arsenal': 2,
    'manchester-city': 3,
    'chelsea': 4,
    'newcastle': 5,
    'aston-villa': 6,
    'nottingham-forest': 7,
    'brighton': 8,
    'bournemouth': 9,
    'brentford': 10,
    'fulham': 11,
    'crystal-palace': 12,
    'everton': 13,
    'west-ham': 14,
    'manchester-united': 15,
    'wolves': 16,
    'tottenham': 17,
    // Clubs promus (n'étaient pas en Premier League 2025/2026)
    'burnley': 18,
    'sunderland': 19,
    'leeds': 20
  };

  // Classement Ligue 1 2025/2026
  const ligue1Ranking: Record<string, number> = {
    'psg': 1,
    'marseille': 2,
    'monaco': 3,
    'nice': 4,
    'lille': 5,
    'lyon': 6,
    'strasbourg': 7,
    'lens': 8,
    'brest': 9,
    'toulouse': 10,
    'auxerre': 11,
    'rennes': 12,
    'nantes': 13,
    'angers': 14,
    'le-havre': 15,
    // Clubs promus (Reims, Saint-Étienne, Montpellier ont été relégués)
    'paris-fc': 16,
    'metz': 17,
    'lorient': 18
  };

  // Classement Liga 2025/2026
  const ligaRanking: Record<string, number> = {
    'barcelona': 1,
    'real-madrid': 2,
    'atletico-madrid': 3,
    'athletic-bilbao': 4,
    'villarreal': 5,
    'real-betis': 6,
    'celta-vigo': 7,
    'rayo-vallecano': 8,
    'osasuna': 9,
    'mallorca': 10,
    'real-sociedad': 11,
    'valencia': 12,
    'getafe': 13,
    'espanyol': 14,
    'alaves': 15,
    'girona': 16,
    'sevilla': 17,
    // Clubs promus (Leganés, Las Palmas, Valladolid ne sont pas dans nos données)
    'levante': 18,
    'elche': 19,
    'real-oviedo': 20
  };

  // Classement Serie A 2025/2026
  const serieARanking: Record<string, number> = {
    'napoli': 1,
    'inter': 2,
    'atalanta': 3,
    'juventus': 4,
    'roma': 5,
    'fiorentina': 6,
    'lazio': 7,
    'milan': 8,
    'bologna': 9,
    'como': 10,
    'torino': 11,
    'udinese': 12,
    'genoa': 13,
    'verona': 14,
    'cagliari': 15,
    'parme': 16,
    'lecce': 17,
    // Clubs promus (Empoli, Venezia, Monza relégués)
    'sassuolo': 18,
    'cremonese': 19,
    'pise': 20
  };

  // Classement Bundesliga 2025/2026
  const bundesligaRanking: Record<string, number> = {
    'bayern': 1,
    'bayer-leverkusen': 2,
    'eintracht-frankfurt': 3,
    'borussia-dortmund': 4,
    'freiburg': 5,
    'mainz': 6,
    'leipzig': 7,
    'werder': 8,
    'stuttgart': 9,
    'borussia-monchengladbach': 10,
    'wolfsburg': 11,
    'augsburg': 12,
    'union-berlin': 13,
    'sankt-pauli': 14,
    'hoffenheim': 15,
    'heidenheim': 16,
    // Clubs promus (Holstein Kiel et VfL Bochum relégués)
    'koln': 17,
    'hambourg': 18
  };

  const filteredTeams = teams
    .filter(team => team.name.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      
      // Pour la Premier League, utiliser le classement personnalisé
      if (leagueId === 'premier-league') {
        const posA = premierLeagueRanking[String(a.id)] || 999;
        const posB = premierLeagueRanking[String(b.id)] || 999;
        return posA - posB;
      }
      
      // Pour la Ligue 1, utiliser le classement personnalisé
      if (leagueId === 'ligue1') {
        const posA = ligue1Ranking[String(a.id)] || 999;
        const posB = ligue1Ranking[String(b.id)] || 999;
        return posA - posB;
      }
      
      // Pour La Liga, utiliser le classement personnalisé
      if (leagueId === 'liga') {
        const posA = ligaRanking[a.slug] || 999;
        const posB = ligaRanking[b.slug] || 999;
        return posA - posB;
      }
      
      // Pour la Serie A, utiliser le classement personnalisé
      if (leagueId === 'serie-a') {
        const posA = serieARanking[a.slug] || 999;
        const posB = serieARanking[b.slug] || 999;
        return posA - posB;
      }
      
      // Pour la Bundesliga, utiliser le classement personnalisé
      if (leagueId === 'bundesliga') {
        const posA = bundesligaRanking[a.slug] || 999;
        const posB = bundesligaRanking[b.slug] || 999;
        return posA - posB;
      }
      
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
                Par classement (de la saison dernière)
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
                key={String(team.id)}
                href={`/${leagueId}/${team.slug || String(team.id)}`}
                className="group bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden transform hover:-translate-y-1"
              >
                <div className="relative h-32 bg-gradient-to-br from-gray-50 via-white to-gray-100">
                  <div className="absolute inset-0 flex items-center justify-center p-4">
                    <Image
                      src={getClubLogoPath(leagueId, team.slug || team.id)}
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
                  {team.stadium && <p className="text-sm text-gray-600 mb-3">{team.stadium}</p>}
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
                      {team.colors && team.colors.map((color, index) => (
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