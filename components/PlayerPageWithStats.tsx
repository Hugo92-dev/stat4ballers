'use client';

import { useState, useEffect } from 'react';
import { Player } from '@/data/types';
import Link from 'next/link';
import { ArrowLeft } from 'lucide-react';
import StatsCards from '@/components/stats/StatsCards';
import StatsRadar from '@/components/stats/StatsRadar';
import SeasonSelector from '@/components/stats/SeasonSelector';
import ViewSelector from '@/components/stats/ViewSelector';
import { getPlayerStatistics, PlayerStatsResponse, PlayerStatistics } from '@/services/sportmonks';
import { slugifyPlayer } from '@/utils/slugify';
import { getOMPlayerIds } from '@/services/sportmonks';

interface PlayerPageWithStatsProps {
  player: Player;
  clubName: string;
  clubSlug: string;
  leagueSlug: string;
  leagueColor: string;
}

export default function PlayerPageWithStats({ 
  player, 
  clubName, 
  clubSlug, 
  leagueSlug,
  leagueColor 
}: PlayerPageWithStatsProps) {
  const [statsData, setStatsData] = useState<PlayerStatsResponse | null>(null);
  const [selectedSeason, setSelectedSeason] = useState<string>('current');
  const [currentView, setCurrentView] = useState<'list' | 'radar'>('radar'); // Vue Radar par défaut
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Calculer l'âge à partir de la date de naissance
  const calculateAge = (birthDate: string | undefined): number => {
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

  const age = calculateAge(player.dateOfBirth);

  // Charger les statistiques du joueur
  useEffect(() => {
    async function loadStats() {
      try {
        setLoading(true);
        setError(null);
        
        // Utiliser l'ID du joueur directement depuis les données
        const playerId = player.id;
        
        // Déterminer la ligue
        const leagueKey = leagueSlug.replace('-', '') as 'ligue1' | 'premierLeague' | 'liga' | 'serieA' | 'bundesliga';
        
        // Récupérer les statistiques via l'API
        const response = await fetch(`/api/player-stats?playerId=${playerId}&league=${leagueKey}`);
        
        if (!response.ok) {
          throw new Error(`Failed to fetch stats: ${response.status}`);
        }
        
        const stats = await response.json();
        
        // Si pas de données réelles, utiliser des données simulées pour tester
        // Note: 0 est une vraie valeur (joueur n'a pas joué), null/undefined = pas de données
        if (!stats.current) {
          // Importer les données simulées
          const { generateMockStatsForPlayer } = await import('@/services/mockData');
          const mockStats = generateMockStatsForPlayer(player);
          
          // Calculer le cumul
          const { calculateCumulativeStats } = await import('@/services/sportmonks');
          const allStats = [mockStats.current, ...mockStats.previous].filter(s => s !== null);
          const cumulative = calculateCumulativeStats(allStats as any);
          
          setStatsData({
            current: mockStats.current,
            previous: mockStats.previous,
            cumulative: cumulative
          });
        } else {
          setStatsData(stats);
        }
        
        // Sélectionner la meilleure vue par défaut
        // On affiche toujours les saisons même avec 0 match (c'est une info valide)
        if (stats.cumulative && stats.cumulative.appearences !== null && stats.cumulative.appearences !== undefined) {
          // Si on a des données cumulées, les afficher par défaut
          setSelectedSeason('cumulative');
        } else if (stats.current) {
          // Sinon, afficher la saison actuelle si elle existe
          setSelectedSeason('current');
        } else {
          // Sinon, chercher la première saison avec des données
          const firstWithData = stats.previous.find(s => s && (s.minutes > 0 || s.appearences > 0));
          if (firstWithData) {
            setSelectedSeason('previous-0');
          }
        }
      } catch (err) {
        console.error('Erreur détaillée lors du chargement des statistiques:', err);
        console.error('Player ID:', playerId);
        console.error('League Key:', leagueKey);
        setError('Erreur lors du chargement des statistiques: ' + (err as Error).message);
      } finally {
        setLoading(false);
      }
    }
    
    // Charger les stats pour tous les joueurs
    loadStats();
  }, [player, clubSlug, leagueSlug]);

  // Obtenir les statistiques de la saison sélectionnée
  const getSelectedSeasonStats = (): PlayerStatistics | null => {
    if (!statsData) return null;
    
    if (selectedSeason === 'cumulative') {
      return statsData.cumulative;
    } else if (selectedSeason === 'current') {
      return statsData.current;
    } else if (selectedSeason.startsWith('previous-')) {
      const index = parseInt(selectedSeason.replace('previous-', ''));
      return statsData.previous[index] || null;
    }
    
    return null;
  };

  const selectedStats = getSelectedSeasonStats();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className={`bg-gradient-to-r ${leagueColor} text-white py-8`}>
        <div className="max-w-7xl mx-auto px-4">
          <Link 
            href={`/${leagueSlug}/${clubSlug}`}
            className="inline-flex items-center gap-2 text-white/80 hover:text-white mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Retour à l'effectif
          </Link>
          
          <div className="flex items-center gap-4">
            <div className="relative">
              {player.image ? (
                <img
                  src={player.image}
                  alt={player.displayName || player.fullName || player.name}
                  className="w-24 h-24 rounded-full object-cover border-4 border-white/30"
                  onError={(e) => {
                    e.currentTarget.style.display = 'none';
                    const fallback = e.currentTarget.nextElementSibling as HTMLElement;
                    if (fallback) fallback.style.display = 'flex';
                  }}
                />
              ) : null}
              <div 
                className={`w-24 h-24 bg-white/20 rounded-full flex items-center justify-center ${player.image ? 'hidden' : ''}`}
                style={player.image ? { display: 'none' } : {}}
              >
                <span className="text-3xl font-bold">{player.jersey || player.number || '?'}</span>
              </div>
              {(player.jersey || player.number) && (
                <div className="absolute -bottom-2 -right-2 w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-lg">
                  <span className="text-lg font-bold text-gray-800">{player.jersey || player.number}</span>
                </div>
              )}
            </div>
            <div>
              <h1 className="text-3xl font-bold">
                {player.displayName || player.fullName || player.name}
              </h1>
              <Link 
                href={`/${leagueSlug}/${clubSlug}`}
                className="text-xl text-white/80 hover:text-white transition-colors inline-block"
              >
                {clubName}
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Player Info */}
      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold mb-6">Informations</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div>
              <p className="text-gray-600 text-sm">Position</p>
              <p className="text-lg font-semibold">{player.position}</p>
            </div>
            
            <div>
              <p className="text-gray-600 text-sm">Nationalité</p>
              <p className="text-lg font-semibold">{player.nationality}</p>
            </div>
            
            <div>
              <p className="text-gray-600 text-sm">Âge</p>
              <p className="text-lg font-semibold">{age > 0 ? `${age} ans` : 'N/A'}</p>
            </div>
            
            {player.height && (
              <div>
                <p className="text-gray-600 text-sm">Taille</p>
                <p className="text-lg font-semibold">{player.height} cm</p>
              </div>
            )}
            
            {player.weight && (
              <div>
                <p className="text-gray-600 text-sm">Poids</p>
                <p className="text-lg font-semibold">{player.weight} kg</p>
              </div>
            )}
            
            {player.dateOfBirth && (
              <div>
                <p className="text-gray-600 text-sm">Date de naissance</p>
                <p className="text-lg font-semibold">
                  {new Date(player.dateOfBirth).toLocaleDateString('fr-FR')}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Statistics Section */}
        <div className="mt-8">
          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold mb-6">Statistiques</h2>
            
            {loading ? (
              <div className="text-center py-12">
                <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                <p className="mt-4 text-gray-600">Chargement des statistiques...</p>
              </div>
            ) : error ? (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <p className="text-red-800">{error}</p>
              </div>
            ) : !statsData ? (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
                <p className="text-yellow-800">Les statistiques seront bientôt disponibles pour ce joueur</p>
              </div>
            ) : (
              <>
                {/* Sélecteurs */}
                {statsData && (statsData.current || statsData.previous.length > 0 || statsData.cumulative) && (
                  <div className="space-y-4">
                    {/* Sélecteur de saison */}
                    <SeasonSelector
                      current={statsData.current}
                      previous={statsData.previous}
                      cumulative={statsData.cumulative}
                      selectedSeason={selectedSeason}
                      onSeasonChange={setSelectedSeason}
                    />
                    
                    {/* Sélecteur de vue */}
                    <ViewSelector
                      currentView={currentView}
                      onViewChange={setCurrentView}
                    />
                  </div>
                )}
                
                {/* Affichage des statistiques selon la vue sélectionnée */}
                {selectedStats && (
                  currentView === 'radar' ? (
                    <StatsRadar 
                      stats={selectedStats} 
                      position={player.position}
                    />
                  ) : (
                    <StatsCards 
                      stats={selectedStats} 
                      position={player.position}
                    />
                  )
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}