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

print("=== TEST: TOUTES les stats de Mason Greenwood ===\n")

player_id = 20333643  # Mason Greenwood

# IDs des saisons qui nous intéressent
SEASON_IDS = {
    # Ligue 1
    21779: "2023/2024 Ligue 1",
    23643: "2024/2025 Ligue 1", 
    25651: "2025/2026 Ligue 1",
    # Liga
    21694: "2023/2024 Liga",
    23621: "2024/2025 Liga",
    25659: "2025/2026 Liga",
    # Premier League
    21646: "2023/2024 PL",
    23614: "2024/2025 PL",
    25583: "2025/2026 PL"
}

# Récupérer TOUTES les stats du joueur pour ces saisons
season_ids_str = ",".join(map(str, SEASON_IDS.keys()))

url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {
    'api_token': API_KEY,
    'include': 'details.type',
    'filters': f'seasonIds:{season_ids_str}'
}

print(f"URL: {url}")
print(f"Filtres: seasonIds={list(SEASON_IDS.keys())}\n")

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        all_stats = data['data']
        print(f"Nombre de saisons trouvées: {len(all_stats)}\n")
        
        for stat_data in all_stats:
            if stat_data.get('has_values'):
                season_id = stat_data.get('season_id')
                team_id = stat_data.get('team_id')
                season_name = SEASON_IDS.get(season_id, f"Season_{season_id}")
                
                print(f"{'='*60}")
                print(f"Saison: {season_name} (ID: {season_id})")
                print(f"Équipe ID: {team_id}")
                
                # Récupérer le nom de l'équipe
                team_url = f"{BASE_URL}/teams/{team_id}"
                team_params = {'api_token': API_KEY}
                team_response = requests.get(team_url, params=team_params)
                
                if team_response.status_code == 200:
                    team_data = team_response.json()
                    if 'data' in team_data:
                        team_name = team_data['data'].get('name', 'Unknown')
                        print(f"Équipe: {team_name}")
                
                print("-" * 60)
                
                # Extraire les stats importantes
                details = stat_data.get('details', [])
                stats_dict = {}
                
                for detail in details:
                    if 'type' in detail:
                        stat_name = detail['type'].get('name', '')
                        value = detail.get('value', {})
                        
                        if isinstance(value, dict):
                            total = value.get('total', value.get('average', None))
                        else:
                            total = value
                        
                        stats_dict[stat_name] = total
                
                # Afficher les stats clés
                print(f"Matchs: {stats_dict.get('Appearances', 'N/A')}")
                print(f"Buts: {stats_dict.get('Goals', 'N/A')}")
                print(f"Passes décisives: {stats_dict.get('Assists', 'N/A')}")
                print(f"Minutes: {stats_dict.get('Minutes Played', 'N/A')}")
                print(f"Tirs: {stats_dict.get('Shots Total', 'N/A')}")
                print(f"Penalties gagnés: {stats_dict.get('Penalties Won', 'N/A')}")
                print(f"Penalties marqués: {stats_dict.get('Penalties Scored', 'N/A')}")
                print(f"Penalties manqués: {stats_dict.get('Penalties Missed', 'N/A')}")
                print(f"xG: {stats_dict.get('Expected Goals', 'N/A')}")
                print(f"xA: {stats_dict.get('Expected Assists', 'N/A')}")
                
                # Afficher TOUTES les stats disponibles
                print("\nToutes les stats disponibles:")
                for stat_name, value in sorted(stats_dict.items()):
                    if value is not None and value != 0:
                        print(f"  - {stat_name}: {value}")
                
                # Stats avec valeur 0
                zero_stats = [name for name, value in stats_dict.items() if value == 0]
                if zero_stats:
                    print(f"\nStats avec valeur 0 (vraies valeurs, pas des null):")
                    print(f"  {', '.join(zero_stats[:10])}")
                    if len(zero_stats) > 10:
                        print(f"  ... et {len(zero_stats)-10} autres")
                
                print()
else:
    print(f"Erreur: {response.status_code}")
    if response.text:
        print(response.text)