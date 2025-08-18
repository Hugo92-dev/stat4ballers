import requests
import json

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
base_url = "https://api.sportmonks.com/v3/football"

def test_squad_with_includes():
    """Test récupération effectif avec includes"""
    print("=" * 60)
    print("TEST 1: SQUAD WITH INCLUDES")
    print("=" * 60)
    
    psg_id = 591
    
    # Essayer avec différents includes
    includes_options = [
        "player",
        "player.nationality",
        "player.country",
        "player;player.nationality",
        "player:nationality"
    ]
    
    for includes in includes_options:
        print(f"\nTrying with include: {includes}")
        response = requests.get(
            f"{base_url}/squads/teams/{psg_id}",
            params={
                'api_token': API_KEY,
                'include': includes
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and len(data['data']) > 0:
                first_entry = data['data'][0]
                print(f"  Success! First entry keys: {list(first_entry.keys())}")
                if 'player' in first_entry:
                    player = first_entry['player']
                    print(f"  Player keys: {list(player.keys())}")
                    if 'nationality' in player:
                        print(f"  Nationality found: {player['nationality']}")
                    if 'country' in player:
                        print(f"  Country found: {player['country']}")
        else:
            print(f"  Failed with status: {response.status_code}")

def test_player_details():
    """Test récupération détails joueur"""
    print("\n" + "=" * 60)
    print("TEST 2: PLAYER DETAILS")
    print("=" * 60)
    
    # D'abord récupérer un player_id
    psg_id = 591
    response = requests.get(
        f"{base_url}/squads/teams/{psg_id}",
        params={'api_token': API_KEY}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            # Prendre les 3 premiers joueurs
            for i, entry in enumerate(data['data'][:3]):
                player_id = entry.get('player_id')
                if player_id:
                    print(f"\nPlayer ID: {player_id}")
                    
                    # Essayer sans include
                    response = requests.get(
                        f"{base_url}/players/{player_id}",
                        params={'api_token': API_KEY}
                    )
                    
                    if response.status_code == 200:
                        player_data = response.json()
                        if 'data' in player_data:
                            player = player_data['data']
                            print(f"  Name: {player.get('display_name', 'Unknown')}")
                            print(f"  Nationality ID: {player.get('nationality_id')}")
                            print(f"  Country ID: {player.get('country_id')}")
                            
                            # Si on a un nationality_id, récupérer le pays
                            nat_id = player.get('nationality_id') or player.get('country_id')
                            if nat_id:
                                country_response = requests.get(
                                    f"{base_url}/countries/{nat_id}",
                                    params={'api_token': API_KEY}
                                )
                                if country_response.status_code == 200:
                                    country_data = country_response.json()
                                    if 'data' in country_data:
                                        country = country_data['data']
                                        print(f"  Country name: {country.get('name')}")
                                        print(f"  Country code: {country.get('code')}")

def test_countries_endpoint():
    """Test endpoint des pays"""
    print("\n" + "=" * 60)
    print("TEST 3: COUNTRIES ENDPOINT")
    print("=" * 60)
    
    # Récupérer quelques pays courants
    country_ids = [17, 462, 161, 82, 113, 32, 11]  # France, England, Spain, Germany, Italy, Brazil, Argentina
    
    for country_id in country_ids:
        response = requests.get(
            f"{base_url}/countries/{country_id}",
            params={'api_token': API_KEY}
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                country = data['data']
                print(f"  ID {country_id}: {country.get('name')} ({country.get('code')})")

if __name__ == "__main__":
    test_squad_with_includes()
    test_player_details()
    test_countries_endpoint()