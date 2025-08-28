#!/usr/bin/env python3
"""Script pour mettre à jour uniquement la Bundesliga avec le mapping corrigé"""

import json
import requests
import time
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import os

# Configuration de l'encodage UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# Saisons pour la Bundesliga
BUNDESLIGA_SEASONS = {
    25660: "2025/2026",
    23622: "2024/2025", 
    21695: "2023/2024"
}

# MAPPING CORRECT ET COMPLET (basé sur l'analyse de l'API)
def get_stat_value(details, type_id):
    """Récupère la valeur correcte pour un type_id donné"""
    for detail in details:
        type_data = detail.get('type', {})
        if isinstance(type_data, dict) and type_data.get('id') == type_id:
            value = detail.get('value', {})
            if isinstance(value, dict):
                # Pour les stats avec total/average
                return value.get('total', value.get('average'))
            else:
                return value
    return None

def process_player_stats(season_data):
    """Process les stats d'un joueur pour une saison"""
    stats = {
        'team': None,
        'team_id': None,
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
    
    # MAPPING CORRECT ET COMPLET
    stats['goals'] = get_stat_value(details, 52)
    stats['assists'] = get_stat_value(details, 58)
    stats['appearences'] = get_stat_value(details, 321)
    stats['lineups'] = get_stat_value(details, 322)
    stats['minutes'] = get_stat_value(details, 119)
    stats['rating'] = get_stat_value(details, 118)
    stats['substitutions'] = get_stat_value(details, 98)
    stats['captain'] = get_stat_value(details, 40) or 0
    
    # Tirs
    stats['shots'] = get_stat_value(details, 64)
    stats['shots_on_target'] = get_stat_value(details, 65)
    stats['hit_woodwork'] = get_stat_value(details, 53)
    
    # Penalties  
    stats['penalties_scored'] = get_stat_value(details, 86)
    stats['penalties_missed'] = get_stat_value(details, 55)
    stats['penalties_won'] = get_stat_value(details, 63)
    stats['penalties_committed'] = get_stat_value(details, 67)
    
    # Passes
    stats['passes'] = get_stat_value(details, 80)
    stats['passes_completed'] = get_stat_value(details, 116)
    stats['passes_accuracy'] = get_stat_value(details, 1584)
    stats['key_passes'] = get_stat_value(details, 102)
    stats['crosses'] = get_stat_value(details, 97)
    stats['crosses_accurate'] = get_stat_value(details, 104)
    
    # Dribbles et duels
    stats['dribbles'] = get_stat_value(details, 108)
    stats['dribbles_successful'] = get_stat_value(details, 109)
    stats['ground_duels'] = get_stat_value(details, 110)
    stats['ground_duels_won'] = get_stat_value(details, 111)
    stats['aerial_duels'] = get_stat_value(details, 117)
    stats['aerial_duels_won'] = get_stat_value(details, 1576)
    
    # Défense
    stats['tackles'] = get_stat_value(details, 105)
    stats['blocks'] = get_stat_value(details, 100)
    stats['interceptions'] = get_stat_value(details, 74)
    stats['clearances'] = get_stat_value(details, 99)
    
    # Fautes et cartons
    stats['fouls'] = get_stat_value(details, 50)
    stats['fouls_drawn'] = get_stat_value(details, 51)
    stats['yellow_cards'] = get_stat_value(details, 84)
    stats['red_cards'] = get_stat_value(details, 83)
    stats['yellowred_cards'] = get_stat_value(details, 1597)
    
    # Autres
    stats['offsides'] = get_stat_value(details, 69)
    stats['ball_losses'] = get_stat_value(details, 91)
    stats['ball_recoveries'] = get_stat_value(details, 94)
    stats['mistakes_leading_to_goals'] = get_stat_value(details, 85)
    stats['touches'] = get_stat_value(details, 112)
    
    # Stats de gardien
    stats['saves'] = get_stat_value(details, 57)
    stats['goals_conceded'] = get_stat_value(details, 88)
    stats['clean_sheets'] = get_stat_value(details, 56)
    stats['penalties_saved'] = get_stat_value(details, 89)
    stats['punches'] = get_stat_value(details, 59)
    stats['inside_box_saves'] = get_stat_value(details, 60)
    
    # XG et XA
    stats['xg'] = get_stat_value(details, 1491)
    stats['xa'] = get_stat_value(details, 1595)
    
    return stats

def fetch_team_players(team_id, team_name, seasons):
    """Récupère les stats de tous les joueurs d'une équipe"""
    
    # D'abord récupérer la liste des joueurs
    url = f"{BASE_URL}/squads/teams/{team_id}/current"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code != 200:
        print(f"   ❌ Erreur {response.status_code} pour l'équipe {team_name}")
        return []
    
    squad_data = response.json().get('data', [])
    
    if not squad_data:
        return []
    
    players_stats = []
    
    # Pour chaque joueur
    for player_data in squad_data:
        player_info = player_data.get('player', {})
        player_id = player_info.get('id')
        
        if not player_id:
            continue
        
        # Récupérer ses stats
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {
            'api_token': API_KEY,
            'include': 'details.type',
            'filters': f'seasonIds:{",".join(map(str, seasons))}'
        }
        
        try:
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                stats_data = response.json().get('data', [])
                
                # Créer l'objet joueur
                player = {
                    'id': player_id,
                    'displayName': player_info.get('display_name', player_info.get('name', 'Unknown')),
                    'position': player_info.get('position', {}).get('name') if isinstance(player_info.get('position'), dict) else player_info.get('position_id'),
                    'jersey': player_data.get('jersey_number'),
                    'stats': {}
                }
                
                # Traiter les stats par saison
                for season_data in stats_data:
                    season_id = season_data.get('season_id')
                    if season_id in seasons:
                        stats = process_player_stats(season_data)
                        stats['team'] = team_name
                        stats['team_id'] = team_id
                        
                        # Clé de saison
                        season_name = seasons[season_id]
                        season_key = f"{season_name} (Bundesliga, {team_name})"
                        player['stats'][season_key] = stats
                
                if player['stats']:  # Si on a des stats
                    players_stats.append(player)
                    print(f"     ✓ {player['displayName']}")
        
        except Exception as e:
            print(f"     ❌ Erreur pour joueur {player_id}: {e}")
    
    return players_stats

def main():
    print("🔧 MISE À JOUR DE LA BUNDESLIGA AVEC LE MAPPING CORRIGÉ")
    print("=" * 60)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Équipes de Bundesliga
    BUNDESLIGA_TEAMS = [
        (45, "Bayern Munich"),
        (43, "Borussia Dortmund"), 
        (35, "Bayer 04 Leverkusen"),
        (63, "RasenBallsport Leipzig"),
        (131, "Eintracht Frankfurt"),
        (130, "VfL Wolfsburg"),
        (104, "SC Freiburg"),
        (72, "VfB Stuttgart"),
        (90, "1. FSV Mainz 05"),
        (102, "TSG 1899 Hoffenheim"),
        (47, "FC Augsburg"),
        (37, "SV Werder Bremen"),
        (87, "Borussia Mönchengladbach"),
        (1374, "1. FC Union Berlin"),
        (110, "VfL Bochum"),
        (123, "1. FC Köln"),
        (1648, "1. FC Heidenheim"),
        (9526, "FC St. Pauli")
    ]
    
    all_players = []
    
    for idx, (team_id, team_name) in enumerate(BUNDESLIGA_TEAMS, 1):
        print(f"\n[{idx}/{len(BUNDESLIGA_TEAMS)}] {team_name}...")
        
        players = fetch_team_players(team_id, team_name, BUNDESLIGA_SEASONS)
        all_players.extend(players)
        
        # Pause entre les équipes pour respecter le rate limit
        if idx % 3 == 0 and idx < len(BUNDESLIGA_TEAMS):
            print("⏳ Pause de 5 secondes...")
            time.sleep(5)
    
    # Générer le fichier TypeScript
    print(f"\n💾 Génération du fichier avec {len(all_players)} joueurs...")
    
    ts_content = f"""// Statistiques complètes des joueurs de Bundesliga
// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
// Version CORRIGÉE avec le mapping des IDs SportMonks

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
    
    # Écrire le fichier
    output_path = Path('../data/bundesligaPlayersCompleteStats.ts')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"✅ Fichier généré: {output_path}")
    print(f"📊 Total: {len(all_players)} joueurs de Bundesliga mis à jour")
    print("\n" + "=" * 60)
    print("✅ MISE À JOUR DE LA BUNDESLIGA TERMINÉE AVEC SUCCÈS!")
    print("   Le mapping des IDs SportMonks est maintenant correct")

if __name__ == "__main__":
    main()