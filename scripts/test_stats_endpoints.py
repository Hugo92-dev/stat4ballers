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
    print("Cle API manquante")
    exit(1)

BASE_URL = "https://api.sportmonks.com/v3/football"

print("=== TEST: Stats de tous les joueurs de l'OM sur differentes saisons ===\n")

# Récupérer d'abord l'effectif actuel de l'OM
print("1. Recuperation de l'effectif actuel de l'OM...")
with open('../data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
    content = f.read()
    
# Extraire les IDs des joueurs de l'OM
import re
om_start = content.find('name: "Olympique de Marseille"')
om_end = content.find('name: "AS Monaco"', om_start)
om_section = content[om_start:om_end]
player_ids = re.findall(r'id: (\d+),', om_section)[:5]  # Prendre les 5 premiers pour tester

print(f"IDs des joueurs OM trouves: {player_ids}")

# Tester les stats pour chaque joueur
for player_id in player_ids:
    print(f"\n2. Stats du joueur {player_id}...")
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': 'seasonIds:23435,21792,19735'  # Filtrer sur les 3 dernières saisons de Ligue 1
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            stats = data['data']
            print(f"  Nombre de saisons trouvees: {len(stats)}")
            
            # Chercher les saisons avec des stats
            for stat in stats:
                if stat.get('has_values'):
                    season_id = stat.get('season_id')
                    team_id = stat.get('team_id')
                    details = stat.get('details', [])
                    
                    print(f"\n  Saison {season_id} - Equipe {team_id}:")
                    print(f"    Nombre de stats: {len(details)}")
                    
                    # Afficher quelques stats
                    for detail in details[:10]:
                        if 'type' in detail:
                            type_info = detail['type']
                            print(f"    - {type_info.get('name', 'Unknown')}: {detail.get('value', 0)}")
                    
                    if len(details) > 10:
                        print(f"    ... et {len(details) - 10} autres stats")
                    
                    break  # On a trouvé des stats, on passe au joueur suivant
    else:
        print(f"  Erreur: {response.status_code}")
    
    if player_ids.index(player_id) >= 2:  # Limiter à 3 joueurs pour le test
        break

print("\n=== TEST: Endpoint alternatif - Player statistics by season ===")
# Tester un endpoint différent pour un joueur
player_id = player_ids[0] if player_ids else 20333643
season_id = 23435  # Ligue 1 2025/2026

url = f"{BASE_URL}/players/{player_id}"
params = {
    'api_token': API_KEY,
    'include': 'statistics.details.type',
    'filters': f'playerStatisticSeasons:{season_id}'
}

print(f"\nURL: {url}")
print(f"Params: {params}")

response = requests.get(url, params=params)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        player = data['data']
        print(f"Joueur: {player.get('display_name', player.get('name'))}")
        
        if 'statistics' in player:
            stats = player['statistics']
            print(f"Nombre de saisons avec stats: {len(stats)}")
            if stats:
                print("\nPremiere saison de stats:")
                print(json.dumps(stats[0], indent=2)[:1000])