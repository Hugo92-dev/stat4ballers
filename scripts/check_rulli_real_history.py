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

# Vérifier l'historique de Rulli
def get_player_info(player_id):
    """Récupère les infos d'un joueur avec son historique"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        "include": "teams,transfers"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data and "data" in data:
                player = data["data"]
                print(f"Joueur: {player.get('display_name')}")
                print(f"Position: {player.get('position', {}).get('name')}")
                print(f"Date de naissance: {player.get('date_of_birth')}")
                
                # Historique des équipes
                if "teams" in player:
                    print("\n📋 HISTORIQUE DES CLUBS:")
                    for team in player["teams"]:
                        print(f"  - {team.get('name')} (ID: {team.get('id')})")
                
                # Transferts
                if "transfers" in player:
                    print("\n💼 TRANSFERTS RÉCENTS:")
                    transfers = sorted(player["transfers"], key=lambda x: x.get('date', ''), reverse=True)[:5]
                    for transfer in transfers:
                        print(f"  {transfer.get('date')}: {transfer.get('from', {}).get('name', 'N/A')} → {transfer.get('to', {}).get('name', 'N/A')}")
                
                return player
        else:
            print(f"Erreur {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Erreur: {e}")
    
    return None

print("=" * 80)
print("VÉRIFICATION DE L'HISTORIQUE DE RULLI")
print("=" * 80)

# ID de Rulli
player_id = 186418
player_info = get_player_info(player_id)

if player_info:
    print("\n📊 SAISONS À VÉRIFIER:")
    print("  - 2025/2026: Olympique Marseille (Ligue 1)")
    print("  - 2024/2025: Olympique Marseille (Ligue 1)")
    print("  - 2023/2024: ? (à vérifier dans l'historique)")