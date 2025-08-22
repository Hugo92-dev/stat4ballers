// Service pour l'API SportMonks
import { LIGUE1_PLAYER_IDS } from './allPlayerIds';
import { LIGUE1_PLAYER_POSITIONS } from './playerPositions';

const API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2';
const BASE_URL = 'https://api.sportmonks.com/v3/football';

// IDs des saisons actuelles (2025/2026)
export const CURRENT_SEASONS = {
  ligue1: 25651,
  premierLeague: 25583,
  liga: 25659,
  serieA: 25533,
  bundesliga: 25646
};

// IDs des saisons précédentes (2024/2025, 2023/2024)
// Note: Pour obtenir des données de test, on va simuler temporairement
export const PREVIOUS_SEASONS = {
  ligue1: [25651, 25651], // On utilise la même saison pour tester
  premierLeague: [25583, 25583],
  liga: [25659, 25659],
  serieA: [25533, 25533],
  bundesliga: [25646, 25646]
};

export interface PlayerStatistics {
  // Général
  minutes?: number;
  appearences?: number;
  lineups?: number;
  captain?: number;
  rating?: number;
  touches?: number;
  ball_recoveries?: number;
  ball_losses?: number;
  
  // Offensif
  goals?: number;
  assists?: number;
  expected_goals?: number;
  expected_assists?: number;
  shots?: number;
  shots_on_target?: number;
  shots_blocked?: number;
  penalties?: number;
  penalties_scored?: number;
  penalties_missed?: number;
  hit_woodwork?: number;
  offsides?: number;
  
  // Créatif (passes & dribbles)
  passes?: number;
  passes_total?: number;
  passes_accuracy?: number;
  key_passes?: number;
  crosses?: number;
  crosses_total?: number;
  crosses_accuracy?: number;
  dribbles?: number;
  dribbles_succeeded?: number;
  dribbles_failed?: number;
  
  // Défensif & Discipline
  tackles?: number;
  interceptions?: number;
  blocks?: number;
  clearances?: number;
  duels?: number;
  duels_won?: number;
  aerial_duels?: number;
  aerial_duels_won?: number;
  fouls?: number;
  fouls_drawn?: number;
  yellow_cards?: number;
  yellowred_cards?: number;
  red_cards?: number;
  penalties_committed?: number;
  mistakes_leading_to_goals?: number;
  
  // Gardien
  saves?: number;
  inside_box_saves?: number;
  penalties_saved?: number;
  clean_sheets?: number;
  goals_conceded?: number;
  
  // Métadonnées
  season_id?: number;
  season_name?: string;
  team_id?: number;
  team_name?: string;
}

export interface PlayerStatsResponse {
  current: PlayerStatistics | null;
  previous: PlayerStatistics[];
  cumulative: PlayerStatistics | null;
  error?: string;
}

/**
 * Récupère les statistiques d'un joueur pour la saison en cours et les saisons précédentes
 */
export async function getPlayerStatistics(
  playerId: number,
  league: keyof typeof CURRENT_SEASONS
): Promise<PlayerStatsResponse> {
  // TODO: Phase 2 - Intégrer l'API réelle SportMonks
  // Pour l'instant, on utilise des données mock pour tous les joueurs
  
  // Vérifier si on devrait utiliser l'API (à implémenter plus tard)
  const USE_REAL_API = false; // Sera mis à true quand l'API sera prête
  
  if (USE_REAL_API) {
    // Future intégration API
    // return await fetchRealPlayerStats(playerId, league);
  }
  
  // Pour l'instant: données mock pour tous les joueurs
  const mockStats = generateMockStats(playerId);
  return mockStats;
}

/**
 * Calcule les statistiques cumulées sur plusieurs saisons
 */
