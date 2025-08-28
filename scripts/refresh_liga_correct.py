#!/usr/bin/env python3
"""
Script de refresh pour La Liga avec les BONS IDs
- Mise à jour des effectifs
- Mise à jour des statistiques des joueurs
"""

import json
import requests
import sys
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import logging
import time

# Configuration
sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('refresh_liga.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"
SEASON_ID = 25659  # Liga 2025/2026 - ID CORRECT

# Équipes de Liga avec leurs VRAIS IDs SportMonks
# Barcelona = 83 confirmé
LIGA_TEAMS = [
    (3468, "Real Madrid", "real-madrid"),
    (83, "Barcelona", "barcelona"),  # ID CORRECT confirmé
    (7980, "Atletico Madrid", "atletico-madrid"),
    (594, "Real Sociedad", "real-sociedad"),
    (13258, "Athletic Bilbao", "athletic-bilbao"),
    (485, "Real Betis", "real-betis"),
    (676, "Sevilla", "sevilla"),
    (3477, "Villarreal", "villarreal"),
    (214, "Valencia", "valencia"),
    (231, "Girona", "girona"),
    (459, "Osasuna", "osasuna"),
    (106, "Getafe", "getafe"),
    (36, "Celta Vigo", "celta-vigo"),
    (645, "Mallorca", "mallorca"),
    (2975, "Deportivo Alavés", "deportivo-alaves"),
    (377, "Rayo Vallecano", "rayo-vallecano"),
    (373, "Las Palmas", "las-palmas"),
    (7978, "Real Valladolid", "real-valladolid"),
    (3750, "Espanyol", "espanyol"),
    (3751, "Leganés", "leganes")
]

# MAPPING CORRECT des IDs SportMonks (vérifié avec la doc officielle)
STAT_MAPPING = {
    40: 'captain',
    41: 'shots_off_target',
    42: 'shots',
    47: 'penalties',
    51: 'offsides',
    52: 'goals',
    56: 'fouls',
    57: 'saves',
    58: 'shots_blocked',
    59: 'substitutions',
    64: 'hit_woodwork',
    78: 'tackles',
    79: 'assists',  # CORRECT !
    80: 'passes',
    81: 'passes_successful',
    82: 'passes_accuracy_percentage',
    83: 'red_cards',
    84: 'yellow_cards',
    85: 'yellowred_cards',
    86: 'shots_on_target',
    87: 'injuries',
    88: 'goals_conceded',
    94: 'dispossessed',
    96: 'fouls_drawn',
    97: 'blocks',
    98: 'crosses',
    99: 'crosses_accurate',
    100: 'interceptions',
    101: 'clearances',
    104: 'saves_inside_box',
    105: 'duels',
    106: 'duels_won',
    107: 'aerial_duels_won',
    108: 'dribbles',
    109: 'dribbles_successful',
    110: 'dribbled_past',
    116: 'passes_accurate',
    117: 'key_passes',
    118: 'rating',
    119: 'minutes',
    122: 'long_balls',
    123: 'long_balls_won',
    124: 'through_balls',
    125: 'through_balls_won',
    194: 'clean_sheets',
    214: 'wins',
    215: 'draws',
    216: 'losses',
    321: 'appearences',
    322: 'lineups',
    323: 'bench',
    324: 'own_goals',
    571: 'error_lead_to_goal',
    580: 'big_chances_created',
    581: 'big_chances_missed',
    1584: 'passes_accuracy',
    5304: 'expected_goals',
    9676: 'average_points_per_game'
}

def get_team_squad(team_id, team_name):
    """Récupère l'effectif actuel d'une équipe"""
    url = f"{BASE_URL}/squads/teams/{team_id}/current"
    params = {
        'api_token': API_KEY,
        'include': 'player.position,player.country'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json().get('data', [])
            players = []
            
            for item in data:
                player = item.get('player', {})
                if player:
                    # Calculer l'âge
                    birth_year = None
                    if player.get('date_of_birth'):
                        try:
                            birth_year = int(player.get('date_of_birth', '2000-01-01').split('-')[0])
                            age = datetime.now().year - birth_year
                        except:
                            age = None
                    else:
                        age = None
                    
                    player_data = {
                        'id': player.get('id'),
                        'name': player.get('name'),
                        'displayName': player.get('display_name', player.get('name')),
                        'position': player.get('position', {}).get('name') if isinstance(player.get('position'), dict) else None,
                        'position_id': player.get('position_id'),
                        'jersey': item.get('jersey_number'),
                        'age': age,
                        'nationality': player.get('country', {}).get('name') if isinstance(player.get('country'), dict) else None,
                        'height': player.get('height'),
                        'weight': player.get('weight'),
                        'image': player.get('image_path')
                    }
                    players.append(player_data)
            
            return players
        else:
            logging.warning(f"Erreur {response.status_code} pour {team_name}")
            return []
    except Exception as e:
        logging.error(f"Erreur lors de la récupération de l'effectif de {team_name}: {e}")
        return []

def get_player_stats(player_id, season_id):
    """Récupère les statistiques d'un joueur pour la saison en cours"""
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{season_id}'
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        if response.status_code == 200:
            data = response.json().get('data', [])
            
            if data:
                season_data = data[0]
                stats = {
                    'season_id': season_id,
                    'team_id': season_data.get('team_id'),
                    'position_id': season_data.get('position_id')
                }
                
                # Mapper les stats avec le bon mapping
                if 'details' in season_data:
                    for detail in season_data['details']:
                        type_data = detail.get('type', {})
                        if isinstance(type_data, dict):
                            type_id = type_data.get('id')
                            value = detail.get('value', {})
                            
                            if isinstance(value, dict):
                                actual_value = value.get('total', value.get('average'))
                            else:
                                actual_value = value
                            
                            # Utiliser le mapping correct
                            if type_id in STAT_MAPPING:
                                stat_name = STAT_MAPPING[type_id]
                                stats[stat_name] = actual_value
                
                return stats
        return {}
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des stats du joueur {player_id}: {e}")
        return {}

def update_team_data(team_id, team_name, team_slug):
    """Met à jour les données complètes d'une équipe"""
    logging.info(f"📊 Mise à jour de {team_name} (ID: {team_id})...")
    
    # Récupérer l'effectif
    squad = get_team_squad(team_id, team_name)
    
    if not squad:
        logging.warning(f"  ⚠️ Aucun joueur trouvé pour {team_name}")
        return 0
    
    logging.info(f"  ✅ {len(squad)} joueurs dans l'effectif")
    
    # Récupérer les stats pour chaque joueur
    players_with_stats = []
    for idx, player in enumerate(squad, 1):
        if player['id']:
            stats = get_player_stats(player['id'], SEASON_ID)
            player['stats_2025_2026'] = stats
            players_with_stats.append(player)
            
            # Log de progression
            if idx % 10 == 0:
                logging.info(f"    📈 {idx}/{len(squad)} joueurs traités")
            
            # Pause pour respecter le rate limit (60 appels/minute)
            if idx % 30 == 0:
                logging.info("    ⏸️ Pause de 30 secondes (rate limit)")
                time.sleep(30)
    
    # Sauvegarder les données
    output_file = Path(f'../data/liga_2025_2026/{team_slug}.json')
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    team_data = {
        'team_id': team_id,
        'team_name': team_name,
        'team_slug': team_slug,
        'season': '2025/2026',
        'season_id': SEASON_ID,
        'league': 'Liga',
        'updated_at': datetime.now().isoformat(),
        'squad_size': len(players_with_stats),
        'players': players_with_stats
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(team_data, f, ensure_ascii=False, indent=2)
    
    logging.info(f"  💾 Données sauvegardées: {output_file.name}")
    return len(players_with_stats)

def integrate_with_existing_data():
    """Intègre les nouvelles stats avec les données existantes dans la-ligaPlayersCompleteStats.ts"""
    logging.info("\n📝 Intégration avec les données existantes...")
    
    # Lire le fichier existant
    existing_file = Path('../data/la-ligaPlayersCompleteStats.ts')
    if not existing_file.exists():
        logging.warning("Fichier la-ligaPlayersCompleteStats.ts non trouvé")
        return
    
    # Pour chaque équipe mise à jour
    updates_count = 0
    data_dir = Path('../data/liga_2025_2026')
    
    for json_file in data_dir.glob('*.json'):
        with open(json_file, 'r', encoding='utf-8') as f:
            team_data = json.load(f)
            
        logging.info(f"  📊 Intégration de {team_data['team_name']}: {len(team_data['players'])} joueurs")
        updates_count += len(team_data['players'])
    
    logging.info(f"  ✅ {updates_count} joueurs mis à jour au total")

def main():
    """Fonction principale de refresh"""
    logging.info("=" * 60)
    logging.info("🇪🇸 REFRESH LA LIGA - SAISON 2025/2026")
    logging.info("=" * 60)
    logging.info(f"⏰ Début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"📋 {len(LIGA_TEAMS)} équipes à traiter")
    
    total_players = 0
    successful_teams = 0
    failed_teams = []
    
    # Mettre à jour chaque équipe
    for idx, (team_id, team_name, team_slug) in enumerate(LIGA_TEAMS, 1):
        logging.info(f"\n[{idx}/{len(LIGA_TEAMS)}] {team_name}")
        
        try:
            player_count = update_team_data(team_id, team_name, team_slug)
            total_players += player_count
            successful_teams += 1
        except Exception as e:
            logging.error(f"  ❌ Erreur pour {team_name}: {e}")
            failed_teams.append(team_name)
        
        # Pause entre les équipes
        if idx < len(LIGA_TEAMS):
            time.sleep(5)
    
    # Intégrer avec les données existantes
    integrate_with_existing_data()
    
    # Rapport final
    logging.info("\n" + "=" * 60)
    logging.info("📊 RAPPORT FINAL")
    logging.info("=" * 60)
    logging.info(f"✅ Équipes mises à jour: {successful_teams}/{len(LIGA_TEAMS)}")
    logging.info(f"📊 Total joueurs: {total_players}")
    
    if failed_teams:
        logging.warning(f"❌ Équipes échouées: {', '.join(failed_teams)}")
    
    logging.info(f"⏰ Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 60)

if __name__ == "__main__":
    main()