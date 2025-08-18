import requests
import json
import os
from datetime import datetime

# Clé API SportMonks
API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"

class SportMonksRealData:
    def __init__(self):
        self.api_key = API_KEY
        self.headers = {
            "Authorization": self.api_key,
            "Accept": "application/json"
        }
        self.base_url = "https://api.sportmonks.com/v3/football"
        
        # IDs des équipes trouvés
        self.team_ids = {
            "psg": 591,
            "marseille": 44,
            "lyon": 79,
            "monaco": 338  # À vérifier
        }
    
    def get_team_squad(self, team_id, team_name):
        """Récupère l'effectif actuel d'une équipe"""
        print(f"\nRécupération de {team_name}...")
        
        url = f"{self.base_url}/squads/teams/{team_id}"
        params = {
            "include": "player.position,player.country"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                squad = data.get("data", [])
                
                players = []
                for player_data in squad:
                    player_info = player_data.get("player", {}).get("data", {})
                    if not player_info:
                        continue
                    
                    # Position
                    position = "N/A"
                    if player_info.get("position") and player_info["position"].get("data"):
                        position = player_info["position"]["data"].get("name", "N/A")
                    
                    # Nationalité
                    nationality = ""
                    if player_info.get("country") and player_info["country"].get("data"):
                        nationality = player_info["country"]["data"].get("name", "")
                    
                    # Calculer l'âge
                    age = 0
                    if player_info.get("date_of_birth"):
                        try:
                            birth = datetime.strptime(player_info["date_of_birth"], "%Y-%m-%d")
                            age = (datetime.now() - birth).days // 365
                        except:
                            pass
                    
                    player = {
                        "id": player_info.get("common_name", "").lower().replace(" ", "-").replace("'", ""),
                        "nom": player_info.get("display_name", player_info.get("common_name", "")),
                        "poste": self.map_position(position),
                        "numero": player_data.get("jersey_number", 0),
                        "age": age,
                        "nationalite": nationality,
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
                        "valeur_marchande": 0,  # À enrichir avec une autre source
                        "last_update": datetime.now().isoformat()
                    }
                    
                    players.append(player)
                    print(f"  - #{player['numero']} {player['nom']} ({player['poste']}) - {player['nationalite']}")
                
                return players
            else:
                print(f"Erreur API: {response.status_code}")
                return []
        except Exception as e:
            print(f"Erreur: {e}")
            return []
    
    def map_position(self, position):
        """Convertit les positions SportMonks en format court"""
        position_map = {
            "Goalkeeper": "GK",
            "Defender": "DEF",
            "Right Back": "RB",
            "Left Back": "LB",
            "Center Back": "CB",
            "Defensive Midfield": "DM",
            "Central Midfield": "CM",
            "Attacking Midfield": "AM",
            "Right Midfield": "RM",
            "Left Midfield": "LM",
            "Right Wing": "RW",
            "Left Wing": "LW",
            "Center Forward": "CF",
            "Striker": "ST",
            "Forward": "FW",
            "Midfielder": "MID",
            "Attacker": "ATT"
        }
        return position_map.get(position, position[:3].upper() if position else "N/A")
    
    def get_monaco_id(self):
        """Trouve l'ID de Monaco"""
        print("\nRecherche de Monaco...")
        url = f"{self.base_url}/teams/countries/17"  # France
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                teams = data.get("data", [])
                
                for team in teams:
                    if "Monaco" in team.get("name", ""):
                        print(f"Trouvé: {team.get('name')} (ID: {team.get('id')})")
                        return team.get("id")
        except Exception as e:
            print(f"Erreur: {e}")
        
        return None
    
    def scrape_all_clubs(self):
        """Récupère les données des 4 clubs de Ligue 1"""
        
        # Trouver l'ID de Monaco
        monaco_id = self.get_monaco_id()
        if monaco_id:
            self.team_ids["monaco"] = monaco_id
        
        all_data = {}
        
        for team_name, team_id in self.team_ids.items():
            players = self.get_team_squad(team_id, team_name.upper())
            if players:
                all_data[team_name] = players
                print(f"  Total: {len(players)} joueurs")
        
        return all_data
    
    def save_data(self, data):
        """Sauvegarde les données en JSON"""
        
        # Sauvegarder le fichier Ligue 1
        output_path = os.path.join('public', 'data', 'ligue1_2025_26_real.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'league': 'ligue1',
                'season': '2025-2026',
                'last_update': datetime.now().isoformat(),
                'source': 'SportMonks API',
                'teams': data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] Données sauvegardées: {output_path}")
        
        # Calculer les stats
        total_players = sum(len(players) for players in data.values())
        print(f"\nRésumé:")
        for team, players in data.items():
            print(f"  - {team.upper()}: {len(players)} joueurs")
        print(f"  Total: {total_players} joueurs")
        
        return output_path

if __name__ == "__main__":
    print("="*50)
    print("RÉCUPÉRATION DES EFFECTIFS RÉELS 2025-2026")
    print("="*50)
    
    scraper = SportMonksRealData()
    data = scraper.scrape_all_clubs()
    
    if data:
        output_file = scraper.save_data(data)
        print("\n[i] Les données sont maintenant dans:")
        print(f"    {output_file}")
        print("\n[i] Prochaine étape:")
        print("    Mettre à jour ClubPageNew pour utiliser ligue1_2025_26_real.json")