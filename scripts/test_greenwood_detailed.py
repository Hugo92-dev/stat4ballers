import requests
import json
from dotenv import load_dotenv
import os
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les variables d'environnement
load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

if not API_KEY:
    print("Clé API manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

print("=== TEST DÉTAILLÉ: Stats de Mason Greenwood pour l'OM ===\n")

# Tester différentes façons de récupérer les stats
player_id = 28575687
om_team_id = 44

# Méthode 1: Stats par saison avec filtre sur l'équipe OM
print("1. Stats filtrées par équipe OM (team_id=44)...")
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {
    'api_token': API_KEY,
    'include': 'details.type',
    'filters': f'teamIds:{om_team_id}'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        stats = data['data']
        print(f"  Nombre de saisons trouvées avec l'OM: {len(stats)}\n")
        
        for stat in stats:
            if stat.get('has_values'):
                season_id = stat.get('season_id')
                details = stat.get('details', [])
                
                # Extraire toutes les stats importantes
                stats_dict = {}
                for detail in details:
                    if 'type' in detail:
                        stat_name = detail['type'].get('name', '')
                        value = detail.get('value', {})
                        
                        if isinstance(value, dict):
                            stats_dict[stat_name] = value.get('total', value.get('average', 0))
                        else:
                            stats_dict[stat_name] = value
                
                print(f"  Season ID: {season_id}")
                print(f"    Matchs: {stats_dict.get('Appearances', 0)}")
                print(f"    Buts: {stats_dict.get('Goals', 0)}")
                print(f"    Passes: {stats_dict.get('Assists', 0)}")
                print(f"    Minutes: {stats_dict.get('Minutes Played', 0)}")
                print(f"    Rating: {stats_dict.get('Rating', 0)}")
                print()

# Méthode 2: Stats de la saison actuelle Ligue 1
print("\n2. Stats pour la saison Ligue 1 actuelle (league_id=61)...")

# D'abord récupérer la saison actuelle de Ligue 1
league_url = f"{BASE_URL}/leagues/61"
league_params = {
    'api_token': API_KEY,
    'include': 'currentSeason'
}

league_response = requests.get(league_url, params=league_params)

if league_response.status_code == 200:
    league_data = league_response.json()
    if 'data' in league_data:
        current_season = league_data['data'].get('currentSeason')
        if current_season:
            current_season_id = current_season.get('id')
            print(f"  Saison actuelle Ligue 1: {current_season.get('name')} (ID: {current_season_id})\n")
            
            # Récupérer les stats de Greenwood pour cette saison
            url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
            params = {
                'api_token': API_KEY,
                'include': 'details.type',
                'filters': f'seasonIds:{current_season_id}'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and len(data['data']) > 0:
                    stat = data['data'][0]
                    if stat.get('has_values'):
                        details = stat.get('details', [])
                        
                        # Extraire toutes les stats
                        for detail in details[:15]:  # Afficher les 15 premières stats
                            if 'type' in detail:
                                stat_name = detail['type'].get('name', '')
                                value = detail.get('value', {})
                                
                                if isinstance(value, dict):
                                    total = value.get('total', value.get('average', 0))
                                    print(f"    {stat_name}: {total}")
                                else:
                                    print(f"    {stat_name}: {value}")

# Méthode 3: Récupérer les saisons précédentes de Ligue 1
print("\n3. Stats pour la saison 2024/25 de Ligue 1...")

# ID de la saison 2024/25 de Ligue 1 (à déterminer)
seasons_url = f"{BASE_URL}/seasons"
seasons_params = {
    'api_token': API_KEY,
    'filters': 'leagueIds:61',
    'include': 'league'
}

seasons_response = requests.get(seasons_url, params=seasons_params)

if seasons_response.status_code == 200:
    seasons_data = seasons_response.json()
    if 'data' in seasons_data:
        ligue1_seasons = seasons_data['data']
        
        # Chercher la saison 2024/25
        for season in ligue1_seasons:
            if '2024' in season.get('name', '') or '24/25' in season.get('name', ''):
                season_id = season.get('id')
                print(f"  Saison trouvée: {season.get('name')} (ID: {season_id})")
                
                # Récupérer les stats de Greenwood
                url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
                params = {
                    'api_token': API_KEY,
                    'include': 'details.type',
                    'filters': f'seasonIds:{season_id}'
                }
                
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    if 'data' in data and len(data['data']) > 0:
                        stat = data['data'][0]
                        if stat.get('has_values'):
                            details = stat.get('details', [])
                            
                            stats_dict = {}
                            for detail in details:
                                if 'type' in detail:
                                    stat_name = detail['type'].get('name', '')
                                    value = detail.get('value', {})
                                    
                                    if isinstance(value, dict):
                                        stats_dict[stat_name] = value.get('total', value.get('average', 0))
                                    else:
                                        stats_dict[stat_name] = value
                            
                            print(f"    Matchs: {stats_dict.get('Appearances', 0)}")
                            print(f"    Buts: {stats_dict.get('Goals', 0)}")
                            print(f"    Passes: {stats_dict.get('Assists', 0)}")
                            print(f"    Minutes: {stats_dict.get('Minutes Played', 0)}")
                            print()
                
                break