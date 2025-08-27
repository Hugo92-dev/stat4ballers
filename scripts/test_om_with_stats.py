#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test rapide - Récupère l'OM avec les stats réelles
"""

import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
SEASON_ID = 25651  # Saison 2025/2026

def fetch_player_statistics(player_id):
    """Récupère les statistiques d'un joueur pour la saison"""
    try:
        stats_url = f"{BASE_URL}/statistics/seasons/players"
        params = {
            "api_token": API_KEY,
            "filters[player_ids]": player_id,
            "filters[season_ids]": SEASON_ID,
            "include": "details"
        }
        
        response = requests.get(stats_url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data and len(data) > 0:
                stats = data[0]
                
                # Stats directes si disponibles
                result = {
                    "goals": stats.get('goals', 0),
                    "assists": stats.get('assists', 0),
                    "yellow_cards": stats.get('yellowcards', 0),
                    "red_cards": stats.get('redcards', 0),
                    "minutes_played": stats.get('minutes_played', 0)
                }
                
                print(f"    Stats trouvées: {result['goals']}B {result['assists']}A {result['minutes_played']}min")
                return result
        
        return {"goals": 0, "assists": 0, "yellow_cards": 0, "red_cards": 0, "minutes_played": 0}
        
    except Exception as e:
        print(f"    ❌ Erreur stats: {str(e)}")
        return {"goals": 0, "assists": 0, "yellow_cards": 0, "red_cards": 0, "minutes_played": 0}

# Test sur l'OM (ID: 591)
print("🔄 Test sur l'Olympique de Marseille...")

# 1. Récupérer l'effectif
squad_url = f"{BASE_URL}/squads/teams/591"
params = {"api_token": API_KEY, "include": "player"}

response = requests.get(squad_url, params=params, timeout=30)
if response.status_code == 200:
    squad = response.json()['data']
    print(f"✅ {len(squad)} joueurs trouvés\n")
    
    # Tester sur les 3 premiers joueurs
    for i, item in enumerate(squad[:3]):
        if item.get('player'):
            player = item['player']
            print(f"👤 {player['name']}")
            stats = fetch_player_statistics(player['id'])
            print()
else:
    print(f"❌ Erreur: {response.status_code}")