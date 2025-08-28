// Service pour l'API SportMonks
import { LIGUE1_PLAYER_IDS } from './allPlayerIds';
import { LIGUE1_PLAYER_POSITIONS } from './playerPositions';
import { ligue1PlayersRealStats } from '@/data/ligue1PlayersCompleteStats';
import { premierleaguePlayersRealStats } from '@/data/premier-leaguePlayersCompleteStats';
import { ligaPlayersRealStats } from '@/data/la-ligaPlayersCompleteStats';
import { serieaPlayersRealStats } from '@/data/serie-aPlayersCompleteStats';
import { bundesligaPlayersRealStats } from '@/data/bundesligaPlayersCompleteStats';

const API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2';
const BASE_URL = 'https://api.sportmonks.com/v3/football';

// Mapping des championnats aux données
const LEAGUE_DATA_MAP: { [key: string]: any } = {
  'ligue1': ligue1PlayersRealStats,
  'premier-league': premierleaguePlayersRealStats,
  'la-liga': ligaPlayersRealStats,
  'serie-a': serieaPlayersRealStats,
  'bundesliga': bundesligaPlayersRealStats
};

// IDs des saisons actuelles (2025/2026)
export const CURRENT_SEASONS = {
  ligue1: 25651,
  premierLeague: 25583,
  liga: 25659,
  serieA: 25533,
  bundesliga: 25646
};

// IDs des saisons précédentes (2024/2025, 2023/2024)
export const PREVIOUS_SEASONS = {
  ligue1: [23643, 21779], // 2024/25, 2023/24
  premierLeague: [23614, 21646], // 2024/25, 2023/24
  liga: [23621, 21694], // 2024/25, 2023/24
  serieA: [23746, 21818], // 2024/25, 2023/24
  bundesliga: [23744, 21795] // 2024/25, 2023/24
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
  
  // Passes
  passes?: number;
  passes_total?: number;
  passes_completed?: number;
  passes_accuracy?: number;
  key_passes?: number;
  crosses?: number;
  crosses_total?: number;
  crosses_accurate?: number;
  crosses_accuracy?: number;
  
  // Défense
  tackles?: number;
  interceptions?: number;
  blocks?: number;
  clearances?: number;
  
  // Discipline
  fouls?: number;
  fouls_drawn?: number;
  yellow_cards?: number;
  yellowred_cards?: number;
  red_cards?: number;
  
  // Duels et dribbles
  duels?: number;
  duels_won?: number;
  ground_duels?: number;
  ground_duels_won?: number;
  aerial_duels?: number;
  aerial_duels_won?: number;
  dribbles?: number;
  dribbles_succeeded?: number;
  dribbles_successful?: number;
  
  // Gardien
  saves?: number;
  inside_box_saves?: number;
  punches?: number;
  goals_conceded?: number;
  clean_sheets?: number;
  penalties_saved?: number;
  
  // XG et XA 
  xg?: number;
  xa?: number;
}

export interface PlayerStatsResponse {
  current: PlayerStatistics | null;
  previous: PlayerStatistics[];
  cumulative: PlayerStatistics | null;
  error?: string;
}

// Fonction pour obtenir les données d'un joueur depuis n'importe quelle ligue
function getPlayerDataFromAllLeagues(playerId: number | string): any {
  const id = String(playerId);
  
  // Chercher dans toutes les ligues
  for (const leagueData of Object.values(LEAGUE_DATA_MAP)) {
    if (leagueData[id]) {
      return leagueData[id];
    }
  }
  
  return null;
}

// Fonction pour obtenir les données d'un joueur depuis une ligue spécifique
function getPlayerDataFromLeague(playerId: number | string, league: string): any {
  const id = String(playerId);
  const leagueKey = league.toLowerCase().replace(' ', '-');
  
  if (LEAGUE_DATA_MAP[leagueKey] && LEAGUE_DATA_MAP[leagueKey][id]) {
    return LEAGUE_DATA_MAP[leagueKey][id];
  }
  
  // Fallback: chercher dans toutes les ligues
  return getPlayerDataFromAllLeagues(id);
}

/**
 * Récupère les statistiques d'un joueur pour la saison en cours et les saisons précédentes
 */
