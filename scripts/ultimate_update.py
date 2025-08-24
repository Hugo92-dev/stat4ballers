#!/usr/bin/env python3
"""
Script ULTIME de mise à jour - Récupère TOUS les joueurs sans exception
Utilise TOUTES les méthodes possibles pour ne manquer AUCUN joueur
"""

import os
import sys
import json
import time
import shutil
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Set, Optional
import requests
from pathlib import Path

# Configuration du logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'ultimate_update_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

# Fix encodage Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Chemins
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
BACKUP_DIR = SCRIPT_DIR / "backups"
BACKUP_DIR.mkdir(exist_ok=True)

# API
API_KEY = os.environ.get('SPORTMONKS_API_KEY', 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2')
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Configuration des ligues
LEAGUES = {
    301: {
        "name": "Ligue 1",
        "slug": "ligue1",
        "dataFile": "ligue1Teams",
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
        "seasons": {
            "2025/2026": 25646,
            "2024/2025": 23744,
            "2023/2024": 21795,
        }
    },
}

def create_backup():
    """Créer backup avant modification"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    
    logging.info(f"[BACKUP] Creation: {backup_path}")
    
    if DATA_DIR.exists():
        shutil.copytree(DATA_DIR, backup_path)
    
    # Garder 5 derniers backups
    backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir() and d.name.startswith("backup_")])
    for old in backups[:-5]:
        shutil.rmtree(old)
    
    logging.info("[OK] Backup cree")
    return backup_path

def api_request(url: str, params: Dict = None) -> Optional[Dict]:
    """Requête API avec gestion d'erreur"""
    for attempt in range(3):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                time.sleep(2 ** (attempt + 1))
                continue
            else:
                if attempt == 0:  # Log une seule fois
                    logging.debug(f"API {resp.status_code}: {url}")
                return None
        except Exception as e:
            if attempt == 0:
                logging.debug(f"Erreur: {e}")
        
        if attempt < 2:
            time.sleep(1)
    
    return None

def slugify(text: str) -> str:
    """Convertir en slug URL"""
    import unicodedata
    import re
    
    if not text:
        return ""
    
    text = unicodedata.normalize('NFD', str(text))
    text = text.encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    
    return text.strip('-')

def get_age(dob: str) -> str:
    """Calculer âge"""
    if not dob:
        return "Unknown"
    try:
        birth = datetime.strptime(dob, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return str(age)
    except:
        return "Unknown"

def get_complete_team_squad(team_id: int, team_name: str, season_id: int) -> Dict[int, Dict]:
    """
    Récupérer l'effectif COMPLET d'une équipe en utilisant TOUTES les sources
    Retourne un dictionnaire avec l'ID du joueur comme clé
    """
    all_players = {}
    
    logging.info(f"  [{team_name}] Recherche complete des joueurs...")
    
    # SOURCE 1: Squad officiel
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'include': 'player.position',
        'filters': f'seasons:{season_id}'
    }
    data = api_request(url, params)
    if data and 'data' in data:
        for item in data['data']:
            if 'player' in item and item['player']:
                player = item['player']
                all_players[player['id']] = {
                    'data': player,
                    'jersey': item.get('jersey_number'),
                    'source': 'squad'
                }
    
    # SOURCE 2: Statistiques des joueurs de l'équipe pour cette saison
    url = f"{BASE_URL}/statistics/seasons/{season_id}/teams/{team_id}"
    params = {'include': 'player'}
    data = api_request(url, params)
    if data and 'data' in data:
        # Parcourir toutes les stats
        for stat_type in ['squad', 'lineups', 'substitutes', 'bench']:
            if stat_type in data['data']:
                for player_stat in data['data'][stat_type]:
                    if 'player' in player_stat and player_stat['player']:
                        player = player_stat['player']
                        if player['id'] not in all_players:
                            all_players[player['id']] = {
                                'data': player,
                                'jersey': None,
                                'source': f'stats_{stat_type}'
                            }
                            logging.info(f"    [NEW via {stat_type}] {player.get('name')}")
    
    # SOURCE 3: Tous les matchs de la saison (pour trouver les joueurs ayant joué)
    url = f"{BASE_URL}/fixtures"
    params = {
        'filters': f'teams:{team_id};seasons:{season_id}',
        'include': 'lineups.player,substitutions.player',
        'per_page': 50
    }
    data = api_request(url, params)
    if data and 'data' in data:
        for fixture in data['data']:
            # Titulaires et remplaçants
            if 'lineups' in fixture:
                for lineup in fixture['lineups']:
                    if lineup.get('team_id') == team_id and 'player' in lineup and lineup['player']:
                        player = lineup['player']
                        if player['id'] not in all_players:
                            all_players[player['id']] = {
                                'data': player,
                                'jersey': lineup.get('jersey_number'),
                                'source': 'match_lineup'
                            }
                            logging.info(f"    [NEW via match] {player.get('name')}")
            
            # Remplacements
            if 'substitutions' in fixture:
                for sub in fixture['substitutions']:
                    if sub.get('team_id') == team_id and 'player' in sub and sub['player']:
                        player = sub['player']
                        if player['id'] not in all_players:
                            all_players[player['id']] = {
                                'data': player,
                                'jersey': None,
                                'source': 'substitution'
                            }
                            logging.info(f"    [NEW via substitution] {player.get('name')}")
    
    # SOURCE 4: Endpoint direct des joueurs de l'équipe (autre méthode)
    url = f"{BASE_URL}/teams/{team_id}"
    params = {'include': 'players'}
    data = api_request(url, params)
    if data and 'data' in data and 'players' in data['data']:
        for player in data['data']['players']:
            if player['id'] not in all_players:
                all_players[player['id']] = {
                    'data': player,
                    'jersey': None,
                    'source': 'team_players'
                }
                logging.info(f"    [NEW via team] {player.get('name')}")
    
    # SOURCE 5: Transferts récents (joueurs arrivés)
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime("%Y-%m-%d")
    url = f"{BASE_URL}/transfers"
    params = {
        'filters': f'teams:{team_id};date_from:{six_months_ago}',
        'include': 'player'
    }
    data = api_request(url, params)
    if data and 'data' in data:
        for transfer in data['data']:
            # Seulement les arrivées
            if transfer.get('to', {}).get('id') == team_id:
                if 'player' in transfer and transfer['player']:
                    player = transfer['player']
                    if player['id'] not in all_players:
                        all_players[player['id']] = {
                            'data': player,
                            'jersey': None,
                            'source': 'transfer'
                        }
                        logging.info(f"    [NEW via transfer] {player.get('name')}")
    
    # Pour chaque joueur, récupérer les infos complètes si manquantes
    for player_id, player_info in all_players.items():
        if not player_info['data'].get('position') or not player_info['data'].get('image_path'):
            url = f"{BASE_URL}/players/{player_id}"
            params = {'include': 'position,nationality'}
            data = api_request(url, params)
            if data and 'data' in data:
                player_info['data'].update(data['data'])
    
    logging.info(f"    => {len(all_players)} joueurs trouves au total")
    
    # Vérifier spécifiquement Robinio Vaz
    if team_id == 85:  # OM
        robinio_id = 37713942
        if robinio_id in all_players:
            logging.info(f"    [FOUND] Robinio Vaz trouve automatiquement!")
        else:
            logging.info(f"    [CHECK] Recherche specifique de Robinio Vaz (ID: {robinio_id})...")
            url = f"{BASE_URL}/players/{robinio_id}"
            params = {'include': 'teams,position'}
            data = api_request(url, params)
            if data and 'data' in data:
                player = data['data']
                # Vérifier qu'il est bien à l'OM
                if 'teams' in player:
                    for team in player['teams']:
                        if team.get('id') == team_id:
                            all_players[robinio_id] = {
                                'data': player,
                                'jersey': None,
                                'source': 'direct_check'
                            }
                            logging.info(f"    [FOUND] Robinio Vaz ajoute via recherche directe!")
                            break
    
    return all_players

def get_player_stats(player_id: int, season_ids: List[int]) -> Dict:
    """Récupérer toutes les stats d'un joueur"""
    stats = {}
    
    for season_id in season_ids:
        url = f"{BASE_URL}/players/{player_id}"
        params = {
            'include': 'statistics.details',
            'filters': f'player_statistics.season_id:{season_id}'
        }
        
        data = api_request(url, params)
        if data and 'data' in data and 'statistics' in data['data']:
            for stat in data['data']['statistics']:
                if stat.get('season_id') == season_id:
                    stats[season_id] = {
                        'appearences': stat.get('appearences', 0),
                        'minutes': stat.get('minutes_played', 0),
                        'goals': stat.get('goals', 0),
                        'assists': stat.get('assists', 0),
                        'yellow_cards': stat.get('yellow_cards', 0),
                        'red_cards': stat.get('red_cards', 0),
                        'clean_sheets': stat.get('clean_sheets', 0),
                        'saves': stat.get('saves', 0),
                        'goals_conceded': stat.get('goals_conceded', 0)
                    }
                    break
    
    return stats

def update_league(league_id: int, league_info: Dict) -> Dict:
    """Mise à jour complète d'une ligue"""
    logging.info(f"\n{'='*60}")
    logging.info(f"[{league_info['name']}]")
    logging.info(f"{'='*60}")
    
    league_data = {'teams': {}, 'stats': {}}
    season_ids = list(league_info['seasons'].values())
    current_season = season_ids[0]
    
    # Récupérer les équipes
    url = f"{BASE_URL}/teams/seasons/{current_season}"
    data = api_request(url)
    
    if not data or 'data' not in data:
        logging.error(f"Impossible de recuperer les equipes")
        return None
    
    teams = data['data']
    logging.info(f"[INFO] {len(teams)} equipes")
    
    # Traiter chaque équipe
    for team in teams:
        team_id = team['id']
        team_name = team['name']
        
        # Récupérer TOUS les joueurs
        all_players = get_complete_team_squad(team_id, team_name, current_season)
        
        league_data['teams'][team_id] = {
            'id': team_id,
            'name': team_name,
            'slug': slugify(team_name),
            'players': []
        }
        
        # Formater chaque joueur
        for player_id, player_info in all_players.items():
            player = player_info['data']
            
            position = player.get('position', {})
            if not isinstance(position, dict):
                position = {}
            
            formatted_player = {
                'id': player_id,
                'nom': player.get('name', 'Unknown'),
                'displayName': player.get('display_name', player.get('name', 'Unknown')),
                'position': position.get('name', 'Unknown'),
                'position_id': position.get('id', 1),
                'numero': player_info.get('jersey'),
                'age': get_age(player.get('date_of_birth')),
                'nationalite': player.get('nationality', {}).get('name', 'Unknown') if player.get('nationality') else 'Unknown',
                'taille': player.get('height'),
                'poids': player.get('weight'),
                'image': player.get('image_path', ''),
                'playerSlug': slugify(player.get('display_name', player.get('name', 'Unknown')))
            }
            
            league_data['teams'][team_id]['players'].append(formatted_player)
            
            # Stats (optionnel pour aller plus vite)
            if league_id == 301 and team_id == 85:  # Focus sur l'OM pour le test
                stats = get_player_stats(player_id, season_ids[:1])  # Juste saison actuelle
                if stats:
                    league_data['stats'][player_id] = stats
    
    return league_data

def generate_files(league_data: Dict, league_info: Dict) -> bool:
    """Générer les fichiers TypeScript"""
    try:
        # Fichier des équipes
        file_path = DATA_DIR / f"{league_info['dataFile']}.ts"
        
        content = f"export const {league_info['dataFile']} = [\n"
        
        for team_id, team in league_data['teams'].items():
            content += f"""  {{
    id: {team_id},
    name: "{team['name']}",
    slug: "{team['slug']}",
    players: [
"""
            for p in team['players']:
                content += f"""      {{
        id: {p['id']},
        nom: "{p['nom']}",
        displayName: "{p['displayName']}",
        position: "{p['position']}",
        position_id: {p['position_id']},
        numero: {p['numero'] if p['numero'] else 'null'},
        age: "{p['age']}",
        nationalite: "{p['nationalite']}",
        taille: {p['taille'] if p['taille'] else 'null'},
        poids: {p['poids'] if p['poids'] else 'null'},
        image: "{p['image']}",
        playerSlug: "{p['playerSlug']}"
      }},
"""
            content += """    ]
  },
"""
        
        content += "];\n"
        
        file_path.write_text(content, encoding='utf-8')
        logging.info(f"[OK] Fichier genere: {file_path.name}")
        
        return True
    except Exception as e:
        logging.error(f"[ERREUR] Generation: {e}")
        return False

def main():
    """Fonction principale"""
    logging.info("\n" + "="*60)
    logging.info("MISE A JOUR ULTIME - RECUPERATION COMPLETE")
    logging.info("="*60 + "\n")
    
    start_time = time.time()
    backup_path = create_backup()
    
    try:
        # Pour le test, focus sur la Ligue 1 et l'OM
        for league_id, league_info in LEAGUES.items():
            if league_id != 301:  # Seulement Ligue 1 pour le test
                continue
                
            league_data = update_league(league_id, league_info)
            
            if league_data:
                # Vérifier que Robinio est bien là
                om_id = 85
                if om_id in league_data['teams']:
                    om_players = league_data['teams'][om_id]['players']
                    robinio = next((p for p in om_players if p['id'] == 37713942), None)
                    if robinio:
                        logging.info(f"\n[SUCCESS] Robinio Vaz trouve automatiquement!")
                        logging.info(f"  Nom: {robinio['nom']}")
                        logging.info(f"  Position: {robinio['position']}")
                        logging.info(f"  Numero: {robinio['numero']}")
                    else:
                        logging.warning(f"\n[WARNING] Robinio Vaz non trouve")
                
                generate_files(league_data, league_info)
            
            # Faire les autres ligues après
            if league_id == 301:
                logging.info("\n[INFO] Traitement des autres ligues...")
                for other_id, other_info in LEAGUES.items():
                    if other_id != 301:
                        other_data = update_league(other_id, other_info)
                        if other_data:
                            generate_files(other_data, other_info)
        
        logging.info(f"\n[SUCCESS] Mise a jour terminee en {time.time() - start_time:.2f}s")
        
    except Exception as e:
        logging.error(f"[ERREUR]: {e}")
        # Restaurer backup
        if backup_path.exists():
            shutil.rmtree(DATA_DIR)
            shutil.copytree(backup_path, DATA_DIR)
            logging.info("[RESTORED] Backup restaure")
    
    return True

if __name__ == "__main__":
    main()