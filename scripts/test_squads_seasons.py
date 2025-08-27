#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test de l'endpoint squads/seasons pour récupérer les stats
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Test de l'endpoint /squads/seasons/{season_id}/teams/{team_id}...\n")

# Real Madrid - Liga 2025/2026
team_id = 3468
season_id = 25659

url = f"{BASE_URL}/squads/seasons/{season_id}/teams/{team_id}"
params = {
    "api_token": API_KEY,
    "include": "player,player.statistics,player.position"
}

response = requests.get(url, params=params, timeout=30)
print(f"Status: {response.status_code}\n")

if response.status_code == 200:
    data = response.json()
    squad = data.get('data', [])
    
    print(f"✅ {len(squad)} joueurs trouvés\n")
    
    # Afficher les 3 premiers joueurs avec leurs stats
    for i, item in enumerate(squad[:3]):
        player = item.get('player', {})
        if player:
            print(f"👤 {player.get('name', 'Unknown')} (ID: {player.get('id')})")
            print(f"   Numéro: {item.get('jersey_number', 'N/A')}")
            
            # Vérifier si on a des stats
            stats = player.get('statistics', {})
            if stats and stats.get('data'):
                stats_data = stats['data']
                print(f"   📊 {len(stats_data)} saisons de stats disponibles")
                
                # Chercher les stats de la saison 2025/2026
                for stat in stats_data:
                    if stat.get('season_id') == season_id:
                        print(f"   ✅ Stats 2025/2026 trouvées!")
                        print(f"      Buts: {stat.get('goals', 0)}")
                        print(f"      Passes: {stat.get('assists', 0)}")
                        print(f"      Minutes: {stat.get('minutes_played', 0)}")
                        break
            else:
                print(f"   ❌ Pas de stats incluses")
            print()

# Test aussi pour récupérer les stats détaillées d'un joueur spécifique
print("="*60)
print("Test des statistiques détaillées pour un joueur...\n")

if squad and squad[0].get('player'):
    player_id = squad[0]['player']['id']
    
    # Essayer de récupérer les stats du joueur pour cette saison
    url = f"{BASE_URL}/players/{player_id}/statistics/seasons/{season_id}"
    params = {
        "api_token": API_KEY,
        "include": "details,details.type"
    }
    
    response = requests.get(url, params=params, timeout=30)
    print(f"Test /players/{player_id}/statistics/seasons/{season_id}")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        stats = data.get('data', {})
        if stats:
            print(f"✅ Stats détaillées trouvées!")
            print(f"   Buts: {stats.get('goals', 0)}")
            print(f"   Passes: {stats.get('assists', 0)}")
            print(f"   Apparitions: {stats.get('appearances', 0)}")