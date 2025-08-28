#!/usr/bin/env python3
"""
Script pour récupérer les stats des ligues restantes uniquement
"""

import json
import requests
import time
from dotenv import load_dotenv
import os
import sys
import re
from datetime import datetime
from pathlib import Path

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("❌ Clé API SportMonks manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# Seulement les ligues qui restent à traiter
LEAGUES_CONFIG = {
    'liga': {
        'name': 'Liga',
        'ts_file': 'ligaTeams.ts',
        'stats_file': 'la-ligaPlayersCompleteStats.ts',
        'seasons': {
            25659: "2025/2026",
            23621: "2024/2025",
            21694: "2023/2024"
        }
    },
    'serie-a': {
        'name': 'Serie A',
        'ts_file': 'serieATeams.ts',
        'stats_file': 'serie-aPlayersCompleteStats.ts',
        'seasons': {
            25533: "2025/2026",
            23746: "2024/2025",
            21818: "2023/2024"
        }
    },
    'bundesliga': {
        'name': 'Bundesliga',
        'ts_file': 'bundesligaTeams.ts',
        'stats_file': 'bundesligaPlayersCompleteStats.ts',
        'seasons': {
            25646: "2025/2026",
            23744: "2024/2025",
            21795: "2023/2024"
        }
    }
}

# Cache global
team_cache = {}
request_count = 0
last_request_time = time.time()

def rate_limit():
    """Gestion simple du rate limit"""
    global request_count, last_request_time
    
    request_count += 1
    
    # Pause tous les 10 appels
    if request_count % 10 == 0:
        time.sleep(2)
    
    # Pause longue tous les 50 appels
    if request_count % 50 == 0:
        print("    ⏸️ Pause anti rate-limit (30s)...")
        time.sleep(30)

def get_team_name(team_id):
    """Récupère le nom d'une équipe"""
    if team_id in team_cache:
        return team_cache[team_id]
    
    try:
        url = f"{BASE_URL}/teams/{team_id}"
        params = {'api_token': API_KEY}
        response = requests.get(url, params=params, timeout=10)
        rate_limit()
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                name = data['data'].get('name', f'Team_{team_id}')
                team_cache[team_id] = name
                return name
    except:
        pass
    
    return f'Team_{team_id}'

def get_player_stats(player_id, season_ids):
    """Récupère les stats d'un joueur"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{",".join(map(str, season_ids))}'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        rate_limit()
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        elif response.status_code == 429:
            print("      ⏳ Rate limit atteint, pause 60s...")
            time.sleep(60)
            return get_player_stats(player_id, season_ids)
    except:
        pass
    
    return []

def map_stats(stat_data, league_name, season_year, team_id=None):
    """Mappe les stats au format attendu"""
    stats = {
        'team': get_team_name(team_id) if team_id else None,
        'team_id': team_id,
        'league': league_name,
        'rating': None,
        'minutes': None,
        'appearences': None,
        'lineups': None,
        'captain': None,
        'touches': None,
        'goals': None,
        'assists': None,
        'xg': None,
        'xa': None,
        'shots': None,
        'shots_on_target': None,
        'hit_woodwork': None,
        'saves': None,
        'goals_conceded': None,
        'clean_sheets': None,
        'penalties_saved': None,
        'punches': None,
        'inside_box_saves': None,
        'passes': None,
        'passes_completed': None,
        'passes_accuracy': None,
        'key_passes': None,
        'crosses': None,
        'crosses_accurate': None,
        'tackles': None,
        'blocks': None,
        'interceptions': None,
        'clearances': None,
        'fouls': None,
        'fouls_drawn': None,
        'yellow_cards': None,
        'red_cards': None,
        'yellowred_cards': None,
        'ground_duels': None,
        'ground_duels_won': None,
        'aerial_duels': None,
        'aerial_duels_won': None,
        'duels': None,
        'duels_won': None,
        'dribbles': None,
        'dribbles_successful': None,
        'penalties': None,
        'penalties_won': None,
        'penalties_scored': None,
        'penalties_missed': None,
        'penalties_committed': None,
        'offsides': None,
        'ball_losses': None,
        'ball_recoveries': None,
        'mistakes_leading_to_goals': None,
        'crosses_accuracy': None
    }
    
    # Mapping simplifié
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
        219: 'ball_losses', 220: 'ball_recoveries', 215: 'mistakes_leading_to_goals',
        68: 'aerial_duels', 69: 'aerial_duels_won'
    }
    
    if 'details' in stat_data:
        for detail in stat_data['details']:
            type_id = detail.get('type', {}).get('id') if isinstance(detail.get('type'), dict) else None
            if type_id in type_map:
                value = detail.get('value', {})
                if isinstance(value, dict):
                    stats[type_map[type_id]] = value.get('total', value.get('average'))
                else:
                    stats[type_map[type_id]] = value
    
    # Calculer l'accuracy des crosses
    if stats['crosses'] and stats['crosses_accurate']:
        try:
            stats['crosses_accuracy'] = round((stats['crosses_accurate'] / stats['crosses']) * 100, 2)
        except:
            pass
    
    return stats

def get_teams(league_key):
    """Récupère les équipes d'une ligue"""
    config = LEAGUES_CONFIG[league_key]
    ts_path = Path(f'../data/{config["ts_file"]}')
    
    if not ts_path.exists():
        print(f"  ❌ Fichier {config['ts_file']} non trouvé")
        return []
    
    with open(ts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    teams = []
    team_pattern = r'\{\s*id:\s*(\d+),\s*name:\s*"([^"]+)"[^}]*?slug:\s*"([^"]+)"'
    
    for match in re.finditer(team_pattern, content, re.DOTALL):
        team_id = int(match.group(1))
        team_name = match.group(2)
        team_slug = match.group(3)
        
        # Extraire la section de cette équipe
        team_start = match.start()
        next_team = re.search(r'\n\s*\{\s*id:\s*\d+,\s*name:', content[team_start + 10:])
        team_end = team_start + next_team.start() if next_team else len(content)
        team_section = content[team_start:team_end]
        
        # Extraire les joueurs
        players = []
        player_pattern = r'\{\s*id:\s*(\d+)[^}]*?displayName:\s*"([^"]+)"[^}]*?position:\s*"([^"]+)"(?:[^}]*?jersey:\s*(\d+))?'
        
        for p_match in re.finditer(player_pattern, team_section, re.DOTALL):
            players.append({
                'id': int(p_match.group(1)),
                'displayName': p_match.group(2),
                'position': p_match.group(3),
                'jersey': int(p_match.group(4)) if p_match.group(4) else None
            })
        
        if players:
            teams.append({
                'id': team_id,
                'name': team_name,
                'slug': team_slug,
                'players': players
            })
    
    return teams

def process_league(league_key):
    """Traite une ligue complète"""
    config = LEAGUES_CONFIG[league_key]
    print(f"\n{'='*60}")
    print(f"🏆 {config['name']}")
    print(f"{'='*60}\n")
    
    teams = get_teams(league_key)
    if not teams:
        return
    
    print(f"📋 {len(teams)} équipes trouvées\n")
    
    all_stats = {}
    season_ids = list(config['seasons'].keys())
    
    for t_idx, team in enumerate(teams, 1):
        print(f"[{t_idx}/{len(teams)}] {team['name']} ({len(team['players'])} joueurs)")
        
        for p_idx, player in enumerate(team['players'], 1):
            print(f"  [{p_idx}/{len(team['players'])}] {player['displayName']}...", end=' ')
            
            # Récupérer les stats
            stats_data = get_player_stats(player['id'], season_ids)
            
            player_stats = {
                'displayName': player['displayName'],
                'position': player['position'],
                'jersey': player['jersey'],
                'stats': {}
            }
            
            # Organiser par saison
            for season_stat in stats_data:
                season_id = season_stat.get('season_id')
                if season_id in config['seasons']:
                    team_id = season_stat.get('team_id', team['id'])
                    mapped = map_stats(
                        season_stat,
                        config['name'],
                        config['seasons'][season_id],
                        team_id
                    )
                    
                    season_key = f"{config['seasons'][season_id]} ({config['name']}, {mapped['team']})"
                    player_stats['stats'][season_key] = mapped
            
            all_stats[player['id']] = player_stats
            print("✓")
        
        # Pause entre équipes
        time.sleep(1)
    
    # Sauvegarder
    save_stats(league_key, all_stats)
    print(f"\n✅ {config['name']} terminé!")

def save_stats(league_key, stats):
    """Sauvegarde les statistiques"""
    config = LEAGUES_CONFIG[league_key]
    output = Path(f"../data/{config['stats_file']}")
    
    ts_content = f"""// Stats complètes des joueurs de {config['name']}
// Généré le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

export interface PlayerSeasonStats {{
  team?: string;
  team_id?: number;
  league?: string;
  rating?: number | null;
  minutes?: number | null;
  appearences?: number | null;
  lineups?: number | null;
  captain?: number | null;
  touches?: number | null;
  goals?: number | null;
  assists?: number | null;
  xg?: number | null;
  xa?: number | null;
  shots?: number | null;
  shots_on_target?: number | null;
  hit_woodwork?: number | null;
  saves?: number | null;
  goals_conceded?: number | null;
  clean_sheets?: number | null;
  penalties_saved?: number | null;
  punches?: number | null;
  inside_box_saves?: number | null;
  passes?: number | null;
  passes_completed?: number | null;
  passes_accuracy?: number | null;
  key_passes?: number | null;
  crosses?: number | null;
  crosses_accurate?: number | null;
  tackles?: number | null;
  blocks?: number | null;
  interceptions?: number | null;
  clearances?: number | null;
  fouls?: number | null;
  fouls_drawn?: number | null;
  yellow_cards?: number | null;
  red_cards?: number | null;
  yellowred_cards?: number | null;
  ground_duels?: number | null;
  ground_duels_won?: number | null;
  aerial_duels?: number | null;
  aerial_duels_won?: number | null;
  duels?: number | null;
  duels_won?: number | null;
  dribbles?: number | null;
  dribbles_successful?: number | null;
  penalties?: number | null;
  penalties_won?: number | null;
  penalties_scored?: number | null;
  penalties_missed?: number | null;
  penalties_committed?: number | null;
  offsides?: number | null;
  ball_losses?: number | null;
  ball_recoveries?: number | null;
  mistakes_leading_to_goals?: number | null;
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

export const {league_key.replace('-', '')}PlayersStats: {{ [playerId: number]: PlayerRealStats }} = {json.dumps(stats, indent=2, ensure_ascii=False)};
"""
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"\n💾 Stats sauvegardées dans {output.name}")

def main():
    print("🚀 Mise à jour des ligues restantes")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Traiter Liga, Serie A et Bundesliga
    for league_key in ['liga', 'serie-a', 'bundesliga']:
        try:
            process_league(league_key)
        except KeyboardInterrupt:
            print("\n⚠️ Interruption")
            break
        except Exception as e:
            print(f"\n❌ Erreur pour {league_key}: {e}")
            continue
    
    print(f"\n✨ Terminé!")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()