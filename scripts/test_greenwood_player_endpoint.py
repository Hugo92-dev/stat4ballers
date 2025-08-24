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

print("=== TEST: Endpoint player avec stats complètes ===\n")

player_id = 28575687  # Mason Greenwood

# Méthode 1: Endpoint player avec toutes les stats
print("1. Récupération via endpoint /players/{id} avec toutes les stats...")
url = f"{BASE_URL}/players/{player_id}"
params = {
    'api_token': API_KEY,
    'include': 'statistics.details.type,team,position'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data:
        player = data['data']
        print(f"Joueur: {player.get('display_name', player.get('name'))}")
        
        if 'team' in player:
            team = player['team']
            print(f"Équipe actuelle: {team.get('name')} (ID: {team.get('id')})")
        
        if 'statistics' in player:
            all_stats = player['statistics']
            print(f"\nNombre total de saisons avec stats: {len(all_stats)}\n")
            
            # Filtrer les stats de l'OM
            om_stats = [s for s in all_stats if s.get('team_id') == 44]
            print(f"Saisons avec l'OM: {len(om_stats)}\n")
            
            for stat_data in om_stats:
                season_id = stat_data.get('season_id')
                
                # Extraire les stats
                details = stat_data.get('details', [])
                stats_dict = {}
                
                for detail in details:
                    if 'type' in detail:
                        stat_name = detail['type'].get('name', '')
                        value = detail.get('value', {})
                        
                        if isinstance(value, dict):
                            stats_dict[stat_name] = value.get('total', value.get('average', 0))
                        else:
                            stats_dict[stat_name] = value
                
                print(f"Season ID: {season_id}")
                print(f"  Matchs: {stats_dict.get('Appearances', 0)}")
                print(f"  Buts: {stats_dict.get('Goals', 0)}")
                print(f"  Passes décisives: {stats_dict.get('Assists', 0)}")
                print(f"  Minutes: {stats_dict.get('Minutes Played', 0)}")
                print(f"  Expected Goals: {stats_dict.get('Expected Goals', 0)}")
                print(f"  Tirs: {stats_dict.get('Shots Total', 0)}")
                print(f"  Tirs cadrés: {stats_dict.get('Shots On Target', 0)}")
                print()

# Méthode 2: Récupération des stats de la saison 2024/25 spécifiquement
print("\n2. Récupération des stats pour la saison ID 21792 (2024/25 potentiel)...")
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {
    'api_token': API_KEY,
    'include': 'details.type',
    'filters': 'seasonIds:21792'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        stat_data = data['data'][0]
        
        if stat_data.get('has_values'):
            print(f"  Team ID: {stat_data.get('team_id')}")
            
            details = stat_data.get('details', [])
            for detail in details:
                if 'type' in detail:
                    stat_name = detail['type'].get('name', '')
                    value = detail.get('value', {})
                    
                    if stat_name in ['Goals', 'Assists', 'Appearances', 'Minutes Played']:
                        if isinstance(value, dict):
                            total = value.get('total', value.get('average', 0))
                            print(f"  {stat_name}: {total}")
                        else:
                            print(f"  {stat_name}: {value}")
        else:
            print("  Pas de stats pour cette saison")

# Méthode 3: Tester avec la saison 23643 (autre ID possible)
print("\n3. Test avec Season ID 23643...")
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {
    'api_token': API_KEY,
    'include': 'details.type',
    'filters': 'seasonIds:23643'
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    if 'data' in data and len(data['data']) > 0:
        stat_data = data['data'][0]
        
        if stat_data.get('has_values'):
            print(f"  Team ID: {stat_data.get('team_id')}")
            
            details = stat_data.get('details', [])
            stats_dict = {}
            
            for detail in details:
                if 'type' in detail:
                    stat_name = detail['type'].get('name', '')
                    value = detail.get('value', {})
                    
                    if isinstance(value, dict):
                        stats_dict[stat_name] = value.get('total', value.get('average', 0))
                    else:
                        stats_dict[stat_name] = value
            
            print(f"  Matchs: {stats_dict.get('Appearances', 0)}")
            print(f"  Buts: {stats_dict.get('Goals', 0)}")
            print(f"  Passes: {stats_dict.get('Assists', 0)}")
            print(f"  Minutes: {stats_dict.get('Minutes Played', 0)}")
        else:
            print("  Pas de stats pour cette saison")