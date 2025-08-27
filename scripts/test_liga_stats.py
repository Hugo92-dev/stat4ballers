#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test rapide - Récupère Real Madrid avec les stats complètes
"""

import requests
import json
import sys
from refresh_stats_utils import fetch_complete_player_statistics

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
SEASON_ID = 25659  # Saison 2025/2026 Liga

# Test sur Real Madrid (ID: 3468)
print("🔄 Test sur le Real Madrid...")
print(f"Season ID: {SEASON_ID}\n")

# 1. Récupérer l'effectif
squad_url = f"{BASE_URL}/squads/teams/3468"
params = {"api_token": API_KEY, "include": "player"}

response = requests.get(squad_url, params=params, timeout=30)
if response.status_code == 200:
    squad = response.json()['data']
    print(f"✅ {len(squad)} joueurs trouvés\n")
    
    # Tester sur les 3 premiers joueurs
    for i, item in enumerate(squad[:3]):
        if item.get('player'):
            player = item['player']
            print(f"👤 {player['name']} (ID: {player['id']})")
            
            # Récupérer les stats complètes
            stats = fetch_complete_player_statistics(player['id'], SEASON_ID, API_KEY, BASE_URL)
            
            # Afficher quelques stats clés
            print(f"   📊 Apparitions: {stats['appearances']}")
            print(f"   ⚽ Buts: {stats['goals']}")
            print(f"   🎯 Passes réussies: {stats['passes']} ({stats['accurate_passes_percentage']}%)")
            print(f"   ⏱️ Minutes: {stats['minutes_played']}")
            print(f"   🛡️ Duels gagnés: {stats['duels_won']}/{stats['total_duels']}")
            
            # Vérifier si on a des stats non nulles
            has_stats = any([
                stats['appearances'] > 0,
                stats['minutes_played'] > 0,
                stats['passes'] > 0
            ])
            
            if has_stats:
                print(f"   ✅ Stats trouvées!")
            else:
                print(f"   ⚠️ Aucune stat pour ce joueur")
            print()
else:
    print(f"❌ Erreur: {response.status_code}")