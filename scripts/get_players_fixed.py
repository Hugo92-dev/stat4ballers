import requests
import json
import os
from datetime import datetime

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"

def get_team_players_correct():
    """Récupère les joueurs avec le bon format"""
    
    headers = {
        "Authorization": API_KEY,
        "Accept": "application/json"
    }
    
    teams = {
        "psg": 591,
        "marseille": 44,
        "lyon": 79
    }
    
    # D'abord, chercher Monaco
    print("Recherche de Monaco...")
    url_teams = "https://api.sportmonks.com/v3/football/teams/countries/17"
    response = requests.get(url_teams, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for team in data.get("data", []):
            if "Monaco" in team.get("name", ""):
                teams["monaco"] = team.get("id")
                print(f"Monaco trouvé: ID {team.get('id')}")
                break
    
    all_data = {}
    
    for team_name, team_id in teams.items():
        print(f"\nRécupération {team_name.upper()}...")
        
        # Récupérer l'équipe avec ses joueurs
        url = f"https://api.sportmonks.com/v3/football/teams/{team_id}"
        params = {
            "include": "players"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                team_data = data.get("data", {})
                
                # Les joueurs sont dans un tableau, pas un objet
                players_data = team_data.get("players", [])
                
                if players_data:
                    formatted_players = []
                    
                    for p in players_data:
                        # Calculer l'âge
                        age = 0
                        if p.get("date_of_birth"):
                            try:
                                birth = datetime.strptime(p["date_of_birth"], "%Y-%m-%d")
                                age = (datetime.now() - birth).days // 365
                            except:
                                pass
                        
                        player = {
                            "id": (p.get("common_name") or p.get("display_name", "")).lower().replace(" ", "-").replace("'", ""),
                            "nom": p.get("display_name") or p.get("common_name", "Unknown"),
                            "poste": "N/A",  # Position pas dans cette réponse
                            "numero": 0,  # Numéro pas dans cette réponse
                            "age": age,
                            "nationalite": p.get("nationality", ""),
                            "matchs_joues": 0,
                            "titularisations": 0,
                            "minutes": 0,
                            "note_moyenne": 0.0,
                            "buts": 0,
                            "passes_decisives": 0,
                            "xg": 0.0,
                            "xa": 0.0,
                            "tirs_total": 0,
                            "tirs_cadres": 0,
                            "penalties_marques": 0,
                            "passes_cles": 0,
                            "passes_reussies_pct": 0.0,
                            "dribbles_reussis": 0,
                            "centres_reussis": 0,
                            "tacles_reussis": 0,
                            "interceptions": 0,
                            "duels_aeriens_gagnes": 0,
                            "cleansheets": 0,
                            "cartons_jaunes": 0,
                            "cartons_rouges": 0,
                            "valeur_marchande": 0,
                            "last_update": datetime.now().isoformat()
                        }
                        
                        formatted_players.append(player)
                    
                    all_data[team_name] = formatted_players
                    print(f"  {len(formatted_players)} joueurs trouvés")
                    
                    # Afficher quelques joueurs
                    for p in formatted_players[:5]:
                        print(f"  - {p['nom']} ({p['age']} ans)")
                
        except Exception as e:
            print(f"Erreur: {e}")
    
    # Sauvegarder les données
    if all_data:
        output_path = os.path.join('public', 'data', 'ligue1_2025_26_real.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'league': 'ligue1',
                'season': '2025-2026',
                'last_update': datetime.now().isoformat(),
                'source': 'SportMonks API',
                'teams': all_data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] Données sauvegardées: {output_path}")
        
        # Stats
        for team, players in all_data.items():
            print(f"  {team.upper()}: {len(players)} joueurs")
    
    return all_data

if __name__ == "__main__":
    print("="*50)
    print("RÉCUPÉRATION EFFECTIFS RÉELS VIA SPORTMONKS")
    print("="*50)
    
    data = get_team_players_correct()
    
    if data:
        print("\n[OK] Succès!")
        print("[i] Les effectifs réels sont maintenant disponibles")
        print("[i] Note: Les positions et numéros nécessitent un endpoint différent")