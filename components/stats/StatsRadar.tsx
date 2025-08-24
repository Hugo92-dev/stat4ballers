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
      stat: displayMode === 'real' ? `Touches (${stats.touches || 0})` : 'Touches', 
      value: displayMode === 'real' ? Math.min(2000, stats.touches || 0) : Math.min(100, (stats.touches || 0) / 20), 
      rawValue: stats.touches || 0,
      percentile: Math.min(100, (stats.touches || 0) / 20)
    },
    { 
      stat: displayMode === 'real' ? `Précision tirs (${shotsAccuracy.toFixed(1)}%)` : 'Précision tirs', 
      value: displayMode === 'real' ? shotsAccuracy : Math.min(100, shotsAccuracy), 
      rawValue: `${shotsAccuracy.toFixed(1)}%`,
      percentile: Math.min(100, shotsAccuracy)
    },
    { 
      stat: displayMode === 'real' ? `Précision passes (${stats.passes_accuracy?.toFixed(1) || 0}%)` : 'Précision passes', 
      value: displayMode === 'real' ? parseFloat(stats.passes_accuracy?.toFixed(1) || '0') : Math.min(100, stats.passes_accuracy || 0), 
      rawValue: `${stats.passes_accuracy?.toFixed(1)}%`,
      percentile: Math.min(100, stats.passes_accuracy || 0)
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
      stat: displayMode === 'real' ? `Buts (${stats.goals || 0})` : 'Buts', 
      value: displayMode === 'real' ? stats.goals || 0 : Math.min(100, (stats.goals || 0) * 5), 
      rawValue: stats.goals || 0,
      percentile: Math.min(100, (stats.goals || 0) * 5)
    },
    { 
      stat: displayMode === 'real' ? `xG (${stats.expected_goals?.toFixed(2) || 0})` : 'xG', 
      value: displayMode === 'real' ? parseFloat(stats.expected_goals?.toFixed(2) || '0') * 20 : Math.min(100, (stats.expected_goals || 0) * 5), 
      rawValue: stats.expected_goals?.toFixed(2) || 0,
      percentile: Math.min(100, (stats.expected_goals || 0) * 5)
    },
    { 
      stat: displayMode === 'real' ? `Passes déc. (${stats.assists || 0})` : 'Passes déc.', 
      value: displayMode === 'real' ? stats.assists || 0 : Math.min(100, (stats.assists || 0) * 8), 
      rawValue: stats.assists || 0,
      percentile: Math.min(100, (stats.assists || 0) * 8)
    },
    { 
      stat: displayMode === 'real' ? `xA (${stats.expected_assists?.toFixed(2) || 0})` : 'xA', 
      value: displayMode === 'real' ? parseFloat(stats.expected_assists?.toFixed(2) || '0') * 20 : Math.min(100, (stats.expected_assists || 0) * 8), 
      rawValue: stats.expected_assists?.toFixed(2) || 0,
      percentile: Math.min(100, (stats.expected_assists || 0) * 8)
    },
    { 
      stat: displayMode === 'real' ? `Total tirs (${stats.shots || 0})` : 'Total tirs', 
      value: displayMode === 'real' ? stats.shots || 0 : Math.min(100, (stats.shots || 0) * 2), 
      rawValue: stats.shots || 0,
      percentile: Math.min(100, (stats.shots || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `Penalties (${stats.penalties || 0})` : 'Penalties', 
      value: displayMode === 'real' ? stats.penalties || 0 : Math.min(100, (stats.penalties || 0) * 20), 
      rawValue: stats.penalties || 0,
      percentile: Math.min(100, (stats.penalties || 0) * 20)
    },
    { 
      stat: displayMode === 'real' ? `Préc. pen. (${penaltyAccuracy.toFixed(1)}%)` : 'Préc. pen.', 
      value: displayMode === 'real' ? penaltyAccuracy : Math.min(100, penaltyAccuracy), 
      rawValue: `${penaltyAccuracy.toFixed(1)}%`,
      percentile: Math.min(100, penaltyAccuracy)
    },
    { 
      stat: displayMode === 'real' ? `Poteaux (${stats.hit_woodwork || 0})` : 'Poteaux', 
      value: displayMode === 'real' ? stats.hit_woodwork || 0 : Math.min(100, (stats.hit_woodwork || 0) * 33), 
      rawValue: stats.hit_woodwork || 0,
      percentile: Math.min(100, (stats.hit_woodwork || 0) * 33)
    },
    { 
      stat: displayMode === 'real' ? `Hors-jeux (${stats.offsides || 0})` : 'Hors-jeux', 
      value: displayMode === 'real' ? stats.offsides || 0 : Math.min(100, 100 - ((stats.offsides || 0) * 4)), 
      rawValue: stats.offsides || 0,
      percentile: Math.min(100, 100 - ((stats.offsides || 0) * 4))
    },
    { 
      stat: displayMode === 'real' ? `Pertes balle (${stats.ball_losses || 0})` : 'Pertes balle', 
      value: displayMode === 'real' ? stats.ball_losses || 0 : Math.min(100, 100 - ((stats.ball_losses || 0) * 0.7)), 
      rawValue: stats.ball_losses || 0,
      percentile: Math.min(100, 100 - ((stats.ball_losses || 0) * 0.7))
    }
  ] : [];

  // 3. CARTE CRÉATIVE - Passes et dribbles
  const creativeData = !isGoalkeeper ? [
    { 
      stat: displayMode === 'real' ? `Total passes (${stats.passes_total || 0})` : 'Total passes', 
      value: displayMode === 'real' ? Math.min(1200, stats.passes_total || 0) : Math.min(100, (stats.passes_total || 0) / 12), 
      rawValue: stats.passes_total || 0,
      percentile: Math.min(100, (stats.passes_total || 0) / 12)
    },
    { 
      stat: displayMode === 'real' ? `Passes clés (${stats.key_passes || 0})` : 'Passes clés', 
      value: displayMode === 'real' ? stats.key_passes || 0 : Math.min(100, (stats.key_passes || 0) * 3), 
      rawValue: stats.key_passes || 0,
      percentile: Math.min(100, (stats.key_passes || 0) * 3)
    },
    { 
      stat: displayMode === 'real' ? `Total centres (${stats.crosses_total || 0})` : 'Total centres', 
      value: displayMode === 'real' ? stats.crosses_total || 0 : Math.min(100, (stats.crosses_total || 0) * 2), 
      rawValue: stats.crosses_total || 0,
      percentile: Math.min(100, (stats.crosses_total || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `Préc. centres (${stats.crosses_accuracy?.toFixed(1)}%)` : 'Préc. centres', 
      value: displayMode === 'real' ? parseFloat(stats.crosses_accuracy?.toFixed(1) || '0') : Math.min(100, stats.crosses_accuracy || 0), 
      rawValue: `${stats.crosses_accuracy?.toFixed(1)}%`,
      percentile: Math.min(100, stats.crosses_accuracy || 0)
    },
    { 
      stat: displayMode === 'real' ? `Total dribbles (${stats.dribbles || 0})` : 'Total dribbles', 
      value: displayMode === 'real' ? stats.dribbles || 0 : Math.min(100, (stats.dribbles || 0) * 2), 
      rawValue: stats.dribbles || 0,
      percentile: Math.min(100, (stats.dribbles || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `Préc. dribbles (${dribbleAccuracy.toFixed(1)}%)` : 'Préc. dribbles', 
      value: displayMode === 'real' ? dribbleAccuracy : Math.min(100, dribbleAccuracy), 
      rawValue: `${dribbleAccuracy.toFixed(1)}%`,
      percentile: Math.min(100, dribbleAccuracy)
    }
  ] : [];

  // 4. CARTE DÉFENSIVE & DISCIPLINE
  const defensiveData = !isGoalkeeper ? [
    { 
      stat: displayMode === 'real' ? `Récupérations (${stats.ball_recoveries || 0})` : 'Récupérations', 
      value: displayMode === 'real' ? stats.ball_recoveries || 0 : Math.min(100, (stats.ball_recoveries || 0) * 1.5), 
      rawValue: stats.ball_recoveries || 0,
      percentile: Math.min(100, (stats.ball_recoveries || 0) * 1.5)
    },
    { 
      stat: displayMode === 'real' ? `Tacles (${stats.tackles || 0})` : 'Tacles', 
      value: displayMode === 'real' ? stats.tackles || 0 : Math.min(100, (stats.tackles || 0) * 1.5), 
      rawValue: stats.tackles || 0,
      percentile: Math.min(100, (stats.tackles || 0) * 1.5)
    },
    { 
      stat: displayMode === 'real' ? `Interceptions (${stats.interceptions || 0})` : 'Interceptions', 
      value: displayMode === 'real' ? stats.interceptions || 0 : Math.min(100, (stats.interceptions || 0) * 2), 
      rawValue: stats.interceptions || 0,
      percentile: Math.min(100, (stats.interceptions || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `Total duels (${stats.duels || 0})` : 'Total duels', 
      value: displayMode === 'real' ? Math.min(200, stats.duels || 0) : Math.min(100, (stats.duels || 0) * 0.5), 
      rawValue: stats.duels || 0,
      percentile: Math.min(100, (stats.duels || 0) * 0.5)
    },
    { 
      stat: displayMode === 'real' ? `Duels gagnés (${stats.duels_won || 0})` : 'Duels gagnés', 
      value: displayMode === 'real' ? stats.duels_won || 0 : Math.min(100, (stats.duels_won || 0) * 0.8), 
      rawValue: stats.duels_won || 0,
      percentile: Math.min(100, (stats.duels_won || 0) * 0.8)
    },
    { 
      stat: displayMode === 'real' ? `Duels aériens (${stats.aerial_duels || 0})` : 'Duels aériens', 
      value: displayMode === 'real' ? stats.aerial_duels || 0 : Math.min(100, (stats.aerial_duels || 0) * 1), 
      rawValue: stats.aerial_duels || 0,
      percentile: Math.min(100, (stats.aerial_duels || 0) * 1)
    },
    { 
      stat: displayMode === 'real' ? `Aériens gagnés (${stats.aerial_duels_won || 0})` : 'Aériens gagnés', 
      value: displayMode === 'real' ? stats.aerial_duels_won || 0 : Math.min(100, (stats.aerial_duels_won || 0) * 2), 
      rawValue: stats.aerial_duels_won || 0,
      percentile: Math.min(100, (stats.aerial_duels_won || 0) * 2)
    },
    { 
      stat: displayMode === 'real' ? `Fautes comm. (${stats.fouls || 0})` : 'Fautes comm.', 
      value: displayMode === 'real' ? stats.fouls || 0 : Math.min(100, 100 - ((stats.fouls || 0) * 2.5)), 
      rawValue: stats.fouls || 0,
      percentile: Math.min(100, 100 - ((stats.fouls || 0) * 2.5))
    },
    { 
      stat: displayMode === 'real' ? `Fautes subies (${stats.fouls_drawn || 0})` : 'Fautes subies', 
      value: displayMode === 'real' ? stats.fouls_drawn || 0 : Math.min(100, (stats.fouls_drawn || 0) * 3), 
      rawValue: stats.fouls_drawn || 0,
      percentile: Math.min(100, (stats.fouls_drawn || 0) * 3)
    },
    { 
      stat: displayMode === 'real' ? `C. jaunes (${stats.yellow_cards || 0})` : 'C. jaunes', 
      value: displayMode === 'real' ? stats.yellow_cards || 0 : Math.min(100, 100 - ((stats.yellow_cards || 0) * 12)), 
      rawValue: stats.yellow_cards || 0,
      percentile: Math.min(100, 100 - ((stats.yellow_cards || 0) * 12))
    },
    { 
      stat: displayMode === 'real' ? `C. rouges (${stats.red_cards || 0})` : 'C. rouges', 
      value: displayMode === 'real' ? stats.red_cards || 0 : Math.min(100, 100 - ((stats.red_cards || 0) * 50)), 
      rawValue: stats.red_cards || 0,
      percentile: Math.min(100, 100 - ((stats.red_cards || 0) * 50))
    },
    { 
      stat: displayMode === 'real' ? `Pen. conc. (${stats.penalties_committed || 0})` : 'Pen. conc.', 
      value: displayMode === 'real' ? stats.penalties_committed || 0 : Math.min(100, 100 - ((stats.penalties_committed || 0) * 25)), 
      rawValue: stats.penalties_committed || 0,
      percentile: Math.min(100, 100 - ((stats.penalties_committed || 0) * 25))
    },
    { 
      stat: displayMode === 'real' ? `Erreurs→but (${stats.mistakes_leading_to_goals || 0})` : 'Erreurs→but', 
      value: displayMode === 'real' ? stats.mistakes_leading_to_goals || 0 : Math.min(100, 100 - ((stats.mistakes_leading_to_goals || 0) * 50)), 
      rawValue: stats.mistakes_leading_to_goals || 0,
      percentile: Math.min(100, 100 - ((stats.mistakes_leading_to_goals || 0) * 50))
    }
  ] : [];

  // 5. CARTE GARDIEN - Stats spécifiques gardien
  const goalkeeperData = isGoalkeeper ? [
    { 
      stat: displayMode === 'real' ? `Arrêts (${stats.saves || 0})` : 'Arrêts', 
      value: displayMode === 'real' ? Math.min(150, stats.saves || 0) : Math.min(100, (stats.saves || 0) / 1.5), 
      rawValue: stats.saves || 0,
      percentile: Math.min(100, (stats.saves || 0) / 1.5)
    },
    { 
      stat: displayMode === 'real' ? `Arrêts surface (${stats.inside_box_saves || 0})` : 'Arrêts surface', 
      value: displayMode === 'real' ? Math.min(100, stats.inside_box_saves || 0) : Math.min(100, (stats.inside_box_saves || 0) / 1), 
      rawValue: stats.inside_box_saves || 0,
      percentile: Math.min(100, (stats.inside_box_saves || 0) / 1)
    },
    { 
      stat: displayMode === 'real' ? `Pen. arrêtés (${stats.penalties_saved || 0})` : 'Pen. arrêtés', 
      value: displayMode === 'real' ? stats.penalties_saved || 0 : Math.min(100, (stats.penalties_saved || 0) * 33), 
      rawValue: stats.penalties_saved || 0,
      percentile: Math.min(100, (stats.penalties_saved || 0) * 33)
    },
    { 
      stat: displayMode === 'real' ? `Clean sheets (${stats.clean_sheets || 0})` : 'Clean sheets', 
      value: displayMode === 'real' ? stats.clean_sheets || 0 : Math.min(100, (stats.clean_sheets || 0) * 10), 
      rawValue: stats.clean_sheets || 0,
      percentile: Math.min(100, (stats.clean_sheets || 0) * 10)
    },
    { 
      stat: displayMode === 'real' ? `Buts encaissés (${stats.goals_conceded || 0})` : 'Buts encaissés', 
      value: displayMode === 'real' ? stats.goals_conceded || 0 : Math.min(100, 100 - ((stats.goals_conceded || 0) * 2.5)), 
      rawValue: stats.goals_conceded || 0,
      percentile: Math.min(100, 100 - ((stats.goals_conceded || 0) * 2.5))
    },
    { 
      stat: displayMode === 'real' ? `Pen. concédés (${stats.penalties_committed || 0})` : 'Pen. concédés', 
      value: displayMode === 'real' ? stats.penalties_committed || 0 : Math.min(100, 100 - ((stats.penalties_committed || 0) * 25)), 
      rawValue: stats.penalties_committed || 0,
      percentile: Math.min(100, 100 - ((stats.penalties_committed || 0) * 25))
    },
    { 
      stat: displayMode === 'real' ? `Erreurs→but (${stats.mistakes_leading_to_goals || 0})` : 'Erreurs→but', 
      value: displayMode === 'real' ? stats.mistakes_leading_to_goals || 0 : Math.min(100, 100 - ((stats.mistakes_leading_to_goals || 0) * 50)), 
      rawValue: stats.mistakes_leading_to_goals || 0,
      percentile: Math.min(100, 100 - ((stats.mistakes_leading_to_goals || 0) * 50))
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
            title="📊 Général"
          />
          <RadarChartComponent 
            data={goalkeeperData} 
            color="#10B981" 
            title="🥅 Gardien"
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
          title="📊 Général"
        />
        <RadarChartComponent 
          data={offensiveData} 
          color="#EF4444" 
          title="⚽ Offensif"
        />
        <RadarChartComponent 
          data={creativeData} 
          color="#10B981" 
          title="🎯 Créatif (passes & dribbles)"
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