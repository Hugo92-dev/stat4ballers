#!/usr/bin/env python3
"""Script pour mettre à jour uniquement la Bundesliga"""

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

# Saisons Bundesliga
BUNDESLIGA_SEASONS = {
    25660: "2025/2026",
    23622: "2024/2025", 
    21695: "2023/2024"
}

# ÉQUIPES BUNDESLIGA 
BUNDESLIGA_TEAMS = [
    # IDs tirés de l'ancienne version
    (95, "Bayern Munich"),
    (68, "Borussia Dortmund"),
    (93, "Bayer 04 Leverkusen"),
    (63, "RasenBallsport Leipzig"),
    (366, "Eintracht Frankfurt"),
    (510, "VfL Wolfsburg"),
    (91, "SC Freiburg"),
    (101, "VfB Stuttgart"),
    (225, "1. FSV Mainz 05"),
    (369, "TSG 1899 Hoffenheim"),
    (113, "FC Augsburg"),
    (86, "SV Werder Bremen"),
    (65, "Borussia Mönchengladbach"),
    (606, "1. FC Union Berlin"),
    (125, "VfL Bochum"),
    (80, "1. FC Köln"),
    (2394, "1. FC Heidenheim"),
    (390, "FC St. Pauli")
]

def extract_stat(details, type_id):
    """Extrait la valeur pour un type_id donné"""
    for detail in details:
        type_data = detail.get('type', {})
        if isinstance(type_data, dict) and type_data.get('id') == type_id:
            value = detail.get('value', {})
            if isinstance(value, dict):
                return value.get('total', value.get('average'))
            else:
                return value
    return None

