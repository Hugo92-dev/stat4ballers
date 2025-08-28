#!/usr/bin/env python3
"""
Script final pour mettre à jour les statistiques de TOUS les clubs
Utilise la même logique que l'OM (omPlayersCompleteStats.ts)
"""

import json
import requests
import time
from dotenv import load_dotenv
import os
import sys
from datetime import datetime
from pathlib import Path

# Fix encodage Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger l'API key
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("❌ Clé API manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# Configuration complète des ligues et saisons
LEAGUES = {
    'ligue1': {
        'name': 'Ligue 1',
        'file': '../data/ligue1PlayersCompleteStats.ts',
        'teams': '../data/ligue1_2025_2026/',
        'seasons': {
            25651: "2025/2026",
            23643: "2024/2025", 
            21779: "2023/2024"
        }
    },
    'premier-league': {
        'name': 'Premier League', 
        'file': '../data/premier-leaguePlayersCompleteStats.ts',
        'teams': '../data/premier-league_2025_2026/',
        'seasons': {
            25583: "2025/2026",
            23614: "2024/2025",
            21646: "2023/2024"
        }
    },
    'liga': {
        'name': 'Liga',
        'file': '../data/la-ligaPlayersCompleteStats.ts',
        'teams': '../data/liga_2025_2026/',
        'seasons': {
            25659: "2025/2026",
            23621: "2024/2025",
            21694: "2023/2024"
        }
    },
    'serie-a': {
        'name': 'Serie A',
        'file': '../data/serie-aPlayersCompleteStats.ts',
        'teams': '../data/serie-a_2025_2026/',
        'seasons': {
            25533: "2025/2026",
            23746: "2024/2025",
            21818: "2023/2024"
        }
    },
    'bundesliga': {
        'name': 'Bundesliga',
        'file': '../data/bundesligaPlayersCompleteStats.ts',
        'teams': '../data/bundesliga_2025_2026/',
        'seasons': {
            25646: "2025/2026",
            23744: "2024/2025",
            21795: "2023/2024"
        }
    }
}

# Cache global pour éviter les requêtes répétées
team_name_cache = {}
api_calls = 0

def get_team_name(team_id):
    """Récupère le nom d'une équipe"""
    if team_id in team_name_cache:
        return team_name_cache[team_id]
    
    try:
        response = requests.get(
            f"{BASE_URL}/teams/{team_id}",
            params={'api_token': API_KEY},
            timeout=10
        )
        if response.status_code == 200:
            name = response.json()['data'].get('name', f'Team_{team_id}')
            team_name_cache[team_id] = name
            return name
    except:
        pass
    
    return f'Team_{team_id}'

def get_player_stats(player_id, season_ids):
    """Récupère les stats d'un joueur pour les saisons données"""
    global api_calls
    api_calls += 1
    
    # Gestion du rate limit
    if api_calls % 20 == 0:
        time.sleep(2)
    if api_calls % 100 == 0:
        print(f"      ⏸️ Pause anti rate-limit...")
        time.sleep(30)
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{",".join(map(str, season_ids))}'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            return response.json().get('data', [])
        elif response.status_code == 429:
            print(f"      ⏳ Rate limit, pause 60s...")
            time.sleep(60)
            return get_player_stats(player_id, season_ids)
    except Exception as e:
        print(f"      ⚠️ Erreur API: {e}")
    
    return []

def map_stat_details(details):
    """Mappe les détails des stats vers notre format (identique à l'OM)"""
    stats = {
        'rating': None, 'minutes': None, 'appearences': None, 'lineups': None,
        'captain': None, 'touches': None, 'goals': None, 'assists': None,
        'xg': None, 'xa': None, 'shots': None, 'shots_on_target': None,
        'hit_woodwork': None, 'saves': None, 'goals_conceded': None,
        'clean_sheets': None, 'penalties_saved': None, 'punches': None,
        'inside_box_saves': None, 'passes': None, 'passes_completed': None,
        'passes_accuracy': None, 'key_passes': None, 'crosses': None,
        'crosses_accurate': None, 'tackles': None, 'blocks': None,
        'interceptions': None, 'clearances': None, 'fouls': None,
        'fouls_drawn': None, 'yellow_cards': None, 'red_cards': None,
        'yellowred_cards': None, 'ground_duels': None, 'ground_duels_won': None,
        'aerial_duels': None, 'aerial_duels_won': None, 'duels': None,
        'duels_won': None, 'dribbles': None, 'dribbles_successful': None,
        'penalties': None, 'penalties_won': None, 'penalties_scored': None,
        'penalties_missed': None, 'penalties_committed': None, 'offsides': None,
        'ball_losses': None, 'ball_recoveries': None,
        'mistakes_leading_to_goals': None, 'crosses_accuracy': None
    }
    
    # Mapping des types SportMonks (identique à l'OM)
    type_map = {
        52: 'rating', 79: 'minutes', 113: 'appearences', 114: 'lineups',
        118: 'captain', 192: 'touches', 208: 'goals', 209: 'assists',
        576: 'xg', 577: 'xa', 42: 'shots', 86: 'shots_on_target',
        81: 'hit_woodwork', 206: 'saves', 131: 'goals_conceded',
        130: 'clean_sheets', 240: 'penalties_saved', 207: 'punches',
        129: 'inside_box_saves', 124: 'passes', 125: 'passes_completed',
        126: 'passes_accuracy', 147: 'key_passes', 45: 'crosses',
        46: 'crosses_accurate', 88: 'tackles', 74: 'blocks',
        75: 'interceptions', 78: 'clearances', 105: 'fouls',
        106: 'fouls_drawn', 56: 'yellow_cards', 57: 'red_cards',
        58: 'yellowred_cards', 127: 'dribbles', 128: 'dribbles_successful',
        85: 'penalties', 218: 'penalties_won', 84: 'penalties_scored',
        83: 'penalties_missed', 217: 'penalties_committed', 41: 'offsides',
        219: 'ball_losses', 220: 'ball_recoveries',
        215: 'mistakes_leading_to_goals', 68: 'aerial_duels',
        69: 'aerial_duels_won', 155: 'ground_duels', 156: 'ground_duels_won',
        212: 'duels', 213: 'duels_won'
    }
    
    # Appliquer le mapping
    for detail in details:
        type_id = detail.get('type', {}).get('id') if isinstance(detail.get('type'), dict) else None
        if type_id in type_map:
            value = detail.get('value', {})
            if isinstance(value, dict):
                stats[type_map[type_id]] = value.get('total', value.get('average'))
            else:
                stats[type_map[type_id]] = value
    
    # Calculer les stats dérivées
    if stats['crosses'] and stats['crosses_accurate']:
        try:
            stats['crosses_accuracy'] = round((stats['crosses_accurate'] / stats['crosses']) * 100, 2)
        except:
            pass
    
    return stats

def get_team_players(team_file):
    """Récupère les joueurs d'une équipe depuis le fichier JSON"""
    try:
        with open(team_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('players', [])
    except:
        return []

def process_league(league_key, league_config):
    """Traite une ligue complète"""
    print(f"\n{'='*60}")
    print(f"🏆 {league_config['name']}")
    print(f"{'='*60}\n")
    
    # Lister toutes les équipes
    teams_dir = Path(league_config['teams'])
    if not teams_dir.exists():
        print(f"  ❌ Dossier {teams_dir} introuvable")
        return {}
    
    team_files = list(teams_dir.glob('*.json'))
    if not team_files:
        print(f"  ❌ Aucune équipe trouvée")
        return {}
    
    print(f"  📋 {len(team_files)} équipes trouvées\n")
    
    all_players_stats = {}
    season_ids = list(league_config['seasons'].keys())
    
    for t_idx, team_file in enumerate(team_files, 1):
        team_name = team_file.stem.replace('-', ' ').title()
        players = get_team_players(team_file)
        
        if not players:
            print(f"  [{t_idx}/{len(team_files)}] {team_name}: aucun joueur")
            continue
        
        print(f"  [{t_idx}/{len(team_files)}] {team_name} ({len(players)} joueurs)")
        
        for p_idx, player in enumerate(players, 1):
            player_id = player.get('id')
            if not player_id:
                continue
            
            print(f"    [{p_idx}/{len(players)}] {player.get('display_name', 'Unknown')}...", end=' ')
            
            # Récupérer les stats
            stats_data = get_player_stats(player_id, season_ids)
            
            # Structure du joueur (identique à l'OM)
            player_stats = {
                'displayName': player.get('display_name', ''),
                'position': player.get('position', ''),
                'jersey': player.get('jersey_number'),
                'stats': {}
            }
            
            # Traiter chaque saison
            for season_stat in stats_data:
                season_id = season_stat.get('season_id')
                if season_id not in league_config['seasons']:
                    continue
                
                team_id = season_stat.get('team_id')
                team_name = get_team_name(team_id) if team_id else None
                
                # Mapper les stats
                mapped_stats = map_stat_details(season_stat.get('details', []))
                mapped_stats['team'] = team_name
                mapped_stats['team_id'] = team_id
                mapped_stats['league'] = league_config['name']
                
                # Clé de la saison
                season_key = f"{league_config['seasons'][season_id]} ({league_config['name']}, {team_name})"
                player_stats['stats'][season_key] = mapped_stats
            
            all_players_stats[player_id] = player_stats
            print("✓")
        
        # Pause entre équipes
        time.sleep(1)
    
    return all_players_stats

def save_league_stats(league_key, league_config, stats):
    """Sauvegarde les stats d'une ligue"""
    output_file = Path(league_config['file'])
    
    # Générer le contenu TypeScript (format identique à l'OM)
    ts_content = f"""// Stats COMPLÈTES des joueurs de {league_config['name']} depuis SportMonks API
// Inclut TOUTES les saisons dans TOUS les clubs (pas seulement {league_config['name']})
// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

export interface PlayerSeasonStats {{
  // Métadonnées
  team?: string;
  team_id?: number;
  league?: string;
  
  // Stats générales
  rating?: number | null;
  minutes?: number | null;
  appearences?: number | null;
  lineups?: number | null;
  captain?: number | null;
  substitutions?: number | null;
  touches?: number | null;
  
  // Stats offensives
  goals?: number | null;
  assists?: number | null;
  xg?: number | null;
  xa?: number | null;
  shots?: number | null;
  shots_on_target?: number | null;
  penalties_won?: number | null;
  penalties?: number | null;
  penalties_scored?: number | null;
  penalties_missed?: number | null;
  hit_woodwork?: number | null;
  offsides?: number | null;
  
  // Stats de passes
  passes?: number | null;
  passes_completed?: number | null;
  passes_accuracy?: number | null;
  key_passes?: number | null;
  crosses?: number | null;
  crosses_accurate?: number | null;
  
  // Stats de dribbles
  dribbles?: number | null;
  dribbles_successful?: number | null;
  
  // Stats défensives
  tackles?: number | null;
  blocks?: number | null;
  interceptions?: number | null;
  clearances?: number | null;
  ground_duels?: number | null;
  ground_duels_won?: number | null;
  aerial_duels?: number | null;
  aerial_duels_won?: number | null;
  
  // Discipline
  fouls?: number | null;
  fouls_drawn?: number | null;
  yellow_cards?: number | null;
  red_cards?: number | null;
  yellowred_cards?: number | null;
  penalties_committed?: number | null;
  
  // Autres
  ball_losses?: number | null;
  ball_recoveries?: number | null;
  mistakes_leading_to_goals?: number | null;
  
  // Stats gardien
  saves?: number | null;
  punches?: number | null;
  inside_box_saves?: number | null;
  clean_sheets?: number | null;
  goals_conceded?: number | null;
  
  // Calculé
  crosses_accuracy?: number | null;
}}

export interface PlayerRealStats {{
  displayName: string;
  position: string;
  jersey?: number;
  stats: {{
    [seasonKey: string]: PlayerSeasonStats | null;
  }};
}}

export const {league_key.replace('-', '')}PlayersRealStats: {{ [playerId: number]: PlayerRealStats }} = {json.dumps(stats, indent=2, ensure_ascii=False)};
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"\n  💾 Stats sauvegardées dans {output_file.name}")
    print(f"  📊 Total: {len(stats)} joueurs avec statistiques")

def main():
    """Fonction principale"""
    print("🚀 Mise à jour complète des statistiques de tous les clubs")
    print(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Traiter chaque ligue
    for league_key, league_config in LEAGUES.items():
        try:
            stats = process_league(league_key, league_config)
            if stats:
                save_league_stats(league_key, league_config, stats)
                print(f"  ✅ {league_config['name']} terminé!")
        except KeyboardInterrupt:
            print("\n⚠️ Interruption utilisateur")
            break
        except Exception as e:
            print(f"  ❌ Erreur pour {league_config['name']}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print(f"✨ Mise à jour terminée!")
    print(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total d'appels API: {api_calls}")

if __name__ == "__main__":
    main()