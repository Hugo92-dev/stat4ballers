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
    print("❌ Clé API SportMonks manquante dans .env.local")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

# Configuration des championnats et saisons
LEAGUES_CONFIG = {
    'ligue1': {
        'name': 'Ligue 1',
        'folder': 'ligue1_2025_2026',
        'ts_file': 'ligue1Teams.ts',
        'seasons': {
            25651: "2025/2026",
            23643: "2024/2025", 
            21779: "2023/2024"
        }
    },
    'premier-league': {
        'name': 'Premier League',
        'folder': 'premier-league_2025_2026',
        'ts_file': 'premierLeagueTeams.ts',
        'seasons': {
            25583: "2025/2026",
            23614: "2024/2025",
            21646: "2023/2024"
        }
    },
    'liga': {
        'name': 'Liga',
        'folder': 'liga_2025_2026',
        'ts_file': 'ligaTeams.ts',
        'seasons': {
            25659: "2025/2026",
            23621: "2024/2025",
            21694: "2023/2024"
        }
    },
    'serie-a': {
        'name': 'Serie A',
        'folder': 'serie-a_2025_2026',
        'ts_file': 'serieATeams.ts',
        'seasons': {
            25533: "2025/2026",
            23746: "2024/2025",
            21818: "2023/2024"
        }
    },
    'bundesliga': {
        'name': 'Bundesliga',
        'folder': 'bundesliga_2025_2026',
        'ts_file': 'bundesligaTeams.ts',
        'seasons': {
            25646: "2025/2026",
            23744: "2024/2025",
            21795: "2023/2024"
        }
    }
}

# Cache pour les noms d'équipes
team_cache = {}

def get_team_name(team_id):
    """Récupère le nom d'une équipe (avec cache)"""
    if team_id in team_cache:
        return team_cache[team_id]
    
    try:
        url = f"{BASE_URL}/teams/{team_id}"
        params = {'api_token': API_KEY}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                name = data['data'].get('name', f'Team_{team_id}')
                team_cache[team_id] = name
                return name
    except:
        pass
    
    name = f'Team_{team_id}'
    team_cache[team_id] = name
    return name

def get_player_all_stats(player_id, season_ids):
    """Récupère toutes les stats d'un joueur pour les saisons spécifiées"""
    season_ids_str = ",".join(map(str, season_ids))
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{season_ids_str}'
    }
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data:
                    return data['data']
            elif response.status_code == 429:
                wait_time = min(60 * (2 ** attempt), 300)
                print(f"    ⏳ Rate limit, pause {wait_time}s...")
                time.sleep(wait_time)
                continue
            elif response.status_code == 404:
                return []
                
        except requests.exceptions.Timeout:
            print(f"    ⚠️ Timeout pour joueur {player_id}, tentative {attempt + 1}/{max_retries}")
            if attempt < max_retries - 1:
                time.sleep(5)
        except Exception as e:
            print(f"    ⚠️ Erreur pour joueur {player_id}: {e}")
            if attempt < max_retries - 1:
                time.sleep(5)
    
    return []

