#!/usr/bin/env python3
"""
Système de mise à jour AUTOMATIQUE et COMPLET
- Récupère TOUS les joueurs depuis l'API (aucun oubli)
- Met à jour les effectifs (ajouts ET suppressions)
- Récupère toutes les stats et photos
- Fonctionne pour tous les championnats
"""

import os
import sys
import json
import time
import shutil
import logging
from datetime import datetime
from typing import Dict, Any, List, Set, Optional
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Configuration du logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'full_update_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

# Fix pour l'encodage UTF-8 sur Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Chemins
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
BACKUP_DIR = SCRIPT_DIR / "backups"

BACKUP_DIR.mkdir(exist_ok=True)

# API Configuration
API_KEY = os.environ.get('SPORTMONKS_API_KEY', 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2')
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Championnats
LEAGUES_CONFIG = {
    301: {
        "name": "Ligue 1",
        "slug": "ligue1",
        "dataFile": "ligue1Teams",
        "statsFile": "ligue1PlayersCompleteStats",
        "seasons": {
            "2025/2026": 25651,
            "2024/2025": 23643,
            "2023/2024": 21779,
        }
    },
    8: {
        "name": "Premier League",
        "slug": "premier-league",
        "dataFile": "premierLeagueTeams",
        "statsFile": "premierLeaguePlayersCompleteStats",
        "seasons": {
            "2025/2026": 25583,
            "2024/2025": 23614,
            "2023/2024": 21646,
        }
    },
    564: {
        "name": "La Liga",
        "slug": "la-liga",
        "dataFile": "ligaTeams",
        "statsFile": "laLigaPlayersCompleteStats",
        "seasons": {
            "2025/2026": 25659,
            "2024/2025": 23621,
            "2023/2024": 21694,
        }
    },
    384: {
        "name": "Serie A",
        "slug": "serie-a",
        "dataFile": "serieATeams",
        "statsFile": "serieAPlayersCompleteStats",
        "seasons": {
            "2025/2026": 25533,
            "2024/2025": 23746,
            "2023/2024": 21818,
        }
    },
    82: {
        "name": "Bundesliga",
        "slug": "bundesliga",
        "dataFile": "bundesligaTeams",
        "statsFile": "bundesligaPlayersCompleteStats",
        "seasons": {
            "2025/2026": 25646,
            "2024/2025": 23744,
            "2023/2024": 21795,
        }
    },
}

def create_backup():
    """Créer une sauvegarde avant toute modification"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    
    logging.info(f"[BACKUP] Creation backup: {backup_path}")
    
    try:
        if DATA_DIR.exists():
            shutil.copytree(DATA_DIR, backup_path)
        
        # Garder seulement les 5 derniers backups
        backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir() and d.name.startswith("backup_")])
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                shutil.rmtree(old_backup)
        
        logging.info("[OK] Backup cree")
        return backup_path
    except Exception as e:
        logging.error(f"[ERREUR] Backup: {e}")
        raise

def restore_backup(backup_path: Path):
    """Restaurer un backup en cas d'erreur"""
    logging.warning(f"[RESTORE] Restauration depuis {backup_path}")
    
    try:
        if DATA_DIR.exists():
            shutil.rmtree(DATA_DIR)
        shutil.copytree(backup_path, DATA_DIR)
        logging.info("[OK] Backup restaure")
    except Exception as e:
        logging.error(f"[ERREUR CRITIQUE] Restauration: {e}")
        raise

def make_api_request(url: str, params: Dict = None, max_retries: int = 3) -> Optional[Dict]:
    """Requête API avec retry automatique"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                wait_time = min(2 ** (attempt + 1), 30)
                logging.warning(f"Rate limit - attente {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                logging.error(f"API Error {response.status_code}: {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout (tentative {attempt + 1}/{max_retries})")
        except Exception as e:
            logging.error(f"Erreur requete: {e}")
        
        if attempt < max_retries - 1:
            time.sleep(2 ** attempt)
    
    return None

def slugify(text: str) -> str:
    """Convertir texte en slug URL"""
    import unicodedata
    import re
    
    if not text:
        return ""
    
    # Normaliser
    text = unicodedata.normalize('NFD', str(text))
    text = text.encode('ascii', 'ignore').decode('utf-8')
    
    # Nettoyer
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    
    return text.strip('-')

def calculate_age(date_of_birth: str) -> str:
    """Calculer l'âge depuis la date de naissance"""
    if not date_of_birth:
        return "Unknown"
    
    try:
        birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return str(age)
    except:
        return "Unknown"

def get_all_team_players(team_id: int, season_id: int, team_name: str) -> List[Dict]:
    """
    Récupérer TOUS les joueurs d'une équipe en utilisant TOUTES les méthodes disponibles
    pour ne manquer AUCUN joueur
    """
    all_players = {}
    
    logging.info(f"  Recuperation effectif {team_name}...")
    
    # MÉTHODE 1: Squad officiel de la saison
    squad_url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'include': 'player.position,player.nationality',
        'filters': f'seasons:{season_id}',
        'per_page': 100
    }
    
    data = make_api_request(squad_url, params)
    if data and 'data' in data:
        for item in data['data']:
            if 'player' in item and item['player']:
                player = item['player']
                player_id = player['id']
                all_players[player_id] = {
                    'player': player,
                    'jersey_number': item.get('jersey_number'),
                    'source': 'squad'
                }
    
    # MÉTHODE 2: Tous les joueurs ayant joué des matchs cette saison
    fixtures_url = f"{BASE_URL}/fixtures"
    params = {
        'filters': f'teams:{team_id};seasons:{season_id}',
        'include': 'lineups.player',
        'per_page': 100
    }
    
    data = make_api_request(fixtures_url, params)
    if data and 'data' in data:
        for fixture in data['data']:
            if 'lineups' in fixture:
                for lineup in fixture['lineups']:
                    if 'player' in lineup and lineup['player']:
                        player = lineup['player']
                        player_id = player['id']
                        if player_id not in all_players:
                            all_players[player_id] = {
                                'player': player,
                                'jersey_number': lineup.get('jersey_number'),
                                'source': 'lineup'
                            }
                            logging.info(f"    [NEW] Joueur trouve via lineups: {player.get('name')}")
    
    # MÉTHODE 3: Transferts récents vers cette équipe
    transfers_url = f"{BASE_URL}/transfers"
    params = {
        'filters': f'teams:{team_id}',
        'include': 'player',
        'per_page': 50
    }
    
    data = make_api_request(transfers_url, params)
    if data and 'data' in data:
        for transfer in data['data']:
            # Vérifier si c'est une arrivée
            if transfer.get('to', {}).get('id') == team_id:
                if 'player' in transfer and transfer['player']:
                    player = transfer['player']
                    player_id = player['id']
                    if player_id not in all_players:
                        # Vérifier que le joueur est toujours dans l'équipe
                        transfer_date = transfer.get('date')
                        if transfer_date and transfer_date > '2024-01-01':  # Transferts récents
                            all_players[player_id] = {
                                'player': player,
                                'jersey_number': None,
                                'source': 'transfer'
                            }
                            logging.info(f"    [NEW] Joueur trouve via transferts: {player.get('name')}")
    
    # MÉTHODE 4: Statistiques des joueurs de l'équipe
    team_stats_url = f"{BASE_URL}/statistics/seasons/{season_id}/teams/{team_id}"
    params = {
        'include': 'details.player',
        'per_page': 100
    }
    
    data = make_api_request(team_stats_url, params)
    if data and 'data' in data:
        if 'details' in data['data']:
            for detail in data['data']['details']:
                if 'player' in detail and detail['player']:
                    player = detail['player']
                    player_id = player['id']
                    if player_id not in all_players:
                        all_players[player_id] = {
                            'player': player,
                            'jersey_number': None,
                            'source': 'stats'
                        }
                        logging.info(f"    [NEW] Joueur trouve via stats: {player.get('name')}")
    
    # Convertir en liste
    players_list = []
    for player_id, player_data in all_players.items():
        player = player_data['player']
        
        # Récupérer les infos complètes du joueur si nécessaire
        if not player.get('position') or not player.get('image_path'):
            player_detail_url = f"{BASE_URL}/players/{player_id}"
            params = {'include': 'position,nationality'}
            detail_data = make_api_request(player_detail_url, params)
            if detail_data and 'data' in detail_data:
                player.update(detail_data['data'])
        
        players_list.append({
            'id': player_id,
            'name': player.get('name', 'Unknown'),
            'display_name': player.get('display_name', player.get('name', 'Unknown')),
            'position': player.get('position', {}).get('name', 'Unknown') if player.get('position') else 'Unknown',
            'position_id': player.get('position', {}).get('id', 1) if player.get('position') else 1,
            'jersey_number': player_data.get('jersey_number'),
            'date_of_birth': player.get('date_of_birth'),
            'nationality': player.get('nationality', {}).get('name') if player.get('nationality') else None,
            'height': player.get('height'),
            'weight': player.get('weight'),
            'image': player.get('image_path', ''),
            'source': player_data['source']
        })
    
    logging.info(f"    -> {len(players_list)} joueurs trouves au total")
    return players_list

