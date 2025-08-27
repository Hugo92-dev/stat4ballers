#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test pour trouver le bon format pour récupérer les stats
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows  
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

print("🔍 Test des différentes façons de récupérer les stats...\n")

# Test avec Mbappé au Real Madrid
player_id = 165153
season_id = 23621  # Liga 2024/2025 (qui a des stats)

print(f"Test avec Mbappé (ID: {player_id}) - Liga 2024/2025\n")

# 1. Test avec l'endpoint /players/{id}/statistics/seasons/{season}
print("1️⃣ /players/{id}/statistics/seasons/{season}:")
url = f"{BASE_URL}/players/{player_id}/statistics/seasons/{season_id}"
response = requests.get(url, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    stats = data.get("data", {})
    if stats:
        print(f"   ✅ Stats trouvées!")
        print(f"      Buts: {stats.get('goals', 0)}")
        print(f"      Passes: {stats.get('assists', 0)}")
        print(f"      Minutes: {stats.get('minutes_played', 0)}")

# 2. Test avec l'endpoint /statistics/seasons/players/{id} avec filtre
print("\n2️⃣ /statistics/seasons/players/{id} avec filtre season:")
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"filters[season_id]": season_id}
response = requests.get(url, headers=headers, params=params)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    stats_list = data.get("data", [])
    for stat in stats_list:
        if stat.get("season_id") == season_id:
            print(f"   ✅ Stats trouvées pour saison {season_id}!")
            print(f"      Buts: {stat.get('goals', 0)}")
            print(f"      Passes: {stat.get('assists', 0)}")

# 3. Test avec l'endpoint /players/{id}?include=statistics
print("\n3️⃣ /players/{id}?include=statistics:")
url = f"{BASE_URL}/players/{player_id}"
params = {"include": "statistics.details"}
response = requests.get(url, headers=headers, params=params)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    player = data.get("data", {})
    if player.get("statistics"):
        stats_data = player["statistics"].get("data", [])
        print(f"   ✅ {len(stats_data)} saisons de stats trouvées")
        for stat in stats_data:
            if stat.get("season_id") == season_id:
                print(f"      Saison {season_id}: {stat.get('goals', 0)}B {stat.get('assists', 0)}A")

# 4. Test pour la saison 2025/2026
print("\n4️⃣ Test Liga 2025/2026 (ID: 25659):")
season_2025 = 25659
url = f"{BASE_URL}/players/{player_id}/statistics/seasons/{season_2025}"
response = requests.get(url, headers=headers)
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    stats = data.get("data", {})
    if stats and stats.get("has_values"):
        print(f"   ✅ Stats 2025/2026 disponibles!")
        print(f"      Buts: {stats.get('goals', 0)}")
    else:
        print(f"   ⚠️ Pas de stats pour 2025/2026")