def map_stats_to_format(stat_data, season_info, team_id=None):
    """Mappe les stats SportMonks vers notre format"""
    
    # Initialiser toutes les stats
    stats = {
        'team': get_team_name(team_id) if team_id else None,
        'team_id': team_id,
        'league': season_info.get('league'),
        'season': season_info.get('year'),
        
        # Stats générales
        'rating': None,
        'minutes': None,
        'appearences': None,
        'lineups': None,
        'captain': None,
        'substitutions': None,
        'touches': None,
        
        # Stats offensives
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
        
        # Stats de passes
        'passes': None,
        'passes_completed': None,
        'passes_accuracy': None,
        'key_passes': None,
        'crosses': None,
        'crosses_accurate': None,
        
        # Stats de dribbles
        'dribbles': None,
        'dribbles_successful': None,
        
        # Stats défensives
        'tackles': None,
        'blocks': None,
        'interceptions': None,
        'clearances': None,
        'ground_duels': None,
        'ground_duels_won': None,
        'aerial_duels': None,
        'aerial_duels_won': None,
        
        # Discipline
        'fouls': None,
        'fouls_drawn': None,
        'yellow_cards': None,
        'red_cards': None,
        'yellowred_cards': None,
        'penalties_committed': None,
        
        # Autres
        'ball_losses': None,
        'ball_recoveries': None,
        'mistakes_leading_to_goals': None,
        
        # Stats gardien
        'saves': None,
        'punches': None,
        'inside_box_saves': None,
        'clean_sheets': None,
        'goals_conceded': None,
        'penalties_saved': None
    }
    
    # Mapping des types SportMonks
    type_mapping = {
        # Général
        52: 'rating',
        79: 'minutes',
        113: 'appearences',
        114: 'lineups',
        118: 'captain',
        
        # Offensif
        208: 'goals',
        209: 'assists',
        42: 'shots',
        86: 'shots_on_target',
        576: 'xg',
        577: 'xa',
        84: 'penalties_scored',
        83: 'penalties_missed',
        85: 'penalties',
        218: 'penalties_won',
        41: 'offsides',
        81: 'hit_woodwork',
        
        # Passes
        124: 'passes',
        125: 'passes_completed',
        126: 'passes_accuracy',
        147: 'key_passes',
        45: 'crosses',
        46: 'crosses_accurate',
        
        # Dribbles
        127: 'dribbles',
        128: 'dribbles_successful',
        
        # Défensif
        88: 'tackles',
        74: 'blocks',
        75: 'interceptions',
        78: 'clearances',
        68: 'aerial_duels',
        69: 'aerial_duels_won',
        
        # Discipline
        105: 'fouls',
        106: 'fouls_drawn',
        56: 'yellow_cards',
        57: 'red_cards',
        58: 'yellowred_cards',
        217: 'penalties_committed',
        
        # Gardien
        206: 'saves',
        207: 'punches',
        130: 'clean_sheets',
        131: 'goals_conceded',
        240: 'penalties_saved',
        129: 'inside_box_saves',
        
        # Autres
        219: 'ball_losses',
        220: 'ball_recoveries',
        96: 'substitutions',
        192: 'touches',
        215: 'mistakes_leading_to_goals'
    }
    
    # Appliquer les mappings
    if 'details' in stat_data:
        for detail in stat_data['details']:
            type_id = detail.get('type', {}).get('id') if isinstance(detail.get('type'), dict) else None
            if type_id and type_id in type_mapping:
                field = type_mapping[type_id]
                value = detail.get('value', {})
                
                # Gérer différents formats de valeur
                if isinstance(value, dict):
                    stats[field] = value.get('total', value.get('average'))
                else:
                    stats[field] = value
    
    # Nettoyer les valeurs
    for key in stats:
        if stats[key] == '':
            stats[key] = None
        elif isinstance(stats[key], str) and key not in ['team', 'league', 'season']:
            try:
                if '.' in stats[key]:
                    stats[key] = float(stats[key])
                else:
                    stats[key] = int(stats[key])
            except:
                pass
                
    return stats

