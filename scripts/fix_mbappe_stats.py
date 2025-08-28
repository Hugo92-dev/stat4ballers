#!/usr/bin/env python3
"""Corrige les stats de Mbappé et vérifie le problème de mapping"""

import json
import requests
import sys
from dotenv import load_dotenv
import os
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv('../.env.local')
API_KEY = os.getenv('SPORTMONKS_API_TOKEN')

BASE_URL = "https://api.sportmonks.com/v3/football"

# ID de Mbappé
MBAPPE_ID = 96611

# Saisons
SEASONS = {
    25659: "2025/2026",
    23621: "2024/2025",
    21694: "2023/2024"
}

# MAPPING VRAIMENT CORRECT
TRUE_MAPPING = {
    52: 'goals',            # Buts (PAS rating!)
    58: 'assists',          # Passes décisives (PAS substitutions!)
    321: 'appearences',     # Matchs joués
    322: 'lineups',         # Titularisations  
    119: 'minutes',         # Minutes
    118: 'rating',          # Note moyenne
    64: 'shots',            # Tirs
    65: 'shots_on_target',  # Tirs cadrés
    86: 'penalties_scored', # Penalties marqués
    108: 'dribbles',        # Dribbles tentés
    109: 'dribbles_successful', # Dribbles réussis
    80: 'passes',           # Passes
    116: 'passes_completed', # Passes réussies
    1584: 'passes_accuracy', # % précision
    102: 'key_passes',      # Passes clés
    69: 'offsides',         # Hors-jeu
    40: 'captain',          # Capitaine
    84: 'yellow_cards',     # Cartons jaunes
    83: 'red_cards'         # Cartons rouges
}

def get_and_fix_stats():
    """Récupère et corrige les stats"""
    
    url = f"{BASE_URL}/statistics/seasons/players/{MBAPPE_ID}"
    params = {
        'api_token': API_KEY,
        'include': 'details.type',
        'filters': f'seasonIds:{",".join(map(str, SEASONS.keys()))}'
    }
    
    response = requests.get(url, params=params, timeout=15)
    
    if response.status_code != 200:
        return None
    
    data = response.json().get('data', [])
    
    player_stats = {
        'displayName': 'Kylian Mbappé',
        'position': 'FW',
        'jersey': 10,
        'stats': {}
    }
    
    for season_data in data:
        season_id = season_data.get('season_id')
        if season_id not in SEASONS:
            continue
        
        # Initialiser les stats
        stats = {
            'team': 'Real Madrid',
            'team_id': 3468,
            'league': 'Liga',
            'rating': None,
            'minutes': None,
            'appearences': None,
            'lineups': None,
            'captain': 0,
            'substitutions': None,
            'touches': None,
            'goals': None,
            'assists': None,
            'xg': None,
            'xa': None,
            'shots': None,
            'shots_on_target': None,
            'penalties_won': None,
            'penalties': None,
            'penalties_scored': None,
            'penalties_missed': None,
            'hit_woodwork': None,
            'offsides': None,
            'passes': None,
            'passes_completed': None,
            'passes_accuracy': None,
            'key_passes': None,
            'crosses': None,
            'crosses_accurate': None,
            'dribbles': None,
            'dribbles_successful': None,
            'tackles': None,
            'blocks': None,
            'interceptions': None,
            'clearances': None,
            'ground_duels': None,
            'ground_duels_won': None,
            'aerial_duels': None,
            'aerial_duels_won': None,
            'fouls': None,
            'fouls_drawn': None,
            'yellow_cards': None,
            'red_cards': None,
            'yellowred_cards': None,
            'penalties_committed': None,
            'ball_losses': None,
            'ball_recoveries': None,
            'mistakes_leading_to_goals': None,
            'saves': None,
            'punches': None,
            'inside_box_saves': None,
            'clean_sheets': None,
            'goals_conceded': None,
            'penalties_saved': None,
            'crosses_accuracy': None
        }
        
        # Appliquer le VRAI mapping
        if 'details' in season_data:
            for detail in season_data['details']:
                type_data = detail.get('type', {})
                if isinstance(type_data, dict):
                    type_id = type_data.get('id')
                    
                    if type_id in TRUE_MAPPING:
                        field = TRUE_MAPPING[type_id]
                        value = detail.get('value', {})
                        
                        if isinstance(value, dict):
                            stats[field] = value.get('total', value.get('average'))
                        else:
                            stats[field] = value
        
        # Ajouter la saison
        season_key = f"{SEASONS[season_id]} (Liga, Real Madrid)"
        player_stats['stats'][season_key] = stats
    
    return player_stats

def main():
    print("🔧 Correction des stats de Mbappé...")
    
    fixed_stats = get_and_fix_stats()
    
    if fixed_stats:
        print("\n✅ Stats corrigées de Mbappé:")
        print("=" * 60)
        
        for season_key, stats in fixed_stats['stats'].items():
            print(f"\n📅 {season_key}")
            print(f"  • Buts: {stats['goals']}")
            print(f"  • Passes décisives: {stats['assists']}")
            print(f"  • Matchs: {stats['appearences']}")
            print(f"  • Minutes: {stats['minutes']}")
            print(f"  • Note: {stats['rating']}")
            print(f"  • Dribbles: {stats['dribbles']} (réussis: {stats['dribbles_successful']})")
            
        # Sauvegarder les stats corrigées
        print("\n💾 Les vraies stats de Mbappé sont:")
        print(json.dumps(fixed_stats, indent=2, ensure_ascii=False))
        
        print("\n⚠️ Le fichier la-ligaPlayersCompleteStats.ts doit être regénéré")
        print("   avec le mapping correct pour TOUS les joueurs Liga")

if __name__ == "__main__":
    main()