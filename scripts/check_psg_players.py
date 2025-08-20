import requests
import json
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def check_team_players(team_id, team_name):
    """Vérifier en détail les joueurs d'une équipe"""
    print(f"\n{'='*60}")
    print(f"EFFECTIF DE {team_name.upper()}")
    print(f"{'='*60}")
    
    url = f"{BASE_URL}/squads/teams/{team_id}"
    params = {
        'api_token': API_KEY,
        'include': 'player'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if 'data' not in data:
            print(f"Erreur: Pas de données pour {team_name}")
            return
        
        squad = data['data']
        print(f"\nTotal: {len(squad)} joueurs\n")
        
        # Trier par numéro de maillot
        squad_sorted = sorted(squad, key=lambda x: x.get('jersey_number', 999) or 999)
        
        for player_data in squad_sorted:
            if 'player' in player_data and player_data['player']:
                player = player_data['player']
                jersey = player_data.get('jersey_number', '?')
                name = player.get('common_name') or player.get('display_name') or 'Unknown'
                position = player_data.get('detailed_position_id', '?')
                
                # Mapper les positions
                positions = {
                    150: 'GK', 151: 'GK',  # Gardiens
                    152: 'DC', 153: 'DC', 154: 'DC',  # Défenseurs centraux
                    155: 'DG', 156: 'DD',  # Latéraux
                    157: 'MDC', 158: 'MC', 159: 'MC',  # Milieux
                    160: 'MOC', 161: 'MG', 162: 'MD',  # Milieux offensifs
                    163: 'AG', 164: 'AD', 165: 'BU'  # Attaquants
                }
                
                pos_str = positions.get(position, str(position))
                
                if jersey and jersey != '?':
                    print(f"  #{str(jersey).rjust(2)} | {name.ljust(25)} | {pos_str}")
                else:
                    print(f"   -- | {name.ljust(25)} | {pos_str}")
        
    except requests.exceptions.RequestException as e:
        print(f"Erreur API: {e}")

# Vérifier quelques clubs clés
clubs_to_check = [
    {'id': 591, 'name': 'Paris Saint-Germain'},
    {'id': 44, 'name': 'Olympique de Marseille'},
    {'id': 79, 'name': 'Olympique Lyonnais'},
    {'id': 6789, 'name': 'AS Monaco'}
]

print("VERIFICATION DES EFFECTIFS - SAISON 2024/2025")
print("Ces joueurs correspondent-ils aux effectifs réels actuels ?")

for club in clubs_to_check:
    check_team_players(club['id'], club['name'])