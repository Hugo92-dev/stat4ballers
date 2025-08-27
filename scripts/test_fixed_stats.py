#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test des stats avec l'endpoint corrigé
"""

import requests
import json
import sys
from refresh_stats_utils import fetch_complete_player_statistics

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("🔍 Test avec l'endpoint corrigé...\n")

# Test avec Mbappé et différentes saisons
player_id = 165153  # Mbappé

seasons = {
    "La Liga 2025/2026": 25659,
    "Ligue 1 2025/2026": 25651
}

for league_name, season_id in seasons.items():
    print(f"📊 Test: Mbappé - {league_name} (Season ID: {season_id})")
    
    stats = fetch_complete_player_statistics(player_id, season_id, API_KEY, BASE_URL)
    
    # Afficher quelques stats clés
    if stats['appearances'] > 0 or stats['goals'] > 0 or stats['minutes_played'] > 0:
        print(f"   ✅ Stats trouvées!")
        print(f"      Apparitions: {stats['appearances']}")
        print(f"      Buts: {stats['goals']}")
        print(f"      Passes décisives: {stats['assists']}")
        print(f"      Minutes: {stats['minutes_played']}")
    else:
        print(f"   ⚠️ Pas de stats (saison pas commencée?)")
    print()

# Test avec un joueur du Real Madrid
print("="*60)
print("Test avec l'effectif du Real Madrid:\n")

# Récupérer l'effectif
squad_url = f"{BASE_URL}/squads/teams/3468"
params = {"api_token": API_KEY, "include": "player"}

response = requests.get(squad_url, params=params, timeout=30)
if response.status_code == 200:
    squad = response.json()['data']
    
    # Tester le premier joueur
    if squad and squad[0].get('player'):
        player = squad[0]['player']
        print(f"👤 {player['name']} (ID: {player['id']})")
        
        stats = fetch_complete_player_statistics(player['id'], 25659, API_KEY, BASE_URL)
        
        if stats['appearances'] > 0 or stats['minutes_played'] > 0:
            print(f"   ✅ Stats trouvées!")
            print(f"      Apparitions: {stats['appearances']}")
            print(f"      Minutes: {stats['minutes_played']}")
        else:
            print(f"   ⚠️ Pas de stats")