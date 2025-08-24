#!/usr/bin/env python3
"""
Vérifier l'effectif complet de l'OM et identifier les problèmes
"""

import requests
import json

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Test 1: Récupérer l'effectif actuel de l'OM
def check_om_squad():
    print("=== VÉRIFICATION DE L'EFFECTIF COMPLET DE L'OM ===\n")
    
    team_id = 85  # OM
    season_id = 25651  # 2025/2026
    
    # Méthode 1: Via squads/teams
    print("1. Via squads/teams (méthode actuelle):")
    squad_url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'include': 'player',
        'filters': f'seasons:{season_id}'
    }
    
    response = requests.get(squad_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        players = data.get('data', [])
        print(f"   → {len(players)} joueurs trouvés")
        
        # Chercher Robinio Vaz
        for p in players:
            if p.get('player'):
                player = p['player']
                if 'robinio' in player.get('name', '').lower() or 'vaz' in player.get('name', '').lower():
                    print(f"   ✓ TROUVÉ: {player['name']} (ID: {player['id']})")
    
    # Méthode 2: Via teams/{team_id}/players
    print("\n2. Via teams/{team_id}/players:")
    players_url = f"{BASE_URL}/teams/{team_id}/players"
    params = {
        'filters': f'seasons:{season_id}'
    }
    
    response = requests.get(players_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        players = data.get('data', [])
        print(f"   → {len(players)} joueurs trouvés")
        
        for player in players:
            if 'robinio' in player.get('name', '').lower() or 'vaz' in player.get('name', '').lower():
                print(f"   ✓ TROUVÉ: {player['name']} (ID: {player['id']})")
    
    # Méthode 3: Recherche directe du joueur
    print("\n3. Recherche directe de Robinio Vaz (ID: 37713942):")
    player_url = f"{BASE_URL}/players/37713942"
    params = {
        'include': 'teams'
    }
    
    response = requests.get(player_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        player = data.get('data', {})
        print(f"   Nom: {player.get('name')}")
        print(f"   Display name: {player.get('display_name')}")
        print(f"   Position: {player.get('position', {}).get('name') if player.get('position') else 'N/A'}")
        
        # Vérifier ses équipes
        if 'teams' in player:
            print(f"   Équipes actuelles:")
            for team in player['teams']:
                print(f"     - {team.get('name')} (ID: {team.get('id')})")
    else:
        print(f"   ✗ Erreur {response.status_code}: {response.text}")
    
    # Méthode 4: Vérifier tous les transferts récents
    print("\n4. Vérification des transferts récents de l'OM:")
    transfers_url = f"{BASE_URL}/transfers"
    params = {
        'filters': f'teams:{team_id};seasons:{season_id}',
        'include': 'player'
    }
    
    response = requests.get(transfers_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        transfers = data.get('data', [])
        print(f"   → {len(transfers)} transferts trouvés")
        
        for t in transfers[:5]:  # Afficher les 5 derniers
            player = t.get('player', {})
            print(f"     - {player.get('name', 'Unknown')} ({t.get('type', 'N/A')})")

if __name__ == "__main__":
    check_om_squad()