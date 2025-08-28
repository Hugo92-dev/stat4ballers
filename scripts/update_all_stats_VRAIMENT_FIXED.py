#!/usr/bin/env python3
"""Script de mise à jour avec le VRAI mapping SportMonks"""

import json
import requests
import time
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os
import logging

# Configuration
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# Championnats et saisons
LEAGUES = {
    'Ligue 1': {
        'teams': [
            (591, "Paris Saint Germain"), (614, "Monaco"), (44, "Olympique Marseille"),
            (77, "Lille"), (69, "Rennes"), (79, "Nice"), (74, "Lens"), (75, "Lyon"),
            (107, "Toulouse"), (81, "Reims"), (82, "Montpellier"), (84, "Nantes"),
            (108, "Strasbourg"), (106, "Brest"), (112, "Havre"), (110, "Angers SCO"),
            (111, "Auxerre"), (3062, "Saint-Étienne")
        ],
        'seasons': {25651: "2025/2026", 23643: "2024/2025", 21779: "2023/2024"}
    },
    'Premier League': {
        'teams': [
            (34, "Newcastle United"), (18, "Chelsea"), (14, "Manchester United"),
            (11, "Arsenal"), (26, "Liverpool"), (10, "Manchester City"),
            (6, "Tottenham Hotspur"), (27, "Aston Villa"), (24, "Brighton & Hove Albion"),
            (17, "Southampton"), (5, "Fulham"), (15, "Everton"), (16, "Nottingham Forest"),
            (29, "Wolverhampton Wanderers"), (28, "Leicester City"), (22, "West Ham United"),
            (23, "Crystal Palace"), (31, "Bournemouth"), (30, "Brentford"),
            (13, "Ipswich Town")
        ],
        'seasons': {25583: "2025/2026", 23601: "2024/2025", 21646: "2023/2024"}
    },
    'Liga': {
        'teams': [
            (3468, "Real Madrid"), (529, "Barcelona"), (554, "Atletico Madrid"),
            (540, "Sevilla"), (538, "Villarreal"), (541, "Real Sociedad"),
            (715, "Athletic Bilbao"), (712, "Real Betis"), (543, "Valencia"),
            (724, "Getafe"), (728, "Rayo Vallecano"), (720, "Celta Vigo"),
            (727, "Osasuna"), (714, "Girona"), (725, "Las Palmas"),
            (546, "Mallorca"), (713, "Deportivo Alavés"), (4003, "Real Valladolid"),
            (721, "Espanyol"), (3752, "Leganés")
        ],
        'seasons': {25659: "2025/2026", 23621: "2024/2025", 21694: "2023/2024"}
    },
    'Serie A': {
        'teams': [
            (496, "Juventus"), (505, "Inter"), (503, "Milan"),
            (502, "Lazio"), (497, "Roma"), (500, "Napoli"),
            (499, "Atalanta"), (506, "Fiorentina"), (507, "Bologna"),
            (1653, "Udinese"), (510, "Torino"), (520, "Empoli"),
            (8636, "Monza"), (867, "Genoa"), (523, "Cagliari"),
            (489, "Hellas Verona"), (738, "Parma"), (8197, "Como"),
            (1003, "Lecce"), (8907, "Venezia")
        ],
        'seasons': {25533: "2025/2026", 23648: "2024/2025", 21768: "2023/2024"}
    },
    'Bundesliga': {
        'teams': [
            (95, "Bayern Munich"), (68, "Borussia Dortmund"), (93, "Bayer 04 Leverkusen"),
            (63, "RasenBallsport Leipzig"), (366, "Eintracht Frankfurt"), (510, "VfL Wolfsburg"),
            (91, "SC Freiburg"), (101, "VfB Stuttgart"), (225, "1. FSV Mainz 05"),
            (369, "TSG 1899 Hoffenheim"), (113, "FC Augsburg"), (86, "SV Werder Bremen"),
            (65, "Borussia Mönchengladbach"), (606, "1. FC Union Berlin"), (125, "VfL Bochum"),
            (80, "1. FC Köln"), (2394, "1. FC Heidenheim"), (390, "FC St. Pauli")
        ],
        'seasons': {25660: "2025/2026", 23622: "2024/2025", 21695: "2023/2024"}
    }
}

# Cache pour les noms d'équipes
TEAM_NAMES = {}

def get_team_name(team_id):
    """Récupère le nom de l'équipe depuis le cache"""
    if team_id in TEAM_NAMES:
        return TEAM_NAMES[team_id]
    return f"Team_{team_id}"

