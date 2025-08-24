#!/usr/bin/env python3
"""
Système de mise à jour COMPLET qui gère :
- Tous les joueurs de l'effectif actuel
- Les joueurs partis (à retirer)
- Les statistiques complètes
- Les photos et infos des joueurs
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
        logging.FileHandler(LOG_DIR / f'complete_update_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Chemins importants
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
BACKUP_DIR = SCRIPT_DIR / "backups"

BACKUP_DIR.mkdir(exist_ok=True)

API_KEY = os.environ.get('SPORTMONKS_API_KEY', 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2')
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Configuration des championnats
TOP_5_LEAGUES = {
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
    """Créer une sauvegarde complète"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    
    logging.info(f"[BACKUP] Creation du backup dans {backup_path}")
    
    try:
        shutil.copytree(DATA_DIR, backup_path)
        
        # Garder seulement les 5 derniers backups
        backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir() and d.name.startswith("backup_")])
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                shutil.rmtree(old_backup)
                logging.info(f"[CLEAN] Ancien backup supprime: {old_backup.name}")
        
        logging.info(f"[OK] Backup cree avec succes")
        return backup_path
    except Exception as e:
        logging.error(f"[ERREUR] Erreur lors de la creation du backup: {e}")
        raise

def make_api_request(url: str, params: Dict = None) -> Optional[Dict]:
    """Faire une requête API avec retry"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                wait_time = min(2 ** attempt, 10)
                logging.warning(f"Rate limit, attente {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                logging.error(f"Erreur API {response.status_code}: {response.text}")
                return None
        except Exception as e:
            logging.error(f"Erreur requete: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    return None

def slugify(text: str) -> str:
    """Convertir un texte en slug URL"""
    import unicodedata
    import re
    
    if not text:
        return ""
    
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    
    return text.strip('-')

def get_complete_squad(team_id: int, season_id: int) -> List[Dict]:
    """
    Récupérer l'effectif COMPLET d'une équipe
    Utilise plusieurs méthodes pour s'assurer d'avoir tous les joueurs
    """
    all_players = {}
    
    # Méthode 1: squads/teams (méthode principale)
    squad_url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'include': 'player.position,player.nationality',
        'filters': f'seasons:{season_id}'
    }
    
    data = make_api_request(squad_url, params)
    if data and 'data' in data:
        for squad_member in data['data']:
            if 'player' in squad_member and squad_member['player']:
                player = squad_member['player']
                player_id = player['id']
                all_players[player_id] = {
                    'squad_data': squad_member,
                    'player_data': player
                }
    
    # Méthode 2: players/teams (autre endpoint)
    players_url = f"{BASE_URL}/players/teams/{team_id}"
    params = {
        'include': 'position',
        'per_page': 100  # S'assurer d'avoir tous les joueurs
    }
    
    data = make_api_request(players_url, params)
    if data and 'data' in data:
        for player in data['data']:
            player_id = player['id']
            if player_id not in all_players:
                logging.info(f"  [NEW] Joueur trouve via teams/players: {player.get('name')}")
                all_players[player_id] = {
                    'squad_data': {'jersey_number': None},
                    'player_data': player
                }
    
    return list(all_players.values())

def get_player_statistics(player_id: int, season_ids: List[int]) -> Dict:
    """Récupérer les statistiques complètes d'un joueur"""
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
            if 'statistics' in player_data and player_data['statistics']:
                for stat in player_data['statistics']:
                    if stat.get('season_id') == season_id:
                        all_stats[season_id] = process_player_statistics(stat)
                        break
    
    return all_stats

def process_player_statistics(stat_data: Dict) -> Dict:
    """Traiter les statistiques d'un joueur"""
    processed = {
        'season_id': stat_data.get('season_id'),
        'season_name': stat_data.get('season', {}).get('name') if stat_data.get('season') else None,
        'appearences': stat_data.get('appearences', 0),
        'lineups': stat_data.get('lineups', 0),
        'minutes': stat_data.get('minutes_played', 0),
        'goals': stat_data.get('goals', 0),
        'assists': stat_data.get('assists', 0),
        'yellow_cards': stat_data.get('yellow_cards', 0),
        'yellowred_cards': stat_data.get('yellowred_cards', 0),
        'red_cards': stat_data.get('red_cards', 0),
        'clean_sheets': stat_data.get('clean_sheets', 0),
        'saves': stat_data.get('saves', 0),
        'goals_conceded': stat_data.get('goals_conceded', 0),
        'penalties_saved': stat_data.get('penalties_saved', 0),
        'penalties_scored': stat_data.get('penalties_scored', 0),
        'penalties_missed': stat_data.get('penalties_missed', 0),
        'rating': stat_data.get('rating'),
    }
    
    # Ajouter les détails si disponibles
    if 'details' in stat_data and stat_data['details']:
        for detail in stat_data['details']:
            type_data = detail.get('type', {})
            type_name = type_data.get('name', '')
            detail_data = detail.get('data', {})
            
            if type_name == 'Shots':
                processed['shots_total'] = detail_data.get('total', 0)
                processed['shots_on_target'] = detail_data.get('on_target', 0)
            elif type_name == 'Goals':
                processed['goals_scored'] = detail_data.get('scored', 0)
                processed['goals_conceded_detail'] = detail_data.get('conceded', 0)
            elif type_name == 'Passes':
                processed['passes_total'] = detail_data.get('total', 0)
                processed['passes_accuracy'] = detail_data.get('accuracy', 0)
                processed['key_passes'] = detail_data.get('key_passes', 0)
            elif type_name == 'Dribbles':
                processed['dribbles_attempted'] = detail_data.get('attempted', 0)
                processed['dribbles_succeeded'] = detail_data.get('succeeded', 0)
            elif type_name == 'Duels':
                processed['duels_total'] = detail_data.get('total', 0)
                processed['duels_won'] = detail_data.get('won', 0)
            elif type_name == 'Others':
                processed['offsides'] = detail_data.get('offsides', 0)
                processed['hit_woodwork'] = detail_data.get('hit_woodwork', 0)
            elif type_name == 'Fouls':
                processed['fouls_drawn'] = detail_data.get('drawn', 0)
                processed['fouls_committed'] = detail_data.get('committed', 0)
    
    return processed

