#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test pour trouver les saisons actuelles avec des stats
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Test des saisons pour récupérer les stats...\n")

# Saisons connues pour 2024/2025
seasons = {
    "Ligue 1": 23871,
    "Premier League": 23924,
    "La Liga": 23887,
    "Serie A": 23918,
    "Bundesliga": 23988
}

print("📊 Test sur un joueur connu (Mbappé ID: 165153) pour chaque championnat:")

for league, season_id in seasons.items():
    stats_url = f"{BASE_URL}/statistics/seasons/players"
    params = {
        "api_token": API_KEY,
        "filters[player_ids]": 165153,  # Mbappé
        "filters[season_ids]": season_id
    }
    
    response = requests.get(stats_url, params=params, timeout=30)
    if response.status_code == 200:
        stats_data = response.json().get('data', [])
        if stats_data and len(stats_data) > 0:
            stats = stats_data[0]
            goals = stats.get('goals', 0)
            assists = stats.get('assists', 0)
            minutes = stats.get('minutes_played', 0)
            if goals > 0 or assists > 0 or minutes > 0:
                print(f"   ✅ {league} (Season {season_id}): {goals}B {assists}A {minutes}min")
            else:
                print(f"   ⚠️ {league} (Season {season_id}): Pas de stats")
        else:
            print(f"   ❌ {league} (Season {season_id}): Aucune donnée")
    else:
        print(f"   ❌ {league}: Erreur {response.status_code}")

print("\n📅 Ces saisons sont probablement 2024/2025.")
print("💡 Pour 2025/2026, les IDs devraient être différents mais les matchs n'ont pas encore commencé.")