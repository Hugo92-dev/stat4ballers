#!/usr/bin/env python3
"""Vérifie le vrai mapping des stats SportMonks"""

import requests
import sys
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# Test avec différents joueurs pour avoir toutes les stats
def check_all_stats():
    """Récupère toutes les stats disponibles"""
    
    # Joueurs à tester (attaquant, milieu, défenseur, gardien)
    players = [
        (96611, "Kylian Mbappé", 23621),  # Liga 2024/2025
        (129771, "Gianluigi Donnarumma", 23643),  # Ligue 1 2024/2025
        (182915, "Erling Haaland", 23601),  # PL 2024/2025
    ]
    
    all_mappings = {}
    
    for player_id, name, season_id in players:
        print(f"\n🎯 {name} (ID: {player_id})")
        print("-" * 50)
        
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {
            'api_token': API_KEY,
            'include': 'details.type',
            'filters': f'seasonIds:{season_id}'
        }
        
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Erreur {response.status_code}")
            continue
        
        data = response.json().get('data', [])
        
        if not data:
            print("❌ Pas de données")
            continue
        
        season_data = data[0]
        
        if 'details' in season_data:
            for detail in season_data['details']:
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
                    
                    # Ajouter au mapping global
                    if type_id not in all_mappings:
                        all_mappings[type_id] = {
                            'name': type_name,
                            'dev_name': dev_name,
                            'found_in': []
                        }
                    
                    all_mappings[type_id]['found_in'].append({
                        'player': name,
                        'value': actual_value
                    })
    
    # Afficher le mapping complet
    print("\n" + "=" * 70)
    print("📊 MAPPING COMPLET TROUVÉ:")
    print("=" * 70)
    
    # Trier par ID
    for type_id in sorted(all_mappings.keys()):
        info = all_mappings[type_id]
        name = info['name']
        dev_name = info['dev_name']
        found = info['found_in']
        
        # Afficher avec exemples
        examples = ", ".join([f"{p['player']}: {p['value']}" for p in found[:2]])
        print(f"ID {type_id:4d}: {name:30s} ({dev_name:25s}) - Ex: {examples}")
    
    # Générer le mapping Python correct
    print("\n" + "=" * 70)
    print("📝 MAPPING PYTHON CORRIGÉ:")
    print("=" * 70)
    
    print("# MAPPING CORRECT BASÉ SUR L'API RÉELLE")
    print("STAT_TYPE_MAPPING = {")
    
    # Mapper vers les noms de champs utilisés
    field_mapping = {
        'Goals': 'goals',
        'Assists': 'assists',
        'Shots Total': 'shots',
        'Shots On Target': 'shots_on_target',
        'Shots Off Target': 'shots_off_target',
        'Shots Blocked': 'shots_blocked',
        'Hit Woodwork': 'hit_woodwork',
        'Penalties': 'penalties',
        'Penalties Scored': 'penalties_scored',
        'Penalties Missed': 'penalties_missed',
        'Penalties Won': 'penalties_won',
        'Saves': 'saves',
        'Goals Conceded': 'goals_conceded',
        'Cleansheets': 'clean_sheets',
        'Punches': 'punches',
        'Yellowcards': 'yellow_cards',
        'Redcards': 'red_cards',
        'Yellowred Cards': 'yellowred_cards',
        'Tackles': 'tackles',
        'Blocks': 'blocks',
        'Interceptions': 'interceptions',
        'Clearances': 'clearances',
        'Fouls': 'fouls',
        'Fouls Drawn': 'fouls_drawn',
        'Offsides': 'offsides',
        'Dribble Attempts': 'dribbles',
        'Successful Dribbles': 'dribbles_successful',
        'Appearances': 'appearences',
        'Lineups': 'lineups',
        'Minutes Played': 'minutes',
        'Rating': 'rating',
        'Passes': 'passes',
        'Accurate Passes': 'passes_completed',
        'Key Passes': 'key_passes',
        'Total Crosses': 'crosses',
        'Accurate Crosses': 'crosses_accurate',
        'Total Duels': 'duels',
        'Duels Won': 'duels_won',
        'Aerials Won': 'aerial_duels_won',
        'Captain': 'captain',
        'Substitutions': 'substitutions'
    }
    
    for type_id, info in sorted(all_mappings.items()):
        name = info['name']
        if name in field_mapping:
            field = field_mapping[name]
            print(f"    {type_id}: '{field}',")
    
    print("}")

if __name__ == "__main__":
    check_all_stats()