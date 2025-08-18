import requests
import json

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
base_url = "https://api.sportmonks.com/v3/football"

def check_positions():
    """Vérifie les IDs de position dans l'API SportMonks"""
    
    # D'abord récupérer toutes les positions disponibles
    print("=" * 60)
    print("FETCHING ALL POSITIONS FROM SPORTMONKS")
    print("=" * 60)
    
    response = requests.get(
        f"{base_url}/types",
        params={'api_token': API_KEY}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(f"\nFound {len(data['data'])} type entries")
            
            # Chercher les positions
            positions = []
            for item in data['data']:
                if 'position' in str(item).lower():
                    positions.append(item)
                    
            if positions:
                print("\nPosition-related types found:")
                for pos in positions:
                    print(f"  {pos}")
    
    # Essayer l'endpoint des positions directement
    print("\n" + "=" * 60)
    print("TRYING POSITIONS ENDPOINT")
    print("=" * 60)
    
    response = requests.get(
        f"{base_url}/positions",
        params={'api_token': API_KEY}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(f"\nFound {len(data['data'])} positions:")
            for pos in data['data']:
                print(f"  ID: {pos.get('id'):3} | Name: {pos.get('name'):20} | Code: {pos.get('code', 'N/A')}")
    else:
        print(f"Positions endpoint failed: {response.status_code}")
    
    # Vérifier les positions d'un joueur spécifique (Mbappé par exemple)
    print("\n" + "=" * 60)
    print("CHECKING SPECIFIC PLAYER POSITIONS")
    print("=" * 60)
    
    # Récupérer l'effectif du PSG
    psg_id = 591
    response = requests.get(
        f"{base_url}/squads/teams/{psg_id}",
        params={'api_token': API_KEY}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            print(f"\nAnalyzing PSG squad positions:")
            
            position_counts = {}
            for entry in data['data'][:10]:  # Analyser les 10 premiers
                pos_id = entry.get('position_id')
                detailed_pos_id = entry.get('detailed_position_id')
                
                if pos_id not in position_counts:
                    position_counts[pos_id] = 0
                position_counts[pos_id] += 1
                
                # Récupérer les infos du joueur
                player_id = entry.get('player_id')
                if player_id:
                    player_response = requests.get(
                        f"{base_url}/players/{player_id}",
                        params={'api_token': API_KEY}
                    )
                    
                    if player_response.status_code == 200:
                        player_data = player_response.json()
                        if 'data' in player_data:
                            player = player_data['data']
                            print(f"\n  Player: {player.get('display_name', 'Unknown')}")
                            print(f"    Squad Position ID: {pos_id}")
                            print(f"    Squad Detailed Position ID: {detailed_pos_id}")
                            print(f"    Player Position ID: {player.get('position_id')}")
                            print(f"    Player Detailed Position ID: {player.get('detailed_position_id')}")
            
            print(f"\nPosition ID distribution:")
            for pos_id, count in sorted(position_counts.items()):
                print(f"  Position ID {pos_id}: {count} players")

if __name__ == "__main__":
    check_positions()