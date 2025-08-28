#!/usr/bin/env python3
"""Test complet de l'API SportMonks pour trouver TOUTES les stats"""

import requests
import sys
from dotenv import load_dotenv
import os
import json

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

def test_complete_stats(player_id, player_name, season_id):
    """Test avec tous les includes possibles"""
    
    print(f"\n🎯 Test complet pour {player_name} (ID: {player_id})")
    print("=" * 70)
    
    # Essayer différents endpoints et includes
    endpoints = [
        {
            'url': f"{BASE_URL}/players/{player_id}",
            'params': {
                'api_token': API_KEY,
                'include': 'statistics.details.type;statistics.season',
                'filters': f'statisticSeasons:{season_id}'
            },
            'name': 'Player endpoint avec statistics'
        },
        {
            'url': f"{BASE_URL}/statistics/seasons/players/{player_id}",
            'params': {
                'api_token': API_KEY,
                'include': 'details.type;team;position',
                'filters': f'seasonIds:{season_id}'
            },
            'name': 'Statistics endpoint direct'
        }
    ]
    
    all_stats = {}
    
    for endpoint in endpoints:
        print(f"\n📌 Test: {endpoint['name']}")
        print("-" * 50)
        
        try:
            response = requests.get(endpoint['url'], params=endpoint['params'], timeout=15)
            
            if response.status_code != 200:
                print(f"❌ Erreur {response.status_code}")
                continue
            
            data = response.json()
            
            # Parser selon le type de réponse
            if 'data' in data:
                if isinstance(data['data'], dict):
                    # Endpoint player
                    if 'statistics' in data['data']:
                        for stat in data['data']['statistics']:
                            if 'details' in stat:
                                for detail in stat['details']:
                                    parse_detail(detail, all_stats)
                elif isinstance(data['data'], list):
                    # Endpoint statistics
                    for item in data['data']:
                        if 'details' in item:
                            for detail in item['details']:
                                parse_detail(detail, all_stats)
            
            print(f"✅ {len(all_stats)} stats trouvées")
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    # Afficher toutes les stats trouvées
    print("\n" + "=" * 70)
    print("📊 TOUTES LES STATS TROUVÉES:")
    print("=" * 70)
    
    # Organiser par catégorie
    categories = {
        'Offensif': ['goal', 'assist', 'shot', 'penalty', 'woodwork', 'offside'],
        'Passes': ['pass', 'key', 'cross', 'accurate'],
        'Défense': ['tackle', 'block', 'intercept', 'clear', 'duel'],
        'Discipline': ['yellow', 'red', 'foul'],
        'Gardien': ['save', 'conceded', 'clean', 'punch'],
        'Autres': []
    }
    
    categorized = {cat: [] for cat in categories}
    
    for stat_id, info in sorted(all_stats.items()):
        name = info['name']
        dev_name = info['dev_name']
        value = info['value']
        
        found = False
        for cat, keywords in categories.items():
            if cat != 'Autres' and any(kw in name.lower() or kw in dev_name.lower() for kw in keywords):
                categorized[cat].append((stat_id, name, dev_name, value))
                found = True
                break
        
        if not found:
            categorized['Autres'].append((stat_id, name, dev_name, value))
    
    # Afficher par catégorie
    for cat, stats in categorized.items():
        if stats:
            print(f"\n{cat}:")
            for stat_id, name, dev_name, value in stats:
                print(f"  ID {stat_id:4d}: {name:30s} ({dev_name:20s}) = {value}")
    
    return all_stats

def parse_detail(detail, all_stats):
    """Parse un detail de stat"""
    type_data = detail.get('type', {})
    if isinstance(type_data, dict):
        type_id = type_data.get('id')
        type_name = type_data.get('name', '')
        dev_name = type_data.get('developer_name', '')
        value = detail.get('value', {})
        
        if isinstance(value, dict):
            actual_value = value.get('total', value.get('average'))
        else:
            actual_value = value
        
        if type_id not in all_stats:
            all_stats[type_id] = {
                'name': type_name,
                'dev_name': dev_name,
                'value': actual_value
            }

def main():
    # Test avec différents joueurs et saisons
    tests = [
        (96611, "Kylian Mbappé", 25659, "Liga 2025/2026"),
        (96611, "Kylian Mbappé", 23621, "Liga 2024/2025"),
        (31739, "Aubameyang", 25651, "Ligue 1 2025/2026"),
        (182915, "Erling Haaland", 25583, "PL 2025/2026")
    ]
    
    for player_id, name, season_id, league in tests:
        print(f"\n{'#' * 70}")
        print(f"TEST: {name} - {league}")
        print('#' * 70)
        stats = test_complete_stats(player_id, name, season_id)
        
        # Vérifier les stats importantes
        print("\n⚠️ VÉRIFICATION DES STATS CLÉS:")
        key_stats = ['assists', 'shots_on_target', 'hit_woodwork']
        for key in key_stats:
            found = False
            for stat_id, info in stats.items():
                if key in info['name'].lower() or key.replace('_', ' ') in info['name'].lower():
                    print(f"✅ {key}: Trouvé (ID={stat_id}, valeur={info['value']})")
                    found = True
                    break
            if not found:
                print(f"❌ {key}: NON TROUVÉ")

if __name__ == "__main__":
    main()