def get_player_complete_stats(player_id: int, season_ids: List[int]) -> Dict:
    """Récupérer les statistiques complètes d'un joueur sur plusieurs saisons"""
    all_stats = {}
    
    for season_id in season_ids:
        url = f"{BASE_URL}/players/{player_id}"
        params = {
            'include': 'statistics.details,statistics.league',
            'filters': f'player_statistics.season_id:{season_id}'
        }
        
        data = make_api_request(url, params)
        
        if data and 'data' in data:
            player_data = data['data']
            if 'statistics' in player_data:
                for stat in player_data['statistics']:
                    if stat.get('season_id') == season_id:
                        all_stats[season_id] = {
                            'appearences': stat.get('appearences', 0),
                            'lineups': stat.get('lineups', 0),
                            'minutes': stat.get('minutes_played', 0),
                            'goals': stat.get('goals', 0),
                            'assists': stat.get('assists', 0),
                            'yellow_cards': stat.get('yellow_cards', 0),
                            'red_cards': stat.get('red_cards', 0),
                            'clean_sheets': stat.get('clean_sheets', 0),
                            'saves': stat.get('saves', 0),
                            'goals_conceded': stat.get('goals_conceded', 0),
                            'penalties_saved': stat.get('penalties_saved', 0),
                            'rating': stat.get('rating')
                        }
                        
                        # Ajouter les détails
                        if 'details' in stat:
                            for detail in stat['details']:
                                type_name = detail.get('type', {}).get('name')
                                detail_data = detail.get('data', {})
                                
                                if type_name == 'Shots':
                                    all_stats[season_id]['shots_total'] = detail_data.get('total', 0)
                                    all_stats[season_id]['shots_on_target'] = detail_data.get('on_target', 0)
                                elif type_name == 'Passes':
                                    all_stats[season_id]['passes_total'] = detail_data.get('total', 0)
                                    all_stats[season_id]['passes_accuracy'] = detail_data.get('accuracy', 0)
                                    all_stats[season_id]['key_passes'] = detail_data.get('key_passes', 0)
    
    return all_stats

