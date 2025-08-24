#!/usr/bin/env python3
"""
Script SÉCURISÉ de mise à jour des données avec backup et validation
Ne casse jamais le site - fait un backup avant et valide après
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
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess
from pathlib import Path

# Configuration du logging
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / f'update_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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

# Créer le dossier de backup s'il n'existe pas
BACKUP_DIR.mkdir(exist_ok=True)

# Récupérer la clé API
API_KEY = os.environ.get('SPORTMONKS_API_KEY', 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2')
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Les 5 grands championnats avec leurs saisons
TOP_5_LEAGUES = {
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
    """Créer une sauvegarde complète du dossier data"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    
    logging.info(f"[BACKUP] Création du backup dans {backup_path}")
    
    try:
        # Copier tout le dossier data
        shutil.copytree(DATA_DIR, backup_path)
        
        # Garder seulement les 5 derniers backups
        backups = sorted([d for d in BACKUP_DIR.iterdir() if d.is_dir() and d.name.startswith("backup_")])
        if len(backups) > 5:
            for old_backup in backups[:-5]:
                shutil.rmtree(old_backup)
                logging.info(f"[CLEAN] Ancien backup supprimé: {old_backup.name}")
        
        logging.info(f"[OK] Backup créé avec succès: {backup_path}")
        return backup_path
    except Exception as e:
        logging.error(f"[ERREUR] Erreur lors de la création du backup: {e}")
        raise

def restore_backup(backup_path: Path):
    """Restaurer un backup en cas d'erreur"""
    logging.warning(f"[ATTENTION] Restauration du backup {backup_path}")
    
    try:
        # Supprimer le dossier data actuel
        if DATA_DIR.exists():
            shutil.rmtree(DATA_DIR)
        
        # Restaurer le backup
        shutil.copytree(backup_path, DATA_DIR)
        logging.info("[OK] Backup restauré avec succès")
    except Exception as e:
        logging.error(f"[ERREUR CRITIQUE] Erreur lors de la restauration: {e}")
        raise

def validate_file(file_path: Path) -> bool:
    """Valider qu'un fichier TypeScript est correct"""
    if not file_path.exists():
        logging.error(f"[ERREUR] Fichier manquant: {file_path}")
        return False
    
    # Vérifier que le fichier n'est pas vide
    if file_path.stat().st_size == 0:
        logging.error(f"[ERREUR] Fichier vide: {file_path}")
        return False
    
    # Vérifier la syntaxe de base
    try:
        content = file_path.read_text(encoding='utf-8')
        if 'export' not in content:
            logging.error(f"[ERREUR] Pas d'export dans {file_path}")
            return False
        
        # Vérifier qu'il y a du contenu
        if len(content) < 100:
            logging.error(f"[ERREUR] Fichier trop court: {file_path}")
            return False
            
    except Exception as e:
        logging.error(f"[ERREUR] Erreur lors de la lecture de {file_path}: {e}")
        return False
    
    return True

