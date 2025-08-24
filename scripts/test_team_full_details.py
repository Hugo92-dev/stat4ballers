#!/usr/bin/env python3
"""
Test complet pour récupérer TOUTES les infos d'une équipe
"""

import sys
import requests
import json

# Fix encodage Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Test avec l'OM (ID 44)
team_id = 44
print("=== RECUPERATION COMPLETE DES DETAILS DE L'OM ===\n")

# 1. Infos de base avec venue
print("1. Infos de base + Stade...")
url = f"{BASE_URL}/teams/{team_id}"
params = {'include': 'venue'}
response = requests.get(url, headers=headers, params=params)

team_data = {}
if response.status_code == 200:
    data = response.json()['data']
    team_data['name'] = data.get('name')
    team_data['short_code'] = data.get('short_code')
    team_data['founded'] = data.get('founded')
    
    venue = data.get('venue')
    if venue:
        team_data['stadium'] = {
            'name': venue.get('name'),
            'capacity': venue.get('capacity'),
            'address': venue.get('address'),
            'surface': venue.get('surface'),
            'image': venue.get('image_path')
        }
    print(f"   ✓ {team_data['name']} - Stade: {team_data.get('stadium', {}).get('name')}")

# 2. Coach actuel
print("\n2. Entraîneur actuel...")
url = f"{BASE_URL}/coaches/teams/{team_id}/current"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    coaches = data.get('data', [])
    if coaches:
        coach = coaches[0] if isinstance(coaches, list) else coaches
        team_data['coach'] = {
            'name': coach.get('display_name') or coach.get('name'),
            'nationality': coach.get('nationality', {}).get('name') if coach.get('nationality') else None,
            'image': coach.get('image_path'),
            'date_of_birth': coach.get('date_of_birth')
        }
        print(f"   ✓ Coach: {team_data['coach']['name']}")

# 3. Statistiques de la saison actuelle
print("\n3. Statistiques saison 2025/2026...")
season_id = 25651  # Ligue 1 2025/2026
url = f"{BASE_URL}/statistics/seasons/{season_id}/teams/{team_id}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    stats = data.get('data', [])
    if stats:
        team_data['statistics'] = {}
        for stat in stats:
            stat_type = stat.get('type', {}).get('name')
            value = stat.get('value', {})
            if stat_type:
                team_data['statistics'][stat_type] = value
        print(f"   ✓ {len(team_data.get('statistics', {}))} statistiques récupérées")

# 4. Trophées / Palmarès (méthode alternative)
print("\n4. Palmarès...")
# On va définir manuellement le palmarès de l'OM
team_data['trophies'] = {
    'Ligue 1': 9,
    'Coupe de France': 10,
    'Coupe de la Ligue': 3,
    'Trophée des Champions': 3,
    'Ligue des Champions': 1,
    'Coupe Intertoto': 1
}
print(f"   ✓ {sum(team_data['trophies'].values())} trophées au total")

# Affichage final
print("\n" + "="*50)
print("RESUME DES DONNEES RECUPEREES:")
print("="*50)

print(f"\n📍 CLUB: {team_data.get('name')}")
print(f"   Fondé en: {team_data.get('founded')}")

if team_data.get('stadium'):
    print(f"\n🏟️ STADE: {team_data['stadium']['name']}")
    print(f"   Capacité: {team_data['stadium']['capacity']} places")
    print(f"   Surface: {team_data['stadium']['surface']}")

if team_data.get('coach'):
    print(f"\n👨‍💼 ENTRAINEUR: {team_data['coach']['name']}")
    if team_data['coach'].get('nationality'):
        print(f"   Nationalité: {team_data['coach']['nationality']}")

if team_data.get('statistics'):
    print(f"\n📊 STATISTIQUES (quelques exemples):")
    for key, value in list(team_data['statistics'].items())[:5]:
        if isinstance(value, dict):
            print(f"   {key}: {value.get('all', value.get('total', value))}")
        else:
            print(f"   {key}: {value}")

if team_data.get('trophies'):
    print(f"\n🏆 PALMARES:")
    for trophy, count in team_data['trophies'].items():
        if count > 0:
            print(f"   {trophy}: {count}x")

# Sauvegarder
with open('om_full_details.json', 'w', encoding='utf-8') as f:
    json.dump(team_data, f, ensure_ascii=False, indent=2)
print(f"\n✅ Données sauvegardées dans om_full_details.json")