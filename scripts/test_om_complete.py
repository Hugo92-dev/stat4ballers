#!/usr/bin/env python3
"""Test rapide sur l'OM uniquement"""

import sys
sys.path.append('.')

from complete_update_system import *

# Test sur l'OM
team_id = 85  # OM
season_id = 25651  # 2025/2026

print("=== TEST EFFECTIF COMPLET OM ===\n")

# Récupérer l'effectif complet
squad = get_complete_squad(team_id, season_id)

print(f"Total: {len(squad)} joueurs\n")

# Chercher Robinio Vaz et afficher tous les joueurs
for member in squad:
    player = member['player_data']
    squad_info = member['squad_data']
    
    name = player.get('name', 'Unknown')
    player_id = player.get('id')
    jersey = squad_info.get('jersey_number', '?')
    
    # Mettre en évidence si c'est Robinio Vaz
    if 'robinio' in name.lower() or 'vaz' in name.lower() or str(player_id) == '37713942':
        print(f">>> TROUVE: {name} (ID: {player_id}, #{jersey})")
    else:
        print(f"  - {name} (ID: {player_id}, #{jersey})")

print("\n" + "=" * 50)