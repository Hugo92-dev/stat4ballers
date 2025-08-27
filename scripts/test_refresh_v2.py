#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test du nouveau système de refresh avec fallback
"""

import requests
import json
import sys
import time
from datetime import datetime
from refresh_stats_utils_v2 import fetch_complete_player_statistics

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("="*60)
print("🔄 TEST DU SYSTÈME DE REFRESH V2")
print("="*60)

# Test avec Real Madrid - Liga
team_id = 3468
season_id = 25659  # Liga 2025/2026

print(f"\n📍 Test avec Real Madrid - Liga 2025/2026")
print(f"   Team ID: {team_id}")
print(f"   Season ID: {season_id}\n")

# 1. Récupérer l'effectif
squad_url = f"{BASE_URL}/squads/teams/{team_id}"
params = {"api_token": API_KEY, "include": "player"}

response = requests.get(squad_url, params=params, timeout=30)

if response.status_code == 200:
    squad_data = response.json().get('data', [])
    print(f"✅ {len(squad_data)} joueurs trouvés\n")
    
    # Tester sur les 3 premiers joueurs
    players_with_stats = 0
    for i, item in enumerate(squad_data[:5]):
        player = item.get('player')
        if not player:
            continue
            
        print(f"👤 {player['name']} (ID: {player['id']})")
        print(f"   Numéro: {item.get('jersey_number', 'N/A')}")
        
        # Récupérer les stats avec la nouvelle fonction
        stats = fetch_complete_player_statistics(
            player['id'],
            season_id,
            API_KEY,
            BASE_URL
        )
        
        # Vérifier si on a des stats
        if stats['appearances'] > 0 or stats['goals'] > 0 or stats['minutes_played'] > 0:
            players_with_stats += 1
            print(f"   ✅ Stats trouvées!")
            print(f"      Apparitions: {stats['appearances']}")
            print(f"      Buts: {stats['goals']}")
            print(f"      Passes décisives: {stats['assists']}")
            print(f"      Minutes: {stats['minutes_played']}")
        else:
            print(f"   ⚠️ Pas de stats")
        print()
        
        # Pause pour ne pas surcharger l'API
        time.sleep(1)
    
    print(f"\n📊 RÉSULTAT: {players_with_stats}/5 joueurs avec des stats")
    
else:
    print(f"❌ Erreur API: {response.status_code}")

print("\n" + "="*60)
print("💡 Le système essaye maintenant:")
print("   1. Les stats 2025/2026 en priorité")
print("   2. Les stats 2024/2025 en fallback si pas disponibles")
print("   3. Retourne des stats vides si aucune donnée")
print("="*60)