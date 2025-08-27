#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test pour trouver comment récupérer les stats de la saison 2025/2026
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Recherche du bon endpoint pour les stats 2025/2026...\n")

# Real Madrid
team_id = 3468
season_id = 25659  # Liga 2025/2026

# 1. Test standard squads endpoint
print("1️⃣ Test /squads/teams/{team_id}:")
url = f"{BASE_URL}/squads/teams/{team_id}"
params = {
    "api_token": API_KEY,
    "include": "player"
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    squad = data.get('data', [])
    if squad:
        print(f"   ✅ {len(squad)} joueurs trouvés")
        
        # Prendre le premier joueur pour tester les stats
        if squad[0].get('player'):
            test_player = squad[0]['player']
            test_player_id = test_player['id']
            print(f"   Test avec: {test_player['name']} (ID: {test_player_id})")
            
            # 2. Essayer de récupérer ses stats pour 2025/2026
            print(f"\n2️⃣ Test stats du joueur {test_player_id} pour saison {season_id}:")
            
            # Option A: Via l'endpoint player avec include
            url = f"{BASE_URL}/players/{test_player_id}"
            params = {
                "api_token": API_KEY,
                "include": "statistics",
                "filters[seasons]": season_id
            }
            response = requests.get(url, params=params, timeout=30)
            print(f"   A) /players/{test_player_id} avec include: {response.status_code}")
            
            # Option B: Endpoint direct statistics
            url = f"{BASE_URL}/players/{test_player_id}/statistics/seasons/{season_id}"
            params = {"api_token": API_KEY}
            response = requests.get(url, params=params, timeout=30)
            print(f"   B) /players/{test_player_id}/statistics/seasons/{season_id}: {response.status_code}")
            
            # Option C: Via seasons endpoint
            url = f"{BASE_URL}/seasons/{season_id}/statistics/players/{test_player_id}"
            params = {"api_token": API_KEY}
            response = requests.get(url, params=params, timeout=30)
            print(f"   C) /seasons/{season_id}/statistics/players/{test_player_id}: {response.status_code}")

# 3. Test avec team season statistics
print(f"\n3️⃣ Test /teams/{team_id}/seasons/{season_id}/player-statistics:")
url = f"{BASE_URL}/teams/{team_id}/seasons/{season_id}/player-statistics"
params = {"api_token": API_KEY}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

# 4. Test avec un endpoint générique statistics
print(f"\n4️⃣ Test endpoint générique /statistics:")
url = f"{BASE_URL}/statistics/seasons/{season_id}/teams/{team_id}/players"
params = {"api_token": API_KEY}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

# 5. Test avec topscorers (qui doit avoir des stats)
print(f"\n5️⃣ Test /seasons/{season_id}/topscorers:")
url = f"{BASE_URL}/seasons/{season_id}/topscorers"
params = {
    "api_token": API_KEY,
    "include": "player"
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    topscorers = data.get('data', [])
    if topscorers:
        print(f"   ✅ {len(topscorers)} buteurs trouvés")
        for scorer in topscorers[:3]:
            player = scorer.get('player', {})
            if player:
                player_data = player.get('data', {}) if 'data' in player else player
                print(f"      - {player_data.get('name', 'Unknown')}: {scorer.get('goals', 0)} buts")