def process_player_stats(season_data, league_name):
    """Process les stats d'un joueur avec le MAPPING CORRECT"""
    
    # Initialiser toutes les stats
    stats = {
        'team': None,
        'team_id': None,
        'league': league_name,
        'rating': None,
        'minutes': None,
        'appearences': None,
        'lineups': None,
        'captain': 0,
        'substitutions': None,
        'touches': None,
        'goals': None,
        'assists': None,
        'xg': None,
        'xa': None,
        'shots': None,
        'shots_on_target': None,
        'penalties_won': None,
        'penalties': None,
        'penalties_scored': None,
        'penalties_missed': None,
        'hit_woodwork': None,
        'offsides': None,
        'passes': None,
        'passes_completed': None,
        'passes_accuracy': None,
        'key_passes': None,
        'crosses': None,
        'crosses_accurate': None,
        'dribbles': None,
        'dribbles_successful': None,
        'tackles': None,
        'blocks': None,
        'interceptions': None,
        'clearances': None,
        'ground_duels': None,
        'ground_duels_won': None,
        'aerial_duels': None,
        'aerial_duels_won': None,
        'fouls': None,
        'fouls_drawn': None,
        'yellow_cards': None,
        'red_cards': None,
        'yellowred_cards': None,
        'penalties_committed': None,
        'ball_losses': None,
        'ball_recoveries': None,
        'mistakes_leading_to_goals': None,
        'saves': None,
        'punches': None,
        'inside_box_saves': None,
        'clean_sheets': None,
        'goals_conceded': None,
        'penalties_saved': None,
        'crosses_accuracy': None
    }
    
    # Récupérer team_id
    team_id = season_data.get('team_id')
    if team_id:
        stats['team_id'] = team_id
        stats['team'] = get_team_name(team_id)
    
    # MAPPING CORRECT BASÉ SUR L'API RÉELLE
    if 'details' in season_data:
        for detail in season_data['details']:
            type_data = detail.get('type')
            if not isinstance(type_data, dict):
                continue
                
            type_id = type_data.get('id')
            value = detail.get('value', {})
            
            # Extraire la vraie valeur
            if isinstance(value, dict):
                actual_value = value.get('total', value.get('average'))
            else:
                actual_value = value
            
            # MAPPING CORRECT VÉRIFIÉ
            # Général
            if type_id == 321:
                stats['appearences'] = actual_value
            elif type_id == 322:
                stats['lineups'] = actual_value
            elif type_id == 323:
                stats['substitutions'] = actual_value
            elif type_id == 119:
                stats['minutes'] = actual_value
            elif type_id == 118:
                stats['rating'] = actual_value
            elif type_id == 40:
                stats['captain'] = actual_value
                
            # Offensif
            elif type_id == 52:
                stats['goals'] = actual_value
            elif type_id == 79:  # CORRECT: Assists
                stats['assists'] = actual_value
            elif type_id == 42:
                stats['shots'] = actual_value
            elif type_id == 86:  # CORRECT: Shots on target
                stats['shots_on_target'] = actual_value
            elif type_id == 64:  # CORRECT: Hit woodwork
                stats['hit_woodwork'] = actual_value
            elif type_id == 51:
                stats['offsides'] = actual_value
                
            # Penalties
            elif type_id == 47:
                stats['penalties'] = actual_value
            elif type_id == 85:
                stats['penalties_scored'] = actual_value
            elif type_id == 62:
                stats['penalties_missed'] = actual_value
            elif type_id == 218:
                stats['penalties_won'] = actual_value
            elif type_id == 217:
                stats['penalties_committed'] = actual_value
                
            # Passes
            elif type_id == 80:
                stats['passes'] = actual_value
            elif type_id == 116:
                stats['passes_completed'] = actual_value
            elif type_id == 1584:
                stats['passes_accuracy'] = actual_value
            elif type_id == 117:
                stats['key_passes'] = actual_value
            elif type_id == 98:
                stats['crosses'] = actual_value
            elif type_id == 99:
                stats['crosses_accurate'] = actual_value
                
            # Défense
            elif type_id == 78:  # CORRECT: Tackles
                stats['tackles'] = actual_value
            elif type_id == 100:  # CORRECT: Interceptions
                stats['interceptions'] = actual_value
            elif type_id == 97:  # CORRECT: Blocks
                stats['blocks'] = actual_value
            elif type_id == 101:
                stats['clearances'] = actual_value
                
            # Duels
            elif type_id == 105:
                stats['ground_duels'] = actual_value
            elif type_id == 106:
                stats['ground_duels_won'] = actual_value
            elif type_id == 107:
                stats['aerial_duels_won'] = actual_value
                
            # Dribbles
            elif type_id == 108:
                stats['dribbles'] = actual_value
            elif type_id == 109:
                stats['dribbles_successful'] = actual_value
            elif type_id == 94:
                stats['ball_losses'] = actual_value
                
            # Discipline
            elif type_id == 56:
                stats['fouls'] = actual_value
            elif type_id == 96:
                stats['fouls_drawn'] = actual_value
            elif type_id == 84:
                stats['yellow_cards'] = actual_value
            elif type_id == 83:
                stats['red_cards'] = actual_value
                
            # Gardien
            elif type_id == 57:
                stats['saves'] = actual_value
            elif type_id == 88:
                stats['goals_conceded'] = actual_value
            elif type_id == 194:
                stats['clean_sheets'] = actual_value
            elif type_id == 207:
                stats['punches'] = actual_value
            elif type_id == 240:
                stats['penalties_saved'] = actual_value
                
            # Stats avancées
            elif type_id == 576:
                stats['xg'] = actual_value
            elif type_id == 577:
                stats['xa'] = actual_value
            elif type_id == 571:
                stats['mistakes_leading_to_goals'] = actual_value
    
    # Calculer crosses_accuracy si possible
    if stats['crosses_accurate'] and stats['crosses']:
        stats['crosses_accuracy'] = round((stats['crosses_accurate'] / stats['crosses']) * 100, 2)
    
    return stats

