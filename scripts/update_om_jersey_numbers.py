#!/usr/bin/env python3
"""
Script pour récupérer les numéros de maillot actuels de l'OM
pour la saison 2025/2026 (ID: 25651)
"""

import requests
import json
from typing import Dict, Optional

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"
SEASON_ID = 25651
OM_TEAM_ID = 44

def make_api_call(endpoint: str, params: dict = None) -> Optional[Dict]:
    """Fait un appel API avec gestion des erreurs"""
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code} for {endpoint}")
            return None
        
    except Exception as e:
        print(f"Exception calling {endpoint}: {e}")
        return None

def get_current_jersey_numbers():
    """Récupère les numéros de maillot actuels de l'OM pour la saison 2025/2026"""
    
    print(f"=== Récupération des numéros de maillot OM - Saison 2025/2026 ===\n")
    
    jersey_numbers = {}
    
    # Méthode 1: Via les statistiques de la saison
    print("1. Tentative via statistiques de saison...")
    stats_response = make_api_call(
        f"statistics/seasons/{SEASON_ID}/teams/{OM_TEAM_ID}/players",
        {'include': 'player'}
    )
    
    if stats_response and 'data' in stats_response:
        for stat in stats_response['data']:
            player = stat.get('player', {})
            player_id = player.get('id')
            player_name = player.get('display_name', 'Unknown')
            jersey = stat.get('jersey_number')
            
            if player_id and jersey:
                jersey_numbers[player_id] = {
                    'name': player_name,
                    'jersey': jersey
                }
                print(f"  Found: {player_name} - #{jersey}")
    
    # Méthode 2: Via les fixtures récentes et les lineups
    print("\n2. Tentative via compositions récentes...")
    fixtures_response = make_api_call(
        "fixtures",
        {
            'filters': f'teamIds:{OM_TEAM_ID};seasonIds:{SEASON_ID}',
            'include': 'lineups.player',
            'per_page': 5
        }
    )
    
    if fixtures_response and 'data' in fixtures_response:
        for fixture in fixtures_response['data']:
            lineups = fixture.get('lineups', [])
            for lineup in lineups:
                if lineup.get('team_id') == OM_TEAM_ID:
                    player = lineup.get('player', {})
                    player_id = player.get('id')
                    player_name = player.get('display_name', 'Unknown')
                    jersey = lineup.get('jersey_number')
                    
                    if player_id and jersey and player_id not in jersey_numbers:
                        jersey_numbers[player_id] = {
                            'name': player_name,
                            'jersey': jersey
                        }
                        print(f"  Found: {player_name} - #{jersey}")
    
    # Méthode 3: Récupérer les détails de chaque joueur individuellement
    print("\n3. Vérification individuelle des joueurs connus...")
    
    # Liste des joueurs OM connus
    known_players = [
        186418,    # Gerónimo Rulli
        29186,     # Jeffrey de Lange
        186456,    # Rubén Blanco
        37593233,  # Jelle Van Neck
        527759,    # Théo Vermot
        13171199,  # Leonardo Balerdi
        32390,     # Ulisses Garcia
        586846,    # Derek Cornelius
        37369302,  # Bamo Meïté
        130063,    # Pol Lirola
        335521,    # Facundo Medina
        28575687,  # CJ Egan-Riley
        512560,    # Amir Murillo
        1744,      # Pierre-Emile Højbjerg
        21803033,  # Azzedine Ounahi
        96691,     # Amine Harit
        95696,     # Geoffrey Kondogbia
        95694,     # Adrien Rabiot
        37541144,  # Bilal Nadir
        608285,    # Angel Gomes
        37737405,  # Darryl Bakola
        433458,    # Amine Gouiri
        31739,     # Pierre-Emerick Aubameyang
        20333643,  # Mason Greenwood
        95776,     # Neal Maupay
        20315925,  # Faris Moumbagna
        29328428,  # Igor Paixão
        537332,    # Timothy Weah
        37657133,  # François Mughe
        34455209,  # Jonathan Rowe
        37713942,  # Robinio Vaz
        37729567,  # Keyliane Abdallah
    ]
    
    for player_id in known_players:
        if player_id not in jersey_numbers:
            # Récupérer les stats du joueur pour cette saison
            player_stats = make_api_call(
                f"players/{player_id}/statistics",
                {'filters': f'seasonIds:{SEASON_ID}'}
            )
            
            if player_stats and 'data' in player_stats:
                for stat in player_stats['data']:
                    if stat.get('team_id') == OM_TEAM_ID:
                        jersey = stat.get('jersey_number')
                        if jersey:
                            # Récupérer le nom du joueur
                            player_data = make_api_call(f"players/{player_id}")
                            if player_data and 'data' in player_data:
                                player_name = player_data['data'].get('display_name', 'Unknown')
                                jersey_numbers[player_id] = {
                                    'name': player_name,
                                    'jersey': jersey
                                }
                                print(f"  Found: {player_name} - #{jersey}")
                            break
    
    return jersey_numbers

def main():
    # Récupérer les numéros actuels
    jersey_numbers = get_current_jersey_numbers()
    
    print(f"\n=== RÉSUMÉ ===")
    print(f"Numéros trouvés: {len(jersey_numbers)}")
    
    # Charger le fichier TypeScript actuel pour comparaison
    print("\n=== Comparaison avec les données actuelles ===")
    
    # Créer le mapping pour mise à jour
    updates_needed = []
    
    for player_id, data in sorted(jersey_numbers.items(), key=lambda x: x[1]['jersey']):
        print(f"#{data['jersey']:2d} - {data['name']} (ID: {player_id})")
        updates_needed.append({
            'id': player_id,
            'name': data['name'],
            'jersey': data['jersey']
        })
    
    # Sauvegarder les mises à jour nécessaires
    with open('om_jersey_updates.json', 'w', encoding='utf-8') as f:
        json.dump({
            'season_id': SEASON_ID,
            'team_id': OM_TEAM_ID,
            'updates': updates_needed
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nMises à jour sauvegardées dans om_jersey_updates.json")
    
    # Générer le code de mise à jour TypeScript
    print("\n=== Code TypeScript pour mise à jour ===")
    print("// Mises à jour des numéros de maillot:")
    for update in updates_needed:
        print(f"// {update['name']}: numero: {update['jersey']}")

if __name__ == "__main__":
    main()