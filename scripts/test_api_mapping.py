#!/usr/bin/env python3
"""Test du mapping réel des IDs SportMonks"""

import requests
import sys
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# Tester avec Mbappé (96611) pour la saison 2024/2025
def test_player_mapping(player_id=96611, season_id=23621):
    """Test les vraies valeurs de l'API"""
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{season_id}'
    }
    
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code != 200:
        print(f"Erreur {response.status_code}")
        return
    
    data = response.json().get('data', [])
    
    if not data:
        print("Pas de données")
        return
    
    season_data = data[0]
    
    print(f"🎯 Test de mapping pour le joueur {player_id}")
    print(f"📅 Saison: {season_id}")
    print("=" * 60)
    
    # Dictionnaire pour stocker le mapping
    mapping = {}
    
    if 'details' in season_data:
        for detail in season_data['details']:
            type_data = detail.get('type', {})
            if isinstance(type_data, dict):
                type_id = type_data.get('id')
                type_name = type_data.get('name', 'unknown')
                developer_name = type_data.get('developer_name', '')
                value = detail.get('value', {})
                
                if isinstance(value, dict):
                    actual_value = value.get('total', value.get('average'))
                else:
                    actual_value = value
                
                mapping[type_id] = {
                    'name': type_name,
                    'developer_name': developer_name,
                    'value': actual_value
                }
    
    # Afficher le mapping trouvé
    print("\n📊 MAPPING TROUVÉ:")
    print("-" * 60)
    
    # Stats importantes à vérifier
    important_stats = {
        'Goals': None,
        'Assists': None,
        'Shots Total': None,
        'Shots On Target': None,
        'Hit Woodwork': None,
        'Saves': None,
        'Goals Conceded': None,
        'Clean Sheets': None,
        'Yellow Cards': None,
        'Red Cards': None,
        'Yellowred Cards': None,
        'Penalties Scored': None,
        'Tackles': None,
        'Blocks': None,
        'Interceptions': None,
        'Clearances': None,
        'Fouls': None,
        'Fouls Drawn': None,
        'Offsides': None,
        'Dribbles': None,
        'Dribbles Won': None
    }
    
    for type_id, info in sorted(mapping.items()):
        name = info['name']
        dev_name = info['developer_name']
        val = info['value']
        
        print(f"ID {type_id:4d}: {name:30s} ({dev_name:20s}) = {val}")
        
        # Stocker les valeurs importantes
        if name in important_stats:
            important_stats[name] = (type_id, val)
    
    print("\n⚠️ STATS IMPORTANTES:")
    print("-" * 60)
    for stat_name, data in important_stats.items():
        if data:
            type_id, val = data
            print(f"{stat_name:20s}: ID={type_id:4d}, Valeur={val}")
        else:
            print(f"{stat_name:20s}: NON TROUVÉ")
    
    return mapping

def test_specific_stats():
    """Test des stats spécifiques qui posent problème"""
    
    # Test avec Aubameyang pour hit_woodwork
    print("\n🔍 Test Aubameyang (31739) - Saison 2025/2026")
    test_player_mapping(31739, 25651)
    
    print("\n🔍 Test Mbappé (96611) - Saison 2024/2025")
    test_player_mapping(96611, 23621)

if __name__ == "__main__":
    test_specific_stats()