def fetch_team_squad(team_id, team_name, seasons, league_name):
    """Récupère les stats de tous les joueurs d'une équipe"""
    
    players_data = {}
    api_calls = 0
    
    # Récupérer la liste des joueurs
    url = f"{BASE_URL}/squads/teams/{team_id}/current"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        api_calls += 1
        
        if response.status_code != 200:
            logging.warning(f"  ❌ Erreur {response.status_code} pour {team_name}")
            return players_data, api_calls
        
        squad_data = response.json().get('data', [])
        
        for player_data in squad_data:
            player_info = player_data.get('player', {})
            player_id = player_info.get('id')
            
            if not player_id:
                continue
            
            # Récupérer les stats du joueur
            stats_url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
            stats_params = {
                'api_token': API_KEY,
                'include': 'details.type',
                'filters': f'seasonIds:{",".join(map(str, seasons.keys()))}'
            }
            
            stats_response = requests.get(stats_url, params=stats_params, timeout=15)
            api_calls += 1
            
            if stats_response.status_code == 200:
                stats_data = stats_response.json().get('data', [])
                
                if stats_data:
                    # Créer l'objet joueur
                    player = {
                        'id': player_id,
                        'displayName': player_info.get('display_name', player_info.get('name', 'Unknown')),
                        'position': player_info.get('position', {}).get('name') if isinstance(player_info.get('position'), dict) else None,
                        'jersey': player_data.get('jersey_number'),
                        'stats': {}
                    }
                    
                    # Traiter les stats par saison
                    for season_data in stats_data:
                        season_id = season_data.get('season_id')
                        if season_id in seasons:
                            stats = process_player_stats(season_data, league_name)
                            stats['team'] = team_name
                            stats['team_id'] = team_id
                            
                            season_key = f"{seasons[season_id]} ({league_name}, {team_name})"
                            player['stats'][season_key] = stats
                    
                    if player['stats']:
                        players_data[str(player_id)] = player
                        logging.info(f"  ✓ {player['displayName']}")
    
    except Exception as e:
        logging.error(f"  ❌ Erreur: {e}")
    
    return players_data, api_calls

