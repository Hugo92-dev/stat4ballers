#!/usr/bin/env python3
"""Retraite les fichiers existants avec le MAPPING CORRECT"""

import json
import sys
from pathlib import Path
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# MAPPING CORRECT basé sur la documentation officielle
CORRECT_MAPPING = {
    40: 'captain',
    41: 'shots_off_target',
    42: 'shots',  # shots-total
    47: 'penalties',
    51: 'offsides',
    52: 'goals',
    56: 'fouls',
    57: 'saves',
    58: 'shots_blocked',  # PAS assists !
    59: 'substitutions',
    64: 'hit_woodwork',
    78: 'tackles',
    79: 'assists',  # Le VRAI ID pour assists !
    80: 'passes',
    81: 'passes_completed',  # successful-passes
    82: 'passes_accuracy',  # successful-passes-percentage
    83: 'red_cards',
    84: 'yellow_cards',
    85: 'yellowred_cards',
    86: 'shots_on_target',
    87: 'injuries',
    88: 'goals_conceded',
    94: 'ball_losses',  # dispossessed
    96: 'fouls_drawn',
    97: 'blocks',  # blocked-shots
    98: 'crosses',  # total-crosses
    99: 'crosses_accurate',  # accurate-crosses
    100: 'interceptions',
    101: 'clearances',
    104: 'inside_box_saves',  # saves-insidebox
    105: 'ground_duels',  # total-duels
    106: 'ground_duels_won',  # duels-won
    107: 'aerial_duels_won',  # aeriels-won
    108: 'dribbles',  # dribble-attempts
    109: 'dribbles_successful',  # successful-dribbles
    110: 'dribbled_past',
    116: 'passes_completed',  # accurate-passes (duplicate de 81)
    117: 'key_passes',
    118: 'rating',
    119: 'minutes',  # minutes-played
    122: 'long_balls',
    123: 'long_balls_won',
    124: 'through_balls',
    125: 'through_balls_won',
    194: 'clean_sheets',  # cleansheets
    214: 'wins',  # team-wins
    215: 'draws',  # team-draws
    216: 'losses',  # team-lost
    321: 'appearences',  # appearances
    322: 'lineups',
    323: 'substitutions',  # bench (on utilise substitutions)
    324: 'own_goals',
    571: 'mistakes_leading_to_goals',  # error-lead-to-goal
    580: 'big_chances_created',
    581: 'big_chances_missed',
    1584: 'passes_accuracy',  # accurate-passes-percentage (duplicate de 82)
    5304: 'xg',  # expected-goals
    9676: 'average_points',  # average-points-per-game
    27255: 'crosses_blocked',
    27259: 'hattricks'
}

def test_api_for_player(player_id=96611, player_name="Mbappé"):
    """Test l'API pour un joueur spécifique"""
    print(f"\n🔍 Test API pour {player_name} (ID: {player_id})")
    print("-" * 60)
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': 'seasonIds:25659,23621'  # Liga 2025/2026 et 2024/2025
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ Erreur API: {response.status_code}")
            return
        
        data = response.json().get('data', [])
        
        for season_data in data:
            season_id = season_data.get('season_id')
            print(f"\n📅 Saison ID: {season_id}")
            
            if 'details' in season_data:
                important_stats = {}
                
                for detail in season_data['details']:
                    type_data = detail.get('type', {})
                    if isinstance(type_data, dict):
                        type_id = type_data.get('id')
                        type_name = type_data.get('name')
                        value = detail.get('value', {})
                        
                        if isinstance(value, dict):
                            actual_value = value.get('total', value.get('average'))
                        else:
                            actual_value = value
                        
                        # Stocker les stats importantes
                        if type_id in [52, 79, 86, 64, 42, 58]:  # goals, assists, shots_on_target, hit_woodwork, shots, shots_blocked
                            field = CORRECT_MAPPING.get(type_id, f'unknown_{type_id}')
                            important_stats[field] = actual_value
                            print(f"  • {field}: {actual_value} (ID {type_id}: {type_name})")
                
                # Vérifier les valeurs
                print(f"\n✅ Résumé avec le mapping CORRECT:")
                print(f"  • goals: {important_stats.get('goals', 'N/A')}")
                print(f"  • assists: {important_stats.get('assists', 'N/A')}")
                print(f"  • shots: {important_stats.get('shots', 'N/A')}")
                print(f"  • shots_on_target: {important_stats.get('shots_on_target', 'N/A')}")
                print(f"  • shots_blocked: {important_stats.get('shots_blocked', 'N/A')}")
                print(f"  • hit_woodwork: {important_stats.get('hit_woodwork', 'N/A')}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    print("=" * 70)
    print("🔧 TEST DU MAPPING CORRECT")
    print("=" * 70)
    
    # Test avec plusieurs joueurs
    players = [
        (96611, "Kylian Mbappé"),
        (31739, "Aubameyang"),
        (182915, "Erling Haaland")
    ]
    
    for player_id, name in players:
        test_api_for_player(player_id, name)
    
    print("\n" + "=" * 70)
    print("📌 CONCLUSION:")
    print("-" * 70)
    print("Le mapping correct est:")
    print("  • ID 79 = assists")
    print("  • ID 58 = shots_blocked")
    print("  • ID 86 = shots_on_target")
    print("  • ID 64 = hit_woodwork")
    print("  • ID 42 = shots (total)")
    print()
    print("Les fichiers actuels utilisent le MAUVAIS mapping.")
    print("Il faut relancer la récupération des données avec le bon mapping!")

if __name__ == "__main__":
    main()