def process_stats(season_data, team_name, team_id):
    """Process les stats d'un joueur pour une saison"""
    stats = {
        'team': team_name,
        'team_id': team_id,
        'league': 'Bundesliga',
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
    
    if 'details' not in season_data:
        return stats
        
    details = season_data['details']
    
    # MAPPING CORRECT (basé sur l'analyse réelle)
    stats['goals'] = extract_stat(details, 52)
    stats['assists'] = extract_stat(details, 58)
    stats['appearences'] = extract_stat(details, 321)
    stats['lineups'] = extract_stat(details, 322)
    stats['minutes'] = extract_stat(details, 119)
    stats['rating'] = extract_stat(details, 118)
    stats['substitutions'] = extract_stat(details, 323)
    stats['captain'] = extract_stat(details, 40) or 0
    
    # Tirs
    stats['shots'] = extract_stat(details, 64)
    stats['shots_on_target'] = extract_stat(details, 65)
    stats['hit_woodwork'] = extract_stat(details, 53)
    
    # Penalties
    stats['penalties_scored'] = extract_stat(details, 86)
    stats['penalties_missed'] = extract_stat(details, 55)
    stats['penalties_won'] = extract_stat(details, 63)
    stats['penalties_committed'] = extract_stat(details, 67)
    
    # Passes
    stats['passes'] = extract_stat(details, 80)
    stats['passes_completed'] = extract_stat(details, 116)
    stats['passes_accuracy'] = extract_stat(details, 1584)
    stats['key_passes'] = extract_stat(details, 102)
    stats['crosses'] = extract_stat(details, 119)
    stats['crosses_accurate'] = extract_stat(details, 104)
    
    # Dribbles
    stats['dribbles'] = extract_stat(details, 108)
    stats['dribbles_successful'] = extract_stat(details, 109)
    
    # Défense
    stats['tackles'] = extract_stat(details, 105)
    stats['blocks'] = extract_stat(details, 100)
    stats['interceptions'] = extract_stat(details, 74)
    stats['clearances'] = extract_stat(details, 99)
    
    # Duels
    stats['ground_duels'] = extract_stat(details, 110)
    stats['ground_duels_won'] = extract_stat(details, 111)
    stats['aerial_duels'] = extract_stat(details, 117)
    stats['aerial_duels_won'] = extract_stat(details, 1576)
    
    # Fautes et cartons
    stats['fouls'] = extract_stat(details, 50)
    stats['fouls_drawn'] = extract_stat(details, 51)
    stats['yellow_cards'] = extract_stat(details, 84)
    stats['red_cards'] = extract_stat(details, 83)
    stats['yellowred_cards'] = extract_stat(details, 1597)
    
    # Autres
    stats['offsides'] = extract_stat(details, 69)
    stats['ball_losses'] = extract_stat(details, 91)
    stats['ball_recoveries'] = extract_stat(details, 94)
    stats['mistakes_leading_to_goals'] = extract_stat(details, 85)
    stats['touches'] = extract_stat(details, 112)
    
    # Stats gardien
    stats['saves'] = extract_stat(details, 57)
    stats['goals_conceded'] = extract_stat(details, 88)
    stats['clean_sheets'] = extract_stat(details, 56)
    stats['penalties_saved'] = extract_stat(details, 89)
    stats['punches'] = extract_stat(details, 59)
    stats['inside_box_saves'] = extract_stat(details, 60)
    
    # XG
    stats['xg'] = extract_stat(details, 1491)
    stats['xa'] = extract_stat(details, 1595)
    
    return stats

def fetch_team_players(team_id, team_name):
    """Récupère les stats des joueurs d'une équipe"""
    all_players = []
    
    # D'abord récupérer la liste des joueurs via transferts
    for season_id in BUNDESLIGA_SEASONS.keys():
        url = f"{BASE_URL}/transfers"
        params = {
            'api_token': API_KEY,
            'filters': f'teamIn:{team_id};seasonIds:{season_id}',
            'include': 'player',
            'per_page': 50
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                transfers = response.json().get('data', [])
                
                for transfer in transfers:
                    player_info = transfer.get('player')
                    if not player_info:
                        continue
                        
                    player_id = player_info.get('id')
                    if not player_id:
                        continue
                    
                    # Récupérer les stats du joueur
                    stats_url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
                    stats_params = {
                        'api_token': API_KEY,
                        'include': 'details.type',
                        'filters': f'seasonIds:{",".join(map(str, BUNDESLIGA_SEASONS.keys()))}'
                    }
                    
                    stats_response = requests.get(stats_url, params=stats_params, timeout=15)
                    
                    if stats_response.status_code == 200:
                        stats_data = stats_response.json().get('data', [])
                        
                        if stats_data:
                            player = {
                                'id': player_id,
                                'displayName': player_info.get('display_name', player_info.get('name', 'Unknown')),
                                'position': player_info.get('position', {}).get('name') if isinstance(player_info.get('position'), dict) else None,
                                'jersey': None,
                                'stats': {}
                            }
                            
                            for season_data in stats_data:
                                season_id = season_data.get('season_id')
                                if season_id in BUNDESLIGA_SEASONS:
                                    stats = process_stats(season_data, team_name, team_id)
                                    season_key = f"{BUNDESLIGA_SEASONS[season_id]} (Bundesliga, {team_name})"
                                    player['stats'][season_key] = stats
                            
                            if player['stats'] and player_id not in [p['id'] for p in all_players]:
                                all_players.append(player)
                                print(f"     ✓ {player['displayName']}")
            
        except Exception as e:
            print(f"   ❌ Erreur: {e}")
    
    return all_players

def main():
    print("🔧 MISE À JOUR DE LA BUNDESLIGA")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_players = []
    api_calls = 0
    
    for idx, (team_id, team_name) in enumerate(BUNDESLIGA_TEAMS, 1):
        print(f"\n[{idx}/{len(BUNDESLIGA_TEAMS)}] {team_name} (ID: {team_id})...")
        
        players = fetch_team_players(team_id, team_name)
        all_players.extend(players)
        api_calls += 5  # Estimation
        
        # Pause pour respecter le rate limit
        if api_calls >= 55:
            print("⏳ Pause de 60 secondes (rate limit)...")
            time.sleep(60)
            api_calls = 0
    
    # Générer le fichier TypeScript
    print(f"\n💾 Génération du fichier avec {len(all_players)} joueurs...")
    
    ts_content = f"""// Statistiques complètes des joueurs de Bundesliga
// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Version CORRIGÉE avec le mapping correct des IDs SportMonks

// ⚠️ NE PAS MODIFIER CE FICHIER MANUELLEMENT
// Bug de mapping résolu: les IDs SportMonks sont correctement mappés aux valeurs

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

export interface Player {{
  id: number;
  displayName: string;
  position: string | null;
  jersey: number | null;
  stats: {{ [key: string]: PlayerSeasonStats }};
}}

export const bundesligaPlayersRealStats: Player[] = {json.dumps(all_players, ensure_ascii=False, indent=2)};

export const BundesligaPlayersCompleteStats = bundesligaPlayersRealStats;
"""
    
    # Sauvegarder
    output_path = Path('../data/bundesligaPlayersCompleteStats.ts')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"✅ Fichier généré: {output_path}")
    print(f"📊 Total: {len(all_players)} joueurs de Bundesliga")
    print("\n" + "=" * 60)
    print("✅ MISE À JOUR TERMINÉE!")
    
if __name__ == "__main__":
    main()