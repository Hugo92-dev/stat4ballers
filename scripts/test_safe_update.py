#!/usr/bin/env python3
"""Test rapide du script de mise à jour sécurisé"""

import sys
import os
sys.path.append('.')

# Importer les fonctions du script principal
from safe_update_all_data import make_api_request, BASE_URL, headers

# Test sur l'OM uniquement
team_id = 85  # OM
season_id = 25651  # Saison 2025/2026

print("Test de récupération de l'effectif de l'OM...")

# Test 1: Récupérer l'équipe
squad_url = f"{BASE_URL}/squads/teams/{team_id}"
params = {
    'include': 'player.position',
    'filters': f'seasons:{season_id}'
}

print(f"URL: {squad_url}")
print(f"Params: {params}")

data = make_api_request(squad_url, params)

if data and 'data' in data:
    print(f"✓ Effectif récupéré: {len(data['data'])} joueurs")
    
    # Afficher quelques joueurs
    for i, squad_member in enumerate(data['data'][:3]):
        if 'player' in squad_member and squad_member['player']:
            player = squad_member['player']
            print(f"  - {player['name']} (#{squad_member.get('jersey_number', '?')})")
else:
    print("✗ Erreur lors de la récupération")
    print(f"Réponse: {data}")