export function calculateCumulativeStats(seasons: PlayerStatistics[]): PlayerStatistics | null {
  if (seasons.length === 0) return null;
  
  const cumulative: PlayerStatistics = {
    season_name: 'Total des 3 dernières saisons',
    
    // Général - SOMME
    minutes: 0,
    appearences: 0,
    lineups: 0,
    captain: 0,
    touches: 0,
    ball_recoveries: 0,
    ball_losses: 0,
    
    // Offensif - SOMME
    goals: 0,
    assists: 0,
    expected_goals: 0,
    expected_assists: 0,
    shots: 0,
    shots_on_target: 0,
    shots_blocked: 0,
    penalties: 0,
    penalties_scored: 0,
    penalties_missed: 0,
    hit_woodwork: 0,
    offsides: 0,
    
    // Créatif - SOMME sauf pourcentages
    passes: 0,
    passes_total: 0,
    key_passes: 0,
    crosses: 0,
    crosses_total: 0,
    dribbles: 0,
    dribbles_succeeded: 0,
    dribbles_failed: 0,
    
    // Défensif & Discipline - SOMME
    tackles: 0,
    interceptions: 0,
    blocks: 0,
    clearances: 0,
    duels: 0,
    duels_won: 0,
    aerial_duels: 0,
    aerial_duels_won: 0,
    fouls: 0,
    fouls_drawn: 0,
    yellow_cards: 0,
    yellowred_cards: 0,
    red_cards: 0,
    penalties_committed: 0,
    mistakes_leading_to_goals: 0,
    
    // Gardien - SOMME
    saves: 0,
    inside_box_saves: 0,
    penalties_saved: 0,
    clean_sheets: 0,
    goals_conceded: 0
  };
  
  // Variables pour moyennes
  let totalRating = 0;
  let ratingCount = 0;
  
  // Additionner les stats de chaque saison
  for (const season of seasons) {
    if (!season) continue;
    
    // Stats simples (somme)
    cumulative.minutes = (cumulative.minutes || 0) + (season.minutes || 0);
    cumulative.appearences = (cumulative.appearences || 0) + (season.appearences || 0);
    cumulative.lineups = (cumulative.lineups || 0) + (season.lineups || 0);
    cumulative.captain = (cumulative.captain || 0) + (season.captain || 0);
    cumulative.touches = (cumulative.touches || 0) + (season.touches || 0);
    cumulative.ball_recoveries = (cumulative.ball_recoveries || 0) + (season.ball_recoveries || 0);
    cumulative.ball_losses = (cumulative.ball_losses || 0) + (season.ball_losses || 0);
    
    cumulative.goals = (cumulative.goals || 0) + (season.goals || 0);
    cumulative.assists = (cumulative.assists || 0) + (season.assists || 0);
    cumulative.expected_goals = (cumulative.expected_goals || 0) + (season.expected_goals || 0);
    cumulative.expected_assists = (cumulative.expected_assists || 0) + (season.expected_assists || 0);
    cumulative.shots = (cumulative.shots || 0) + (season.shots || 0);
    cumulative.shots_on_target = (cumulative.shots_on_target || 0) + (season.shots_on_target || 0);
    cumulative.shots_blocked = (cumulative.shots_blocked || 0) + (season.shots_blocked || 0);
    cumulative.penalties = (cumulative.penalties || 0) + (season.penalties || 0);
    cumulative.penalties_scored = (cumulative.penalties_scored || 0) + (season.penalties_scored || 0);
    cumulative.penalties_missed = (cumulative.penalties_missed || 0) + (season.penalties_missed || 0);
    cumulative.hit_woodwork = (cumulative.hit_woodwork || 0) + (season.hit_woodwork || 0);
    cumulative.offsides = (cumulative.offsides || 0) + (season.offsides || 0);
    
    cumulative.passes = (cumulative.passes || 0) + (season.passes || 0);
    cumulative.passes_total = (cumulative.passes_total || 0) + (season.passes_total || 0);
    cumulative.key_passes = (cumulative.key_passes || 0) + (season.key_passes || 0);
    cumulative.crosses = (cumulative.crosses || 0) + (season.crosses || 0);
    cumulative.crosses_total = (cumulative.crosses_total || 0) + (season.crosses_total || 0);
    cumulative.dribbles = (cumulative.dribbles || 0) + (season.dribbles || 0);
    cumulative.dribbles_succeeded = (cumulative.dribbles_succeeded || 0) + (season.dribbles_succeeded || 0);
    cumulative.dribbles_failed = (cumulative.dribbles_failed || 0) + (season.dribbles_failed || 0);
    
    cumulative.tackles = (cumulative.tackles || 0) + (season.tackles || 0);
    cumulative.interceptions = (cumulative.interceptions || 0) + (season.interceptions || 0);
    cumulative.blocks = (cumulative.blocks || 0) + (season.blocks || 0);
    cumulative.clearances = (cumulative.clearances || 0) + (season.clearances || 0);
    cumulative.duels = (cumulative.duels || 0) + (season.duels || 0);
    cumulative.duels_won = (cumulative.duels_won || 0) + (season.duels_won || 0);
    cumulative.aerial_duels = (cumulative.aerial_duels || 0) + (season.aerial_duels || 0);
    cumulative.aerial_duels_won = (cumulative.aerial_duels_won || 0) + (season.aerial_duels_won || 0);
    cumulative.fouls = (cumulative.fouls || 0) + (season.fouls || 0);
    cumulative.fouls_drawn = (cumulative.fouls_drawn || 0) + (season.fouls_drawn || 0);
    cumulative.yellow_cards = (cumulative.yellow_cards || 0) + (season.yellow_cards || 0);
    cumulative.yellowred_cards = (cumulative.yellowred_cards || 0) + (season.yellowred_cards || 0);
    cumulative.red_cards = (cumulative.red_cards || 0) + (season.red_cards || 0);
    cumulative.penalties_committed = (cumulative.penalties_committed || 0) + (season.penalties_committed || 0);
    cumulative.mistakes_leading_to_goals = (cumulative.mistakes_leading_to_goals || 0) + (season.mistakes_leading_to_goals || 0);
    
    cumulative.saves = (cumulative.saves || 0) + (season.saves || 0);
    cumulative.inside_box_saves = (cumulative.inside_box_saves || 0) + (season.inside_box_saves || 0);
    cumulative.penalties_saved = (cumulative.penalties_saved || 0) + (season.penalties_saved || 0);
    cumulative.clean_sheets = (cumulative.clean_sheets || 0) + (season.clean_sheets || 0);
    cumulative.goals_conceded = (cumulative.goals_conceded || 0) + (season.goals_conceded || 0);
    
    // Note moyenne
    if (season.rating && season.rating > 0) {
      totalRating += season.rating;
      ratingCount++;
    }
  }
  
  // Calculer les moyennes et pourcentages
  if (ratingCount > 0) {
    cumulative.rating = totalRating / ratingCount;
  }
  
  // Calculer les pourcentages
  if (cumulative.passes_total && cumulative.passes_total > 0) {
    cumulative.passes_accuracy = (cumulative.passes / cumulative.passes_total) * 100;
  }
  
  if (cumulative.crosses_total && cumulative.crosses_total > 0) {
    cumulative.crosses_accuracy = (cumulative.crosses / cumulative.crosses_total) * 100;
  }
  
  return cumulative;
}

