#!/usr/bin/env python3
"""Test des stats de Donnarumma"""

import requests
import json
import sys
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# ID de Donnarumma
DONNARUMMA_ID = 129771

# Saisons Ligue 1
SEASONS = {
    25651: "2025/2026",
    23643: "2024/2025",
    21779: "2023/2024"
}

def get_player_stats():
    """Récupère les vraies stats de Donnarumma"""
    
    url = f"{BASE_URL}/statistics/seasons/players/{DONNARUMMA_ID}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{",".join(map(str, SEASONS.keys()))}'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('data', [])
    except Exception as e:
        print(f"Erreur: {e}")
    
    return []

def parse_stats(stats_data):
    """Parse les stats correctement"""
    
    print("📊 Statistiques de Gianluigi Donnarumma (PSG)")
    print("=" * 60)
    
    for season_data in stats_data:
        season_id = season_data.get('season_id')
        if season_id not in SEASONS:
            continue
            
        print(f"\n🏆 Saison {SEASONS[season_id]}")
        print("-" * 40)
        
        # Debug: voir tous les types disponibles
        print("\n  📋 Données brutes disponibles:")
        if 'details' in season_data:
            for detail in season_data['details']:
                type_data = detail.get('type')
                if isinstance(type_data, dict):
                    type_id = type_data.get('id')
                    type_name = type_data.get('name', 'Unknown')
                    value = detail.get('value', {})
                    if isinstance(value, dict):
                        val = value.get('total', value.get('average', 0))
                    else:
                        val = value
                    
                    if val and val != 0:
                        print(f"    ID {type_id}: {type_name} = {val}")

def main():
    print("🔍 Récupération des stats réelles de Donnarumma...")
    stats = get_player_stats()
    
    if stats:
        parse_stats(stats)
    else:
        print("❌ Aucune statistique trouvée")

if __name__ == "__main__":
    main()