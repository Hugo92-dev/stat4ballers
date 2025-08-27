#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test pour trouver la bonne saison de Liga avec des stats
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Recherche de la saison actuelle de Liga avec des stats...\n")

# 1. Récupérer les saisons de Liga
league_url = f"{BASE_URL}/leagues/564"  # Liga ID: 564
params = {
    "api_token": API_KEY,
    "include": "currentseason,seasons"
}

response = requests.get(league_url, params=params, timeout=30)
if response.status_code == 200:
    data = response.json()['data']
    
    # Saison actuelle
    current = data.get('currentseason', {})
    if current:
        print(f"📅 Saison actuelle: {current.get('name')} (ID: {current.get('id')})")
    
    # Toutes les saisons
    if data.get('seasons'):
        seasons = data['seasons']['data']
        print(f"\n📊 Dernières saisons de Liga:")
        for season in seasons[-5:]:  # 5 dernières saisons
            print(f"   - {season.get('name')} (ID: {season.get('id')}) - Terminée: {season.get('is_finished')}")
    
    # 2. Tester les stats d'un joueur connu (Bellingham) sur différentes saisons
    print(f"\n🧪 Test des stats de Bellingham (ID: 346340) sur différentes saisons:")
    
    test_seasons = [25659, 23490, 22768, 21639]  # Différentes saisons à tester
    
    for season_id in test_seasons:
        stats_url = f"{BASE_URL}/statistics/seasons/players"
        params = {
            "api_token": API_KEY,
            "filters[player_ids]": 346340,  # Bellingham
            "filters[season_ids]": season_id
        }
        
        response = requests.get(stats_url, params=params, timeout=30)
        if response.status_code == 200:
            stats_data = response.json().get('data', [])
            if stats_data and len(stats_data) > 0:
                stats = stats_data[0]
                print(f"   ✅ Season {season_id}: {stats.get('goals', 0)} buts, {stats.get('assists', 0)} passes")
            else:
                print(f"   ❌ Season {season_id}: Pas de stats")
                
else:
    print(f"❌ Erreur: {response.status_code}")