/**
 * Récupère les statistiques d'un joueur pour une saison spécifique
 */
async function fetchSeasonStats(
  playerId: number,
  seasonId: number,
  seasonName: string
): Promise<PlayerStatistics | null> {
  try {
    const url = `${BASE_URL}/statistics/seasons/players/${playerId}`;
    const params = new URLSearchParams({
      api_token: API_TOKEN,
      filters: `season_ids:${seasonId}`
    });
    
    const response = await fetch(`${url}?${params}`);
    
    if (!response.ok) {
      console.error(`Erreur API: ${response.status}`);
      return null;
    }
    
    const data = await response.json();
    const stats = data.data?.[0];
    
    if (!stats) {
      return null;
    }
    
    // Vérifier si le joueur a des données pour cette saison
    if (!stats.minutes && !stats.appearences && !stats.goals) {
      return null;
    }
    
    // Mapper les données de l'API vers notre structure
    return {
      // Général
      minutes: stats.minutes || 0,
      appearences: stats.appearences || 0,
      lineups: stats.lineups || 0,
      captain: stats.captain || 0,
      rating: stats.rating || 0,
      touches: stats.touches || 0,
      ball_recoveries: stats.ball_recoveries || 0,
      ball_losses: stats.ball_losses || 0,
      
      // Offensif
      goals: stats.goals || 0,
      assists: stats.assists || 0,
      expected_goals: stats.expected_goals || 0,
      expected_assists: stats.expected_assists || 0,
      shots: stats.shots || stats.shots_total || 0,
      shots_on_target: stats.shots_on_target || 0,
      shots_blocked: stats.shots_blocked || 0,
      penalties: stats.penalties || 0,
      penalties_scored: stats.penalties_scored || 0,
      penalties_missed: stats.penalties_missed || 0,
      hit_woodwork: stats.hit_woodwork || 0,
      offsides: stats.offsides || 0,
      
      // Créatif
      passes: stats.passes || 0,
      passes_total: stats.passes_total || 0,
      passes_accuracy: stats.passes_accuracy || 0,
      key_passes: stats.key_passes || stats.passes_key || 0,
      crosses: stats.crosses || stats.crosses_accurate || 0,
      crosses_total: stats.crosses_total || 0,
      crosses_accuracy: stats.crosses_accuracy || 0,
      dribbles: stats.dribbles || 0,
      dribbles_succeeded: stats.dribbles_succeeded || 0,
      dribbles_failed: stats.dribbles_failed || 0,
      
      // Défensif & Discipline
      tackles: stats.tackles || 0,
      interceptions: stats.interceptions || 0,
      blocks: stats.blocks || 0,
      clearances: stats.clearances || 0,
      duels: stats.duels || 0,
      duels_won: stats.duels_won || 0,
      aerial_duels: stats.aerial_duels || 0,
      aerial_duels_won: stats.aerial_duels_won || 0,
      fouls: stats.fouls || stats.fouls_committed || 0,
      fouls_drawn: stats.fouls_drawn || 0,
      yellow_cards: stats.yellow_cards || 0,
      yellowred_cards: stats.yellowred_cards || 0,
      red_cards: stats.red_cards || 0,
      penalties_committed: stats.penalties_committed || 0,
      mistakes_leading_to_goals: stats.mistakes_leading_to_goals || 0,
      
      // Gardien
      saves: stats.saves || 0,
      inside_box_saves: stats.inside_box_saves || 0,
      penalties_saved: stats.penalties_saved || 0,
      clean_sheets: stats.clean_sheets || 0,
      goals_conceded: stats.goals_conceded || 0,
      
      // Métadonnées
      season_id: seasonId,
      season_name: seasonName,
      team_id: stats.team_id,
      team_name: stats.team_name
    };
  } catch (error) {
    console.error(`Erreur pour le joueur ${playerId}, saison ${seasonId}:`, error);
    return null;
  }
}

