#!/usr/bin/env python3
"""
Script pour chercher Robinio Vaz et autres joueurs manquants de l'OM
"""

import requests
import json
import time

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

def make_api_call(endpoint, params=None):
    if params is None:
        params = {}
    
    params['api_token'] = API_TOKEN
    
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text[:200]}")
            return None
        
    except Exception as e:
        print(f"Exception: {e}")
        return None

def search_player_by_name(name):
    """Cherche un joueur par nom"""
    print(f"\n=== Recherche de {name} ===")
    
    # Essayer l'endpoint de recherche
    search_endpoints = [
        f"players/search/{name}",
        f"players?search={name}",
    ]
    
    for endpoint in search_endpoints:
        print(f"Testing: {endpoint}")
        result = make_api_call(endpoint)
        
        if result and 'data' in result:
            players = result['data'] if isinstance(result['data'], list) else [result['data']]
            print(f"Found {len(players)} players")
            
            for player in players:
                if isinstance(player, dict):
                    print(f"  - {player.get('display_name')} (ID: {player.get('id')})")
                    print(f"    Born: {player.get('date_of_birth')}, Height: {player.get('height')}cm")
                    
                    # Vérifier ses équipes actuelles
                    if player.get('id'):
                        player_details = make_api_call(f"players/{player.get('id')}", {'include': 'teams'})
                        if player_details and 'data' in player_details:
                            teams = player_details['data'].get('teams', [])
                            print(f"    Teams: {len(teams)}")
                            for team in teams:
                                team_name = team.get('name', 'Unknown')
                                team_id = team.get('id')
                                print(f"      → {team_name} (ID: {team_id})")
                                if 'marseille' in team_name.lower():
                                    print(f"        *** PLAYS FOR OM! ***")
                                    return player.get('id')
            return None

def find_all_om_players_via_transfers():
    """Cherche les joueurs OM via les transferts récents"""
    print("\n=== Recherche via transferts récents ===")
    
    # Chercher les transferts récents vers l'OM
    transfer_endpoints = [
        "transfers/latest",
        "transfers"
    ]
    
    for endpoint in transfer_endpoints:
        print(f"\nTesting transfers: {endpoint}")
        result = make_api_call(endpoint)
        
        if result and 'data' in result:
            transfers = result['data'] if isinstance(result['data'], list) else [result['data']]
            print(f"Found {len(transfers)} transfers")
            
            om_transfers = []
            for transfer in transfers[:50]:  # Regarder les 50 premiers
                if isinstance(transfer, dict):
                    to_team = transfer.get('to_team', {})
                    if to_team and 'marseille' in str(to_team.get('name', '')).lower():
                        player = transfer.get('player', {})
                        print(f"  → Transfer TO OM: {player.get('display_name')} (ID: {player.get('id')})")
                        om_transfers.append(player.get('id'))
            
            if om_transfers:
                return om_transfers
    
    return []

def get_current_ligue1_squads():
    """Récupère tous les effectifs de Ligue 1 pour trouver l'OM"""
    print("\n=== Recherche dans tous les effectifs Ligue 1 ===")
    
    # Récupérer toutes les équipes de Ligue 1 saison 2025/26
    season_data = make_api_call("seasons/25651", {'include': 'teams'})
    
    if season_data and 'data' in season_data:
        teams = season_data['data'].get('teams', [])
        
        for team in teams:
            team_name = team.get('name', '')
            team_id = team.get('id')
            
            if 'marseille' in team_name.lower():
                print(f"\nFound OM: {team_name} (ID: {team_id})")
                
                # Essayer de récupérer les stats des joueurs de cette équipe pour cette saison
                print("Searching for OM players in season statistics...")
                
                # Chercher dans les top scorers, assists, etc.
                stat_endpoints = [
                    f"seasons/25651/topscorers",
                    f"seasons/25651/statistics/players",
                ]
                
                om_player_ids = set()
                
                for endpoint in stat_endpoints:
                    print(f"  Checking: {endpoint}")
                    stats = make_api_call(endpoint)
                    
                    if stats and 'data' in stats:
                        players_stats = stats['data']
                        
                        for stat in players_stats[:100]:  # Regarder les 100 premiers
                            if isinstance(stat, dict):
                                # Chercher l'équipe participante
                                participant = stat.get('participant', {})
                                if participant and participant.get('id') == team_id:
                                    player = stat.get('player', {})
                                    if player and player.get('id'):
                                        om_player_ids.add(player.get('id'))
                                        print(f"    → Found OM player: {player.get('display_name')} (ID: {player.get('id')})")
                
                print(f"\nTotal OM players found in stats: {len(om_player_ids)}")
                return list(om_player_ids)
    
    return []

def main():
    print("=== Recherche de joueurs OM manquants ===")
    
    # 1. Chercher Robinio Vaz spécifiquement
    robinio_id = search_player_by_name("Robinio Vaz")
    if robinio_id:
        print(f"Robinio Vaz trouvé avec ID: {robinio_id}")
    
    # Aussi essayer d'autres variantes
    search_player_by_name("Vaz")
    search_player_by_name("Robinio")
    
    # 2. Chercher via les transferts
    transfer_players = find_all_om_players_via_transfers()
    
    # 3. Chercher via les statistiques de la saison
    stats_players = get_current_ligue1_squads()
    
    # 4. Comparer avec nos données actuelles
    with open('om_complete_squad_final.json', 'r', encoding='utf-8') as f:
        our_data = json.load(f)
    
    our_player_ids = {p['id'] for p in our_data['players']}
    
    print(f"\n=== COMPARAISON ===")
    print(f"Nos données actuelles: {len(our_player_ids)} joueurs")
    
    all_found_ids = set()
    if transfer_players:
        all_found_ids.update(transfer_players)
    if stats_players:
        all_found_ids.update(stats_players)
    if robinio_id:
        all_found_ids.add(robinio_id)
    
    print(f"IDs trouvés via API: {len(all_found_ids)} joueurs")
    
    missing_players = all_found_ids - our_player_ids
    
    if missing_players:
        print(f"\nJoueurs MANQUANTS ({len(missing_players)}):")
        for pid in missing_players:
            player_info = make_api_call(f"players/{pid}")
            if player_info and 'data' in player_info:
                p = player_info['data']
                print(f"  - ID {pid}: {p.get('display_name')} ({p.get('position', {}).get('name', 'Unknown pos')})")
            else:
                print(f"  - ID {pid}: (impossible de récupérer les infos)")
    else:
        print("Aucun joueur manquant détecté")

if __name__ == "__main__":
    main()