def calculate_cumulative_stats(stats_by_season: Dict) -> Dict:
    """Calculer les statistiques cumulées sur toutes les saisons"""
    if not stats_by_season:
        return None
    
    cumulative = {
        'appearences': 0,
        'lineups': 0,
        'minutes': 0,
        'goals': 0,
        'assists': 0,
        'yellow_cards': 0,
        'red_cards': 0,
        'clean_sheets': 0,
        'saves': 0,
        'goals_conceded': 0,
        'penalties_saved': 0,
        'shots_total': 0,
        'shots_on_target': 0,
        'passes_total': 0,
        'key_passes': 0,
        'dribbles_attempted': 0,
        'dribbles_succeeded': 0,
    }
    
    for season_stats in stats_by_season.values():
        for key in cumulative:
            if key in season_stats:
                cumulative[key] += season_stats[key] or 0
    
    # Calculer les moyennes
    if cumulative['passes_total'] > 0:
        total_accuracy = sum(s.get('passes_accuracy', 0) * s.get('passes_total', 0) 
                           for s in stats_by_season.values() if s.get('passes_total'))
        cumulative['passes_accuracy'] = round(total_accuracy / cumulative['passes_total'], 1)
    
    return cumulative

def update_league_data(league_id: int, league_info: Dict) -> Dict:
    """Mettre à jour les données complètes d'un championnat"""
    logging.info(f"\n[UPDATE] Traitement de {league_info['name']}")
    
    league_data = {
        'teams': {},
        'stats': {},
        'removed_players': []
    }
    
    # Récupérer toutes les saisons
    season_ids = list(league_info['seasons'].values())
    current_season_id = league_info['seasons']['2025/2026']
    
    # Récupérer toutes les équipes de la saison actuelle
    teams_url = f"{BASE_URL}/teams/seasons/{current_season_id}"
    teams_data = make_api_request(teams_url)
    
    if not teams_data or 'data' not in teams_data:
        logging.error(f"[ERREUR] Impossible de recuperer les equipes pour {league_info['name']}")
        return None
    
    # Traiter chaque équipe
    for team in teams_data['data']:
        team_id = team['id']
        team_name = team['name']
        
        logging.info(f"  Processing {team_name}...")
        
        # Récupérer l'effectif COMPLET
        squad_members = get_complete_squad(team_id, current_season_id)
        
        league_data['teams'][team_id] = {
            'id': team_id,
            'name': team_name,
            'slug': slugify(team_name),
            'players': []
        }
        
        # Traiter chaque joueur
        for member in squad_members:
            player = member['player_data']
            squad_info = member['squad_data']
            
            # Obtenir la position correctement
            position_data = player.get('position', {})
            position_id = position_data.get('id', 1) if position_data else 1
            position_name = position_data.get('name', 'Unknown') if position_data else 'Unknown'
            
            # Calculer l'âge
            age = "Unknown"
            if player.get('date_of_birth'):
                try:
                    birth_date = datetime.strptime(player['date_of_birth'], "%Y-%m-%d")
                    today = datetime.today()
                    age = str(today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day)))
                except:
                    pass
            
            player_data = {
                'id': player['id'],
                'nom': player['name'],
                'displayName': player.get('display_name', player['name']),
                'position': position_name,
                'position_id': position_id,
                'numero': squad_info.get('jersey_number'),
                'age': age,
                'nationalite': player.get('nationality', {}).get('name') if player.get('nationality') else 'Unknown',
                'taille': player.get('height'),
                'poids': player.get('weight'),
                'image': player.get('image_path', ''),
                'playerSlug': slugify(player.get('display_name', player['name']))
            }
            
            league_data['teams'][team_id]['players'].append(player_data)
            
            # Récupérer les statistiques du joueur
            player_stats = get_player_statistics(player['id'], season_ids)
            if player_stats:
                # Organiser les stats par saison
                stats_organized = {
                    'current': player_stats.get(season_ids[0]),  # 2025/2026
                    'previous': [],
                    'cumulative': None
                }
                
                # Ajouter les saisons précédentes
                for season_id in season_ids[1:]:
                    if season_id in player_stats:
                        stats_organized['previous'].append(player_stats[season_id])
                
                # Calculer les stats cumulées
                if player_stats:
                    stats_organized['cumulative'] = calculate_cumulative_stats(player_stats)
                
                league_data['stats'][player['id']] = stats_organized
        
        logging.info(f"    -> {len(league_data['teams'][team_id]['players'])} joueurs")
    
    return league_data