/**
 * Génère des statistiques mock réalistes pour un joueur
 */
function generateMockStats(playerId: number): PlayerStatsResponse {
  // Déterminer la position du joueur
  // D'abord vérifier dans les positions connues (Ligue 1 pour l'instant)
  const knownGoalkeepers = LIGUE1_PLAYER_POSITIONS.goalkeepers;
  const knownDefenders = LIGUE1_PLAYER_POSITIONS.defenders;
  const knownMidfielders = LIGUE1_PLAYER_POSITIONS.midfielders;
  const knownForwards = LIGUE1_PLAYER_POSITIONS.forwards;
  
  let position: 'goalkeeper' | 'defender' | 'midfielder' | 'forward';
  
  // Vérifier si on connaît la position
  if (knownGoalkeepers.includes(playerId)) {
    position = 'goalkeeper';
  } else if (knownDefenders.includes(playerId)) {
    position = 'defender';
  } else if (knownMidfielders.includes(playerId)) {
    position = 'midfielder';
  } else if (knownForwards.includes(playerId)) {
    position = 'forward';
  } else {
    // Pour les joueurs dont on ne connaît pas la position (autres ligues)
    // Utiliser un hash de l'ID pour déterminer une position cohérente
    const hash = playerId % 100;
    if (hash < 10) {
      position = 'goalkeeper'; // 10% des joueurs
    } else if (hash < 45) {
      position = 'defender'; // 35% des joueurs
    } else if (hash < 75) {
      position = 'midfielder'; // 30% des joueurs
    } else {
      position = 'forward'; // 25% des joueurs
    }
  }
  
  let baseStats: Partial<PlayerStatistics>;
  
  if (position === 'goalkeeper') {
    // Stats pour gardiens
    baseStats = {
      minutes: 2700 + Math.floor(Math.random() * 900),
      appearences: 30 + Math.floor(Math.random() * 8),
      lineups: 28 + Math.floor(Math.random() * 7),
      captain: Math.floor(Math.random() * 5),
      rating: 6.5 + Math.random() * 0.8,
      saves: 85 + Math.floor(Math.random() * 40),
      inside_box_saves: 45 + Math.floor(Math.random() * 25),
      clean_sheets: 8 + Math.floor(Math.random() * 7),
      goals_conceded: 28 + Math.floor(Math.random() * 15),
      penalties_saved: Math.floor(Math.random() * 3),
      penalties_committed: Math.floor(Math.random() * 2),
      mistakes_leading_to_goals: Math.floor(Math.random() * 3),
      yellow_cards: Math.floor(Math.random() * 4),
      red_cards: 0,
      passes: 650 + Math.floor(Math.random() * 200),
      passes_total: 800 + Math.floor(Math.random() * 250),
      passes_accuracy: 75 + Math.floor(Math.random() * 15)
    };
  } else if (position === 'defender') {
    // Stats pour défenseurs
    baseStats = {
      minutes: 2200 + Math.floor(Math.random() * 1000),
      appearences: 25 + Math.floor(Math.random() * 10),
      lineups: 22 + Math.floor(Math.random() * 10),
      captain: Math.floor(Math.random() * 8),
      rating: 6.8 + Math.random() * 0.6,
      touches: 1500 + Math.floor(Math.random() * 500),
      ball_recoveries: 150 + Math.floor(Math.random() * 50),
      ball_losses: 80 + Math.floor(Math.random() * 30),
      goals: Math.floor(Math.random() * 4),
      assists: Math.floor(Math.random() * 5),
      shots: 15 + Math.floor(Math.random() * 20),
      shots_on_target: 5 + Math.floor(Math.random() * 10),
      passes: 1200 + Math.floor(Math.random() * 400),
      passes_total: 1400 + Math.floor(Math.random() * 500),
      passes_accuracy: 82 + Math.floor(Math.random() * 10),
      key_passes: 10 + Math.floor(Math.random() * 15),
      crosses: 5 + Math.floor(Math.random() * 15),
      crosses_total: 10 + Math.floor(Math.random() * 25),
      crosses_accuracy: 20 + Math.floor(Math.random() * 30),
      dribbles: 15 + Math.floor(Math.random() * 20),
      dribbles_succeeded: 8 + Math.floor(Math.random() * 12),
      tackles: 50 + Math.floor(Math.random() * 30),
      interceptions: 40 + Math.floor(Math.random() * 25),
      duels: 180 + Math.floor(Math.random() * 70),
      duels_won: 100 + Math.floor(Math.random() * 50),
      aerial_duels: 80 + Math.floor(Math.random() * 40),
      aerial_duels_won: 45 + Math.floor(Math.random() * 25),
      fouls: 25 + Math.floor(Math.random() * 15),
      fouls_drawn: 15 + Math.floor(Math.random() * 10),
      yellow_cards: 4 + Math.floor(Math.random() * 4),
      red_cards: Math.floor(Math.random() * 2),
      penalties_committed: Math.floor(Math.random() * 2),
      mistakes_leading_to_goals: Math.floor(Math.random() * 2)
    };
  } else if (position === 'midfielder') {
    // Stats pour milieux
    baseStats = {
      minutes: 2000 + Math.floor(Math.random() * 1200),
      appearences: 25 + Math.floor(Math.random() * 12),
      lineups: 20 + Math.floor(Math.random() * 12),
      captain: Math.floor(Math.random() * 10),
      rating: 6.9 + Math.random() * 0.7,
      touches: 1800 + Math.floor(Math.random() * 600),
      ball_recoveries: 120 + Math.floor(Math.random() * 60),
      ball_losses: 100 + Math.floor(Math.random() * 40),
      goals: 2 + Math.floor(Math.random() * 8),
      assists: 3 + Math.floor(Math.random() * 9),
      expected_goals: 2 + Math.random() * 6,
      expected_assists: 3 + Math.random() * 7,
      shots: 25 + Math.floor(Math.random() * 35),
      shots_on_target: 10 + Math.floor(Math.random() * 15),
      penalties: Math.floor(Math.random() * 3),
      penalties_scored: Math.floor(Math.random() * 3),
      hit_woodwork: Math.floor(Math.random() * 3),
      offsides: Math.floor(Math.random() * 5),
      passes: 1400 + Math.floor(Math.random() * 600),
      passes_total: 1600 + Math.floor(Math.random() * 700),
      passes_accuracy: 83 + Math.floor(Math.random() * 12),
      key_passes: 30 + Math.floor(Math.random() * 25),
      crosses: 15 + Math.floor(Math.random() * 25),
      crosses_total: 25 + Math.floor(Math.random() * 35),
      crosses_accuracy: 25 + Math.floor(Math.random() * 25),
      dribbles: 35 + Math.floor(Math.random() * 40),
      dribbles_succeeded: 20 + Math.floor(Math.random() * 25),
      tackles: 40 + Math.floor(Math.random() * 25),
      interceptions: 30 + Math.floor(Math.random() * 20),
      duels: 150 + Math.floor(Math.random() * 80),
      duels_won: 75 + Math.floor(Math.random() * 45),
      aerial_duels: 30 + Math.floor(Math.random() * 30),
      aerial_duels_won: 15 + Math.floor(Math.random() * 15),
      fouls: 20 + Math.floor(Math.random() * 15),
      fouls_drawn: 25 + Math.floor(Math.random() * 15),
      yellow_cards: 3 + Math.floor(Math.random() * 5),
      red_cards: Math.floor(Math.random() * 1.5),
      penalties_committed: Math.floor(Math.random() * 2),
      mistakes_leading_to_goals: Math.floor(Math.random() * 2)
    };
  } else { // position === 'forward'
    // Stats pour attaquants
    baseStats = {
      minutes: 1800 + Math.floor(Math.random() * 1200),
      appearences: 22 + Math.floor(Math.random() * 13),
      lineups: 18 + Math.floor(Math.random() * 12),
      captain: Math.floor(Math.random() * 3),
      rating: 6.8 + Math.random() * 0.8,
      touches: 900 + Math.floor(Math.random() * 400),
      ball_recoveries: 30 + Math.floor(Math.random() * 20),
      ball_losses: 120 + Math.floor(Math.random() * 50),
      goals: 8 + Math.floor(Math.random() * 12),
      assists: 3 + Math.floor(Math.random() * 7),
      expected_goals: 7 + Math.random() * 10,
      expected_assists: 3 + Math.random() * 5,
      shots: 60 + Math.floor(Math.random() * 50),
      shots_on_target: 25 + Math.floor(Math.random() * 25),
      penalties: Math.floor(Math.random() * 5),
      penalties_scored: Math.floor(Math.random() * 5),
      hit_woodwork: Math.floor(Math.random() * 4),
      offsides: 15 + Math.floor(Math.random() * 20),
      passes: 500 + Math.floor(Math.random() * 300),
      passes_total: 600 + Math.floor(Math.random() * 350),
      passes_accuracy: 75 + Math.floor(Math.random() * 15),
      key_passes: 20 + Math.floor(Math.random() * 20),
      crosses: 10 + Math.floor(Math.random() * 20),
      crosses_total: 20 + Math.floor(Math.random() * 30),
      crosses_accuracy: 20 + Math.floor(Math.random() * 30),
      dribbles: 45 + Math.floor(Math.random() * 45),
      dribbles_succeeded: 25 + Math.floor(Math.random() * 25),
      tackles: 10 + Math.floor(Math.random() * 15),
      interceptions: 5 + Math.floor(Math.random() * 10),
      duels: 120 + Math.floor(Math.random() * 60),
      duels_won: 50 + Math.floor(Math.random() * 30),
      aerial_duels: 40 + Math.floor(Math.random() * 30),
      aerial_duels_won: 15 + Math.floor(Math.random() * 15),
      fouls: 15 + Math.floor(Math.random() * 10),
      fouls_drawn: 30 + Math.floor(Math.random() * 20),
      yellow_cards: 2 + Math.floor(Math.random() * 4),
      red_cards: Math.floor(Math.random() * 1.2),
      penalties_committed: Math.floor(Math.random() * 1.5),
      mistakes_leading_to_goals: Math.floor(Math.random() * 1.5)
    };
  }
  
  // Créer les stats complètes pour 3 saisons
  const currentStats: PlayerStatistics = {
    ...baseStats as PlayerStatistics,
    season_id: CURRENT_SEASONS.ligue1,
    season_name: '2025/2026',
    team_id: 85,
    team_name: 'Olympique de Marseille'
  };
  
  const prevStats1: PlayerStatistics = {
    ...baseStats as PlayerStatistics,
    minutes: Math.floor((baseStats.minutes || 0) * 0.95),
    appearences: Math.floor((baseStats.appearences || 0) * 0.95),
    goals: Math.floor((baseStats.goals || 0) * 0.9),
    assists: Math.floor((baseStats.assists || 0) * 0.9),
    season_id: 21646,
    season_name: '2024/2025',
    team_id: 85,
    team_name: 'Olympique de Marseille'
  };
  
  const prevStats2: PlayerStatistics = {
    ...baseStats as PlayerStatistics,
    minutes: Math.floor((baseStats.minutes || 0) * 0.85),
    appearences: Math.floor((baseStats.appearences || 0) * 0.85),
    goals: Math.floor((baseStats.goals || 0) * 0.85),
    assists: Math.floor((baseStats.assists || 0) * 0.85),
    season_id: 19686,
    season_name: '2023/2024',
    team_id: 85,
    team_name: 'Olympique de Marseille'
  };
  
  const allStats = [currentStats, prevStats1, prevStats2];
  const cumulative = calculateCumulativeStats(allStats);
  
  return {
    current: currentStats,
    previous: [prevStats1, prevStats2],
    cumulative: cumulative
  };
}

