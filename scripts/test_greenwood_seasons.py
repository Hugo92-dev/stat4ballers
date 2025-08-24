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

print("=== TEST: Stats de Mason Greenwood (ID: 28575687) ===\n")

# Récupérer toutes les stats de Greenwood
url = f"{BASE_URL}/statistics/seasons/players/28575687"
params = {
    'api_token': API_KEY,
    'include': 'details.type'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        all_stats = data['data']
        print(f"Nombre total de saisons trouvées: {len(all_stats)}\n")
        
        # Filtrer les saisons avec des stats
        seasons_with_stats = [s for s in all_stats if s.get('has_values')]
        
        print(f"Saisons avec des stats: {len(seasons_with_stats)}\n")
        
        for stat in seasons_with_stats:
            season_id = stat.get('season_id')
            team_id = stat.get('team_id')
            details = stat.get('details', [])
            
            # Chercher les buts et les matchs
            goals = 0
            matches = 0
            assists = 0
            
            for detail in details:
                if 'type' in detail:
                    stat_name = detail['type'].get('name', '')
                    value = detail.get('value', {})
                    
                    if stat_name == 'Goals':
                        goals = value.get('total', 0) if isinstance(value, dict) else value
                    elif stat_name == 'Appearances':
                        matches = value.get('total', 0) if isinstance(value, dict) else value
                    elif stat_name == 'Assists':
                        assists = value.get('total', 0) if isinstance(value, dict) else value
            
            print(f"Season ID: {season_id} - Team ID: {team_id}")
            print(f"  Matchs: {matches}, Buts: {goals}, Passes: {assists}")
            
            # Si c'est une saison importante, afficher plus de détails
            if goals > 15 or (team_id == 44 and matches > 5):
                print(f"  >>> SAISON IMPORTANTE! <<<")
                
                # Récupérer les infos de la saison
                season_url = f"{BASE_URL}/seasons/{season_id}"
                season_params = {'api_token': API_KEY}
                season_response = requests.get(season_url, params=season_params)
                
                if season_response.status_code == 200:
                    season_data = season_response.json()
                    if 'data' in season_data:
                        season_info = season_data['data']
                        print(f"  Nom de la saison: {season_info.get('name', 'Unknown')}")
                        print(f"  League ID: {season_info.get('league_id')}")
                        print(f"  Fin: {season_info.get('ending_at', 'Unknown')}")
            
            print()
else:
    print(f"Erreur: {response.status_code}")

print("\n=== Récupération des détails de l'équipe 44 (OM) ===")
team_url = f"{BASE_URL}/teams/44"
team_params = {'api_token': API_KEY}
team_response = requests.get(team_url, params=team_params)

if team_response.status_code == 200:
    team_data = team_response.json()
    if 'data' in team_data:
        team_info = team_data['data']
        print(f"Équipe: {team_info.get('name', 'Unknown')}")
        print(f"ID: {team_info.get('id')}")