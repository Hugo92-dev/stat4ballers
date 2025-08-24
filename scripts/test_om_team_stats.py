import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "C3Wid19g74gH2DUPrtoJPpRx8w7obNSgSWpBD8rIoq66HJCEjxFSe3OwCJHF"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Récupérer les joueurs de l'OM pour la saison 2024/2025
def get_om_squad():
    url = f"{BASE_URL}/teams/44"  # 44 = OM
    params = {
        "include": "squad.player"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data and "data" in data:
                squad = data['data'].get('squad', [])
                print(f"✅ Trouvé {len(squad)} joueurs dans l'effectif OM")
                
                # Chercher Rulli
                for player_data in squad:
                    player = player_data.get('player', {})
                    if 'Rulli' in player.get('display_name', ''):
                        print(f"\n🎯 RULLI TROUVÉ:")
                        print(f"  ID: {player.get('id')}")
                        print(f"  Nom: {player.get('display_name')}")
                        print(f"  Position: {player_data.get('position', {}).get('name')}")
                        print(f"  Numéro: {player_data.get('jersey_number')}")
                        return player.get('id')
                
                # Lister tous les gardiens
                print("\n🥅 GARDIENS DE L'OM:")
                for player_data in squad:
                    player = player_data.get('player', {})
                    position = player_data.get('position', {}).get('name', '')
                    if 'Goalkeeper' in position or 'keeper' in position.lower():
                        print(f"  - {player.get('display_name')} (ID: {player.get('id')})")
                        
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    return None

# Test
print("=" * 80)
print("TEST: RECHERCHE DE RULLI DANS L'EFFECTIF OM")
print("=" * 80)

rulli_id = get_om_squad()

if rulli_id:
    print(f"\n📊 Maintenant récupérons ses stats avec l'ID correct: {rulli_id}")
    
    # Récupérer ses stats pour 2024/2025
    url = f"{BASE_URL}/statistics/seasons/players/{rulli_id}"
    params = {
        "seasons": 23643,  # 2024/2025
        "include": "details",
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data and "data" in data and len(data["data"]) > 0:
            stats = data["data"][0]
            details = stats.get("details", [])
            if details:
                detail = details[0]
                print(f"\n✅ STATS 2024/2025 TROUVÉES:")
                print(f"  Matchs: {detail.get('games', {}).get('appearences')}")
                print(f"  Minutes: {detail.get('minutes')}")
                print(f"  Clean sheets: {detail.get('goalkeeper', {}).get('cleansheets')}")
                print(f"  Buts encaissés: {detail.get('goalkeeper', {}).get('goals_conceded')}")
        else:
            print("❌ Pas de stats trouvées")