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
    const shotsAccuracy = stats.shots && stats.shots > 0 
      ? ((stats.shots_on_target || 0) / stats.shots * 100) 
      : 0;

    return [
      { stat: 'Note moyenne', value: (stats.rating || 0) * 10 },
      { stat: 'Minutes', value: Math.min(100, (stats.minutes || 0) / 30) },
      { stat: 'Titularisations', value: Math.min(100, (stats.lineups || 0) * 4) },
      { stat: 'Matchs', value: Math.min(100, (stats.appearences || 0) * 3) },
      { stat: 'Capitaine', value: Math.min(100, (stats.captain || 0) * 20) },
      { stat: 'Touches', value: Math.min(100, (stats.touches || 0) / 20) },
      { stat: 'Préc. tirs', value: shotsAccuracy },
      { stat: 'Préc. passes', value: stats.passes_accuracy || 0 }
    ];
  };

  // CARTE 1: GÉNÉRAL pour gardiens
  const generalDataGoalkeeper = (stats: PlayerStatistics) => {
    return [
      { stat: 'Note moyenne', value: (stats.rating || 0) * 10 },
      { stat: 'Minutes', value: Math.min(100, (stats.minutes || 0) / 30) },
      { stat: 'Titularisations', value: Math.min(100, (stats.lineups || 0) * 4) },
      { stat: 'Matchs', value: Math.min(100, (stats.appearences || 0) * 3) },
      { stat: 'Capitaine', value: Math.min(100, (stats.captain || 0) * 20) },
      { stat: 'Préc. passes', value: stats.passes_accuracy || 0 },
      { stat: 'C. jaunes', value: Math.max(0, 100 - ((stats.yellow_cards || 0) * 12)) },
      { stat: 'C. rouges', value: Math.max(0, 100 - ((stats.red_cards || 0) * 50)) }
    ];
  };

  // CARTE 2: OFFENSIVE
  const offensiveData = (stats: PlayerStatistics) => {
    const penaltyAccuracy = stats.penalties && stats.penalties > 0 
      ? ((stats.penalties_scored || 0) / stats.penalties * 100) 
      : 0;

    return [
      { stat: 'Buts', value: Math.min(100, (stats.goals || 0) * 5) },
      { stat: 'xG', value: Math.min(100, (stats.expected_goals || 0) * 5) },
      { stat: 'Passes déc.', value: Math.min(100, (stats.assists || 0) * 8) },
      { stat: 'xA', value: Math.min(100, (stats.expected_assists || 0) * 8) },
      { stat: 'Total tirs', value: Math.min(100, (stats.shots || 0) * 2) },
      { stat: 'Penalties', value: Math.min(100, (stats.penalties || 0) * 20) },
      { stat: 'Préc. pen.', value: penaltyAccuracy },
      { stat: 'Poteaux', value: Math.min(100, (stats.hit_woodwork || 0) * 33) },
      { stat: 'Hors-jeux', value: Math.max(0, 100 - ((stats.offsides || 0) * 4)) },
      { stat: 'Pertes balle', value: Math.max(0, 100 - ((stats.ball_losses || 0) * 0.7)) }
    ];
  };

  // CARTE 3: CRÉATIVE (passes & dribbles)
  const creativeData = (stats: PlayerStatistics) => {
    const dribbleAccuracy = stats.dribbles && stats.dribbles > 0
      ? ((stats.dribbles_succeeded || 0) / stats.dribbles * 100)
      : 0;

    return [
      { stat: 'Total passes', value: Math.min(100, (stats.passes_total || 0) / 12) },
      { stat: 'Passes clés', value: Math.min(100, (stats.key_passes || 0) * 3) },
      { stat: 'Total centres', value: Math.min(100, (stats.crosses_total || 0) * 2) },
      { stat: 'Préc. centres', value: stats.crosses_accuracy || 0 },
      { stat: 'Total dribbles', value: Math.min(100, (stats.dribbles || 0) * 2) },
      { stat: 'Préc. dribbles', value: dribbleAccuracy }
    ];
  };

  // CARTE 4: DÉFENSIVE & DISCIPLINE
  const defensiveData = (stats: PlayerStatistics) => {
    return [
      { stat: 'Récupérations', value: Math.min(100, (stats.ball_recoveries || 0) * 1.5) },
      { stat: 'Tacles', value: Math.min(100, (stats.tackles || 0) * 1.5) },
      { stat: 'Interceptions', value: Math.min(100, (stats.interceptions || 0) * 2) },
      { stat: 'Total duels', value: Math.min(100, (stats.duels || 0) * 0.5) },
      { stat: 'Duels gagnés', value: Math.min(100, (stats.duels_won || 0) * 0.8) },
      { stat: 'Duels aériens', value: Math.min(100, (stats.aerial_duels || 0) * 1) },
      { stat: 'Aériens gagnés', value: Math.min(100, (stats.aerial_duels_won || 0) * 2) },
      { stat: 'Fautes comm.', value: Math.max(0, 100 - ((stats.fouls || 0) * 2.5)) },
      { stat: 'Fautes subies', value: Math.min(100, (stats.fouls_drawn || 0) * 3) },
      { stat: 'C. jaunes', value: Math.max(0, 100 - ((stats.yellow_cards || 0) * 12)) },
      { stat: 'C. rouges', value: Math.max(0, 100 - ((stats.red_cards || 0) * 50)) },
      { stat: 'Pen. conc.', value: Math.max(0, 100 - ((stats.penalties_committed || 0) * 25)) },
      { stat: 'Erreurs→but', value: Math.max(0, 100 - ((stats.mistakes_leading_to_goals || 0) * 50)) }
    ];
  };

  // CARTE GARDIEN: Stats spécifiques gardien
  const goalkeeperData = (stats: PlayerStatistics) => {
    return [
      { stat: 'Arrêts', value: Math.min(100, (stats.saves || 0) / 1.5) },
      { stat: 'Arrêts surface', value: Math.min(100, (stats.inside_box_saves || 0) / 1) },
      { stat: 'Pen. arrêtés', value: Math.min(100, (stats.penalties_saved || 0) * 33) },
      { stat: 'Clean sheets', value: Math.min(100, (stats.clean_sheets || 0) * 10) },
      { stat: 'Buts encaissés', value: Math.max(0, 100 - ((stats.goals_conceded || 0) * 2.5)) },
      { stat: 'Pen. concédés', value: Math.max(0, 100 - ((stats.penalties_committed || 0) * 25)) },
      { stat: 'Erreurs→but', value: Math.max(0, 100 - ((stats.mistakes_leading_to_goals || 0) * 50)) }
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
            title="🥅 Gardien"
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
          title="📊 Général"
        />
        <RadarChartComponent 
          data={prepareRadarData(offensiveData)} 
          title="⚽ Offensif"
        />
        <RadarChartComponent 
          data={prepareRadarData(creativeData)} 
          title="🎯 Créatif (passes & dribbles)"
        />
        <RadarChartComponent 
          data={prepareRadarData(defensiveData)} 
          title="🛡️ Défensif & Discipline"
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