export async function getPlayerStatistics(
  playerId: number,
  league: keyof typeof CURRENT_SEASONS
): Promise<PlayerStatsResponse> {
  // Chercher le joueur dans les données complètes
  const playerData = getPlayerDataFromAllLeagues(playerId);
  
  if (playerData && playerData.stats) {
    // Convertir les stats réelles au format attendu
    // Chercher les stats par année (peu importe le club/ligue)
    const findStatsBySeason = (year: string) => {
      for (const key in playerData.stats) {
        if (key.startsWith(year)) {
          return playerData.stats[key];
        }
      }
      return null;
    };
    
    let current = findStatsBySeason('2025/2026');
    const prev1 = findStatsBySeason('2024/2025');
    const prev2 = findStatsBySeason('2023/2024');
    
    // Si pas de stats pour la saison en cours mais que le joueur fait partie de l'équipe
    // Créer des stats à 0 (il n'a pas encore joué)
    if (!current && playerData.jersey) {
      current = {
        appearences: 0,
        minutes: 0,
        lineups: 0,
        captain: 0,
        rating: null,
        touches: 0,
        goals: 0,
        assists: 0,
        xg: null,
        xa: null,
        shots: 0,
        shots_on_target: 0,
        hit_woodwork: 0,
        passes: 0,
        passes_completed: 0,
        passes_accuracy: null,
        key_passes: 0,
        crosses: 0,
        crosses_accurate: 0,
        tackles: 0,
        blocks: 0,
        interceptions: 0,
        clearances: 0,
        fouls: 0,
        fouls_drawn: 0,
        yellow_cards: 0,
        red_cards: 0,
        yellowred_cards: 0,
        ground_duels: 0,
        ground_duels_won: 0,
        aerial_duels: 0,
        aerial_duels_won: 0,
        duels: 0,
        duels_won: 0,
        dribbles: 0,
        dribbles_successful: 0,
        penalties: 0,
        penalties_won: 0,
        penalties_scored: 0,
        penalties_missed: 0,
        penalties_committed: 0,
        offsides: 0,
        ball_losses: 0,
        ball_recoveries: 0,
        mistakes_leading_to_goals: 0,
        saves: 0,
        penalties_saved: 0,
        punches: 0,
        inside_box_saves: 0,
        goals_conceded: 0,
        clean_sheets: 0
      };
    }
    
    // Créer les objets de stats avec le bon format
    const currentStats: PlayerStatistics | null = current ? {
      season_name: 'Saison 2025/2026',
      minutes: current.minutes ?? 0,
      appearences: current.appearences ?? 0,
      lineups: current.lineups ?? 0,
      captain: current.captain ?? 0,
      rating: current.rating,
      touches: current.touches ?? 0,
      
      goals: current.goals ?? 0,
      assists: current.assists ?? 0,
      expected_goals: current.xg ?? 0,
      expected_assists: current.xa ?? 0,
      shots: current.shots ?? 0,
      shots_on_target: current.shots_on_target ?? 0,
      penalties: (current.penalties_won ?? current.penalties) ?? 0,
      penalties_scored: current.penalties_scored ?? 0,
      penalties_missed: current.penalties_missed ?? 0,
      hit_woodwork: current.hit_woodwork ?? 0,
      offsides: current.offsides ?? 0,
      
      passes: current.passes ?? 0,
      passes_total: current.passes ?? 0,
      passes_completed: current.passes_completed ?? 0,
      passes_accuracy: current.passes_accuracy,
      key_passes: current.key_passes ?? 0,
      crosses: current.crosses ?? 0,
      crosses_total: current.crosses ?? 0,
      crosses_accurate: current.crosses_accurate ?? 0,
      crosses_accuracy: current.crosses_accurate && current.crosses ? ((current.crosses_accurate / current.crosses) * 100) : undefined,
      dribbles: current.dribbles ?? 0,
      dribbles_succeeded: current.dribbles_successful ?? 0,
      dribbles_successful: current.dribbles_successful ?? 0,
      
      tackles: current.tackles ?? 0,
      interceptions: current.interceptions ?? 0,
      blocks: current.blocks ?? 0,
      clearances: current.clearances ?? 0,
      duels: current.duels ?? 0,
      duels_won: current.duels_won ?? 0,
      ground_duels: current.ground_duels ?? 0,
      ground_duels_won: current.ground_duels_won ?? 0,
      aerial_duels: current.aerial_duels ?? 0,
      aerial_duels_won: current.aerial_duels_won ?? 0,
      
      fouls: current.fouls ?? 0,
      fouls_drawn: current.fouls_drawn ?? 0,
      yellow_cards: current.yellow_cards ?? 0,
      yellowred_cards: current.yellowred_cards ?? 0,
      red_cards: current.red_cards ?? 0,
      
      ball_losses: current.ball_losses ?? 0,
      ball_recoveries: current.ball_recoveries ?? 0,
      
      // Stats gardien
      saves: current.saves ?? 0,
      inside_box_saves: current.inside_box_saves ?? 0,
      punches: current.punches ?? 0,
      goals_conceded: current.goals_conceded ?? 0,
      clean_sheets: current.clean_sheets ?? 0,
      penalties_saved: current.penalties_saved ?? 0,
      
      xg: current.xg,
      xa: current.xa
    } as PlayerStatistics : null;
    
    // Stats des saisons précédentes
    const previousStats: PlayerStatistics[] = [];
    
    if (prev1) {
      previousStats.push({
        season_name: 'Saison 2024/2025',
        minutes: prev1.minutes ?? 0,
        appearences: prev1.appearences ?? 0,
        lineups: prev1.lineups ?? 0,
        captain: prev1.captain ?? 0,
        rating: prev1.rating,
        touches: prev1.touches ?? 0,
        goals: prev1.goals ?? 0,
        assists: prev1.assists ?? 0,
        expected_goals: prev1.xg ?? 0,
        expected_assists: prev1.xa ?? 0,
        shots: prev1.shots ?? 0,
        shots_on_target: prev1.shots_on_target ?? 0,
        penalties: (prev1.penalties_won ?? prev1.penalties) ?? 0,
        penalties_scored: prev1.penalties_scored ?? 0,
        penalties_missed: prev1.penalties_missed ?? 0,
        hit_woodwork: prev1.hit_woodwork ?? 0,
        offsides: prev1.offsides ?? 0,
        passes: prev1.passes ?? 0,
        passes_total: prev1.passes ?? 0,
        passes_completed: prev1.passes_completed ?? 0,
        passes_accuracy: prev1.passes_accuracy,
        key_passes: prev1.key_passes ?? 0,
        crosses: prev1.crosses ?? 0,
        crosses_total: prev1.crosses ?? 0,
        crosses_accurate: prev1.crosses_accurate ?? 0,
        crosses_accuracy: prev1.crosses_accurate && prev1.crosses ? ((prev1.crosses_accurate / prev1.crosses) * 100) : undefined,
        dribbles: prev1.dribbles ?? 0,
        dribbles_succeeded: prev1.dribbles_successful ?? 0,
        dribbles_successful: prev1.dribbles_successful ?? 0,
        tackles: prev1.tackles ?? 0,
        interceptions: prev1.interceptions ?? 0,
        blocks: prev1.blocks ?? 0,
        clearances: prev1.clearances ?? 0,
        duels: prev1.duels ?? 0,
        duels_won: prev1.duels_won ?? 0,
        ground_duels: prev1.ground_duels ?? 0,
        ground_duels_won: prev1.ground_duels_won ?? 0,
        aerial_duels: prev1.aerial_duels ?? 0,
        aerial_duels_won: prev1.aerial_duels_won ?? 0,
        fouls: prev1.fouls ?? 0,
        fouls_drawn: prev1.fouls_drawn ?? 0,
        yellow_cards: prev1.yellow_cards ?? 0,
        yellowred_cards: prev1.yellowred_cards ?? 0,
        red_cards: prev1.red_cards ?? 0,
        ball_losses: prev1.ball_losses ?? 0,
        ball_recoveries: prev1.ball_recoveries ?? 0,
        saves: prev1.saves ?? 0,
        inside_box_saves: prev1.inside_box_saves ?? 0,
        punches: prev1.punches ?? 0,
        goals_conceded: prev1.goals_conceded ?? 0,
        clean_sheets: prev1.clean_sheets ?? 0,
        penalties_saved: prev1.penalties_saved ?? 0,
        xg: prev1.xg,
        xa: prev1.xa
      } as PlayerStatistics);
    }
    
    if (prev2) {
      previousStats.push({
        season_name: 'Saison 2023/2024',
        minutes: prev2.minutes ?? 0,
        appearences: prev2.appearences ?? 0,
        lineups: prev2.lineups ?? 0,
        captain: prev2.captain ?? 0,
        rating: prev2.rating,
        touches: prev2.touches ?? 0,
        goals: prev2.goals ?? 0,
        assists: prev2.assists ?? 0,
        expected_goals: prev2.xg ?? 0,
        expected_assists: prev2.xa ?? 0,
        shots: prev2.shots ?? 0,
        shots_on_target: prev2.shots_on_target ?? 0,
        penalties: (prev2.penalties_won ?? prev2.penalties) ?? 0,
        penalties_scored: prev2.penalties_scored ?? 0,
        penalties_missed: prev2.penalties_missed ?? 0,
        hit_woodwork: prev2.hit_woodwork ?? 0,
        offsides: prev2.offsides ?? 0,
        passes: prev2.passes ?? 0,
        passes_total: prev2.passes ?? 0,
        passes_completed: prev2.passes_completed ?? 0,
        passes_accuracy: prev2.passes_accuracy,
        key_passes: prev2.key_passes ?? 0,
        crosses: prev2.crosses ?? 0,
        crosses_total: prev2.crosses ?? 0,
        crosses_accurate: prev2.crosses_accurate ?? 0,
        crosses_accuracy: prev2.crosses_accurate && prev2.crosses ? ((prev2.crosses_accurate / prev2.crosses) * 100) : undefined,
        dribbles: prev2.dribbles ?? 0,
        dribbles_succeeded: prev2.dribbles_successful ?? 0,
        dribbles_successful: prev2.dribbles_successful ?? 0,
        tackles: prev2.tackles ?? 0,
        interceptions: prev2.interceptions ?? 0,
        blocks: prev2.blocks ?? 0,
        clearances: prev2.clearances ?? 0,
        duels: prev2.duels ?? 0,
        duels_won: prev2.duels_won ?? 0,
        ground_duels: prev2.ground_duels ?? 0,
        ground_duels_won: prev2.ground_duels_won ?? 0,
        aerial_duels: prev2.aerial_duels ?? 0,
        aerial_duels_won: prev2.aerial_duels_won ?? 0,
        fouls: prev2.fouls ?? 0,
        fouls_drawn: prev2.fouls_drawn ?? 0,
        yellow_cards: prev2.yellow_cards ?? 0,
        yellowred_cards: prev2.yellowred_cards ?? 0,
        red_cards: prev2.red_cards ?? 0,
        ball_losses: prev2.ball_losses ?? 0,
        ball_recoveries: prev2.ball_recoveries ?? 0,
        saves: prev2.saves ?? 0,
        inside_box_saves: prev2.inside_box_saves ?? 0,
        punches: prev2.punches ?? 0,
        goals_conceded: prev2.goals_conceded ?? 0,
        clean_sheets: prev2.clean_sheets ?? 0,
        penalties_saved: prev2.penalties_saved ?? 0,
        xg: prev2.xg,
        xa: prev2.xa
      } as PlayerStatistics);
    }
    
    // Calculer les stats cumulées
    const allSeasons = [current, prev1, prev2].filter(s => s !== null);
    
    // Calculer la moyenne du rating (seulement les saisons où le rating existe)
    const ratingsWithValues = allSeasons.filter(s => s?.rating && s.rating > 0);
    const averageRating = ratingsWithValues.length > 0 
      ? ratingsWithValues.reduce((sum, s) => sum + (s?.rating ?? 0), 0) / ratingsWithValues.length 
      : undefined;
    
    // Calculer la précision des passes moyenne pondérée par le nombre de passes
    const totalPassesCompleted = allSeasons.reduce((sum, s) => sum + (s?.passes_completed ?? 0), 0);
    const totalPasses = allSeasons.reduce((sum, s) => sum + (s?.passes ?? 0), 0);
    const averagePassAccuracy = totalPasses > 0 
      ? (totalPassesCompleted / totalPasses) * 100 
      : undefined;
    
    const cumulative: PlayerStatistics | null = allSeasons.length > 0 ? {
      season_name: 'Toutes saisons',
      minutes: allSeasons.reduce((sum, s) => sum + (s?.minutes ?? 0), 0),
      appearences: allSeasons.reduce((sum, s) => sum + (s?.appearences ?? 0), 0),
      lineups: allSeasons.reduce((sum, s) => sum + (s?.lineups ?? 0), 0),
      captain: allSeasons.reduce((sum, s) => sum + (s?.captain ?? 0), 0),
      rating: averageRating,
      touches: allSeasons.reduce((sum, s) => sum + (s?.touches ?? 0), 0),
      goals: allSeasons.reduce((sum, s) => sum + (s?.goals ?? 0), 0),
      assists: allSeasons.reduce((sum, s) => sum + (s?.assists ?? 0), 0),
      expected_goals: allSeasons.reduce((sum, s) => sum + (s?.xg ?? 0), 0),
      expected_assists: allSeasons.reduce((sum, s) => sum + (s?.xa ?? 0), 0),
      shots: allSeasons.reduce((sum, s) => sum + (s?.shots ?? 0), 0),
      shots_on_target: allSeasons.reduce((sum, s) => sum + (s?.shots_on_target ?? 0), 0),
      penalties: allSeasons.reduce((sum, s) => sum + ((s?.penalties_won ?? s?.penalties) ?? 0), 0),
      penalties_scored: allSeasons.reduce((sum, s) => sum + (s?.penalties_scored ?? 0), 0),
      penalties_missed: allSeasons.reduce((sum, s) => sum + (s?.penalties_missed ?? 0), 0),
      hit_woodwork: allSeasons.reduce((sum, s) => sum + (s?.hit_woodwork ?? 0), 0),
      offsides: allSeasons.reduce((sum, s) => sum + (s?.offsides ?? 0), 0),
      passes: allSeasons.reduce((sum, s) => sum + (s?.passes ?? 0), 0),
      passes_total: allSeasons.reduce((sum, s) => sum + (s?.passes ?? 0), 0),
      passes_completed: allSeasons.reduce((sum, s) => sum + (s?.passes_completed ?? 0), 0),
      passes_accuracy: averagePassAccuracy,
      key_passes: allSeasons.reduce((sum, s) => sum + (s?.key_passes ?? 0), 0),
      crosses: allSeasons.reduce((sum, s) => sum + (s?.crosses ?? 0), 0),
      crosses_total: allSeasons.reduce((sum, s) => sum + (s?.crosses ?? 0), 0),
      crosses_accurate: allSeasons.reduce((sum, s) => sum + (s?.crosses_accurate ?? 0), 0),
      dribbles: allSeasons.reduce((sum, s) => sum + (s?.dribbles ?? 0), 0),
      dribbles_succeeded: allSeasons.reduce((sum, s) => sum + (s?.dribbles_successful ?? 0), 0),
      dribbles_successful: allSeasons.reduce((sum, s) => sum + (s?.dribbles_successful ?? 0), 0),
      tackles: allSeasons.reduce((sum, s) => sum + (s?.tackles ?? 0), 0),
      interceptions: allSeasons.reduce((sum, s) => sum + (s?.interceptions ?? 0), 0),
      blocks: allSeasons.reduce((sum, s) => sum + (s?.blocks ?? 0), 0),
      clearances: allSeasons.reduce((sum, s) => sum + (s?.clearances ?? 0), 0),
      duels: allSeasons.reduce((sum, s) => sum + (s?.duels ?? 0), 0),
      duels_won: allSeasons.reduce((sum, s) => sum + (s?.duels_won ?? 0), 0),
      ground_duels: allSeasons.reduce((sum, s) => sum + (s?.ground_duels ?? 0), 0),
      ground_duels_won: allSeasons.reduce((sum, s) => sum + (s?.ground_duels_won ?? 0), 0),
      aerial_duels: allSeasons.reduce((sum, s) => sum + (s?.aerial_duels ?? 0), 0),
      aerial_duels_won: allSeasons.reduce((sum, s) => sum + (s?.aerial_duels_won ?? 0), 0),
      fouls: allSeasons.reduce((sum, s) => sum + (s?.fouls ?? 0), 0),
      fouls_drawn: allSeasons.reduce((sum, s) => sum + (s?.fouls_drawn ?? 0), 0),
      yellow_cards: allSeasons.reduce((sum, s) => sum + (s?.yellow_cards ?? 0), 0),
      yellowred_cards: allSeasons.reduce((sum, s) => sum + (s?.yellowred_cards ?? 0), 0),
      red_cards: allSeasons.reduce((sum, s) => sum + (s?.red_cards ?? 0), 0),
      ball_losses: allSeasons.reduce((sum, s) => sum + (s?.ball_losses ?? 0), 0),
      ball_recoveries: allSeasons.reduce((sum, s) => sum + (s?.ball_recoveries ?? 0), 0),
      saves: allSeasons.reduce((sum, s) => sum + (s?.saves ?? 0), 0),
      inside_box_saves: allSeasons.reduce((sum, s) => sum + (s?.inside_box_saves ?? 0), 0),
      punches: allSeasons.reduce((sum, s) => sum + (s?.punches ?? 0), 0),
      goals_conceded: allSeasons.reduce((sum, s) => sum + (s?.goals_conceded ?? 0), 0),
      clean_sheets: allSeasons.reduce((sum, s) => sum + (s?.clean_sheets ?? 0), 0),
      penalties_saved: allSeasons.reduce((sum, s) => sum + (s?.penalties_saved ?? 0), 0),
      xg: allSeasons.reduce((sum, s) => sum + (s?.xg ?? 0), 0),
      xa: allSeasons.reduce((sum, s) => sum + (s?.xa ?? 0), 0)
    } : null;
    
    return {
      current: currentStats,
      previous: previousStats,
      cumulative,
    };
  }
  
  // Si pas de données locales, retourner les données simulées
  return generateMockStats(playerId, league);
}

