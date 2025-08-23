'use client';

import { useState, useEffect } from 'react';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import { fullSearchDatabase as searchDatabase } from '@/data/searchDatabase';
import { getPlayerStatistics, PlayerStatistics } from '@/services/sportmonks';
import { generateMockStatsForPlayer } from '@/services/mockData';
import PlayerComparisonRadar from '@/components/PlayerComparisonRadar';
import PlayerComparisonList from '@/components/PlayerComparisonList';
import ViewSelector from '@/components/stats/ViewSelector';

interface Player {
  id: number;
  name: string;
  fullName?: string;
  displayName?: string;
  position: string;
  club: string;
  league: string;
  clubSlug: string;
  leagueSlug: string;
  playerSlug: string;
  image?: string;
}

interface PlayerWithStats extends Player {
  stats: PlayerStatistics;
}

export default function ComparePage() {
  const searchParams = useSearchParams();
  const [players, setPlayers] = useState<PlayerWithStats[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentView, setCurrentView] = useState<'list' | 'radar'>('radar');

  useEffect(() => {
    const loadPlayersData = async () => {
      try {
        setLoading(true);
        setError(null);

        const playerIds = searchParams.get('players')?.split(',').map(id => parseInt(id)) || [];
        
        if (playerIds.length < 2) {
          setError('Au moins 2 joueurs sont nécessaires pour la comparaison');
          return;
        }

        const playersData: PlayerWithStats[] = [];

        for (const playerId of playerIds) {
          // Trouver le joueur dans la base de données de recherche
          const playerResult = searchDatabase.find(item => 
            item.type === 'player' && item.id === playerId
          );

          if (!playerResult) {
            console.warn(`Joueur avec l'ID ${playerId} non trouvé`);
            continue;
          }

          // Extraire les informations du joueur
          const pathParts = playerResult.path.split('/');
          const leagueSlug = pathParts[1];
          const clubSlug = pathParts[2];
          const playerSlug = pathParts[3];

          // Récupérer l'image du joueur depuis les données des équipes
          let playerImage: string | undefined;
          try {
            // Importer dynamiquement les données de l'équipe
            const leagueDataFile = leagueSlug.replace('-', '') + 'Teams';
            const teamData = await import(`@/data/${leagueDataFile === 'ligaTeams' ? 'ligaTeams' : leagueDataFile === 'serieaTeams' ? 'serieATeams' : leagueDataFile}`);
            const teams = teamData[leagueDataFile] || teamData.default;
            
            // Trouver l'équipe et le joueur
            const team = teams.find((t: any) => t.slug === clubSlug);
            if (team) {
              const playerData = team.players.find((p: any) => p.id === playerId);
              if (playerData) {
                playerImage = playerData.image;
              }
            }
          } catch (err) {
            console.warn(`Impossible de charger l'image pour le joueur ${playerId}`);
          }

          const player: Player = {
            id: playerId,
            name: playerResult.name,
            fullName: playerResult.fullName,
            displayName: playerResult.displayName,
            position: playerResult.position || 'Unknown',
            club: playerResult.club || 'Unknown Club',
            league: playerResult.league || 'Unknown League',
            clubSlug,
            leagueSlug,
            playerSlug,
            image: playerImage
          };

          // Charger les statistiques du joueur
          const leagueKey = leagueSlug.replace('-', '') as 'ligue1' | 'premierLeague' | 'liga' | 'serieA' | 'bundesliga';
          
          try {
            let stats = await getPlayerStatistics(playerId, leagueKey);
            
            // Si pas de données réelles, utiliser des données simulées
            if (!stats.current || (stats.current.minutes === 0 && stats.current.appearences === 0)) {
              const mockStatsData = generateMockStatsForPlayer(player);
              stats = {
                current: mockStatsData.current,
                previous: mockStatsData.previous,
                cumulative: mockStatsData.current // Utiliser current comme cumulative pour la comparaison
              };
            }

            // Utiliser les stats cumulatives pour la comparaison, sinon current
            const playerStats = stats.cumulative || stats.current;
            
            if (playerStats) {
              playersData.push({
                ...player,
                stats: playerStats
              });
            }
          } catch (err) {
            console.error(`Erreur lors du chargement des stats pour ${player.name}:`, err);
            // Générer des stats mock en cas d'erreur
            const mockStatsData = generateMockStatsForPlayer(player);
            playersData.push({
              ...player,
              stats: mockStatsData.current
            });
          }
        }

        if (playersData.length < 2) {
          setError('Impossible de charger les données de comparaison');
          return;
        }

        setPlayers(playersData);
      } catch (err) {
        console.error('Erreur lors du chargement des joueurs:', err);
        setError('Erreur lors du chargement des données');
      } finally {
        setLoading(false);
      }
    };

    loadPlayersData();
  }, [searchParams]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600 text-lg">Chargement de la comparaison...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">Erreur de comparaison</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <Link 
            href="/"
            className="inline-flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            <ArrowLeft className="w-4 h-4" />
            Retour à l'accueil
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-8">
        <div className="max-w-7xl mx-auto px-4">
          <Link 
            href="/"
            className="inline-flex items-center gap-2 text-white/80 hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Retour à l'accueil
          </Link>
          
          <div className="mb-4">
            <h1 className="text-3xl font-bold">Comparaison de Joueurs</h1>
            <p className="text-white/80">Analyse comparative des performances</p>
          </div>

          {/* Joueurs comparés */}
          <div className="flex flex-wrap gap-4">
            {players.map((player, index) => (
              <div key={player.id} className="flex items-center gap-3 bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3">
                <div className="relative">
                  {player.image ? (
                    <img
                      src={player.image}
                      alt={player.displayName || player.fullName || player.name}
                      className="w-12 h-12 rounded-full object-cover border-2 border-white/30"
                      onError={(e) => {
                        e.currentTarget.style.display = 'none';
                        const fallback = e.currentTarget.nextElementSibling as HTMLElement;
                        if (fallback) fallback.style.display = 'flex';
                      }}
                    />
                  ) : null}
                  <div 
                    className={`w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-lg font-bold ${player.image ? 'hidden' : ''}`}
                    style={player.image ? { display: 'none' } : {}}
                  >
                    {index + 1}
                  </div>
                  <div className="absolute -bottom-1 -right-1 w-5 h-5 bg-white rounded-full flex items-center justify-center text-xs font-bold text-gray-800">
                    {index + 1}
                  </div>
                </div>
                <div>
                  <Link 
                    href={`/${player.leagueSlug}/${player.clubSlug}/${player.playerSlug}`}
                    className="font-medium hover:underline"
                  >
                    {player.displayName || player.fullName || player.name}
                  </Link>
                  <div className="text-sm text-white/70">
                    <Link 
                      href={`/${player.leagueSlug}/${player.clubSlug}`}
                      className="hover:underline"
                    >
                      {player.club}
                    </Link>
                    <span> • {player.position}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Contenu principal */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          {/* Sélecteur de vue */}
          <div className="mb-8">
            <ViewSelector
              currentView={currentView}
              onViewChange={setCurrentView}
            />
          </div>

          {/* Affichage selon la vue sélectionnée */}
          {currentView === 'radar' ? (
            <PlayerComparisonRadar players={players} />
          ) : (
            <PlayerComparisonList players={players} />
          )}
        </div>
      </div>
    </div>
  );
}