import requests
import json

# Test rapide de l'API SportMonks
API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"

def test_api():
    """Test basique pour voir ce qui est disponible"""
    
    headers = {
        "Authorization": f"{API_KEY}",
        "Accept": "application/json"
    }
    
    # 1. Test de base - Récupérer les ligues disponibles
    print("=" * 50)
    print("TEST 1: Ligues disponibles")
    print("=" * 50)
    
    url = "https://api.sportmonks.com/v3/football/leagues"
    params = {
        "filters[country_id]": "17"  # France
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            print(f"[OK] API fonctionne!")
            if data.get("data"):
                for league in data["data"][:3]:
                    print(f"  - {league.get('name')} (ID: {league.get('id')})")
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            print(response.text[:500])
    except Exception as e:
        print(f"[ERREUR] {e}")
    
    # 2. Test Ligue 1 - Récupérer les équipes
    print("\n" + "=" * 50)
    print("TEST 2: Équipes de Ligue 1")
    print("=" * 50)
    
    # ID Ligue 1 = 301
    url = "https://api.sportmonks.com/v3/football/teams/countries/17"  # Teams from France
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            teams = data.get("data", [])
            
            # Chercher PSG, Marseille, Lyon, Monaco
            target_teams = ["Paris Saint Germain", "Marseille", "Lyon", "Monaco"]
            found_teams = []
            
            for team in teams:
                if any(target in team.get("name", "") for target in target_teams):
                    found_teams.append(team)
                    print(f"  - {team.get('name')} (ID: {team.get('id')})")
            
            # 3. Test effectif PSG
            if found_teams:
                psg = next((t for t in found_teams if "Paris" in t.get("name", "")), None)
                if psg:
                    print("\n" + "=" * 50)
                    print(f"TEST 3: Effectif {psg.get('name')}")
                    print("=" * 50)
                    
                    # Récupérer l'effectif du PSG
                    team_id = psg.get("id")
                    url = f"https://api.sportmonks.com/v3/football/squads/teams/{team_id}"
                    params = {
                        "include": "player"
                    }
                    
                    response = requests.get(url, headers=headers, params=params)
                    if response.status_code == 200:
                        data = response.json()
                        squad = data.get("data", [])
                        
                        print(f"[OK] {len(squad)} joueurs trouvés")
                        
                        # Afficher les 5 premiers joueurs
                        for player_data in squad[:5]:
                            player = player_data.get("player", {}).get("data", {})
                            if player:
                                print(f"  - #{player_data.get('jersey_number', '?')} {player.get('display_name', 'Unknown')} ({player.get('position', {}).get('data', {}).get('name', 'N/A') if player.get('position') else 'N/A'})")
                    else:
                        print(f"[ERREUR] Code: {response.status_code}")
        else:
            print(f"[ERREUR] Code: {response.status_code}")
            print(response.text[:500])
    except Exception as e:
        print(f"[ERREUR] {e}")
    
    print("\n" + "=" * 50)
    print("RÉSUMÉ")
    print("=" * 50)
    print("[i] Si les tests passent, SportMonks peut fournir:")
    print("    - Effectifs complets et à jour")
    print("    - Stats détaillées des joueurs")
    print("    - Numéros de maillot")
    print("    - Positions des joueurs")
    print("    - Et bien plus...")

if __name__ == "__main__":
    test_api()