import requests
import json

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def test_squad(team_id, team_name):
    """Tester l'effectif d'une équipe"""
    print(f"\n{team_name} (ID: {team_id})")
    print("-" * 40)
    
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if 'data' in data:
                squad = data['data']
                print(f"Joueurs: {len(squad)}")
                
                if squad:
                    # Afficher les 5 premiers joueurs
                    print("\nPremiers joueurs:")
                    for i, player_data in enumerate(squad[:5]):
                        if 'player' in player_data and player_data['player']:
                            player = player_data['player']
                            name = player.get('common_name', player.get('display_name', 'Unknown'))
                            jersey = player_data.get('jersey_number', '?')
                            print(f"  #{jersey} {name}")
                else:
                    print("ERREUR: Liste vide")
            else:
                print(f"ERREUR: Pas de 'data' dans la réponse")
                print(f"Réponse: {json.dumps(data, indent=2)[:500]}")
        else:
            print(f"ERREUR HTTP: {response.text[:200]}")
            
    except Exception as e:
        print(f"EXCEPTION: {e}")

print("=" * 60)
print("TEST SIMPLE API SPORTMONKS - NANTES ET BREST")
print("=" * 60)

# Tester Nantes
test_squad(59, "FC Nantes")

# Tester Brest  
test_squad(266, "Stade Brestois")

# Tester PSG pour comparaison
test_squad(591, "Paris Saint-Germain")

print("\n" + "=" * 60)
print("TEST AVEC D'AUTRES ENDPOINTS")
print("=" * 60)

# Essayer l'endpoint players directement
print("\nTEST: /players endpoint pour chercher des joueurs de Nantes")
url = f"{BASE_URL}/players"
params = {
    'api_token': API_KEY,
    'filters': 'teamId:59',
    'include': 'team'
}

try:
    response = requests.get(url, params=params)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            print(f"Joueurs trouvés: {len(data['data'])}")
except Exception as e:
    print(f"Erreur: {e}")