def generate_typescript_files(league_data: Dict, league_info: Dict) -> bool:
    """Générer les fichiers TypeScript pour une ligue"""
    try:
        # Fichier des équipes
        teams_file = DATA_DIR / f"{league_info['dataFile']}.ts"
        stats_file = DATA_DIR / f"{league_info['statsFile']}.ts"
        
        # Générer le contenu des équipes
        teams_content = f"export const {league_info['dataFile']} = [\n"
        
        for team_id, team_data in league_data['teams'].items():
            teams_content += f"""  {{
    id: {team_id},
    name: "{team_data['name']}",
    slug: "{team_data['slug']}",
    players: [
"""
            for player in team_data['players']:
                teams_content += f"""      {{
        id: {player['id']},
        nom: "{player['nom']}",
        displayName: "{player['displayName']}",
        position: "{player['position']}",
        position_id: {player['position_id']},
        numero: {player['numero'] if player['numero'] is not None else 'null'},
        age: "{player['age']}",
        nationalite: "{player['nationalite']}",
        taille: {player['taille'] if player['taille'] else 'null'},
        poids: {player['poids'] if player['poids'] else 'null'},
        image: "{player['image']}",
        playerSlug: "{player['playerSlug']}"
      }},
"""
            teams_content += """    ]
  },
"""
        
        teams_content += "];\n"
        
        # Écrire le fichier des équipes
        teams_file.write_text(teams_content, encoding='utf-8')
        logging.info(f"[OK] Fichier genere: {teams_file.name}")
        
        # Générer le fichier des statistiques
        if league_data['stats']:
            stats_content = f"export const {league_info['statsFile']}: {{ [key: number]: any }} = {{\n"
            
            for player_id, stats in league_data['stats'].items():
                if stats:
                    stats_content += f"  {player_id}: {json.dumps(stats, indent=2)},\n"
            
            stats_content += "};\n"
            
            stats_file.write_text(stats_content, encoding='utf-8')
            logging.info(f"[OK] Fichier stats genere: {stats_file.name}")
        
        return True
        
    except Exception as e:
        logging.error(f"[ERREUR] Generation des fichiers: {e}")
        return False

def main():
    """Fonction principale de mise à jour complète"""
    logging.info("=" * 60)
    logging.info("[START] MISE A JOUR COMPLETE DES DONNEES")
    logging.info("=" * 60)
    
    start_time = time.time()
    backup_path = None
    success = True
    
    try:
        # Créer un backup
        backup_path = create_backup()
        
        # Traiter chaque ligue
        for league_id, league_info in TOP_5_LEAGUES.items():
            league_data = update_league_data(league_id, league_info)
            
            if not league_data:
                logging.error(f"[ERREUR] Echec pour {league_info['name']}")
                continue
            
            # Générer les fichiers TypeScript
            if not generate_typescript_files(league_data, league_info):
                logging.error(f"[ERREUR] Generation echouee pour {league_info['name']}")
                success = False
                break
        
        if not success and backup_path:
            # Restaurer le backup si erreur
            logging.warning("[RESTORE] Restauration du backup...")
            shutil.rmtree(DATA_DIR)
            shutil.copytree(backup_path, DATA_DIR)
            logging.info("[OK] Backup restaure")
        
    except Exception as e:
        logging.error(f"[ERREUR CRITIQUE]: {e}")
        if backup_path:
            shutil.rmtree(DATA_DIR)
            shutil.copytree(backup_path, DATA_DIR)
        success = False
    
    elapsed_time = time.time() - start_time
    logging.info("\n" + "=" * 60)
    if success:
        logging.info(f"[SUCCESS] MISE A JOUR TERMINEE EN {elapsed_time:.2f} SECONDES")
    else:
        logging.info(f"[FAIL] MISE A JOUR ECHOUEE APRES {elapsed_time:.2f} SECONDES")
    logging.info("=" * 60)
    
    # Statut
    status_file = SCRIPT_DIR / 'last_update.json'
    status_file.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'duration': elapsed_time,
        'success': success
    }, indent=2))
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)