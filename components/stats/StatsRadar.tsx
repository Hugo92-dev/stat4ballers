'use client';

import { useState } from 'react';
import { PlayerStatistics } from '@/services/sportmonks';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

interface StatsRadarProps {
  stats: PlayerStatistics;
  position?: string;
}

export default function StatsRadar({ stats, position }: StatsRadarProps) {
  const [displayMode, setDisplayMode] = useState<'real' | 'percentile'>('real'); // Valeurs réelles par défaut
  
  const isGoalkeeper = position?.toLowerCase().includes('gardien') || 
                       position?.toLowerCase().includes('goalkeeper') ||
                       position?.toLowerCase() === 'gk';

  // Si pas de stats, afficher un message
  if (!stats || (!stats.minutes && !stats.appearences)) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
        <p className="text-yellow-800">Aucune statistique disponible pour cette saison car le joueur n'a pas encore joué de match officiel</p>
      </div>
    );
  }

  // Calculer les pourcentages
  const shotsAccuracy = stats.shots && stats.shots > 0 
    ? ((stats.shots_on_target || 0) / stats.shots * 100) 
    : 0;
  
  const penaltyAccuracy = stats.penalties && stats.penalties > 0 
    ? ((stats.penalties_scored || 0) / stats.penalties * 100) 
    : 0;
    
  const dribbleAccuracy = stats.dribbles && stats.dribbles > 0
    ? ((stats.dribbles_succeeded || 0) / stats.dribbles * 100)
    : 0;

  // 1. CARTE GÉNÉRALE - Stats générales pour joueurs de champ
  const generalDataField = [
    { 
      stat: displayMode === 'real' ? `Appearances (${stats.appearences || 0})` : 'Appearances', 
      value: displayMode === 'real' ? stats.appearences || 0 : Math.min(100, (stats.appearences || 0) * 3), 
      rawValue: stats.appearences || 0,
      percentile: Math.min(100, (stats.appearences || 0) * 3)
    },
    { 
      stat: displayMode === 'real' ? `Lineups (${stats.lineups || 0})` : 'Lineups', 
      value: displayMode === 'real' ? stats.lineups || 0 : Math.min(100, (stats.lineups || 0) * 4), 
      rawValue: stats.lineups || 0,
      percentile: Math.min(100, (stats.lineups || 0) * 4)
    },
    { 
      stat: displayMode === 'real' ? `MinutesPlayed (${stats.minutes || 0})` : 'MinutesPlayed', 
      value: displayMode === 'real' ? Math.min(3000, stats.minutes || 0) : Math.min(100, (stats.minutes || 0) / 30), 
      rawValue: stats.minutes || 0,
      percentile: Math.min(100, (stats.minutes || 0) / 30)
    },
    { 
      stat: displayMode === 'real' ? `Captain (${stats.captain || 0})` : 'Captain', 
      value: displayMode === 'real' ? stats.captain || 0 : Math.min(100, (stats.captain || 0) * 20), 
      rawValue: stats.captain || 0,
      percentile: Math.min(100, (stats.captain || 0) * 20)
    },
    { 
      stat: displayMode === 'real' ? `Rating (${stats.rating?.toFixed(2) || 0})` : 'Rating', 
      value: displayMode === 'real' ? parseFloat(stats.rating?.toFixed(2) || '0') * 10 : Math.min(100, ((stats.rating || 6) - 5) * 20), 
      rawValue: stats.rating?.toFixed(2) || 0,
      percentile: Math.min(100, ((stats.rating || 6) - 5) * 20)
    }
  ];

  // 1. CARTE GÉNÉRALE - Stats générales pour gardiens
  const generalDataGoalkeeper = [
    { 
      stat: displayMode === 'real' ? `Note moyenne (${stats.rating?.toFixed(2) || 0})` : 'Note moyenne', 
      value: displayMode === 'real' ? parseFloat(stats.rating?.toFixed(2) || '0') * 10 : Math.min(100, ((stats.rating || 6) - 5) * 20), 
      rawValue: stats.rating?.toFixed(2) || 0,
      percentile: Math.min(100, ((stats.rating || 6) - 5) * 20)
    },
    { 
      stat: displayMode === 'real' ? `Minutes (${stats.minutes || 0})` : 'Minutes', 
      value: displayMode === 'real' ? Math.min(3000, stats.minutes || 0) : Math.min(100, (stats.minutes || 0) / 30), 
      rawValue: stats.minutes || 0,
      percentile: Math.min(100, (stats.minutes || 0) / 30)
    },
    { 
      stat: displayMode === 'real' ? `Titularisations (${stats.lineups || 0})` : 'Titularisations', 
      value: displayMode === 'real' ? stats.lineups || 0 : Math.min(100, (stats.lineups || 0) * 4), 
      rawValue: stats.lineups || 0,
      percentile: Math.min(100, (stats.lineups || 0) * 4)
    },
    { 
      stat: displayMode === 'real' ? `Matchs (${stats.appearences || 0})` : 'Matchs', 
      value: displayMode === 'real' ? stats.appearences || 0 : Math.min(100, (stats.appearences || 0) * 3), 
      rawValue: stats.appearences || 0,
      percentile: Math.min(100, (stats.appearences || 0) * 3)
    },
    { 
      stat: displayMode === 'real' ? `Capitaine (${stats.captain || 0})` : 'Capitaine', 
      value: displayMode === 'real' ? stats.captain || 0 : Math.min(100, (stats.captain || 0) * 20), 
      rawValue: stats.captain || 0,
      percentile: Math.min(100, (stats.captain || 0) * 20)
    },
    { 
      stat: displayMode === 'real' ? `Précision passes (${stats.passes_accuracy?.toFixed(1) || 0}%)` : 'Précision passes', 
      value: displayMode === 'real' ? parseFloat(stats.passes_accuracy?.toFixed(1) || '0') : Math.min(100, stats.passes_accuracy || 0), 
      rawValue: `${stats.passes_accuracy?.toFixed(1)}%`,
      percentile: Math.min(100, stats.passes_accuracy || 0)
    },
    { 
      stat: displayMode === 'real' ? `Cartons jaunes (${stats.yellow_cards || 0})` : 'Cartons jaunes', 
      value: displayMode === 'real' ? stats.yellow_cards || 0 : Math.min(100, 100 - ((stats.yellow_cards || 0) * 12)), 
      rawValue: stats.yellow_cards || 0,
      percentile: Math.min(100, 100 - ((stats.yellow_cards || 0) * 12))
    },
    { 
      stat: displayMode === 'real' ? `Cartons rouges (${stats.red_cards || 0})` : 'Cartons rouges', 
      value: displayMode === 'real' ? stats.red_cards || 0 : Math.min(100, 100 - ((stats.red_cards || 0) * 50)), 
      rawValue: stats.red_cards || 0,
      percentile: Math.min(100, 100 - ((stats.red_cards || 0) * 50))
    }
  ];

  // 2. CARTE OFFENSIVE
  const offensiveData = !isGoalkeeper ? [
    { 
      stat: displayMode === 'real' ? `Goals (${stats.goals || 0})` : 'Goals', 
      value: displayMode === 'real' ? stats.goals || 0 : Math.min(100, (stats.goals || 0) * 5), 
      rawValue: stats.goals || 0,
      percentile: Math.min(100, (stats.goals || 0) * 5)
    },
    { 
      stat: displayMode === 'real' ? `Assists (${stats.assists || 0})` : 'Assists', 
      value: displayMode === 'real' ? stats.assists || 0 : Math.min(100, (stats.assists || 0) * 8), 
      rawValue: stats.assists || 0,
      percentile: Math.min(100, (stats.assists || 0) * 8)
    },
    { 
      stat: displayMode === 'real' ? `ShotsTotal (${stats.shots || 0})` : 'ShotsTotal', 
      value: displayMode === 'real' ? stats.shots || 0 : Math.min(100, (stats.shots || 0) * 2), 
      rawValue: stats.shots || 0,
      percentile: Math.min(100, (stats.shots || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `ShotsOnTarget (${stats.shots_on_target || 0})` : 'ShotsOnTarget', 
      value: displayMode === 'real' ? stats.shots_on_target || 0 : Math.min(100, (stats.shots_on_target || 0) * 3), 
      rawValue: stats.shots_on_target || 0,
      percentile: Math.min(100, (stats.shots_on_target || 0) * 3)
    },
    { 
      stat: displayMode === 'real' ? `HitWoodwork (${stats.hit_woodwork || 0})` : 'HitWoodwork', 
      value: displayMode === 'real' ? stats.hit_woodwork || 0 : Math.min(100, (stats.hit_woodwork || 0) * 33), 
      rawValue: stats.hit_woodwork || 0,
      percentile: Math.min(100, (stats.hit_woodwork || 0) * 33)
    },
    { 
      stat: displayMode === 'real' ? `Offsides (${stats.offsides || 0})` : 'Offsides', 
      value: displayMode === 'real' ? stats.offsides || 0 : Math.min(100, 100 - ((stats.offsides || 0) * 4)), 
      rawValue: stats.offsides || 0,
      percentile: Math.min(100, 100 - ((stats.offsides || 0) * 4))
    },
    { 
      stat: displayMode === 'real' ? `Hattricks (${stats.hattricks || 0})` : 'Hattricks', 
      value: displayMode === 'real' ? stats.hattricks || 0 : Math.min(100, (stats.hattricks || 0) * 50), 
      rawValue: stats.hattricks || 0,
      percentile: Math.min(100, (stats.hattricks || 0) * 50)
    },
    { 
      stat: displayMode === 'real' ? `BigChancesMissed (${stats.big_chances_missed || 0})` : 'BigChancesMissed', 
      value: displayMode === 'real' ? stats.big_chances_missed || 0 : Math.min(100, 100 - ((stats.big_chances_missed || 0) * 10)), 
      rawValue: stats.big_chances_missed || 0,
      percentile: Math.min(100, 100 - ((stats.big_chances_missed || 0) * 10))
    }
  ] : [];

  // 3. CARTE CRÉATIVE - Passes et dribbles
  const creativeData = !isGoalkeeper ? [
    { 
      stat: displayMode === 'real' ? `Passes (${stats.passes_total || stats.passes || 0})` : 'Passes', 
      value: displayMode === 'real' ? Math.min(1200, stats.passes_total || stats.passes || 0) : Math.min(100, (stats.passes_total || stats.passes || 0) / 12), 
      rawValue: stats.passes_total || stats.passes || 0,
      percentile: Math.min(100, (stats.passes_total || stats.passes || 0) / 12)
    },
    { 
      stat: displayMode === 'real' ? `AccuratePassesPercentage (${stats.passes_accuracy?.toFixed(1) || 0}%)` : 'AccuratePassesPercentage', 
      value: displayMode === 'real' ? parseFloat(stats.passes_accuracy?.toFixed(1) || '0') : Math.min(100, stats.passes_accuracy || 0), 
      rawValue: `${stats.passes_accuracy?.toFixed(1)}%`,
      percentile: Math.min(100, stats.passes_accuracy || 0)
    },
    { 
      stat: displayMode === 'real' ? `KeyPasses (${stats.key_passes || 0})` : 'KeyPasses', 
      value: displayMode === 'real' ? stats.key_passes || 0 : Math.min(100, (stats.key_passes || 0) * 3), 
      rawValue: stats.key_passes || 0,
      percentile: Math.min(100, (stats.key_passes || 0) * 3)
    },
    { 
      stat: displayMode === 'real' ? `BigChancesCreated (${stats.big_chances_created || 0})` : 'BigChancesCreated', 
      value: displayMode === 'real' ? stats.big_chances_created || 0 : Math.min(100, (stats.big_chances_created || 0) * 10), 
      rawValue: stats.big_chances_created || 0,
      percentile: Math.min(100, (stats.big_chances_created || 0) * 10)
    },
    { 
      stat: displayMode === 'real' ? `ThroughBalls (${stats.through_balls || 0})` : 'ThroughBalls', 
      value: displayMode === 'real' ? stats.through_balls || 0 : Math.min(100, (stats.through_balls || 0) * 5), 
      rawValue: stats.through_balls || 0,
      percentile: Math.min(100, (stats.through_balls || 0) * 5)
    },
    { 
      stat: displayMode === 'real' ? `LongBalls (${stats.long_balls || 0})` : 'LongBalls', 
      value: displayMode === 'real' ? stats.long_balls || 0 : Math.min(100, (stats.long_balls || 0) * 2), 
      rawValue: stats.long_balls || 0,
      percentile: Math.min(100, (stats.long_balls || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `TotalCrosses (${stats.crosses_total || stats.crosses || 0})` : 'TotalCrosses', 
      value: displayMode === 'real' ? stats.crosses_total || stats.crosses || 0 : Math.min(100, (stats.crosses_total || stats.crosses || 0) * 2), 
      rawValue: stats.crosses_total || stats.crosses || 0,
      percentile: Math.min(100, (stats.crosses_total || stats.crosses || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `AccurateCrosses (${stats.accurate_crosses || 0})` : 'AccurateCrosses', 
      value: displayMode === 'real' ? stats.accurate_crosses || 0 : Math.min(100, (stats.accurate_crosses || 0) * 5), 
      rawValue: stats.accurate_crosses || 0,
      percentile: Math.min(100, (stats.accurate_crosses || 0) * 5)
    }
  ] : [];

  // 4. CARTE DÉFENSIVE & DISCIPLINE
  const totalRedCards = (stats.red_cards || 0) + (stats.yellowred_cards || 0);
  const defensiveData = !isGoalkeeper ? [
    { 
      stat: displayMode === 'real' ? `TotalDuels (${stats.duels || 0})` : 'TotalDuels', 
      value: displayMode === 'real' ? Math.min(200, stats.duels || 0) : Math.min(100, (stats.duels || 0) * 0.5), 
      rawValue: stats.duels || 0,
      percentile: Math.min(100, (stats.duels || 0) * 0.5)
    },
    { 
      stat: displayMode === 'real' ? `DuelsWon (${stats.duels_won || 0})` : 'DuelsWon', 
      value: displayMode === 'real' ? stats.duels_won || 0 : Math.min(100, (stats.duels_won || 0) * 0.8), 
      rawValue: stats.duels_won || 0,
      percentile: Math.min(100, (stats.duels_won || 0) * 0.8)
    },
    { 
      stat: displayMode === 'real' ? `AerialsWon (${stats.aerial_duels_won || 0})` : 'AerialsWon', 
      value: displayMode === 'real' ? stats.aerial_duels_won || 0 : Math.min(100, (stats.aerial_duels_won || 0) * 2), 
      rawValue: stats.aerial_duels_won || 0,
      percentile: Math.min(100, (stats.aerial_duels_won || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `Tackles (${stats.tackles || 0})` : 'Tackles', 
      value: displayMode === 'real' ? stats.tackles || 0 : Math.min(100, (stats.tackles || 0) * 1.5), 
      rawValue: stats.tackles || 0,
      percentile: Math.min(100, (stats.tackles || 0) * 1.5)
    },
    { 
      stat: displayMode === 'real' ? `DribbledPast (${stats.dribbled_past || 0})` : 'DribbledPast', 
      value: displayMode === 'real' ? stats.dribbled_past || 0 : Math.min(100, 100 - ((stats.dribbled_past || 0) * 3)), 
      rawValue: stats.dribbled_past || 0,
      percentile: Math.min(100, 100 - ((stats.dribbled_past || 0) * 3))
    },
    { 
      stat: displayMode === 'real' ? `ErrorLeadToGoal (${stats.mistakes_leading_to_goals || 0})` : 'ErrorLeadToGoal', 
      value: displayMode === 'real' ? stats.mistakes_leading_to_goals || 0 : Math.min(100, 100 - ((stats.mistakes_leading_to_goals || 0) * 50)), 
      rawValue: stats.mistakes_leading_to_goals || 0,
      percentile: Math.min(100, 100 - ((stats.mistakes_leading_to_goals || 0) * 50))
    },
    { 
      stat: displayMode === 'real' ? `CrossesBlocked (${stats.crosses_blocked || 0})` : 'CrossesBlocked', 
      value: displayMode === 'real' ? stats.crosses_blocked || 0 : Math.min(100, (stats.crosses_blocked || 0) * 10), 
      rawValue: stats.crosses_blocked || 0,
      percentile: Math.min(100, (stats.crosses_blocked || 0) * 10)
    },
    { 
      stat: displayMode === 'real' ? `Fouls (${stats.fouls || 0})` : 'Fouls', 
      value: displayMode === 'real' ? stats.fouls || 0 : Math.min(100, 100 - ((stats.fouls || 0) * 2.5)), 
      rawValue: stats.fouls || 0,
      percentile: Math.min(100, 100 - ((stats.fouls || 0) * 2.5))
    },
    { 
      stat: displayMode === 'real' ? `FoulsDrawn (${stats.fouls_drawn || 0})` : 'FoulsDrawn', 
      value: displayMode === 'real' ? stats.fouls_drawn || 0 : Math.min(100, (stats.fouls_drawn || 0) * 3), 
      rawValue: stats.fouls_drawn || 0,
      percentile: Math.min(100, (stats.fouls_drawn || 0) * 3)
    },
    { 
      stat: displayMode === 'real' ? `Yellowcards (${stats.yellow_cards || 0})` : 'Yellowcards', 
      value: displayMode === 'real' ? stats.yellow_cards || 0 : Math.min(100, 100 - ((stats.yellow_cards || 0) * 12)), 
      rawValue: stats.yellow_cards || 0,
      percentile: Math.min(100, 100 - ((stats.yellow_cards || 0) * 12))
    },
    { 
      stat: displayMode === 'real' ? `Redcards (${totalRedCards || 0})` : 'Redcards', 
      value: displayMode === 'real' ? totalRedCards || 0 : Math.min(100, 100 - ((totalRedCards || 0) * 50)), 
      rawValue: totalRedCards || 0,
      percentile: Math.min(100, 100 - ((totalRedCards || 0) * 50))
    },
    { 
      stat: displayMode === 'real' ? `OwnGoals (${stats.own_goals || 0})` : 'OwnGoals', 
      value: displayMode === 'real' ? stats.own_goals || 0 : Math.min(100, 100 - ((stats.own_goals || 0) * 25)), 
      rawValue: stats.own_goals || 0,
      percentile: Math.min(100, 100 - ((stats.own_goals || 0) * 25))
    }
  ] : [];

  // 5. CARTE GARDIEN - Stats spécifiques gardien
  const goalkeeperData = isGoalkeeper ? [
    { 
      stat: displayMode === 'real' ? `GoalsConceded (${stats.goals_conceded || 0})` : 'GoalsConceded', 
      value: displayMode === 'real' ? stats.goals_conceded || 0 : Math.min(100, 100 - ((stats.goals_conceded || 0) * 2.5)), 
      rawValue: stats.goals_conceded || 0,
      percentile: Math.min(100, 100 - ((stats.goals_conceded || 0) * 2.5))
    },
    { 
      stat: displayMode === 'real' ? `Saves (${stats.saves || 0})` : 'Saves', 
      value: displayMode === 'real' ? Math.min(150, stats.saves || 0) : Math.min(100, (stats.saves || 0) / 1.5), 
      rawValue: stats.saves || 0,
      percentile: Math.min(100, (stats.saves || 0) / 1.5)
    },
    { 
      stat: displayMode === 'real' ? `SavesInsidebox (${stats.inside_box_saves || 0})` : 'SavesInsidebox', 
      value: displayMode === 'real' ? Math.min(100, stats.inside_box_saves || 0) : Math.min(100, (stats.inside_box_saves || 0) / 1), 
      rawValue: stats.inside_box_saves || 0,
      percentile: Math.min(100, (stats.inside_box_saves || 0) / 1)
    }
  ] : [];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload[0]) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-800">{data.stat}</p>
          <p className="text-gray-600">Valeur réelle: {data.rawValue}</p>
          {displayMode === 'percentile' && (
            <p className="text-xs text-gray-500">Percentile: {data.percentile.toFixed(0)}/100</p>
          )}
        </div>
      );
    }
    return null;
  };

  const RadarChartComponent = ({ data, color, title }: { data: any[], color: string, title: string }) => (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-lg font-bold mb-4 text-gray-800 border-b pb-2">{title}</h3>
      <ResponsiveContainer width="100%" height={300}>
        <RadarChart data={data}>
          <PolarGrid 
            stroke="#e5e7eb"
            strokeDasharray="3 3"
          />
          <PolarAngleAxis 
            dataKey="stat" 
            tick={{ fontSize: 11 }}
            className="text-gray-600"
          />
          <PolarRadiusAxis 
            domain={displayMode === 'percentile' ? [0, 100] : [0, 'auto']} 
            tick={{ fontSize: 10 }}
            axisLine={false}
            tickCount={5}
          />
          <Radar 
            name="Stats" 
            dataKey="value" 
            stroke={color}
            fill={color}
            fillOpacity={0.3}
            strokeWidth={2}
          />
          <Tooltip content={<CustomTooltip />} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );

  // Vue différente pour les gardiens (seulement 2 cartes)
  if (isGoalkeeper) {
    return (
      <div>
        {/* Sélecteur de mode d'affichage */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setDisplayMode('real')}
            className={`
              px-4 py-2 rounded-lg text-sm font-medium transition-all
              ${displayMode === 'real' 
                ? 'bg-blue-600 text-white shadow-md' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }
            `}
          >
            📊 Valeurs réelles
          </button>
          <button
            onClick={() => setDisplayMode('percentile')}
            className={`
              px-4 py-2 rounded-lg text-sm font-medium transition-all
              ${displayMode === 'percentile' 
                ? 'bg-purple-600 text-white shadow-md' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }
            `}
          >
            📈 Percentiles
          </button>
        </div>
        {displayMode === 'percentile' && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
            <p className="text-sm text-purple-800">
              💡 Les percentiles indiquent la position du joueur par rapport aux autres (0 = pire, 100 = meilleur).
              Un score de 99 signifie que le joueur est meilleur que 99% des autres joueurs.
            </p>
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <RadarChartComponent 
            data={generalDataGoalkeeper} 
            color="#3B82F6" 
            title="🟦 Général"
          />
          <RadarChartComponent 
            data={goalkeeperData} 
            color="#10B981" 
            title="🧤 Gardien"
          />
        </div>
      </div>
    );
  }

  // Vue normale pour les joueurs de champ (4 cartes)
  return (
    <div>
      {/* Sélecteur de mode d'affichage */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setDisplayMode('real')}
          className={`
            px-4 py-2 rounded-lg text-sm font-medium transition-all
            ${displayMode === 'real' 
              ? 'bg-blue-600 text-white shadow-md' 
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }
          `}
        >
          📊 Valeurs réelles
        </button>
        <button
          onClick={() => setDisplayMode('percentile')}
          className={`
            px-4 py-2 rounded-lg text-sm font-medium transition-all
            ${displayMode === 'percentile' 
              ? 'bg-purple-600 text-white shadow-md' 
              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }
          `}
        >
          📈 Percentiles
        </button>
      </div>
      {displayMode === 'percentile' && (
        <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-6">
          <p className="text-sm text-purple-800">
            💡 Les percentiles indiquent la position du joueur par rapport aux autres (0 = pire, 100 = meilleur).
            Un score de 99 signifie que le joueur est meilleur que 99% des autres joueurs.
          </p>
        </div>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <RadarChartComponent 
          data={generalDataField} 
          color="#3B82F6" 
          title="🟦 Général"
        />
        <RadarChartComponent 
          data={offensiveData} 
          color="#EF4444" 
          title="🔴 Offensif"
        />
        <RadarChartComponent 
          data={creativeData} 
          color="#10B981" 
          title="🟢 Créatif"
        />
        <RadarChartComponent 
          data={defensiveData} 
          color="#F59E0B" 
          title="🛡️ Défensif & Discipline"
        />
      </div>
    </div>
  );
}