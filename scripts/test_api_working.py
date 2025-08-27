#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test pour trouver le bon endpoint qui retourne vraiment les stats
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Recherche des stats réelles pour la saison 2025/2026...\n")

# Test avec un joueur star du Real Madrid
# Essayons avec Mbappé ou Bellingham
bellingham_id = 346340
mbappe_id = 165153
vinicius_id = 188881

season_id = 25659  # Liga 2025/2026

print("Test de différents formats d'endpoints:\n")

# Test 1: Players endpoint avec paramètres corrects
print("1️⃣ Test /players/{id} avec différents paramètres:")
for player_id, name in [(bellingham_id, "Bellingham"), (mbappe_id, "Mbappé")]:
    url = f"{BASE_URL}/players/{player_id}"
    
    # Essayer différentes combinaisons de paramètres
    param_combinations = [
        {"api_token": API_KEY},
        {"api_token": API_KEY, "include": "statistics"},
        {"api_token": API_KEY, "include": "statistics.season"},
        {"api_token": API_KEY, "include": "statistics.details"},
        {"api_token": API_KEY, "include": "statistics", "seasons": season_id},
    ]
    
    for params in param_combinations:
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json().get('data', {})
                if data.get('statistics'):
                    stats_data = data['statistics'].get('data', [])
                    for stat in stats_data:
                        if stat.get('season_id') == season_id:
                            print(f"   ✅ {name} - Stats trouvées pour saison {season_id}!")
                            print(f"      Buts: {stat.get('goals', 0)}, Assists: {stat.get('assists', 0)}")
                            break
        except:
            pass

# Test 2: Via team players
print("\n2️⃣ Test /teams/{team_id}/players:")
url = f"{BASE_URL}/teams/3468/players"  # Real Madrid
params = {
    "api_token": API_KEY,
    "include": "player.statistics",
    "seasons": season_id
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

# Test 3: Statistics aggregated
print("\n3️⃣ Test /teams/{team_id}/statistics/seasons/{season_id}:")
url = f"{BASE_URL}/teams/3468/statistics/seasons/{season_id}"
params = {"api_token": API_KEY}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Response keys: {list(data.keys())}")

# Test 4: Topscorers/Topassists (doit forcément avoir des stats)
print("\n4️⃣ Test /topscorers/seasons/{season_id}:")
url = f"{BASE_URL}/topscorers/seasons/{season_id}"
params = {
    "api_token": API_KEY,
    "include": "participant"
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    topscorers = data.get('data', [])
    if topscorers:
        print(f"   ✅ {len(topscorers)} buteurs trouvés")
        for scorer in topscorers[:3]:
            participant = scorer.get('participant')
            if participant:
                print(f"      - {participant.get('name', 'Unknown')}: {scorer.get('goals', 0)} buts")

# Test 5: Player statistics direct
print("\n5️⃣ Test /players/{id}/seasons/{season_id}/statistics:")
for player_id, name in [(bellingham_id, "Bellingham"), (mbappe_id, "Mbappé")]:
    url = f"{BASE_URL}/players/{player_id}/seasons/{season_id}/statistics"
    params = {"api_token": API_KEY}
    response = requests.get(url, params=params, timeout=10)
    print(f"   {name}: Status {response.status_code}")