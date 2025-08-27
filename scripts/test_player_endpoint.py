#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test de l'endpoint players pour récupérer les stats
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Test de différents endpoints pour les stats...\n")

# Test avec un joueur connu (Bellingham au Real Madrid)
player_id = 346340

print(f"👤 Test avec Bellingham (ID: {player_id})\n")

# 1. Endpoint player avec stats
print("1️⃣ Test endpoint /players/{id} avec stats:")
url = f"{BASE_URL}/players/{player_id}"
params = {
    "api_token": API_KEY,
    "include": "statistics.season,statistics.details"
}

response = requests.get(url, params=params, timeout=30)
if response.status_code == 200:
    data = response.json().get('data', {})
    stats = data.get('statistics', {})
    if stats:
        stats_data = stats.get('data', [])
        print(f"   ✅ {len(stats_data)} saisons de stats trouvées")
        for stat in stats_data[:3]:  # 3 premières saisons
            season = stat.get('season', {})
            season_name = season.get('data', {}).get('name', 'Unknown') if season else 'Unknown'
            goals = stat.get('goals', 0)
            assists = stat.get('assists', 0)
            print(f"      - {season_name}: {goals}B {assists}A")
    else:
        print(f"   ❌ Pas de stats")
else:
    print(f"   ❌ Erreur: {response.status_code}")

# 2. Test avec l'endpoint /players/{id}/statistics
print("\n2️⃣ Test endpoint /players/{id}/statistics:")
url = f"{BASE_URL}/players/{player_id}/statistics"
params = {
    "api_token": API_KEY
}

response = requests.get(url, params=params, timeout=30)
if response.status_code == 200:
    data = response.json().get('data', [])
    print(f"   ✅ {len(data)} entrées de stats trouvées")
    if data:
        for stat in data[:3]:
            print(f"      - Season {stat.get('season_id')}: {stat.get('goals', 0)}B {stat.get('assists', 0)}A")
else:
    print(f"   ❌ Erreur: {response.status_code}")

# 3. Test avec team squad + statistics
print("\n3️⃣ Test avec squad Real Madrid + statistics:")
url = f"{BASE_URL}/squads/teams/3468"
params = {
    "api_token": API_KEY,
    "include": "player.statistics"
}

response = requests.get(url, params=params, timeout=30)
if response.status_code == 200:
    data = response.json().get('data', [])
    print(f"   ✅ {len(data)} joueurs trouvés")
    # Chercher Bellingham
    for item in data:
        player = item.get('player', {})
        if player.get('id') == player_id:
            stats = player.get('statistics', {})
            if stats:
                stats_data = stats.get('data', [])
                print(f"      Bellingham: {len(stats_data)} saisons de stats")
            else:
                print(f"      Bellingham: Pas de stats incluses")
            break
else:
    print(f"   ❌ Erreur: {response.status_code}")