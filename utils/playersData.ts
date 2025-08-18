// Gestion des données des joueurs saison 2025-2026
import playersData from '@/public/data/players_2025_26.json';

export interface Player {
  id: string;
  nom: string;
  poste: string;
  numero: number;
  age: number;
  nationalite: string;
  matchs_joues: number;
  titularisations: number;
  minutes: number;
  note_moyenne: number;
  buts: number;
  passes_decisives: number;
  xg: number;
  xa: number;
  tirs_total: number;
  tirs_cadres: number;
  penalties_marques: number;
  passes_cles: number;
  passes_reussies_pct: number;
  dribbles_reussis: number;
  centres_reussis: number;
  tacles_reussis: number;
  interceptions: number;
  duels_aeriens_gagnes: number;
  cleansheets: number;
  cartons_jaunes: number;
  cartons_rouges: number;
  last_update: string;
}

export interface TeamData {
  [playerName: string]: Player[];
}

export interface LeagueData {
  [teamName: string]: Player[];
}

export interface AllPlayersData {
  season: string;
  last_update: string;
  total_clubs: number;
  total_players: number;
  leagues: {
    [leagueName: string]: LeagueData;
  };
}

// Fonction pour obtenir les joueurs d'un club
export function getTeamPlayers(league: string, team: string): Player[] {
  const data = playersData as AllPlayersData;
  
  // Normaliser les noms pour la correspondance
  const normalizedLeague = league.toLowerCase();
  const normalizedTeam = team.toLowerCase();
  
  if (data.leagues[normalizedLeague] && data.leagues[normalizedLeague][normalizedTeam]) {
    return data.leagues[normalizedLeague][normalizedTeam];
  }
  
  return [];
}

// Fonction pour obtenir un joueur spécifique
export function getPlayer(league: string, team: string, playerId: string): Player | null {
  const players = getTeamPlayers(league, team);
  return players.find(p => p.id === playerId) || null;
}

// Fonction pour obtenir tous les clubs d'une ligue
export function getLeagueTeams(league: string): string[] {
  const data = playersData as AllPlayersData;
  const normalizedLeague = league.toLowerCase();
  
  if (data.leagues[normalizedLeague]) {
    return Object.keys(data.leagues[normalizedLeague]);
  }
  
  return [];
}

// Stats pour les radar charts
export function getPlayerRadarStats(player: Player) {
  return {
    // Radar 1: Stats générales
    general: {
      'Buts': player.buts,
      'Passes D.': player.passes_decisives,
      'Minutes': Math.round(player.minutes / 100), // Scaled down
      'Note': player.note_moyenne * 10, // Sur 100
      'Matchs': player.matchs_joues,
      'Titularisations': player.titularisations
    },
    
    // Radar 2: Stats offensives
    offensive: {
      'Buts': player.buts,
      'xG': player.xg,
      'Tirs': player.tirs_total,
      'Tirs cadrés': player.tirs_cadres,
      'Penalties': player.penalties_marques,
      'Dribbles': player.dribbles_reussis
    },
    
    // Radar 3: Stats créatives
    creative: {
      'Passes D.': player.passes_decisives,
      'xA': player.xa,
      'Passes clés': player.passes_cles,
      'Passes %': player.passes_reussies_pct,
      'Centres': player.centres_reussis,
      'Dribbles': player.dribbles_reussis
    },
    
    // Radar 4: Stats défensives
    defensive: {
      'Tacles': player.tacles_reussis,
      'Interceptions': player.interceptions,
      'Duels aériens': player.duels_aeriens_gagnes,
      'Clean sheets': player.cleansheets,
      'Cartons J': player.cartons_jaunes,
      'Cartons R': player.cartons_rouges
    }
  };
}