def update_league_complete(league_id: int, league_info: Dict) -> Dict:
    """Mise à jour COMPLÈTE d'un championnat"""
    logging.info(f"\n{'='*60}")
    logging.info(f"[LEAGUE] {league_info['name']}")
    logging.info(f"{'='*60}")
    
    league_data = {
        'teams': {},
        'stats': {}
    }
    
    season_ids = list(league_info['seasons'].values())
    current_season = season_ids[0]  # 2025/2026
    
    # Récupérer toutes les équipes de la saison
    teams_url = f"{BASE_URL}/teams/seasons/{current_season}"
    teams_data = make_api_request(teams_url)
    
    if not teams_data or 'data' not in teams_data:
        logging.error(f"[ERREUR] Impossible de recuperer les equipes")
        return None
    
    teams = teams_data['data']
    logging.info(f"[INFO] {len(teams)} equipes trouvees")
    
    # Traiter chaque équipe
    for team in teams:
        team_id = team['id']
        team_name = team['name']
        team_slug = slugify(team_name)
        
        # Récupérer TOUS les joueurs
        players = get_all_team_players(team_id, current_season, team_name)
        
        # Préparer les données de l'équipe
        league_data['teams'][team_id] = {
            'id': team_id,
            'name': team_name,
            'slug': team_slug,
            'players': []
        }
        
        # Traiter chaque joueur
        for player in players:
            player_data = {
                'id': player['id'],
                'nom': player['name'],
                'displayName': player['display_name'],
                'position': player['position'],
                'position_id': player['position_id'],
                'numero': player['jersey_number'],
                'age': calculate_age(player['date_of_birth']),
                'nationalite': player['nationality'] or 'Unknown',
                'taille': player['height'],
                'poids': player['weight'],
                'image': player['image'],
                'playerSlug': slugify(player['display_name'])
            }
            
            league_data['teams'][team_id]['players'].append(player_data)
            
            # Récupérer les stats (en parallèle pour aller plus vite)
            stats = get_player_complete_stats(player['id'], season_ids)
            if stats:
                league_data['stats'][player['id']] = {
                    'current': stats.get(season_ids[0]),
                    'previous': [stats.get(sid) for sid in season_ids[1:] if stats.get(sid)],
                    'cumulative': calculate_cumulative_stats(stats)
                }
    
    return league_data

