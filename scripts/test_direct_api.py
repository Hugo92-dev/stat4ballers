#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test direct de l'API pour voir ce qui est vraiment retourné
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Test direct de l'API SportMonks...\n")

# Test avec un joueur connu (Bellingham)
player_id = 346340

print(f"Test avec Bellingham (ID: {player_id})\n")

# 1. Test simple sans include
print("1️⃣ Sans include:")
url = f"{BASE_URL}/players/{player_id}"
params = {"api_token": API_KEY}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Data keys: {list(data.get('data', {}).keys())}")

# 2. Test avec include statistics
print("\n2️⃣ Avec include=statistics:")
params = {"api_token": API_KEY, "include": "statistics"}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    player_data = data.get('data', {})
    if 'statistics' in player_data:
        stats = player_data['statistics']
        if 'data' in stats:
            stats_list = stats['data']
            print(f"   ✅ {len(stats_list)} entrées de stats trouvées")
            for stat in stats_list[:3]:
                season_id = stat.get('season_id')
                goals = stat.get('goals', 0)
                assists = stat.get('assists', 0)
                print(f"      Season {season_id}: {goals}B {assists}A")

# 3. Test de l'endpoint teams pour voir la structure
print("\n3️⃣ Test /teams/3468 (Real Madrid):")
url = f"{BASE_URL}/teams/3468"
params = {"api_token": API_KEY}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Data keys: {list(data.get('data', {}).keys())}")

# 4. Test squads avec player.statistics
print("\n4️⃣ Test /squads/teams/3468 avec include:")
url = f"{BASE_URL}/squads/teams/3468"
params = {"api_token": API_KEY, "include": "player.statistics"}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    squad = data.get('data', [])
    if squad and squad[0].get('player'):
        player = squad[0]['player']
        print(f"   Premier joueur: {player.get('name')}")
        if 'statistics' in player:
            stats = player['statistics']
            if 'data' in stats:
                print(f"      ✅ Stats incluses: {len(stats['data'])} entrées")