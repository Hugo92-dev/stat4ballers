'use client';

import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { PlayerStatistics } from '@/services/sportmonks';
import PlayerStrengths from './PlayerStrengths';

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
}

interface PlayerWithStats extends Player {
  stats: PlayerStatistics;
}

interface PlayerComparisonRadarProps {
  players: PlayerWithStats[];
}

// Couleurs pour chaque joueur
const PLAYER_COLORS = [
  '#3B82F6', // blue-500
  '#EF4444', // red-500
  '#10B981', // emerald-500
  '#F59E0B', // amber-500
];

export default function PlayerComparisonRadar({ players }: PlayerComparisonRadarProps) {
  // Déterminer si on a des gardiens
  const hasGoalkeeper = players.some(p => 
    p.position?.toLowerCase().includes('gardien') || 
    p.position?.toLowerCase().includes('goalkeeper') ||
    p.position?.toLowerCase() === 'gk'
  );

  // Préparer les données pour chaque carte radar
  const prepareRadarData = (statsExtractor: (stats: PlayerStatistics) => { stat: string; value: number }[]) => {
    const allStats = new Set<string>();
    const playerData: Record<string, Record<string, number>> = {};

    // Extraire toutes les stats uniques et les valeurs par joueur
    players.forEach(player => {
      const playerName = player.displayName || player.fullName || player.name;
      const stats = statsExtractor(player.stats);
      playerData[playerName] = {};
      
      stats.forEach(({ stat, value }) => {
        allStats.add(stat);
        playerData[playerName][stat] = value;
      });
    });

    // Créer le tableau de données pour le radar
    return Array.from(allStats).map(stat => {
      const dataPoint: any = { stat };
      Object.keys(playerData).forEach(playerName => {
        dataPoint[playerName] = playerData[playerName][stat] || 0;
      });
      return dataPoint;
    });
  };

  // CARTE 1: GÉNÉRAL pour joueurs de champ
  const generalDataField = (stats: PlayerStatistics) => {
    return [
      { stat: 'Matchs joués', value: Math.min(100, (stats.appearences || 0) * 3) },
      { stat: 'Titularisations', value: Math.min(100, (stats.lineups || 0) * 4) },
      { stat: 'Minutes', value: Math.min(100, (stats.minutes || 0) / 30) },
      { stat: 'Capitaine', value: Math.min(100, (stats.captain || 0) * 20) },
      { stat: 'Note moyenne', value: (stats.rating || 0) * 10 }
    ];
  };

  // CARTE 1: GÉNÉRAL pour gardiens
  const generalDataGoalkeeper = (stats: PlayerStatistics) => {
    const totalRedCards = (stats.red_cards || 0) + (stats.yellowred_cards || 0);
    return [
      { stat: 'Note moyenne', value: (stats.rating || 0) * 10 },
      { stat: 'Minutes', value: Math.min(100, (stats.minutes || 0) / 30) },
      { stat: 'Titularisations', value: Math.min(100, (stats.lineups || 0) * 4) },
      { stat: 'Matchs', value: Math.min(100, (stats.appearences || 0) * 3) },
      { stat: 'Capitaine', value: Math.min(100, (stats.captain || 0) * 20) },
      { stat: 'Préc. passes', value: stats.passes_accuracy || 0 },
      { stat: 'C. jaunes', value: Math.max(0, 100 - ((stats.yellow_cards || 0) * 12)) },
      { stat: 'C. rouges', value: Math.max(0, 100 - (totalRedCards * 50)) }
    ];
  };

  // CARTE 2: OFFENSIVE
  const offensiveData = (stats: PlayerStatistics) => {
    return [
      { stat: 'Buts', value: Math.min(100, (stats.goals || 0) * 5) },
      { stat: 'Passes décisives', value: Math.min(100, (stats.assists || 0) * 8) },
      { stat: 'Tirs tentés', value: Math.min(100, (stats.shots || 0) * 2) },
      { stat: 'Tirs cadrés', value: Math.min(100, (stats.shots_on_target || 0) * 4) },
      { stat: 'Tirs montants', value: Math.min(100, (stats.hit_woodwork || 0) * 33) },
      { stat: 'Hors-jeu', value: Math.max(0, 100 - ((stats.offsides || 0) * 4)) }
    ];
  };

  // CARTE 3: CRÉATIVE
  const creativeData = (stats: PlayerStatistics) => {
    return [
      { stat: 'Passes', value: Math.min(100, ((stats.passes_total || stats.passes || 0)) / 12) },
      { stat: 'Préc. passes', value: stats.passes_accuracy || 0 },
      { stat: 'Passes clés', value: Math.min(100, (stats.key_passes || 0) * 3) },
      { stat: 'Centres', value: Math.min(100, ((stats.crosses_total || stats.crosses || 0)) * 2) }
    ];
  };

  // CARTE 4: DÉFENSIVE & DISCIPLINE
  const defensiveData = (stats: PlayerStatistics) => {
    const totalRedCards = (stats.red_cards || 0) + (stats.yellowred_cards || 0);
    return [
      { stat: 'Duels totaux', value: Math.min(100, (stats.duels || 0) * 0.5) },
      { stat: 'Duels gagnés', value: Math.min(100, (stats.duels_won || 0) * 0.8) },
      { stat: 'Aériens gagnés', value: Math.min(100, (stats.aerial_duels_won || 0) * 2) },
      { stat: 'Tacles', value: Math.min(100, (stats.tackles || 0) * 1.5) },
      { stat: 'Fautes comm.', value: Math.max(0, 100 - ((stats.fouls || 0) * 2.5)) },
      { stat: 'Fautes subies', value: Math.min(100, (stats.fouls_drawn || 0) * 3) },
      { stat: 'C. jaunes', value: Math.max(0, 100 - ((stats.yellow_cards || 0) * 12)) },
      { stat: 'C. rouges', value: Math.max(0, 100 - (totalRedCards * 50)) }
    ];
  };

  // CARTE GARDIEN: Stats spécifiques gardien
  const goalkeeperData = (stats: PlayerStatistics) => {
    return [
      { stat: 'Buts encaissés', value: Math.max(0, 100 - ((stats.goals_conceded || 0) * 2.5)) },
      { stat: 'Arrêts', value: Math.min(100, (stats.saves || 0) / 1.5) },
      { stat: 'Arrêts surface', value: Math.min(100, (stats.inside_box_saves || 0) / 1) }
    ];
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length > 0) {
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-800 mb-2">{payload[0].payload.stat}</p>
          {payload.map((entry: any, index: number) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: {entry.value.toFixed(1)}
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  const RadarChartComponent = ({ data, title }: { data: any[], title: string }) => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={data}>
          <PolarGrid stroke="#e5e7eb" strokeDasharray="3 3" />
          <PolarAngleAxis dataKey="stat" tick={{ fontSize: 11 }} className="text-gray-600" />
          <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 10 }} axisLine={false} tickCount={5} />
          
          {players.map((player, index) => {
            const playerName = player.displayName || player.fullName || player.name;
            return (
              <Radar
                key={player.id}
                name={playerName}
                dataKey={playerName}
                stroke={PLAYER_COLORS[index]}
                fill={PLAYER_COLORS[index]}
                fillOpacity={0.1}
                strokeWidth={2}
              />
            );
          })}
          
          <Tooltip content={<CustomTooltip />} />
          <Legend />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );

  // Vue pour les gardiens (2 cartes)
  if (hasGoalkeeper) {
    return (
      <div className="space-y-8">
        {/* Points forts en haut */}
        <PlayerStrengths players={players} />
        
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-2">Comparaison Radar</h2>
          <p className="text-gray-600">Visualisation des performances relatives (normalisées sur 100)</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <RadarChartComponent 
            data={prepareRadarData(generalDataGoalkeeper)} 
            title="📊 Général"
          />
          <RadarChartComponent 
            data={prepareRadarData(goalkeeperData)} 
            title="🧤 Carte Gardien"
          />
        </div>

        {/* Note sur la normalisation */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <h3 className="font-medium text-blue-900 mb-2">Note sur la visualisation</h3>
          <p className="text-sm text-blue-800">
            Les valeurs sont normalisées sur une échelle de 0 à 100 pour permettre une comparaison équitable. 
            Pour les statistiques négatives (cartons, erreurs), une valeur élevée signifie moins d'incidents.
          </p>
        </div>
      </div>
    );
  }

  // Vue pour les joueurs de champ (4 cartes)
  return (
    <div className="space-y-8">
      {/* Points forts en haut */}
      <PlayerStrengths players={players} />
      
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Comparaison Radar</h2>
        <p className="text-gray-600">Visualisation des performances relatives (normalisées sur 100)</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RadarChartComponent 
          data={prepareRadarData(generalDataField)} 
          title="⚽ Carte Générale"
        />
        <RadarChartComponent 
          data={prepareRadarData(offensiveData)} 
          title="⚔️ Carte Offensive"
        />
        <RadarChartComponent 
          data={prepareRadarData(creativeData)} 
          title="🧑‍🎨 Carte Créative"
        />
        <RadarChartComponent 
          data={prepareRadarData(defensiveData)} 
          title="🛡️ Carte Défensive & Discipline"
        />
      </div>

      {/* Note sur la normalisation */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 className="font-medium text-blue-900 mb-2">Note sur la visualisation</h3>
        <p className="text-sm text-blue-800">
          Les valeurs sont normalisées sur une échelle de 0 à 100 pour permettre une comparaison équitable. 
          Pour les statistiques négatives (cartons, fautes, pertes de balle), une valeur élevée signifie moins d'incidents.
        </p>
      </div>
    </div>
  );
}