#!/usr/bin/env python3
"""
Système de mise à jour COMPLET et AUTOMATIQUE
- Traite TOUS les championnats (Ligue 1, Premier League, La Liga, Serie A, Bundesliga)
- Récupère TOUS les joueurs de TOUS les clubs
- Met à jour toutes les statistiques
- Optimisé pour éviter les timeouts
"""

import os
import sys
import json
import time
import shutil
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration du logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'complete_update_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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

# API Configuration
API_KEY = os.environ.get('SPORTMONKS_API_KEY', 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2')
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Configuration des 5 grands championnats
ALL_LEAGUES = {
    301: {
        "name": "Ligue 1",
        "slug": "ligue1",
        "dataFile": "ligue1Teams",
        "statsFile": "ligue1PlayersCompleteStats",
        "current_season": 25651
    },
    8: {
        "name": "Premier League",
        "slug": "premier-league",
        "dataFile": "premierLeagueTeams",
        "statsFile": "premierLeaguePlayersCompleteStats",
        "current_season": 25583
    },
    564: {
        "name": "La Liga",
        "slug": "la-liga",
        "dataFile": "ligaTeams",
        "statsFile": "laLigaPlayersCompleteStats",
        "current_season": 25659
    },
    384: {
        "name": "Serie A",
        "slug": "serie-a",
        "dataFile": "serieATeams",
        "statsFile": "serieAPlayersCompleteStats",
        "current_season": 25533
    },
    82: {
        "name": "Bundesliga",
        "slug": "bundesliga",
        "dataFile": "bundesligaTeams",
        "statsFile": "bundesligaPlayersCompleteStats",
        "current_season": 25646
    }
}

def create_backup():
    """Créer une sauvegarde avant modification"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    
    logging.info(f"[BACKUP] Creation backup...")
    
    if DATA_DIR.exists():
        shutil.copytree(DATA_DIR, backup_path)
        
        # Garder seulement les 5 derniers
        backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir() and d.name.startswith("backup_")])
        for old in backups[:-5]:
            shutil.rmtree(old)
    
    logging.info("[BACKUP] OK")
    return backup_path

def restore_backup(backup_path: Path):
    """Restaurer le backup en cas d'erreur"""
    logging.warning("[RESTORE] Restauration du backup...")
    if DATA_DIR.exists():
        shutil.rmtree(DATA_DIR)
    shutil.copytree(backup_path, DATA_DIR)
    logging.info("[RESTORE] OK")

def make_api_request(url: str, params: Dict = None, retries: int = 3) -> Optional[Dict]:
    """Requête API avec retry automatique"""
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=20)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Rate limit
                wait = min(2 ** (attempt + 1), 10)
                time.sleep(wait)
                continue
            else:
                return None
                
        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                time.sleep(1)
            continue
        except Exception:
            return None
    
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

def get_age(date_of_birth: str) -> str:
    """Calculer l'âge"""
    if not date_of_birth:
        return "Unknown"
    
    try:
        birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        return str(age)
    except:
        return "Unknown"

def get_all_players_for_team(team_id: int, season_id: int) -> List[Dict]:
    """
    Récupérer TOUS les joueurs d'une équipe en utilisant l'endpoint le plus fiable
    """
    all_players = []
    
    # Méthode principale: Squad de la saison
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'include': 'player.position',
        'filters': f'seasons:{season_id}',
        'per_page': 100
    }
    
    data = make_api_request(url, params)
    if data and 'data' in data:
        for item in data['data']:
            if 'player' in item and item['player']:
                player = item['player']
                
                # Récupérer plus d'infos si nécessaire
                if not player.get('image_path') or not player.get('nationality'):
                    player_url = f"{BASE_URL}/players/{player['id']}"
                    player_data = make_api_request(player_url, {'include': 'nationality'})
                    if player_data and 'data' in player_data:
                        player.update(player_data['data'])
                
                all_players.append({
                    'id': player['id'],
                    'name': player.get('name', 'Unknown'),
                    'display_name': player.get('display_name', player.get('name', 'Unknown')),
                    'position': player.get('position', {}).get('name', 'Unknown') if player.get('position') else 'Unknown',
                    'position_id': player.get('position', {}).get('id', 1) if player.get('position') else 1,
                    'jersey_number': item.get('jersey_number'),
                    'date_of_birth': player.get('date_of_birth'),
                    'nationality': player.get('nationality', {}).get('name') if player.get('nationality') else 'Unknown',
                    'height': player.get('height'),
                    'weight': player.get('weight'),
                    'image': player.get('image_path', '')
                })
    
    return all_players

