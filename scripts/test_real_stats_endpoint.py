#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test du vrai endpoint qui fonctionne pour les stats
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

print("🔍 Test du bon endpoint pour les stats 2025/2026...\n")

# Test avec un joueur du Real Madrid (Bellingham)
player_id = 346340
season_ids = [25659, 23621]  # Liga 2025/2026 et 2024/2025

print(f"Test avec Bellingham (ID: {player_id})\n")

# Test de l'endpoint /statistics/seasons/players/{player_id}
url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"seasons": ",".join(map(str, season_ids))}

response = requests.get(url, headers=headers, params=params)
print(f"Endpoint: /statistics/seasons/players/{player_id}")
print(f"Params: seasons={','.join(map(str, season_ids))}")
print(f"Status: {response.status_code}\n")

if response.status_code == 200:
    data = response.json()
    stats_data = data.get("data", [])
    
    print(f"✅ {len(stats_data)} entrées de stats trouvées\n")
    
    for stat in stats_data:
        season_id = stat.get("season_id")
        has_values = stat.get("has_values", False)
        
        if has_values:
            print(f"📊 Saison {season_id}:")
            
            # Stats directes
            print(f"   Apparitions: {stat.get('appearances', 0)}")
            print(f"   Buts: {stat.get('goals', 0)}")
            print(f"   Passes décisives: {stat.get('assists', 0)}")
            print(f"   Minutes: {stat.get('minutes_played', 0)}")
            
            # Détails si disponibles
            if "details" in stat and stat["details"]:
                print(f"   ✅ {len(stat['details'])} détails disponibles")
            print()
        else:
            print(f"❌ Saison {season_id}: Pas de valeurs\n")
else:
    print(f"❌ Erreur: {response.status_code}")
    print(response.text)