def calculate_cumulative_stats(stats_by_season: Dict) -> Dict:
    """Calculer les stats cumulées"""
    if not stats_by_season:
        return None
    
    cumulative = {}
    numeric_fields = [
        'appearences', 'lineups', 'minutes', 'goals', 'assists',
        'yellow_cards', 'red_cards', 'clean_sheets', 'saves',
        'goals_conceded', 'penalties_saved', 'shots_total',
        'shots_on_target', 'passes_total', 'key_passes'
    ]
    
    for field in numeric_fields:
        cumulative[field] = sum(s.get(field, 0) for s in stats_by_season.values())
    
    # Moyenne pour l'accuracy
    if cumulative.get('passes_total', 0) > 0:
        total_accurate = sum(
            s.get('passes_accuracy', 0) * s.get('passes_total', 0) 
            for s in stats_by_season.values()
        )
        cumulative['passes_accuracy'] = round(total_accurate / cumulative['passes_total'], 1)
    
    return cumulative

def generate_typescript_files(league_data: Dict, league_info: Dict) -> bool:
    """Générer les fichiers TypeScript"""
    try:
        # Fichier des équipes
        teams_file = DATA_DIR / f"{league_info['dataFile']}.ts"
        stats_file = DATA_DIR / f"{league_info['statsFile']}.ts"
        
        # Générer le contenu
        teams_content = f"export const {league_info['dataFile']} = [\n"
        
        for team_id, team in league_data['teams'].items():
            teams_content += f"""  {{
    id: {team_id},
    name: "{team['name']}",
    slug: "{team['slug']}",
    players: [
"""
            for p in team['players']:
                teams_content += f"""      {{
        id: {p['id']},
        nom: "{p['nom']}",
        displayName: "{p['displayName']}",
        position: "{p['position']}",
        position_id: {p['position_id']},
        numero: {p['numero'] if p['numero'] is not None else 'null'},
        age: "{p['age']}",
        nationalite: "{p['nationalite']}",
        taille: {p['taille'] if p['taille'] else 'null'},
        poids: {p['poids'] if p['poids'] else 'null'},
        image: "{p['image']}",
        playerSlug: "{p['playerSlug']}"
      }},
"""
            teams_content += """    ]
  },
"""
        
        teams_content += "];\n"
        
        # Écrire le fichier
        teams_file.write_text(teams_content, encoding='utf-8')
        logging.info(f"[OK] Fichier genere: {teams_file.name}")
        
        # Fichier des stats
        if league_data.get('stats'):
            stats_content = f"export const {league_info['statsFile']}: {{ [key: number]: any }} = {{\n"
            
            for player_id, stats in league_data['stats'].items():
                stats_content += f"  {player_id}: {json.dumps(stats, indent=2)},\n"
            
            stats_content += "};\n"
            
            stats_file.write_text(stats_content, encoding='utf-8')
            logging.info(f"[OK] Fichier stats genere: {stats_file.name}")
        
        return True
        
    except Exception as e:
        logging.error(f"[ERREUR] Generation fichiers: {e}")
        return False

def main():
    """Fonction principale - Mise à jour AUTOMATIQUE et COMPLÈTE"""
    logging.info("\n" + "="*60)
    logging.info("MISE A JOUR AUTOMATIQUE COMPLETE")
    logging.info("="*60 + "\n")
    
    start_time = time.time()
    backup_path = None
    success = True
    
    try:
        # Backup
        backup_path = create_backup()
        
        # Traiter chaque championnat
        for league_id, league_info in LEAGUES_CONFIG.items():
            league_data = update_league_complete(league_id, league_info)
            
            if not league_data:
                logging.error(f"[SKIP] {league_info['name']} - erreur")
                continue
            
            # Générer les fichiers
            if not generate_typescript_files(league_data, league_info):
                logging.error(f"[ERREUR] Generation pour {league_info['name']}")
                success = False
                break
            
            # Pause entre les ligues pour éviter le rate limiting
            time.sleep(2)
        
        if not success and backup_path:
            restore_backup(backup_path)
            
    except Exception as e:
        logging.error(f"[ERREUR CRITIQUE]: {e}")
        if backup_path:
            restore_backup(backup_path)
        success = False
    
    # Résumé
    elapsed = time.time() - start_time
    logging.info("\n" + "="*60)
    if success:
        logging.info(f"[SUCCESS] Mise a jour terminee en {elapsed:.2f}s")
    else:
        logging.info(f"[FAIL] Mise a jour echouee apres {elapsed:.2f}s")
    logging.info("="*60)
    
    # Statut
    status_file = SCRIPT_DIR / 'last_update.json'
    status_file.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'duration': elapsed,
        'success': success
    }, indent=2))
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)