def process_team(team_data: Dict, season_id: int) -> Dict:
    """Traiter une équipe et récupérer tous ses joueurs"""
    team_id = team_data['id']
    team_name = team_data['name']
    
    # Récupérer tous les joueurs
    players = get_all_players_for_team(team_id, season_id)
    
    # Formater les données de l'équipe
    formatted_players = []
    for player in players:
        formatted_players.append({
            'id': player['id'],
            'nom': player['name'],
            'displayName': player['display_name'],
            'position': player['position'],
            'position_id': player['position_id'],
            'numero': player['jersey_number'],
            'age': get_age(player['date_of_birth']),
            'nationalite': player['nationality'],
            'taille': player['height'],
            'poids': player['weight'],
            'image': player['image'],
            'playerSlug': slugify(player['display_name'])
        })
    
    return {
        'id': team_id,
        'name': team_name,
        'slug': slugify(team_name),
        'players': formatted_players
    }

def update_league(league_id: int, league_info: Dict) -> Optional[Dict]:
    """Mettre à jour un championnat complet"""
    league_name = league_info['name']
    season_id = league_info['current_season']
    
    logging.info(f"\n{'='*50}")
    logging.info(f"[{league_name}] Debut traitement")
    logging.info(f"{'='*50}")
    
    # Récupérer toutes les équipes
    url = f"{BASE_URL}/teams/seasons/{season_id}"
    data = make_api_request(url)
    
    if not data or 'data' not in data:
        logging.error(f"[{league_name}] Impossible de recuperer les equipes")
        return None
    
    teams = data['data']
    logging.info(f"[{league_name}] {len(teams)} equipes trouvees")
    
    # Traiter chaque équipe
    league_data = {'teams': {}}
    
    for i, team in enumerate(teams, 1):
        logging.info(f"[{league_name}] Equipe {i}/{len(teams)}: {team['name']}")
        
        team_result = process_team(team, season_id)
        league_data['teams'][team['id']] = team_result
        
        logging.info(f"  -> {len(team_result['players'])} joueurs")
        
        # Petite pause pour éviter le rate limiting
        if i % 5 == 0:
            time.sleep(1)
    
    logging.info(f"[{league_name}] Traitement termine")
    
    return league_data

def generate_typescript_file(league_data: Dict, league_info: Dict) -> bool:
    """Générer le fichier TypeScript pour un championnat"""
    try:
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
        numero: {p['numero'] if p['numero'] is not None else 'null'},
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
        
        # Écrire le fichier
        file_path.write_text(content, encoding='utf-8')
        logging.info(f"[FILE] {file_path.name} genere avec succes")
        
        return True
        
    except Exception as e:
        logging.error(f"[ERROR] Generation fichier: {e}")
        return False

def main():
    """Fonction principale - Mise à jour COMPLETE de TOUS les championnats"""
    logging.info("\n" + "="*60)
    logging.info("MISE A JOUR COMPLETE - TOUS LES CHAMPIONNATS")
    logging.info("="*60)
    
    start_time = time.time()
    backup_path = None
    success = True
    
    try:
        # Créer un backup
        backup_path = create_backup()
        
        # Statistiques globales
        total_teams = 0
        total_players = 0
        
        # Traiter TOUS les championnats
        for league_id, league_info in ALL_LEAGUES.items():
            league_data = update_league(league_id, league_info)
            
            if not league_data:
                logging.error(f"[SKIP] {league_info['name']} - Erreur")
                success = False
                continue
            
            # Générer le fichier TypeScript
            if not generate_typescript_file(league_data, league_info):
                logging.error(f"[ERROR] Generation pour {league_info['name']}")
                success = False
                continue
            
            # Stats
            teams_count = len(league_data['teams'])
            players_count = sum(len(team['players']) for team in league_data['teams'].values())
            total_teams += teams_count
            total_players += players_count
            
            logging.info(f"[{league_info['name']}] Complete: {teams_count} equipes, {players_count} joueurs")
            
            # Pause entre les ligues
            time.sleep(2)
        
        # Résumé final
        elapsed = time.time() - start_time
        logging.info("\n" + "="*60)
        logging.info("RESUME FINAL")
        logging.info(f"- Championnats traites: {len(ALL_LEAGUES)}")
        logging.info(f"- Total equipes: {total_teams}")
        logging.info(f"- Total joueurs: {total_players}")
        logging.info(f"- Duree: {elapsed:.2f} secondes")
        
        if success:
            logging.info("- Statut: SUCCESS")
        else:
            logging.info("- Statut: PARTIAL (certains championnats ont echoue)")
        
        logging.info("="*60)
        
    except Exception as e:
        logging.error(f"[ERREUR CRITIQUE]: {e}")
        success = False
        
        # Restaurer le backup en cas d'erreur
        if backup_path and backup_path.exists():
            restore_backup(backup_path)
    
    # Créer un fichier de statut
    status_file = SCRIPT_DIR / 'last_update.json'
    status_file.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'duration': time.time() - start_time,
        'success': success,
        'stats': {
            'teams': total_teams if 'total_teams' in locals() else 0,
            'players': total_players if 'total_players' in locals() else 0
        }
    }, indent=2))
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)