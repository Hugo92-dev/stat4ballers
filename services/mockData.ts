import { PlayerStatistics } from './sportmonks';
import { Player } from '@/data/types';

/**
 * Génère des statistiques réalistes basées sur la position du joueur
 */
export function generateRealisticStats(player: Player, seasonName: string): PlayerStatistics {
  const position = player.position?.toUpperCase();
  const isGoalkeeper = position === 'GK';
  const isDefender = position === 'DF' || position === 'DEF';
  const isMidfielder = position === 'MF' || position === 'MID';
  const isForward = position === 'FW' || position === 'ATT';
  
  // Base stats communes
  const baseStats: PlayerStatistics = {
    season_name: seasonName,
    minutes: Math.floor(Math.random() * 2000) + 1000,
    appearences: Math.floor(Math.random() * 25) + 10,
    lineups: Math.floor(Math.random() * 20) + 5,
    captain: Math.floor(Math.random() * 5),
    rating: 6.5 + Math.random() * 1.5,
    touches: Math.floor(Math.random() * 1500) + 500,
    ball_recoveries: Math.floor(Math.random() * 100) + 20,
    ball_losses: Math.floor(Math.random() * 150) + 50,
    
    // Passes
    passes: Math.floor(Math.random() * 1000) + 300,
    passes_total: Math.floor(Math.random() * 1200) + 400,
    passes_accuracy: 75 + Math.random() * 20,
    key_passes: Math.floor(Math.random() * 30) + 5,
    
    // Discipline
    yellow_cards: Math.floor(Math.random() * 8),
    red_cards: Math.random() > 0.9 ? 1 : 0,
    fouls: Math.floor(Math.random() * 40) + 10,
    fouls_drawn: Math.floor(Math.random() * 30) + 10,
  };
  
  // Stats spécifiques par position
  if (isGoalkeeper) {
    return {
      ...baseStats,
      goals: 0,
      assists: 0,
      saves: Math.floor(Math.random() * 80) + 40,
      inside_box_saves: Math.floor(Math.random() * 50) + 20,
      penalties_saved: Math.floor(Math.random() * 3),
      clean_sheets: Math.floor(Math.random() * 10) + 3,
      goals_conceded: Math.floor(Math.random() * 40) + 15,
      shots: 0,
      shots_on_target: 0,
    };
  }
  
  if (isDefender) {
    return {
      ...baseStats,
      goals: Math.floor(Math.random() * 3),
      assists: Math.floor(Math.random() * 4),
      tackles: Math.floor(Math.random() * 80) + 40,
      interceptions: Math.floor(Math.random() * 60) + 30,
      blocks: Math.floor(Math.random() * 30) + 10,
      clearances: Math.floor(Math.random() * 100) + 50,
      duels: Math.floor(Math.random() * 200) + 100,
      duels_won: Math.floor(Math.random() * 120) + 60,
      aerial_duels: Math.floor(Math.random() * 100) + 50,
      aerial_duels_won: Math.floor(Math.random() * 60) + 30,
      shots: Math.floor(Math.random() * 15) + 5,
      shots_on_target: Math.floor(Math.random() * 5) + 1,
    };
  }
  
  if (isMidfielder) {
    return {
      ...baseStats,
      goals: Math.floor(Math.random() * 8) + 2,
      assists: Math.floor(Math.random() * 10) + 3,
      expected_goals: Math.random() * 8 + 2,
      expected_assists: Math.random() * 10 + 3,
      tackles: Math.floor(Math.random() * 60) + 20,
      interceptions: Math.floor(Math.random() * 40) + 15,
      dribbles: Math.floor(Math.random() * 60) + 20,
      dribbles_succeeded: Math.floor(Math.random() * 40) + 10,
      crosses: Math.floor(Math.random() * 50) + 10,
      crosses_total: Math.floor(Math.random() * 80) + 20,
      shots: Math.floor(Math.random() * 40) + 15,
      shots_on_target: Math.floor(Math.random() * 15) + 5,
      key_passes: Math.floor(Math.random() * 50) + 20,
    };
  }
  
  if (isForward) {
    return {
      ...baseStats,
      goals: Math.floor(Math.random() * 20) + 8,
      assists: Math.floor(Math.random() * 10) + 3,
      expected_goals: Math.random() * 20 + 8,
      expected_assists: Math.random() * 10 + 3,
      shots: Math.floor(Math.random() * 80) + 40,
      shots_on_target: Math.floor(Math.random() * 35) + 15,
      shots_blocked: Math.floor(Math.random() * 20) + 5,
      penalties: Math.floor(Math.random() * 5),
      penalties_scored: Math.floor(Math.random() * 4),
      hit_woodwork: Math.floor(Math.random() * 3),
      offsides: Math.floor(Math.random() * 25) + 10,
      dribbles: Math.floor(Math.random() * 80) + 30,
      dribbles_succeeded: Math.floor(Math.random() * 50) + 15,
    };
  }
  
  // Par défaut (si position inconnue)
  return baseStats;
}

/**
 * Génère des statistiques pour les 3 saisons
 */
export function generateMockStatsForPlayer(player: Player) {
  const current = generateRealisticStats(player, '2025/2026');
  const previous1 = generateRealisticStats(player, '2024/2025');
  const previous2 = generateRealisticStats(player, '2023/2024');
  
  // Ajuster légèrement les stats pour plus de réalisme
  current.minutes = Math.floor(current.minutes * 0.3); // Saison en cours
  current.appearences = Math.floor(current.appearences * 0.3);
  
  return {
    current,
    previous: [previous1, previous2]
  };
}