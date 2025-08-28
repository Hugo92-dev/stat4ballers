#!/usr/bin/env python3
"""Test des vraies stats de Mbappé"""

import requests
import sys
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# ID de Mbappé
MBAPPE_ID = 96611

# Saisons Liga
SEASONS = {
    25659: "2025/2026",
    23621: "2024/2025"
}

def get_real_stats():
    """Récupère les vraies stats"""
    
    url = f"{BASE_URL}/statistics/seasons/players/{MBAPPE_ID}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{",".join(map(str, SEASONS.keys()))}'
    }
    
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code == 200:
        return response.json().get('data', [])
    
    return []

def parse_and_display(stats_data):
    """Parse et affiche les vraies stats"""
    
    print("⚽ Statistiques de Kylian Mbappé (Real Madrid)")
    print("=" * 60)
    
    for season_data in stats_data:
        season_id = season_data.get('season_id')
        if season_id not in SEASONS:
            continue
        
        print(f"\n🏆 Saison {SEASONS[season_id]}")
        print("-" * 40)
        
        # Mapping correct basé sur l'analyse
        correct_stats = {}
        
        if 'details' in season_data:
            for detail in season_data['details']:
                type_data = detail.get('type', {})
                if isinstance(type_data, dict):
                    type_id = type_data.get('id')
                    type_name = type_data.get('name', 'Unknown')
                    value = detail.get('value', {})
                    
                    if isinstance(value, dict):
                        val = value.get('total', value.get('average', 0))
                    else:
                        val = value
                    
                    # Afficher les stats principales
                    if type_id == 52:  # Goals
                        correct_stats['Buts'] = val
                    elif type_id == 58:  # Assists
                        correct_stats['Passes décisives'] = val
                    elif type_id == 321:  # Appearances
                        correct_stats['Matchs joués'] = val
                    elif type_id == 119:  # Minutes
                        correct_stats['Minutes'] = val
                    elif type_id == 118:  # Rating
                        correct_stats['Note moyenne'] = val
                    elif type_id == 64:  # Shots
                        correct_stats['Tirs'] = val
                    elif type_id == 108:  # Dribbles
                        correct_stats['Dribbles tentés'] = val
                    elif type_id == 109:  # Successful dribbles
                        correct_stats['Dribbles réussis'] = val
                    elif type_id == 86:  # Penalties scored
                        correct_stats['Penalties marqués'] = val
                    elif type_id == 80:  # Passes
                        correct_stats['Passes'] = val
                    elif type_id == 116:  # Accurate passes
                        correct_stats['Passes réussies'] = val
        
        # Afficher les stats
        for stat_name, value in correct_stats.items():
            if value:
                print(f"  • {stat_name}: {value}")

def main():
    print("🔍 Récupération des vraies stats de Mbappé...")
    stats = get_real_stats()
    
    if stats:
        parse_and_display(stats)
    else:
        print("❌ Pas de données disponibles")
    
    print("\n📌 Page de Mbappé:")
    print("   http://localhost:3000/liga/real-madrid/kylian-mbappe")

if __name__ == "__main__":
    main()