def make_api_request(url: str, params: Dict = None) -> Optional[Dict]:
    """Faire une requête API avec retry et gestion d'erreur"""
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
            logging.error(f"Erreur requête: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
            else:
                return None
    return None

def slugify(text: str) -> str:
    """Convertir un texte en slug URL-friendly"""
    import unicodedata
    import re
    
    if not text:
        return ""
    
    # Normaliser le texte
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    
    # Convertir en minuscules et remplacer les espaces
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    
    return text.strip('-')

def get_existing_team_data(league_info: Dict) -> Dict:
    """Charger les données existantes d'une ligue"""
    file_path = DATA_DIR / f"{league_info['dataFile']}.ts"
    
    if not file_path.exists():
        logging.warning(f"[ATTENTION] Fichier existant non trouvé: {file_path}")
        return {}
    
    try:
        # Lire le fichier et extraire les données
        content = file_path.read_text(encoding='utf-8')
        
        # Parser basique pour extraire les équipes
        # (Dans un cas réel, on pourrait utiliser un parser TypeScript)
        teams = {}
        
        # Extraire les IDs des équipes du fichier existant
        import re
        team_pattern = r'id:\s*(\d+),'
        team_ids = re.findall(team_pattern, content)
        
        for team_id in team_ids:
            teams[int(team_id)] = True
            
        logging.info(f"[INFO] {len(teams)} équipes existantes trouvées dans {file_path.name}")
        return teams
        
    except Exception as e:
        logging.error(f"Erreur lors de la lecture de {file_path}: {e}")
        return {}

def get_team_squads_safe(league_id: int, season_id: int, league_info: Dict) -> Dict:
    """Récupérer les effectifs de manière sécurisée"""
    logging.info(f"[UPDATE] Récupération des effectifs pour {league_info['name']}, saison {season_id}")
    
    # Charger les données existantes pour comparaison
    existing_teams = get_existing_team_data(league_info)
    
    # Récupérer toutes les équipes de la saison
    teams_url = f"{BASE_URL}/teams/seasons/{season_id}"
    teams_data = make_api_request(teams_url)
    
    if not teams_data or 'data' not in teams_data:
        logging.error(f"[ERREUR] Impossible de récupérer les équipes pour la saison {season_id}")
        return None  # Retourner None pour indiquer l'échec
    
    teams = {}
    new_players_count = 0
    
    for team in teams_data['data']:
        team_id = team['id']
        team_name = team['name']
        
        # Récupérer l'effectif de l'équipe
        squad_url = f"{BASE_URL}/squads/teams/{team_id}"
        params = {
            'include': 'player.position',
            'filters': f'seasons:{season_id}'
        }
        
        squad_data = make_api_request(squad_url, params)
        
        if squad_data and 'data' in squad_data:
            teams[team_id] = {
                'name': team_name,
                'slug': slugify(team_name),
                'players': []
            }
            
            for squad_member in squad_data['data']:
                if 'player' in squad_member and squad_member['player']:
                    player = squad_member['player']
                    # Obtenir l'ID de position correctement
                    position_data = player.get('position', {})
                    position_id = position_data.get('id', 1) if position_data else 1
                    
                    teams[team_id]['players'].append({
                        'id': player['id'],
                        'name': player['name'],
                        'display_name': player.get('display_name', player['name']),
                        'position': position_data.get('name', 'Unknown') if position_data else 'Unknown',
                        'position_id': position_id,
                        'jersey_number': squad_member.get('jersey_number'),
                        'image': player.get('image_path'),
                        'date_of_birth': player.get('date_of_birth'),
                        'nationality': player.get('nationality', {}).get('name') if player.get('nationality') else None,
                        'height': player.get('height'),
                        'weight': player.get('weight')
                    })
                    
                    # Compter les nouveaux joueurs
                    if team_id not in existing_teams:
                        new_players_count += 1
            
            logging.info(f"  [OK] {team_name}: {len(teams[team_id]['players'])} joueurs")
        else:
            logging.warning(f"  [ATTENTION] Pas de données pour {team_name}")
    
    if new_players_count > 0:
        logging.info(f"  [NEW] {new_players_count} nouveaux joueurs détectés")
    
    return teams

def generate_typescript_files_safe(league_data: Dict, league_info: Dict) -> bool:
    """Générer les fichiers TypeScript de manière sécurisée"""
    
    if not league_data or 'teams' not in league_data:
        logging.error(f"[ERREUR] Pas de données pour générer les fichiers de {league_info['name']}")
        return False
    
    try:
        # Fichier des équipes
        output_file = DATA_DIR / f"{league_info['dataFile']}.ts"
        stats_file = DATA_DIR / f"{league_info['slug'].replace('-', '')}PlayersCompleteStats.ts"
        
        # Générer le contenu TypeScript pour les équipes
        typescript_content = f"""export const {league_info['dataFile']} = [
"""
        
        for team_id, team_data in league_data['teams'].items():
            typescript_content += f"""  {{
    id: {team_id},
    name: "{team_data['name']}",
    slug: "{team_data['slug']}",
    players: [
"""
            for player in team_data['players']:
                age = calculate_age(player.get('date_of_birth'))
                typescript_content += f"""      {{
        id: {player['id']},
        nom: "{player['name']}",
        displayName: "{player.get('display_name', player['name'])}",
        position: "{player['position']}",
        position_id: {player.get('position_id', 1)},
        numero: {player.get('jersey_number') or 'null'},
        age: "{age}",
        nationalite: "{player.get('nationality') or 'Unknown'}",
        taille: {player.get('height') or 'null'},
        poids: {player.get('weight') or 'null'},
        image: "{player.get('image') or ''}",
        playerSlug: "{slugify(player.get('display_name', player['name']))}"
      }},
"""
            typescript_content += """    ]
  },
"""
        
        typescript_content += "];\n"
        
        # Écrire le fichier des équipes
        output_file.write_text(typescript_content, encoding='utf-8')
        
        # Valider le fichier généré
        if not validate_file(output_file):
            logging.error(f"[ERREUR] Validation échouée pour {output_file}")
            return False
        
        logging.info(f"[OK] Fichier généré et validé: {output_file.name}")
        
        # Générer le fichier des statistiques si disponible
        if 'stats' in league_data and league_data['stats']:
            stats_content = f"""export const {league_info['slug'].replace('-', '')}PlayersCompleteStats: {{ [key: number]: any }} = {{
"""
            
            for player_id, stats in league_data['stats'].items():
                if stats:
                    stats_content += f"  {player_id}: {json.dumps(stats, indent=2)},\n"
            
            stats_content += "};\n"
            
            stats_file.write_text(stats_content, encoding='utf-8')
            
            if not validate_file(stats_file):
                logging.error(f"[ERREUR] Validation échouée pour {stats_file}")
                return False
                
            logging.info(f"[OK] Fichier stats généré et validé: {stats_file.name}")
        
        return True
        
    except Exception as e:
        logging.error(f"[ERREUR] Erreur lors de la génération des fichiers: {e}")
        return False

def calculate_age(date_of_birth: str) -> str:
    """Calculer l'âge à partir de la date de naissance"""
    if not date_of_birth:
        return "Unknown"
    
    try:
        birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return str(age)
    except:
        return "Unknown"

def test_compilation() -> bool:
    """Tester la compilation TypeScript"""
    logging.info("[TEST] Test de compilation TypeScript...")
    
    try:
        result = subprocess.run(
            ['npm', 'run', 'build'],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
            timeout=120
        )
        
        if result.returncode == 0:
            logging.info("[OK] Compilation réussie")
            return True
        else:
            logging.error(f"[ERREUR] Erreurs de compilation:\n{result.stderr}")
            return False
    except Exception as e:
        logging.error(f"[ERREUR] Erreur lors de la compilation: {e}")
        return False

def main():
    """Fonction principale avec gestion d'erreur complète"""
    logging.info("=" * 60)
    logging.info("[START] DÉBUT DE LA MISE À JOUR SÉCURISÉE DES DONNÉES")
    logging.info("=" * 60)
    
    start_time = time.time()
    backup_path = None
    success = True
    
    try:
        # ÉTAPE 1: Créer un backup
        backup_path = create_backup()
        
        # ÉTAPE 2: Traiter chaque ligue
        for league_id, league_info in TOP_5_LEAGUES.items():
            logging.info(f"\n--- Traitement de {league_info['name']} ---")
            
            league_data = {
                'teams': {},
                'stats': {}
            }
            
            # Récupérer la saison actuelle
            current_season_id = league_info['seasons']['2025/2026']
            
            # Récupérer les effectifs de manière sécurisée
            teams = get_team_squads_safe(league_id, current_season_id, league_info)
            
            if teams is None:
                logging.error(f"[ERREUR] Échec pour {league_info['name']}, passage à la ligue suivante")
                continue
            
            league_data['teams'] = teams
            
            # TODO: Ajouter la récupération des stats ici si nécessaire
            # Pour l'instant, on se concentre sur les effectifs
            
            # Générer les fichiers TypeScript de manière sécurisée
            if not generate_typescript_files_safe(league_data, league_info):
                logging.error(f"[ERREUR] Génération échouée pour {league_info['name']}")
                success = False
                break
        
        # ÉTAPE 3: Tester la compilation
        if success:
            if not test_compilation():
                logging.error("[ERREUR] La compilation a échoué, restauration du backup...")
                success = False
        
        # ÉTAPE 4: Restaurer si nécessaire
        if not success and backup_path:
            restore_backup(backup_path)
            logging.error("[ATTENTION] Mise à jour annulée, backup restauré")
        else:
            logging.info("[SUCCESS] Mise à jour réussie!")
        
    except Exception as e:
        logging.error(f"[ERREUR CRITIQUE]: {e}")
        if backup_path:
            restore_backup(backup_path)
        success = False
    
    # Rapport final
    elapsed_time = time.time() - start_time
    logging.info("\n" + "=" * 60)
    if success:
        logging.info(f"[SUCCESS] MISE À JOUR TERMINÉE AVEC SUCCÈS EN {elapsed_time:.2f} SECONDES")
    else:
        logging.info(f"[FAIL] MISE À JOUR ÉCHOUÉE APRÈS {elapsed_time:.2f} SECONDES")
    logging.info("=" * 60)
    
    # Créer un fichier de statut
    status_file = SCRIPT_DIR / 'last_update.json'
    status_file.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'duration': elapsed_time,
        'success': success
    }, indent=2))
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main() else 1)