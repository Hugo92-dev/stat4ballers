#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des stats avec les bonnes Season IDs
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Season IDs confirmés
seasons = {
    "Ligue 1": 25651,
    "Premier League": 25583,
    "La Liga": 25659,
    "Serie A": 25533,
    "Bundesliga": 25646
}

print("🔍 Test de l'API SportMonks avec les Season IDs 2025/2026...\n")

# Test de l'endpoint statistics
print("📊 Test de l'endpoint /statistics/seasons/players\n")

# Test avec Mbappé au Real Madrid (La Liga)
player_id = 165153  # Mbappé
season_id = 25659   # La Liga 2025/2026

url = f"{BASE_URL}/statistics/seasons/players"
params = {
    "api_token": API_KEY,
    "filters[player_ids]": player_id,
    "filters[season_ids]": season_id,
    "include": "details.type"
}

print(f"Test: Mbappé (ID: {player_id}) - La Liga 2025/2026 (ID: {season_id})")
response = requests.get(url, params=params, timeout=30)

print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")
    
    stats_data = data.get('data', [])
    if stats_data:
        print(f"\n✅ Stats trouvées!")
        stats = stats_data[0]
        print(f"   Goals: {stats.get('goals', 0)}")
        print(f"   Assists: {stats.get('assists', 0)}")
        print(f"   Minutes: {stats.get('minutes_played', 0)}")
    else:
        print("\n⚠️ Pas de stats disponibles (saison pas encore commencée?)")
        
else:
    print(f"❌ Erreur API: {response.text}")

# Test si on a des données de test ou de pré-saison
print("\n" + "="*60)
print("💡 Note: La saison 2025/2026 n'a probablement pas encore commencé.")
print("Les stats seront disponibles une fois les matchs joués.")