/**
 * Calcule les statistiques cumulatives pour plusieurs saisons
 */
export function calculateCumulativeStats(seasons: PlayerStatistics[]): PlayerStatistics | null {
  if (!seasons || seasons.length === 0) return null;
  
  // Calculer la moyenne du rating (seulement les saisons où le rating existe)
  const ratingsWithValues = seasons.filter(s => s?.rating && s.rating > 0);
  const averageRating = ratingsWithValues.length > 0 
    ? ratingsWithValues.reduce((sum, s) => sum + (s?.rating ?? 0), 0) / ratingsWithValues.length 
    : undefined;
  
  // Calculer la précision des passes moyenne pondérée par le nombre de passes
  const totalPassesCompleted = seasons.reduce((sum, s) => sum + (s?.passes_completed ?? 0), 0);
  const totalPasses = seasons.reduce((sum, s) => sum + (s?.passes ?? 0), 0);
  const averagePassAccuracy = totalPasses > 0 
    ? (totalPassesCompleted / totalPasses) * 100 
    : undefined;
  
  return {
    season_name: 'Total des 3 dernières saisons',
    minutes: seasons.reduce((sum, s) => sum + (s?.minutes ?? 0), 0),
    appearences: seasons.reduce((sum, s) => sum + (s?.appearences ?? 0), 0),
    lineups: seasons.reduce((sum, s) => sum + (s?.lineups ?? 0), 0),
    captain: seasons.reduce((sum, s) => sum + (s?.captain ?? 0), 0),
    rating: averageRating,
    touches: seasons.reduce((sum, s) => sum + (s?.touches ?? 0), 0),
    goals: seasons.reduce((sum, s) => sum + (s?.goals ?? 0), 0),
    assists: seasons.reduce((sum, s) => sum + (s?.assists ?? 0), 0),
    expected_goals: seasons.reduce((sum, s) => sum + (s?.expected_goals ?? 0), 0),
    expected_assists: seasons.reduce((sum, s) => sum + (s?.expected_assists ?? 0), 0),
    shots: seasons.reduce((sum, s) => sum + (s?.shots ?? 0), 0),
    shots_on_target: seasons.reduce((sum, s) => sum + (s?.shots_on_target ?? 0), 0),
    penalties: seasons.reduce((sum, s) => sum + (s?.penalties ?? 0), 0),
    penalties_scored: seasons.reduce((sum, s) => sum + (s?.penalties_scored ?? 0), 0),
    penalties_missed: seasons.reduce((sum, s) => sum + (s?.penalties_missed ?? 0), 0),
    hit_woodwork: seasons.reduce((sum, s) => sum + (s?.hit_woodwork ?? 0), 0),
    offsides: seasons.reduce((sum, s) => sum + (s?.offsides ?? 0), 0),
    passes: seasons.reduce((sum, s) => sum + (s?.passes ?? 0), 0),
    passes_total: seasons.reduce((sum, s) => sum + (s?.passes_total ?? 0), 0),
    passes_completed: totalPassesCompleted,
    passes_accuracy: averagePassAccuracy,
    key_passes: seasons.reduce((sum, s) => sum + (s?.key_passes ?? 0), 0),
    crosses: seasons.reduce((sum, s) => sum + (s?.crosses ?? 0), 0),
    crosses_total: seasons.reduce((sum, s) => sum + (s?.crosses_total ?? 0), 0),
    crosses_accurate: seasons.reduce((sum, s) => sum + (s?.crosses_accurate ?? 0), 0),
    dribbles: seasons.reduce((sum, s) => sum + (s?.dribbles ?? 0), 0),
    dribbles_succeeded: seasons.reduce((sum, s) => sum + (s?.dribbles_succeeded ?? 0), 0),
    dribbles_successful: seasons.reduce((sum, s) => sum + (s?.dribbles_successful ?? 0), 0),
    tackles: seasons.reduce((sum, s) => sum + (s?.tackles ?? 0), 0),
    interceptions: seasons.reduce((sum, s) => sum + (s?.interceptions ?? 0), 0),
    blocks: seasons.reduce((sum, s) => sum + (s?.blocks ?? 0), 0),
    clearances: seasons.reduce((sum, s) => sum + (s?.clearances ?? 0), 0),
    duels: seasons.reduce((sum, s) => sum + (s?.duels ?? 0), 0),
    duels_won: seasons.reduce((sum, s) => sum + (s?.duels_won ?? 0), 0),
    ground_duels: seasons.reduce((sum, s) => sum + (s?.ground_duels ?? 0), 0),
    ground_duels_won: seasons.reduce((sum, s) => sum + (s?.ground_duels_won ?? 0), 0),
    aerial_duels: seasons.reduce((sum, s) => sum + (s?.aerial_duels ?? 0), 0),
    aerial_duels_won: seasons.reduce((sum, s) => sum + (s?.aerial_duels_won ?? 0), 0),
    fouls: seasons.reduce((sum, s) => sum + (s?.fouls ?? 0), 0),
    fouls_drawn: seasons.reduce((sum, s) => sum + (s?.fouls_drawn ?? 0), 0),
    yellow_cards: seasons.reduce((sum, s) => sum + (s?.yellow_cards ?? 0), 0),
    yellowred_cards: seasons.reduce((sum, s) => sum + (s?.yellowred_cards ?? 0), 0),
    red_cards: seasons.reduce((sum, s) => sum + (s?.red_cards ?? 0), 0),
    ball_losses: seasons.reduce((sum, s) => sum + (s?.ball_losses ?? 0), 0),
    ball_recoveries: seasons.reduce((sum, s) => sum + (s?.ball_recoveries ?? 0), 0),
    saves: seasons.reduce((sum, s) => sum + (s?.saves ?? 0), 0),
    inside_box_saves: seasons.reduce((sum, s) => sum + (s?.inside_box_saves ?? 0), 0),
    punches: seasons.reduce((sum, s) => sum + (s?.punches ?? 0), 0),
    goals_conceded: seasons.reduce((sum, s) => sum + (s?.goals_conceded ?? 0), 0),
    clean_sheets: seasons.reduce((sum, s) => sum + (s?.clean_sheets ?? 0), 0),
    penalties_saved: seasons.reduce((sum, s) => sum + (s?.penalties_saved ?? 0), 0),
    xg: seasons.reduce((sum, s) => sum + (s?.xg ?? 0), 0),
    xa: seasons.reduce((sum, s) => sum + (s?.xa ?? 0), 0),
  };
}

