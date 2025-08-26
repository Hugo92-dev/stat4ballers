// Stats réelles des joueurs de l'OM depuis SportMonks API
// Généré automatiquement

export interface PlayerSeasonStats {
  rating: number;
  minutes: number;
  appearences: number;
  lineups: number;
  captain: number;
  substitutions: number;
  touches: number;
  saves: number;
  punches: number;
  goals: number;
  assists: number;
  shots: number;
  shots_on_target: number;
  xg: number;
  xa: number;
  offsides: number;
  penalties: number;
  penalties_scored: number;
  penalties_missed: number;
  hit_woodwork: number;
  tackles: number;
  blocks: number;
  interceptions: number;
  clearances: number;
  aerial_duels: number;
  aerial_duels_won: number;
  ground_duels: number;
  ground_duels_won: number;
  fouls: number;
  fouls_drawn: number;
  yellow_cards: number;
  red_cards: number;
  clean_sheets: number;
  goals_conceded: number;
  passes: number;
  passes_completed: number;
  passes_accuracy: number;
  key_passes: number;
  crosses: number;
  crosses_accurate: number;
  long_balls: number;
  long_balls_accurate: number;
  through_balls: number;
  through_balls_accurate: number;
  dribbles: number;
  dribbles_successful: number;
  progressive_carries: number;
  big_chances_created: number;
}

export interface PlayerRealStats {
  id: number;
  name: string;
  display_name?: string;
  position: string;
  jersey?: number;
  stats: {
    [season: string]: PlayerSeasonStats;
  };
}

export const omRealStats: { [playerId: number]: PlayerRealStats } = {};
