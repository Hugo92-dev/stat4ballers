import requests
import json
import os
from datetime import datetime

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"

def get_team_players():
    """Teste différents endpoints pour récupérer les joueurs"""
    
    headers = {
        "Authorization": API_KEY,
        "Accept": "application/json"
    }
    
    # IDs des équipes
    teams = {
        "psg": 591,
        "marseille": 44,
        "lyon": 79
    }
    
    all_data = {}
    
    for team_name, team_id in teams.items():
        print(f"\n{'='*50}")
        print(f"Test pour {team_name.upper()} (ID: {team_id})")
        print('='*50)
        
        # Méthode 1: Via l'endpoint teams avec include players
        url = f"https://api.sportmonks.com/v3/football/teams/{team_id}"
        params = {
            "include": "players"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                team_data = data.get("data", {})
                
                # Info équipe
                print(f"Équipe: {team_data.get('name')}")
                
                # Joueurs
                if team_data.get("players") and team_data["players"].get("data"):
                    players_list = team_data["players"]["data"]
                    print(f"Joueurs trouvés: {len(players_list)}")
                    
                    formatted_players = []
                    for p in players_list[:10]:  # 10 premiers pour test
                        player = {
                            "id": p.get("common_name", "").lower().replace(" ", "-"),
                            "nom": p.get("display_name", p.get("common_name", "")),
                            "poste": p.get("position", {}).get("data", {}).get("name", "N/A") if p.get("position") else "N/A",
                            "numero": 0,  # Pas dans cette réponse
                            "age": 0,
                            "nationalite": "",
                            "matchs_joues": 0,
                            "minutes": 0,
                            "buts": 0,
                            "passes_decisives": 0,
                            "valeur_marchande": 0,
                            "last_update": datetime.now().isoformat()
                        }
                        formatted_players.append(player)
                        print(f"  - {player['nom']}")
                    
                    all_data[team_name] = formatted_players
                else:
                    print("Pas de joueurs dans la réponse")
                    
                    # Essayer une autre méthode
                    print("\nEssai méthode 2: endpoint players avec filtre team_id")
                    url2 = "https://api.sportmonks.com/v3/football/players"
                    params2 = {
                        "filters": f"teamID:{team_id}"
                    }
                    
                    response2 = requests.get(url2, headers=headers, params=params2)
                    print(f"Status méthode 2: {response2.status_code}")
                    
                    if response2.status_code == 200:
                        data2 = response2.json()
                        if data2.get("data"):
                            print(f"Joueurs trouvés: {len(data2['data'])}")
            else:
                print(f"Erreur: {response.text[:200]}")
                
        except Exception as e:
            print(f"Exception: {e}")
    
    # Sauvegarder si on a des données
    if all_data:
        output_path = os.path.join('public', 'data', 'ligue1_sportmonks_test.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'league': 'ligue1',
                'season': '2025-2026',
                'last_update': datetime.now().isoformat(),
                'teams': all_data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] Données sauvegardées: {output_path}")
    
    return all_data

if __name__ == "__main__":
    print("TEST RÉCUPÉRATION JOUEURS SPORTMONKS")
    data = get_team_players()
    
    if not data:
        print("\n[!] Aucune donnée récupérée")
        print("[i] Il se peut que l'API SportMonks nécessite un plan spécifique")
        print("[i] ou que les endpoints aient changé")
        
        print("\n[ALTERNATIVE] Utilisation des données manuelles mises à jour")
        print("Je vais créer un fichier avec les effectifs actuels connus")