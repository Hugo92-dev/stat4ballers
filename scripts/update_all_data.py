#!/usr/bin/env python3
"""
Script de mise à jour complète des données de l'application
- Met à jour les effectifs (nouveaux joueurs, transferts)
- Met à jour les statistiques de tous les joueurs
- Génère les fichiers TypeScript pour l'application
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, Any, List, Set
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import subprocess

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'update_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Récupérer la clé API depuis l'environnement ou utiliser celle par défaut
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

def make_api_request(url: str, params: Dict = None) -> Dict:
    """Faire une requête API avec retry"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                time.sleep(2 ** attempt)
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
    
    # Normaliser le texte
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    
    # Convertir en minuscules et remplacer les espaces
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    
    return text.strip('-')

def get_team_squads(league_id: int, season_id: int) -> Dict:
    """Récupérer tous les effectifs d'une ligue pour une saison"""
    logging.info(f"Récupération des effectifs pour la ligue {league_id}, saison {season_id}")
    
    # Récupérer toutes les équipes de la saison
    teams_url = f"{BASE_URL}/teams/seasons/{season_id}"
    teams_data = make_api_request(teams_url)
    
    if not teams_data or 'data' not in teams_data:
        logging.error(f"Impossible de récupérer les équipes pour la saison {season_id}")
        return {}
    
    teams = {}
    for team in teams_data['data']:
        team_id = team['id']
        team_name = team['name']
        
        # Récupérer l'effectif de l'équipe
        squad_url = f"{BASE_URL}/squads/teams/{team_id}"
        params = {
            'include': 'player.position,player.detailedposition,player.statistics.details',
            'filters[seasons]': season_id
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
                    teams[team_id]['players'].append({
                        'id': player['id'],
                        'name': player['name'],
                        'display_name': player.get('display_name', player['name']),
                        'position': player.get('position', {}).get('name', 'Unknown'),
                        'position_id': player.get('position', {}).get('id', 1),
                        'jersey_number': squad_member.get('jersey_number'),
                        'image': player.get('image_path'),
                        'date_of_birth': player.get('date_of_birth'),
                        'nationality': player.get('nationality', {}).get('name'),
                        'height': player.get('height'),
                        'weight': player.get('weight')
                    })
            
            logging.info(f"  ✓ {team_name}: {len(teams[team_id]['players'])} joueurs")
    
    return teams

def get_player_statistics(player_id: int, season_ids: List[int]) -> Dict:
    """Récupérer les statistiques d'un joueur pour plusieurs saisons"""
    stats = {}
    
    for season_id in season_ids:
        url = f"{BASE_URL}/players/{player_id}"
        params = {
            'include': 'statistics.details',
            'filters[player_statistics][season_id]': season_id
        }
        
        data = make_api_request(url, params)
        
        if data and 'data' in data:
            player_data = data['data']
            if 'statistics' in player_data and player_data['statistics']:
                for stat in player_data['statistics']:
                    if stat.get('season_id') == season_id:
                        stats[season_id] = process_statistics(stat)
                        break
    
    return stats

def process_statistics(stat_data: Dict) -> Dict:
    """Traiter les statistiques d'un joueur"""
    processed = {
        'appearences': stat_data.get('appearences', 0),
        'minutes': stat_data.get('minutes_played', 0),
        'goals': stat_data.get('goals', 0),
        'assists': stat_data.get('assists', 0),
        'yellow_cards': stat_data.get('yellow_cards', 0),
        'red_cards': stat_data.get('red_cards', 0),
        'clean_sheets': stat_data.get('clean_sheets', 0),
    }
    
    # Ajouter les détails si disponibles
    if 'details' in stat_data and stat_data['details']:
        for detail in stat_data['details']:
            detail_data = detail.get('data', {})
            
            # Passes
            if detail.get('type', {}).get('name') == 'Passes':
                processed['passes_total'] = detail_data.get('total', 0)
                processed['passes_accuracy'] = detail_data.get('accuracy', 0)
                processed['key_passes'] = detail_data.get('key_passes', 0)
            
            # Tirs
            elif detail.get('type', {}).get('name') == 'Shots':
                processed['shots_total'] = detail_data.get('total', 0)
                processed['shots_on_target'] = detail_data.get('on_target', 0)
            
            # Défense
            elif detail.get('type', {}).get('name') == 'Defending':
                processed['tackles'] = detail_data.get('tackles', 0)
                processed['interceptions'] = detail_data.get('interceptions', 0)
                processed['blocks'] = detail_data.get('blocks', 0)
            
            # Dribbles
            elif detail.get('type', {}).get('name') == 'Dribbles':
                processed['dribbles_attempted'] = detail_data.get('attempted', 0)
                processed['dribbles_succeeded'] = detail_data.get('succeeded', 0)
            
            # Gardien
            elif detail.get('type', {}).get('name') == 'Goalkeeper':
                processed['saves'] = detail_data.get('saves', 0)
                processed['goals_conceded'] = detail_data.get('goals_conceded', 0)
                processed['penalties_saved'] = detail_data.get('penalties_saved', 0)
    
    return processed

def generate_typescript_files(league_data: Dict, league_info: Dict):
    """Générer les fichiers TypeScript pour une ligue"""
    output_file = f"../data/{league_info['dataFile']}.ts"
    stats_file = f"../data/{league_info['slug']}PlayersCompleteStats.ts"
    
    # Générer le fichier des équipes
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
            typescript_content += f"""      {{
        id: {player['id']},
        nom: "{player['name']}",
        displayName: "{player['display_name']}",
        position: "{player['position']}",
        position_id: {player['position_id']},
        numero: {player['jersey_number'] or 'null'},
        age: "{calculate_age(player['date_of_birth'])}",
        nationalite: "{player['nationality'] or 'Unknown'}",
        taille: {player['height'] or 'null'},
        poids: {player['weight'] or 'null'},
        image: "{player['image'] or ''}",
        playerSlug: "{slugify(player['display_name'])}"
      }},
"""
        typescript_content += """    ]
  },
"""
    
    typescript_content += "];\n"
    
    # Écrire le fichier des équipes
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(typescript_content)
    
    logging.info(f"✓ Fichier TypeScript généré: {output_file}")
    
    # Générer le fichier des statistiques
    stats_content = f"""export const {league_info['slug'].replace('-', '')}PlayersCompleteStats: {{ [key: number]: any }} = {{
"""
    
    for player_id, stats in league_data['stats'].items():
        if stats:
            stats_content += f"  {player_id}: {json.dumps(stats, indent=2)},\n"
    
    stats_content += "};\n"
    
    with open(stats_file, 'w', encoding='utf-8') as f:
        f.write(stats_content)
    
    logging.info(f"✓ Fichier des statistiques généré: {stats_file}")

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

def update_search_database(all_leagues_data: Dict):
    """Mettre à jour la base de données de recherche"""
    search_db = []
    
    for league_id, league_data in all_leagues_data.items():
        league_info = TOP_5_LEAGUES[league_id]
        
        for team_id, team_data in league_data['teams'].items():
            # Ajouter l'équipe
            search_db.append({
                'type': 'club',
                'id': team_id,
                'name': team_data['name'],
                'league': league_info['name'],
                'path': f"/{league_info['slug']}/{team_data['slug']}"
            })
            
            # Ajouter les joueurs
            for player in team_data['players']:
                search_db.append({
                    'type': 'player',
                    'id': player['id'],
                    'name': player['name'],
                    'displayName': player['display_name'],
                    'position': player['position'],
                    'club': team_data['name'],
                    'league': league_info['name'],
                    'path': f"/{league_info['slug']}/{team_data['slug']}/{slugify(player['display_name'])}"
                })
    
    # Écrire le fichier de recherche
    with open('../data/searchDatabase.ts', 'w', encoding='utf-8') as f:
        f.write("export const fullSearchDatabase = ")
        f.write(json.dumps(search_db, indent=2, ensure_ascii=False))
        f.write(";\n")
    
    logging.info(f"✓ Base de données de recherche mise à jour: {len(search_db)} entrées")

def main():
    """Fonction principale"""
    logging.info("=== DÉBUT DE LA MISE À JOUR COMPLÈTE DES DONNÉES ===")
    start_time = time.time()
    
    all_leagues_data = {}
    
    # Traiter chaque ligue
    for league_id, league_info in TOP_5_LEAGUES.items():
        logging.info(f"\n--- Traitement de {league_info['name']} ---")
        
        league_data = {
            'teams': {},
            'stats': {}
        }
        
        # Récupérer la saison actuelle
        current_season_id = league_info['seasons']['2025/2026']
        
        # Récupérer les effectifs
        teams = get_team_squads(league_id, current_season_id)
        league_data['teams'] = teams
        
        # Récupérer les statistiques pour tous les joueurs
        all_player_ids = []
        for team_data in teams.values():
            for player in team_data['players']:
                all_player_ids.append(player['id'])
        
        logging.info(f"Récupération des statistiques pour {len(all_player_ids)} joueurs...")
        
        # Récupérer les stats en parallèle
        season_ids = list(league_info['seasons'].values())
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_player = {
                executor.submit(get_player_statistics, player_id, season_ids): player_id
                for player_id in all_player_ids
            }
            
            for future in as_completed(future_to_player):
                player_id = future_to_player[future]
                try:
                    stats = future.result()
                    if stats:
                        league_data['stats'][player_id] = stats
                except Exception as e:
                    logging.error(f"Erreur pour le joueur {player_id}: {e}")
        
        # Générer les fichiers TypeScript
        generate_typescript_files(league_data, league_info)
        
        all_leagues_data[league_id] = league_data
    
    # Mettre à jour la base de données de recherche
    update_search_database(all_leagues_data)
    
    # Compiler le projet pour vérifier
    logging.info("\n--- Vérification de la compilation TypeScript ---")
    try:
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, 
                              text=True, 
                              cwd='..')
        if result.returncode == 0:
            logging.info("✓ Compilation réussie")
        else:
            logging.error(f"⚠ Erreurs de compilation:\n{result.stderr}")
    except Exception as e:
        logging.error(f"Erreur lors de la compilation: {e}")
    
    elapsed_time = time.time() - start_time
    logging.info(f"\n=== MISE À JOUR TERMINÉE EN {elapsed_time:.2f} SECONDES ===")
    
    # Créer un fichier de statut
    with open('last_update.json', 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'duration': elapsed_time,
            'success': True
        }, f, indent=2)

if __name__ == "__main__":
    main()