/**
 * Récupère les IDs SportMonks des joueurs de l'OM
 * IDs réels récupérés depuis l'API SportMonks
 */
export function getOMPlayerIds(): Record<string, number> {
  return {
    // Gardiens
    'GeronimoRulli': 186418,  // ID vérifié depuis l'API SportMonks
    'JeffreydeLange': 29186,
    'RubenBlanco': 186456,
    'JelleVanNeck': 37593233,
    
    // Défenseurs  
    'CJEganRiley': 28575687,
    'LeonardoBalerdi': 13171199,
    'UlissesGarcia': 32390,
    'DerekCornelius': 586846,
    'BamoMeite': 37369302,
    'PolLirola': 130063,
    'FacundoMedina': 335521,
    'AmirMurillo': 512560,
    
    // Milieux
    'AngelGomes': 608285,
    'AmineHarit': 96691,
    'GeoffreyKondogbia': 95696,
    'PierreEmileHojbjerg': 1744,
    'AdrienRabiot': 95694,
    'BilalNadir': 37541144,
    'AzzedineOunahi': 21803033,
    'DarrylBakola': 37737405,
    
    // Attaquants
    'NealMaupay': 95776,
    'AmineGouiri': 433458,
    'MasonGreenwood': 20333643,
    'IgorPaixao': 29328428,
    'JonathanRowe': 34455209,
    'TimothyWeah': 537332,
    'FrancoisMughe': 37657133,
    'PierreEmerickAubameyang': 31739,
    'FarisMoumbagna': 20315925
  };
}

/**
 * Récupère les statistiques de tous les joueurs de l'OM
 */
export async function getAllOMPlayersStatistics(): Promise<Map<string, PlayerStatsResponse>> {
  const playerIds = getOMPlayerIds();
  const results = new Map<string, PlayerStatsResponse>();
  
  for (const [playerSlug, playerId] of Object.entries(playerIds)) {
    const stats = await getPlayerStatistics(playerId, 'ligue1');
    results.set(playerSlug, stats);
    
    // Attendre un peu entre chaque requête pour éviter de surcharger l'API
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  return results;
}