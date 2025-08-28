#!/usr/bin/env python3
import json
import requests
import time
from dotenv import load_dotenv
import os
import sys
import re
from datetime import datetime
from pathlib import Path
import concurrent.futures
from typing import Dict, List, Optional

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
        'stats_file': 'ligue1PlayersCompleteStats.ts',
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
        'stats_file': 'premier-leaguePlayersCompleteStats.ts',
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
        'stats_file': 'la-ligaPlayersCompleteStats.ts',
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
        'stats_file': 'serie-aPlayersCompleteStats.ts',
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
        'stats_file': 'bundesligaPlayersCompleteStats.ts',
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
        response = requests.get(url, params=params, timeout=10)
        
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

def get_player_all_stats(player_id: int, season_ids: List[int]) -> List[Dict]:
    """Récupère toutes les stats d'un joueur pour les saisons spécifiées"""
    season_ids_str = ",".join(map(str, season_ids))
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{season_ids_str}'
    }
    
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=20)
            
            if response.status_code == 200:
                data = response.json()
                return data.get('data', [])
            elif response.status_code == 429:
                wait_time = 30 * (attempt + 1)
                time.sleep(wait_time)
            elif response.status_code == 404:
                return []
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2)
    
    return []

def map_stats_to_format(stat_data: Dict, league_name: str, season_year: str, team_id: Optional[int] = None) -> Dict:
    """Mappe les stats SportMonks vers notre format"""
    
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
    
    # Mapping des types SportMonks
    type_mapping = {
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
    
    # Appliquer les mappings
    if 'details' in stat_data:
        for detail in stat_data['details']:
            type_id = detail.get('type', {}).get('id') if isinstance(detail.get('type'), dict) else None
            if type_id and type_id in type_mapping:
                field = type_mapping[type_id]
                value = detail.get('value', {})
                
                if isinstance(value, dict):
                    stats[field] = value.get('total', value.get('average'))
                else:
                    stats[field] = value
    
    # Calculer les stats composées
    if stats['crosses'] and stats['crosses_accurate']:
        try:
            stats['crosses_accuracy'] = round((stats['crosses_accurate'] / stats['crosses']) * 100, 2)
        except:
            pass
    
    # Nettoyer les valeurs
    for key in stats:
        if stats[key] == '':
            stats[key] = None
        elif isinstance(stats[key], str) and key not in ['team', 'league']:
            try:
                stats[key] = float(stats[key]) if '.' in stats[key] else int(stats[key])
            except:
                pass
                
    return stats

def get_league_teams(league_key: str) -> List[Dict]:
    """Récupère les équipes d'un championnat depuis le fichier TypeScript"""
    config = LEAGUES_CONFIG[league_key]
    ts_path = Path(f'../data/{config["ts_file"]}')
    
    if not ts_path.exists():
        print(f"  ⚠️ Fichier {config['ts_file']} non trouvé")
        return []
    
    with open(ts_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    teams = []
    
    # Pattern pour trouver toutes les équipes
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
        
        if players:
            teams.append({
                'id': team_id,
                'name': team_name,
                'slug': team_slug,
                'players': players
            })
    
    return teams

def check_already_processed(team_slug: str, league_key: str) -> bool:
    """Vérifie si une équipe a déjà été traitée récemment"""
    stats_file = Path(f"../data/{league_key}PlayersStats_{team_slug}.ts")
    
    if stats_file.exists():
        mtime = datetime.fromtimestamp(stats_file.stat().st_mtime)
        age_minutes = (datetime.now() - mtime).total_seconds() / 60
        
        # Si le fichier a été modifié dans les 2 dernières heures, on le considère comme traité
        if age_minutes < 120:
            return True
    
    return False

def process_team(team: Dict, league_key: str) -> Optional[Dict]:
    """Traite une équipe et récupère les stats de tous ses joueurs"""
    config = LEAGUES_CONFIG[league_key]
    season_ids = list(config['seasons'].keys())
    
    # Vérifier si déjà traité
    if check_already_processed(team['slug'], league_key):
        print(f"  ⏭️ {team['name']} déjà traité récemment")
        return None
    
    print(f"  📊 {team['name']} ({len(team['players'])} joueurs)...")
    
    all_players_stats = {}
    
    for player in team['players']:
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
                team_id = season_stat.get('team_id', team['id'])
                
                mapped_stats = map_stats_to_format(
                    season_stat, 
                    config['name'],
                    config['seasons'][season_id],
                    team_id
                )
                
                season_key = f"{config['seasons'][season_id]} ({config['name']}, {mapped_stats['team']})"
                player_stats['stats'][season_key] = mapped_stats
        
        all_players_stats[player['id']] = player_stats
        
        # Petite pause anti rate-limit
        time.sleep(0.3)
    
    return all_players_stats

def save_league_stats(league_key: str, all_teams_stats: Dict):
    """Sauvegarde toutes les stats d'un championnat dans un fichier TypeScript unifié"""
    config = LEAGUES_CONFIG[league_key]
    output_file = Path(f"../data/{config['stats_file']}")
    
    ts_content = f"""// Stats complètes des joueurs de {config['name']}
// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

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

export const {league_key.replace('-', '').replace('1', 'Un')}PlayersStats: {{ [playerId: number]: PlayerRealStats }} = {json.dumps(all_teams_stats, indent=2, ensure_ascii=False)};
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"    💾 Stats consolidées sauvegardées dans {output_file.name}")

def update_league(league_key: str):
    """Met à jour toutes les équipes d'un championnat"""
    print(f"\n{'='*60}")
    print(f"🏆 Mise à jour {LEAGUES_CONFIG[league_key]['name']}")
    print(f"{'='*60}")
    
    # Récupérer toutes les équipes
    teams = get_league_teams(league_key)
    
    if not teams:
        print(f"  ⚠️ Aucune équipe trouvée pour {league_key}")
        return
    
    print(f"  📋 {len(teams)} équipes trouvées\n")
    
    all_teams_stats = {}
    
    # Traiter chaque équipe
    for i, team in enumerate(teams, 1):
        print(f"  [{i}/{len(teams)}]", end=" ")
        try:
            team_stats = process_team(team, league_key)
            if team_stats:
                # Fusionner les stats
                all_teams_stats.update(team_stats)
                print(f"    ✅ {len(team_stats)} joueurs traités")
        except Exception as e:
            print(f"    ❌ Erreur: {e}")
            continue
        
        # Pause entre les équipes
        time.sleep(1)
    
    # Sauvegarder toutes les stats dans un fichier unifié
    if all_teams_stats:
        save_league_stats(league_key, all_teams_stats)
    
    print(f"\n✅ {LEAGUES_CONFIG[league_key]['name']} terminé!")

def main():
    """Fonction principale"""
    print("🚀 Démarrage de la mise à jour optimisée des stats")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ordre de traitement des ligues
    leagues_order = ['ligue1', 'premier-league', 'liga', 'serie-a', 'bundesliga']
    
    # Demander confirmation pour continuer
    print("\n📋 Ligues à traiter:")
    for league in leagues_order:
        print(f"  • {LEAGUES_CONFIG[league]['name']}")
    
    for league_key in leagues_order:
        try:
            update_league(league_key)
        except KeyboardInterrupt:
            print("\n⚠️ Interruption utilisateur")
            break
        except Exception as e:
            print(f"\n❌ Erreur critique pour {league_key}: {e}")
            continue
    
    print(f"\n✨ Mise à jour terminée!")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()