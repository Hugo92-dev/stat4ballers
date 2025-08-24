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

print("=== TEST: Vérification de l'accès API et des plans ===\n")

# 1. Vérifier le statut de l'API et notre plan
print("1. Vérification du statut de l'API...")
url = f"{BASE_URL}/my"
params = {'api_token': API_KEY}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        plan_info = data['data']
        print(f"  Plan: {plan_info.get('name', 'Unknown')}")
        print(f"  Requêtes restantes: {plan_info.get('requests_left', 'Unknown')}")
        
        if 'included_features' in plan_info:
            features = plan_info['included_features']
            print(f"  Features incluses: {', '.join(features)}")
        
        if 'excluded_features' in plan_info:
            excluded = plan_info['excluded_features'] 
            print(f"  Features exclues: {', '.join(excluded[:5]) if excluded else 'Aucune'}")
else:
    print(f"  Erreur: {response.status_code}")

# 2. Tester avec Aubameyang (ID: 186418)
print("\n2. Test avec Aubameyang (ID: 186418)...")
url = f"{BASE_URL}/players/186418"
params = {
    'api_token': API_KEY,
    'include': 'statistics.details.type'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        player = data['data']
        print(f"  Joueur: {player.get('display_name', player.get('name'))}")
        
        if 'statistics' in player:
            stats = player['statistics']
            print(f"  Nombre de saisons avec stats: {len(stats)}")
            
            # Chercher les stats avec l'OM
            om_stats = [s for s in stats if s.get('team_id') == 44]
            print(f"  Saisons avec l'OM: {len(om_stats)}")
            
            if om_stats:
                latest = om_stats[0]
                details = latest.get('details', [])
                
                for detail in details[:5]:
                    if 'type' in detail:
                        stat_name = detail['type'].get('name', '')
                        value = detail.get('value', {})
                        
                        if isinstance(value, dict):
                            total = value.get('total', value.get('average', 0))
                            print(f"    {stat_name}: {total}")
                        else:
                            print(f"    {stat_name}: {value}")

# 3. Vérifier les saisons disponibles pour la Ligue 1
print("\n3. Saisons disponibles pour la Ligue 1...")
url = f"{BASE_URL}/leagues/61/seasons"
params = {
    'api_token': API_KEY
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        seasons = data['data']
        print(f"  Nombre de saisons: {len(seasons)}")
        
        # Afficher les 5 dernières saisons
        recent_seasons = sorted(seasons, key=lambda x: x.get('ending_at', ''), reverse=True)[:5]
        
        for season in recent_seasons:
            print(f"  - {season.get('name')} (ID: {season.get('id')}) - Fin: {season.get('ending_at')}")

# 4. Test spécifique: Stats de Greenwood pour la saison en cours
print("\n4. Recherche de la bonne saison pour Greenwood...")

# Tester plusieurs IDs de saison possibles
test_seasons = [21792, 23643, 25651, 24893, 23672]

for season_id in test_seasons:
    url = f"{BASE_URL}/statistics/seasons/players/28575687"
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
                team_id = stat.get('team_id')
                details = stat.get('details', [])
                
                # Chercher les buts
                goals = 0
                apps = 0
                for detail in details:
                    if 'type' in detail:
                        if detail['type'].get('name') == 'Goals':
                            value = detail.get('value', {})
                            goals = value.get('total', 0) if isinstance(value, dict) else value
                        elif detail['type'].get('name') == 'Appearances':
                            value = detail.get('value', {})
                            apps = value.get('total', 0) if isinstance(value, dict) else value
                
                if apps > 0:
                    print(f"  Season {season_id} - Team {team_id}: {apps} matchs, {goals} buts")