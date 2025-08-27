#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test complet de tous les endpoints possibles pour les stats 2025/2026
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Test exhaustif des endpoints pour la saison 2025/2026...\n")

# Mbappé au Real Madrid
player_id = 165153
season_id = 25659  # Liga 2025/2026

print(f"Test avec Mbappé (ID: {player_id}) - Liga 2025/2026 (ID: {season_id})\n")

# 1. Test direct sur le joueur
print("1️⃣ Test /players/{id}:")
url = f"{BASE_URL}/players/{player_id}"
params = {
    "api_token": API_KEY,
    "include": "statistics.season,statistics.details,team"
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json().get('data', {})
    if data.get('statistics'):
        stats_data = data['statistics'].get('data', [])
        print(f"   ✅ {len(stats_data)} saisons de stats trouvées")
        # Chercher la saison 2025/2026
        for stat in stats_data:
            if stat.get('season_id') == season_id:
                print(f"   🎯 Saison {season_id} trouvée!")
                print(f"      Buts: {stat.get('goals', 0)}, Assists: {stat.get('assists', 0)}")

print("\n2️⃣ Test /statistics/seasons/players/{id} avec filtre:")
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {
    "api_token": API_KEY,
    "filters[season_id]": season_id
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Response: {json.dumps(data, indent=2)[:500]}...")

print("\n3️⃣ Test /players/{id}/statistics:")
url = f"{BASE_URL}/players/{player_id}/statistics"
params = {
    "api_token": API_KEY,
    "filters[season_id]": season_id,
    "include": "season"
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

print("\n4️⃣ Test /seasons/{season_id}/statistics:")
url = f"{BASE_URL}/seasons/{season_id}/statistics"
params = {
    "api_token": API_KEY,
    "filters[player_id]": player_id
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

print("\n5️⃣ Test /teams/3468/players avec stats (Real Madrid):")
url = f"{BASE_URL}/teams/3468/players"
params = {
    "api_token": API_KEY,
    "include": "statistics",
    "filters[season_id]": season_id
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

print("\n6️⃣ Test /squads/seasons/{season_id}/teams/3468:")
url = f"{BASE_URL}/squads/seasons/{season_id}/teams/3468"
params = {
    "api_token": API_KEY,
    "include": "player.statistics"
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

print("\n7️⃣ Test /player-statistics avec filtres:")
url = f"{BASE_URL}/player-statistics"
params = {
    "api_token": API_KEY,
    "filters[player_ids]": player_id,
    "filters[season_ids]": season_id
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")

print("\n8️⃣ Test /statistics sans sous-path:")
url = f"{BASE_URL}/statistics"
params = {
    "api_token": API_KEY,
    "filters[player_id]": player_id,
    "filters[season_id]": season_id
}
response = requests.get(url, params=params, timeout=30)
print(f"   Status: {response.status_code}")