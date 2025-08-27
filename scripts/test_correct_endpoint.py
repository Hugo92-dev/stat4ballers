#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test pour trouver le bon endpoint des stats
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Test des endpoints possibles pour les stats...\n")

player_id = 165153  # Mbappé
season_id = 25659   # La Liga

endpoints = [
    "/players/{player_id}/statistics/seasons/{season_id}",
    "/players/{player_id}/statistics/seasons",
    "/statistics/seasons/players/{player_id}",
    "/seasons/{season_id}/statistics/players/{player_id}",
    "/seasons/{season_id}/player-statistics",
    "/player-statistics"
]

for endpoint_template in endpoints:
    endpoint = endpoint_template.format(player_id=player_id, season_id=season_id)
    url = f"{BASE_URL}{endpoint}"
    
    print(f"Test: {endpoint}")
    
    params = {"api_token": API_KEY}
    
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code == 200:
        print(f"   ✅ SUCCESS! Status: {response.status_code}")
        data = response.json()
        if 'data' in data:
            print(f"   Data found: {type(data['data'])}")
            if isinstance(data['data'], list) and len(data['data']) > 0:
                print(f"   {len(data['data'])} entries")
            elif isinstance(data['data'], dict):
                print(f"   Dict with keys: {list(data['data'].keys())[:5]}")
        break
    else:
        print(f"   ❌ Status: {response.status_code}")

# Test aussi avec l'ancien endpoint qui marchait
print("\n" + "="*60)
print("Test de l'endpoint /players/{id}/statistics/seasons/{season_id}:")
url = f"{BASE_URL}/players/{player_id}/statistics/seasons/{season_id}"
params = {
    "api_token": API_KEY,
    "include": "details.type"
}

response = requests.get(url, params=params, timeout=30)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    stats = data.get('data', {})
    if stats:
        print(f"✅ Stats trouvées!")
        print(f"   Goals: {stats.get('goals', 0)}")
        print(f"   Assists: {stats.get('assists', 0)}")
        print(f"   Minutes: {stats.get('minutes_played', 0)}")