def main():
    logging.info("\n" + "=" * 70)
    logging.info("🏆 MISE À JOUR COMPLÈTE AVEC LE MAPPING CORRECT")
    logging.info("=" * 70)
    
    total_api_calls = 0
    
    for league_name, league_data in LEAGUES.items():
        logging.info(f"\n{'=' * 60}")
        logging.info(f"🏆 {league_name}")
        logging.info(f"{'=' * 60}")
        
        teams = league_data['teams']
        seasons = league_data['seasons']
        
        # Mettre à jour le cache des noms
        for team_id, team_name in teams:
            TEAM_NAMES[team_id] = team_name
        
        logging.info(f"📋 {len(teams)} équipes trouvées\n")
        
        all_players = {}
        
        for idx, (team_id, team_name) in enumerate(teams, 1):
            logging.info(f"[{idx}/{len(teams)}] {team_name}")
            
            players, api_calls = fetch_team_squad(team_id, team_name, seasons, league_name)
            all_players.update(players)
            total_api_calls += api_calls
            
            # Pause pour respecter le rate limit (60 appels/minute)
            if total_api_calls >= 55:
                logging.info("⏳ Pause de 60 secondes (rate limit)...")
                time.sleep(60)
                total_api_calls = 0
        
        # Générer le fichier TypeScript
        file_name = league_name.lower().replace(' ', '').replace('-', '')
        if league_name == "Liga":
            file_name = "la-liga"
        elif league_name == "Premier League":
            file_name = "premier-league"
        elif league_name == "Serie A":
            file_name = "serie-a"
        
        ts_content = generate_typescript(all_players, league_name)
        
        output_path = Path(f'../data/{file_name}PlayersCompleteStats.ts')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(ts_content)
        
        logging.info(f"💾 Sauvegardé: {output_path.name}")
        logging.info(f"📊 Total: {len(all_players)} joueurs avec statistiques")
        logging.info(f"✅ {league_name} terminé!")
    
    logging.info(f"\n📊 Total d'appels API: {total_api_calls}")
    logging.info("\n" + "=" * 70)
    logging.info("✅ TOUTES LES MISES À JOUR TERMINÉES AVEC LE MAPPING CORRECT!")

def generate_typescript(players_data, league_name):
    """Génère le contenu TypeScript"""
    
    export_name = league_name.lower().replace(' ', '').replace('-', '') + "PlayersRealStats"
    if league_name == "Liga":
        export_name = "ligaPlayersRealStats"
    elif league_name == "Premier League":
        export_name = "premierleaguePlayersRealStats"
    elif league_name == "Serie A":
        export_name = "serieaPlayersRealStats"
    elif league_name == "Bundesliga":
        export_name = "bundesligaPlayersRealStats"
    
    return f"""// Statistiques complètes des joueurs de {league_name}
// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Version CORRIGÉE avec le mapping correct des IDs SportMonks

// ⚠️ NE PAS MODIFIER CE FICHIER MANUELLEMENT
// Mapping corrigé: ID 79=assists, ID 86=shots_on_target, ID 64=hit_woodwork

export interface PlayerSeasonStats {{
  team: string;
  team_id: number;
  league: string;
  rating: number | null;
  minutes: number | null;
  appearences: number | null;
  lineups: number | null;
  captain: number;
  substitutions: number | null;
  touches: number | null;
  goals: number | null;
  assists: number | null;
  xg: number | null;
  xa: number | null;
  shots: number | null;
  shots_on_target: number | null;
  penalties_won: number | null;
  penalties: number | null;
  penalties_scored: number | null;
  penalties_missed: number | null;
  hit_woodwork: number | null;
  offsides: number | null;
  passes: number | null;
  passes_completed: number | null;
  passes_accuracy: number | null;
  key_passes: number | null;
  crosses: number | null;
  crosses_accurate: number | null;
  dribbles: number | null;
  dribbles_successful: number | null;
  tackles: number | null;
  blocks: number | null;
  interceptions: number | null;
  clearances: number | null;
  ground_duels: number | null;
  ground_duels_won: number | null;
  aerial_duels: number | null;
  aerial_duels_won: number | null;
  fouls: number | null;
  fouls_drawn: number | null;
  yellow_cards: number | null;
  red_cards: number | null;
  yellowred_cards: number | null;
  penalties_committed: number | null;
  ball_losses: number | null;
  ball_recoveries: number | null;
  mistakes_leading_to_goals: number | null;
  saves: number | null;
  punches: number | null;
  inside_box_saves: number | null;
  clean_sheets: number | null;
  goals_conceded: number | null;
  penalties_saved: number | null;
  crosses_accuracy: number | null;
}}

export interface PlayerRealStats {{
  displayName: string;
  position: string | null;
  jersey: number | null;
  stats: {{ [key: string]: PlayerSeasonStats }};
}}

export const {export_name}: {{ [playerId: number]: PlayerRealStats }} = {json.dumps(players_data, ensure_ascii=False, indent=2)};
"""

if __name__ == "__main__":
    main()