/**
 * Génère des statistiques simulées pour un joueur
 */
function generateMockStats(
  playerId: number,
  league: keyof typeof CURRENT_SEASONS
): PlayerStatsResponse {
  // Déterminer la position du joueur
  const playerIdKey = Object.keys(LIGUE1_PLAYER_IDS).find(
    key => LIGUE1_PLAYER_IDS[key as keyof typeof LIGUE1_PLAYER_IDS] === playerId
  );
  
  let position = 'MID';
  if (playerIdKey) {
    const playerKey = playerIdKey.replace(/_/g, '').toLowerCase();
    const positionEntry = Object.entries(LIGUE1_PLAYER_POSITIONS).find(
      ([key]) => key.toLowerCase() === playerKey
    );
    if (positionEntry) {
      position = positionEntry[1];
    }
  }

  // Générer des stats basées sur la position
  const isGoalkeeper = position === 'GK';
  const isDefender = position === 'DEF';
  const isAttacker = position === 'ATT';
  const isMidfielder = position === 'MID';

  const baseStats = {
    minutes: Math.floor(Math.random() * 2000) + 500,
    appearences: Math.floor(Math.random() * 25) + 5,
    lineups: Math.floor(Math.random() * 20) + 3,
    captain: Math.floor(Math.random() * 5),
    rating: Number((Math.random() * 2 + 6).toFixed(2)),
    touches: Math.floor(Math.random() * 1500) + 500,
  };

  const offensiveStats = {
    goals: isAttacker ? Math.floor(Math.random() * 15) : isDefender ? Math.floor(Math.random() * 3) : Math.floor(Math.random() * 8),
    assists: isMidfielder ? Math.floor(Math.random() * 10) : Math.floor(Math.random() * 5),
    expected_goals: isAttacker ? Number((Math.random() * 12).toFixed(2)) : Number((Math.random() * 5).toFixed(2)),
    expected_assists: Number((Math.random() * 8).toFixed(2)),
    shots: isAttacker ? Math.floor(Math.random() * 60) + 20 : Math.floor(Math.random() * 20),
    shots_on_target: isAttacker ? Math.floor(Math.random() * 30) + 10 : Math.floor(Math.random() * 10),
    penalties: Math.floor(Math.random() * 3),
    penalties_scored: Math.floor(Math.random() * 3),
    penalties_missed: Math.floor(Math.random() * 2),
    hit_woodwork: Math.floor(Math.random() * 3),
    offsides: isAttacker ? Math.floor(Math.random() * 20) : Math.floor(Math.random() * 5),
  };

  const passingStats = {
    passes: Math.floor(Math.random() * 1500) + 500,
    passes_total: Math.floor(Math.random() * 1500) + 500,
    passes_completed: Math.floor(Math.random() * 1200) + 400,
    passes_accuracy: Number((Math.random() * 20 + 75).toFixed(1)),
    key_passes: Math.floor(Math.random() * 40) + 10,
    crosses: Math.floor(Math.random() * 50) + 10,
    crosses_total: Math.floor(Math.random() * 50) + 10,
    crosses_accurate: Math.floor(Math.random() * 20) + 5,
    crosses_accuracy: Number((Math.random() * 30 + 20).toFixed(1)),
  };

  const defensiveStats = {
    tackles: isDefender ? Math.floor(Math.random() * 60) + 20 : Math.floor(Math.random() * 30),
    interceptions: isDefender ? Math.floor(Math.random() * 50) + 20 : Math.floor(Math.random() * 20),
    blocks: isDefender ? Math.floor(Math.random() * 30) + 10 : Math.floor(Math.random() * 10),
    clearances: isDefender ? Math.floor(Math.random() * 100) + 30 : Math.floor(Math.random() * 20),
    duels: Math.floor(Math.random() * 200) + 50,
    duels_won: Math.floor(Math.random() * 100) + 25,
    ground_duels: Math.floor(Math.random() * 150) + 30,
    ground_duels_won: Math.floor(Math.random() * 75) + 15,
    aerial_duels: isDefender ? Math.floor(Math.random() * 80) + 20 : Math.floor(Math.random() * 40),
    aerial_duels_won: isDefender ? Math.floor(Math.random() * 40) + 10 : Math.floor(Math.random() * 20),
  };

  const disciplineStats = {
    fouls: Math.floor(Math.random() * 30) + 5,
    fouls_drawn: Math.floor(Math.random() * 30) + 5,
    yellow_cards: Math.floor(Math.random() * 8),
    yellowred_cards: Math.random() > 0.9 ? 1 : 0,
    red_cards: Math.random() > 0.95 ? 1 : 0,
  };

  const dribbleStats = {
    dribbles: isAttacker ? Math.floor(Math.random() * 80) + 20 : Math.floor(Math.random() * 30),
    dribbles_succeeded: isAttacker ? Math.floor(Math.random() * 40) + 10 : Math.floor(Math.random() * 15),
    dribbles_successful: isAttacker ? Math.floor(Math.random() * 40) + 10 : Math.floor(Math.random() * 15),
  };

  const goalkeeperStats = isGoalkeeper ? {
    saves: Math.floor(Math.random() * 80) + 20,
    inside_box_saves: Math.floor(Math.random() * 60) + 15,
    punches: Math.floor(Math.random() * 20) + 5,
    goals_conceded: Math.floor(Math.random() * 40) + 10,
    clean_sheets: Math.floor(Math.random() * 10) + 2,
    penalties_saved: Math.floor(Math.random() * 3),
  } : {
    saves: 0,
    inside_box_saves: 0,
    punches: 0,
    goals_conceded: 0,
    clean_sheets: 0,
    penalties_saved: 0,
  };

  const miscStats = {
    ball_losses: Math.floor(Math.random() * 200) + 50,
    ball_recoveries: Math.floor(Math.random() * 150) + 30,
    xg: isAttacker ? Number((Math.random() * 15).toFixed(2)) : Number((Math.random() * 5).toFixed(2)),
    xa: Number((Math.random() * 10).toFixed(2)),
  };

  const currentSeasonStats: PlayerStatistics = {
    ...baseStats,
    ...offensiveStats,
    ...passingStats,
    ...defensiveStats,
    ...disciplineStats,
    ...dribbleStats,
    ...goalkeeperStats,
    ...miscStats,
  };

  // Générer des stats pour les saisons précédentes avec une variation
  const previousStats: PlayerStatistics[] = [];
  for (let i = 0; i < 2; i++) {
    const variation = 0.8 + Math.random() * 0.4; // Variation de ±20%
    const prevStats: PlayerStatistics = Object.fromEntries(
      Object.entries(currentSeasonStats).map(([key, value]) => {
        if (typeof value === 'number') {
          return [key, Math.floor(value * variation)];
        }
        return [key, value];
      })
    ) as PlayerStatistics;
    previousStats.push(prevStats);
  }

  // Calculer les stats cumulées
  const cumulative: PlayerStatistics = Object.fromEntries(
    Object.entries(currentSeasonStats).map(([key, value]) => {
      if (typeof value === 'number' && !['rating', 'passes_accuracy', 'crosses_accuracy'].includes(key)) {
        const total = value + previousStats.reduce((sum, stats) => sum + (stats[key as keyof PlayerStatistics] as number || 0), 0);
        return [key, total];
      }
      return [key, value];
    })
  ) as PlayerStatistics;

  return {
    current: currentSeasonStats,
    previous: previousStats,
    cumulative,
  };
}

export async function searchPlayers(query: string): Promise<any[]> {
  // Pour l'instant, retourner un tableau vide
  // Cette fonction pourrait être implémentée pour chercher dans les données locales
  return [];
}