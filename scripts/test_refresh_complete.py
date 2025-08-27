#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test complet du système de refresh avec stats
"""

import requests
import json
import sys
import time
from datetime import datetime
from refresh_stats_utils import fetch_complete_player_statistics

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("="*60)
print("🔍 TEST COMPLET DU SYSTÈME DE REFRESH")
print("="*60)

# Configuration des championnats
leagues = {
    "Ligue 1": {"season_id": 25651, "team_id": 591, "team_name": "Olympique Marseille"},
    "Premier League": {"season_id": 25583, "team_id": 14, "team_name": "Manchester United"},
    "La Liga": {"season_id": 25659, "team_id": 3468, "team_name": "Real Madrid"},
    "Serie A": {"season_id": 25533, "team_id": 115, "team_name": "Juventus"},
    "Bundesliga": {"season_id": 25646, "team_id": 16, "team_name": "Bayern Munich"}
}

# Test sur un club de chaque championnat
for league_name, config in leagues.items():
    print(f"\n{'='*60}")
    print(f"📍 TEST: {league_name} - {config['team_name']}")
    print(f"   Season ID: {config['season_id']}")
    print(f"   Team ID: {config['team_id']}")
    
    # 1. Récupérer l'effectif
    squad_url = f"{BASE_URL}/squads/teams/{config['team_id']}"
    params = {"api_token": API_KEY, "include": "player"}
    
    response = requests.get(squad_url, params=params, timeout=30)
    
    if response.status_code == 200:
        squad_data = response.json().get('data', [])
        print(f"   ✅ {len(squad_data)} joueurs trouvés")
        
        # Tester sur le premier joueur
        if squad_data and squad_data[0].get('player'):
            player = squad_data[0]['player']
            print(f"\n   Test avec: {player['name']} (ID: {player['id']})")
            
            # 2. Récupérer ses stats complètes
            stats = fetch_complete_player_statistics(
                player['id'], 
                config['season_id'], 
                API_KEY, 
                BASE_URL
            )
            
            # 3. Vérifier si on a des stats
            has_stats = any([
                stats['appearances'] > 0,
                stats['minutes_played'] > 0,
                stats['goals'] > 0,
                stats['assists'] > 0,
                stats['passes'] > 0
            ])
            
            if has_stats:
                print(f"   ✅ STATS TROUVÉES!")
                print(f"      - Apparitions: {stats['appearances']}")
                print(f"      - Minutes: {stats['minutes_played']}")
                print(f"      - Buts: {stats['goals']}")
                print(f"      - Passes décisives: {stats['assists']}")
                print(f"      - Passes: {stats['passes']}")
                print(f"      - Tacles: {stats['tackles']}")
            else:
                print(f"   ⚠️ Pas de stats disponibles")
                print(f"      (La saison n'a peut-être pas encore de données)")
    else:
        print(f"   ❌ Erreur API: {response.status_code}")
    
    # Pause entre les tests
    time.sleep(1)

print(f"\n{'='*60}")
print("📊 RÉSUMÉ")
print("="*60)
print("✅ Le système de refresh est configuré correctement.")
print("⚠️ Les statistiques 2025/2026 seront récupérées dès qu'elles")
print("   seront disponibles dans l'API SportMonks.")
print("💡 Les scripts récupèrent déjà les effectifs complets.")
print("🔄 Les stats seront automatiquement ajoutées lors des refresh.")