def get_league_teams(league_key):
    """Récupère les équipes d'un championnat depuis le fichier TypeScript"""
    config = LEAGUES_CONFIG[league_key]
    ts_path = Path(f'../data/{config["ts_file"]}')
    
    if not ts_path.exists():
        print(f"  ⚠️ Fichier {config['ts_file']} non trouvé")
        return []
    
    with open(ts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    teams = []
    
    # Rechercher toutes les équipes dans le fichier
    team_pattern = r'\{\s*id:\s*(\d+),\s*name:\s*"([^"]+)"[^}]*?slug:\s*"([^"]+)"'
    matches = re.finditer(team_pattern, content, re.DOTALL)
    
    for match in matches:
        team_id = int(match.group(1))
        team_name = match.group(2)
        team_slug = match.group(3)
        
        # Extraire les joueurs de cette équipe
        team_start = match.start()
        next_team = re.search(r'\n\s*\{\s*id:\s*\d+,\s*name:', content[team_start + 10:])
        team_end = team_start + next_team.start() if next_team else len(content)
        
        team_section = content[team_start:team_end]
        
        # Extraire les joueurs
        players = []
        player_pattern = r'\{\s*id:\s*(\d+)[^}]*?displayName:\s*"([^"]+)"[^}]*?position:\s*"([^"]+)"(?:[^}]*?jersey:\s*(\d+))?'
        player_matches = re.finditer(player_pattern, team_section, re.DOTALL)
        
        for p_match in player_matches:
            player_info = {
                'id': int(p_match.group(1)),
                'displayName': p_match.group(2),
                'position': p_match.group(3),
                'jersey': int(p_match.group(4)) if p_match.group(4) else None
            }
            players.append(player_info)
        
        if players:  # Ne garder que les équipes avec des joueurs
            teams.append({
                'id': team_id,
                'name': team_name,
                'slug': team_slug,
                'players': players
            })
    
    return teams

def process_team(team, league_key):
    """Traite une équipe et récupère les stats de tous ses joueurs"""
    config = LEAGUES_CONFIG[league_key]
    season_ids = list(config['seasons'].keys())
    
    print(f"\n  📊 {team['name']} ({len(team['players'])} joueurs)")
    
    team_stats = {}
    
    for i, player in enumerate(team['players'], 1):
        print(f"    [{i}/{len(team['players'])}] {player['displayName']}...", end='')
        
        # Récupérer les stats du joueur
        stats_data = get_player_all_stats(player['id'], season_ids)
        
        player_stats = {
            'displayName': player['displayName'],
            'position': player['position'],
            'jersey': player['jersey'],
            'stats': {}
        }
        
        # Organiser par saison
        for season_stat in stats_data:
            season_id = season_stat.get('season_id')
            if season_id and season_id in config['seasons']:
                season_info = {
                    'league': config['name'],
                    'year': config['seasons'][season_id]
                }
                
                # Obtenir l'ID de l'équipe pour cette saison
                team_id = season_stat.get('team_id', team['id'])
                
                # Mapper les stats
                mapped_stats = map_stats_to_format(
                    season_stat, 
                    season_info,
                    team_id
                )
                
                # Clé pour cette saison
                season_key = f"{config['seasons'][season_id]} ({config['name']}, {mapped_stats['team']})"
                player_stats['stats'][season_key] = mapped_stats
                
        team_stats[player['id']] = player_stats
        print(" ✓")
        
        # Pause anti rate-limit
        time.sleep(0.5)
    
    return team_stats

def save_team_stats(team_stats, team_slug, league_key):
    """Sauvegarde les stats d'une équipe"""
    config = LEAGUES_CONFIG[league_key]
    
    # Créer le fichier TypeScript pour cette équipe
    output_file = Path(f"../data/{league_key}PlayersStats_{team_slug}.ts")
    
    ts_content = f"""// Stats complètes des joueurs de {team_slug}
// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

export interface PlayerSeasonStats {{
  team?: string;
  team_id?: number;
  league?: string;
  season?: string;
  rating?: number | null;
  minutes?: number | null;
  appearences?: number | null;
  lineups?: number | null;
  captain?: number | null;
  substitutions?: number | null;
  touches?: number | null;
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
  passes?: number | null;
  passes_completed?: number | null;
  passes_accuracy?: number | null;
  key_passes?: number | null;
  crosses?: number | null;
  crosses_accurate?: number | null;
  dribbles?: number | null;
  dribbles_successful?: number | null;
  tackles?: number | null;
  blocks?: number | null;
  interceptions?: number | null;
  clearances?: number | null;
  ground_duels?: number | null;
  ground_duels_won?: number | null;
  aerial_duels?: number | null;
  aerial_duels_won?: number | null;
  fouls?: number | null;
  fouls_drawn?: number | null;
  yellow_cards?: number | null;
  red_cards?: number | null;
  yellowred_cards?: number | null;
  penalties_committed?: number | null;
  ball_losses?: number | null;
  ball_recoveries?: number | null;
  mistakes_leading_to_goals?: number | null;
  saves?: number | null;
  punches?: number | null;
  inside_box_saves?: number | null;
  clean_sheets?: number | null;
  goals_conceded?: number | null;
  penalties_saved?: number | null;
}}

export interface PlayerRealStats {{
  displayName: string;
  position: string;
  jersey?: number;
  stats: {{
    [seasonKey: string]: PlayerSeasonStats | null;
  }};
}}

export const {team_slug.replace('-', '_')}PlayersStats: {{ [playerId: number]: PlayerRealStats }} = {json.dumps(team_stats, indent=2, ensure_ascii=False)};
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"    💾 Stats sauvegardées dans {output_file.name}")
    
    # Sauvegarder aussi en JSON pour backup
    json_file = Path(f"../data/{config['folder']}/{team_slug}_stats.json")
    json_file.parent.mkdir(exist_ok=True)
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(team_stats, f, indent=2, ensure_ascii=False)

def update_league(league_key):
    """Met à jour toutes les équipes d'un championnat"""
    print(f"\n{'='*60}")
    print(f"🏆 Mise à jour {LEAGUES_CONFIG[league_key]['name']}")
    print(f"{'='*60}")
    
    # Récupérer toutes les équipes
    teams = get_league_teams(league_key)
    
    if not teams:
        print(f"  ⚠️ Aucune équipe trouvée pour {league_key}")
        return
    
    print(f"  📋 {len(teams)} équipes trouvées")
    
    # Traiter chaque équipe
    for team in teams:
        try:
            team_stats = process_team(team, league_key)
            if team_stats:
                save_team_stats(team_stats, team['slug'], league_key)
        except Exception as e:
            print(f"  ❌ Erreur pour {team['name']}: {e}")
            continue
        
        # Pause entre les équipes
        time.sleep(2)
    
    print(f"\n✅ {LEAGUES_CONFIG[league_key]['name']} terminé!")

def main():
    """Fonction principale"""
    print("🚀 Démarrage de la mise à jour complète des stats")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ordre de traitement des ligues
    leagues_order = ['ligue1', 'premier-league', 'liga', 'serie-a', 'bundesliga']
    
    for league_key in leagues_order:
        try:
            update_league(league_key)
        except Exception as e:
            print(f"\n❌ Erreur critique pour {league_key}: {e}")
            continue
    
    print(f"\n✨ Mise à jour complète terminée!")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()