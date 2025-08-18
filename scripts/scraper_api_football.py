import requests
import json
import os
from datetime import datetime
import time

class FootballAPIScaper:
    """
    Scraper utilisant API-FOOTBALL (https://www.api-football.com/)
    Version gratuite: 100 requêtes/jour
    Plus fiable que le scraping direct
    """
    
    def __init__(self):
        # Clé API gratuite (à remplacer par ta propre clé)
        # Inscription gratuite sur https://www.api-football.com/
        self.api_key = "YOUR_API_KEY_HERE"  # À remplacer
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "v3.football.api-sports.io"
        }
        
        # IDs des ligues dans l'API
        self.league_ids = {
            "ligue1": 61,      # Ligue 1 2024-2025
            "premier-league": 39,  # Premier League 2024-2025
            "liga": 140,       # La Liga 2024-2025
            "serie-a": 135,    # Serie A 2024-2025  
            "bundesliga": 78   # Bundesliga 2024-2025
        }
        
        # Mapping des équipes (ID API -> nom standardisé)
        self.teams_mapping = {
            # Ligue 1
            85: "psg",
            91: "monaco",
            81: "marseille",
            79: "lille",
            84: "nice",
            80: "lyon",
            116: "lens",
            106: "brest",
            94: "rennes",
            96: "toulouse",
            95: "strasbourg",
            83: "nantes",
            111: "le-havre",
            110: "auxerre",
            77: "angers",
            112: "metz",
            101: "lorient",
            98: "montpellier",
            99: "reims",
            93: "saint-etienne",
            
            # Premier League (exemples)
            42: "arsenal",
            40: "liverpool",
            50: "manchester-city",
            33: "manchester-united",
            49: "chelsea",
            47: "tottenham",
            
            # La Liga (exemples)
            541: "real-madrid",
            529: "barcelona",
            530: "atletico-madrid",
            
            # Serie A (exemples)
            505: "inter",
            489: "milan",
            496: "juventus",
            492: "napoli",
            
            # Bundesliga (exemples)
            157: "bayern",
            165: "borussia-dortmund",
            168: "bayer-leverkusen"
        }
    
    def get_team_squad(self, team_id, season=2024):
        """Récupère l'effectif complet d'une équipe"""
        url = f"{self.base_url}/players/squads"
        params = {
            "team": team_id
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data["results"] > 0:
                    return data["response"][0]["players"]
            return []
        except Exception as e:
            print(f"Erreur API: {e}")
            return []
    
    def get_player_stats(self, player_id, season=2024):
        """Récupère les stats détaillées d'un joueur"""
        url = f"{self.base_url}/players"
        params = {
            "id": player_id,
            "season": season
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data["results"] > 0:
                    return data["response"][0]
            return None
        except Exception as e:
            print(f"Erreur API: {e}")
            return None
    
    def format_player_data(self, player_info, team_name):
        """Formate les données du joueur pour notre structure"""
        # Si on a les stats détaillées
        if "statistics" in player_info:
            stats = player_info["statistics"][0]  # Stats de la ligue actuelle
            return {
                "id": player_info["player"]["name"].lower().replace(" ", "-"),
                "nom": player_info["player"]["name"],
                "club": team_name,
                "poste": stats["games"]["position"],
                "age": player_info["player"]["age"] or 0,
                "numero": stats["games"]["number"] or 0,
                "nationalite": player_info["player"]["nationality"],
                "photo": player_info["player"]["photo"],
                
                # Stats de base
                "matchs_joues": stats["games"]["appearences"] or 0,
                "titularisations": stats["games"]["lineups"] or 0,
                "minutes": stats["games"]["minutes"] or 0,
                "note_moyenne": float(stats["games"]["rating"] or 0),
                
                # Stats offensives
                "buts": stats["goals"]["total"] or 0,
                "passes_decisives": stats["goals"]["assists"] or 0,
                "tirs_total": stats["shots"]["total"] or 0,
                "tirs_cadres": stats["shots"]["on"] or 0,
                "penalties_marques": stats["penalty"]["scored"] or 0,
                "penalties_rates": stats["penalty"]["missed"] or 0,
                
                # Stats créatives
                "passes_cles": stats["passes"]["key"] or 0,
                "passes_totales": stats["passes"]["total"] or 0,
                "passes_reussies": stats["passes"]["accuracy"] or 0,
                "dribbles_reussis": stats["dribbles"]["success"] or 0,
                "dribbles_tentes": stats["dribbles"]["attempts"] or 0,
                
                # Stats défensives
                "tacles": stats["tackles"]["total"] or 0,
                "interceptions": stats["tackles"]["interceptions"] or 0,
                "duels_gagnes": stats["duels"]["won"] or 0,
                "duels_totaux": stats["duels"]["total"] or 0,
                
                # Cartons
                "cartons_jaunes": stats["cards"]["yellow"] or 0,
                "cartons_rouges": stats["cards"]["red"] or 0,
                
                # Autres
                "fautes_commises": stats["fouls"]["committed"] or 0,
                "fautes_subies": stats["fouls"]["drawn"] or 0,
                
                "last_update": datetime.now().isoformat()
            }
        
        # Si on a juste les infos basiques (depuis squad)
        else:
            return {
                "id": player_info["name"].lower().replace(" ", "-"),
                "nom": player_info["name"],
                "club": team_name,
                "poste": player_info.get("position", "N/A"),
                "age": player_info.get("age", 0),
                "numero": player_info.get("number", 0),
                "nationalite": player_info.get("nationality", ""),
                "photo": player_info.get("photo", ""),
                
                # Stats vides (à remplir plus tard)
                "matchs_joues": 0,
                "titularisations": 0,
                "minutes": 0,
                "buts": 0,
                "passes_decisives": 0,
                "last_update": datetime.now().isoformat()
            }
    
    def scrape_all_leagues(self):
        """Récupère tous les joueurs de tous les championnats"""
        all_players = {}
        
        for league_name, league_id in self.league_ids.items():
            print(f"\n📊 Scraping {league_name}...")
            all_players[league_name] = []
            
            # Récupérer toutes les équipes de la ligue
            url = f"{self.base_url}/teams"
            params = {
                "league": league_id,
                "season": 2024
            }
            
            try:
                response = requests.get(url, headers=self.headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    teams = data["response"]
                    
                    for team in teams:
                        team_id = team["team"]["id"]
                        team_name = self.teams_mapping.get(team_id, team["team"]["name"].lower().replace(" ", "-"))
                        
                        print(f"  🔍 {team['team']['name']}...")
                        
                        # Récupérer l'effectif
                        squad = self.get_team_squad(team_id)
                        
                        for player in squad[:15]:  # Limiter à 15 joueurs principaux
                            player_data = self.format_player_data(player, team_name)
                            all_players[league_name].append(player_data)
                            print(f"    ✅ {player_data['nom']}")
                        
                        # Pause pour respecter la limite API
                        time.sleep(1)
                
            except Exception as e:
                print(f"❌ Erreur pour {league_name}: {e}")
        
        return all_players
    
    def save_to_json(self, data, filename="all_players.json"):
        """Sauvegarde les données en JSON"""
        output_path = os.path.join('public', 'data', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'last_update': datetime.now().isoformat(),
                'leagues': data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Données sauvegardées dans {output_path}")

# Données de secours si l'API ne fonctionne pas
def get_fallback_data():
    """Retourne des données actuelles pour tous les clubs (saison 2024-2025)"""
    return {
        "ligue1": {
            "psg": [
                {"nom": "Gianluigi Donnarumma", "poste": "GK", "numero": 99, "age": 25},
                {"nom": "Achraf Hakimi", "poste": "RB", "numero": 2, "age": 26},
                {"nom": "Marquinhos", "poste": "CB", "numero": 5, "age": 30},
                {"nom": "Lucas Hernández", "poste": "CB", "numero": 21, "age": 28},
                {"nom": "Nuno Mendes", "poste": "LB", "numero": 25, "age": 22},
                {"nom": "Vitinha", "poste": "CM", "numero": 17, "age": 24},
                {"nom": "Warren Zaïre-Emery", "poste": "CM", "numero": 33, "age": 18},
                {"nom": "Fabián Ruiz", "poste": "CM", "numero": 8, "age": 28},
                {"nom": "Ousmane Dembélé", "poste": "RW", "numero": 10, "age": 27},
                {"nom": "Gonçalo Ramos", "poste": "ST", "numero": 9, "age": 23},
                {"nom": "Bradley Barcola", "poste": "LW", "numero": 29, "age": 22},
                {"nom": "Randal Kolo Muani", "poste": "ST", "numero": 23, "age": 26},
                {"nom": "Lee Kang-in", "poste": "AM", "numero": 19, "age": 23},
                {"nom": "Marco Asensio", "poste": "RW", "numero": 11, "age": 28},
                {"nom": "Milan Škriniar", "poste": "CB", "numero": 37, "age": 29}
            ],
            "marseille": [
                {"nom": "Pau López", "poste": "GK", "numero": 16, "age": 30},
                {"nom": "Jonathan Clauss", "poste": "RB", "numero": 7, "age": 32},
                {"nom": "Leonardo Balerdi", "poste": "CB", "numero": 5, "age": 25},
                {"nom": "Chancel Mbemba", "poste": "CB", "numero": 99, "age": 30},
                {"nom": "Renan Lodi", "poste": "LB", "numero": 12, "age": 26},
                {"nom": "Valentin Rongier", "poste": "DM", "numero": 21, "age": 30},
                {"nom": "Jordan Veretout", "poste": "CM", "numero": 27, "age": 31},
                {"nom": "Amine Harit", "poste": "AM", "numero": 11, "age": 27},
                {"nom": "Ismaïla Sarr", "poste": "RW", "numero": 23, "age": 26},
                {"nom": "Pierre-Emerick Aubameyang", "poste": "ST", "numero": 10, "age": 35},
                {"nom": "Iliman Ndiaye", "poste": "LW", "numero": 29, "age": 24}
            ],
            "monaco": [
                {"nom": "Philipp Köhn", "poste": "GK", "numero": 16, "age": 26},
                {"nom": "Vanderson", "poste": "RB", "numero": 2, "age": 23},
                {"nom": "Guillermo Maripán", "poste": "CB", "numero": 3, "age": 30},
                {"nom": "Mohammed Salisu", "poste": "CB", "numero": 22, "age": 25},
                {"nom": "Caio Henrique", "poste": "LB", "numero": 12, "age": 27},
                {"nom": "Denis Zakaria", "poste": "DM", "numero": 6, "age": 28},
                {"nom": "Youssouf Fofana", "poste": "CM", "numero": 19, "age": 25},
                {"nom": "Aleksandr Golovin", "poste": "AM", "numero": 17, "age": 28},
                {"nom": "Takumi Minamino", "poste": "RW", "numero": 18, "age": 29},
                {"nom": "Wissam Ben Yedder", "poste": "ST", "numero": 10, "age": 34},
                {"nom": "Folarin Balogun", "poste": "ST", "numero": 29, "age": 23}
            ]
        },
        "premier-league": {
            "manchester-city": [
                {"nom": "Ederson", "poste": "GK", "numero": 31, "age": 31},
                {"nom": "Kyle Walker", "poste": "RB", "numero": 2, "age": 34},
                {"nom": "Rúben Dias", "poste": "CB", "numero": 3, "age": 27},
                {"nom": "John Stones", "poste": "CB", "numero": 5, "age": 30},
                {"nom": "Joško Gvardiol", "poste": "LB", "numero": 24, "age": 22},
                {"nom": "Rodri", "poste": "DM", "numero": 16, "age": 28},
                {"nom": "Kevin De Bruyne", "poste": "CM", "numero": 17, "age": 33},
                {"nom": "Bernardo Silva", "poste": "AM", "numero": 20, "age": 30},
                {"nom": "Phil Foden", "poste": "RW", "numero": 47, "age": 24},
                {"nom": "Erling Haaland", "poste": "ST", "numero": 9, "age": 24},
                {"nom": "Jack Grealish", "poste": "LW", "numero": 10, "age": 29}
            ],
            "arsenal": [
                {"nom": "David Raya", "poste": "GK", "numero": 22, "age": 29},
                {"nom": "Ben White", "poste": "RB", "numero": 4, "age": 27},
                {"nom": "William Saliba", "poste": "CB", "numero": 2, "age": 23},
                {"nom": "Gabriel Magalhães", "poste": "CB", "numero": 6, "age": 27},
                {"nom": "Oleksandr Zinchenko", "poste": "LB", "numero": 35, "age": 28},
                {"nom": "Declan Rice", "poste": "DM", "numero": 41, "age": 25},
                {"nom": "Martin Ødegaard", "poste": "AM", "numero": 8, "age": 26},
                {"nom": "Kai Havertz", "poste": "AM", "numero": 29, "age": 25},
                {"nom": "Bukayo Saka", "poste": "RW", "numero": 7, "age": 23},
                {"nom": "Gabriel Jesus", "poste": "ST", "numero": 9, "age": 27},
                {"nom": "Gabriel Martinelli", "poste": "LW", "numero": 11, "age": 23}
            ]
        },
        # Ajouter les autres ligues de la même manière...
    }

if __name__ == "__main__":
    print("🚀 Démarrage du scraping via API-Football...")
    print("="*50)
    
    # Option 1: Utiliser l'API (nécessite une clé API)
    # scraper = FootballAPIScaper()
    # data = scraper.scrape_all_leagues()
    
    # Option 2: Utiliser les données de secours
    print("\n📌 Utilisation des données de secours (saison 2024-2025)")
    data = get_fallback_data()
    
    # Sauvegarder
    output_path = os.path.join('public', 'data', 'all_players_2024.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'last_update': datetime.now().isoformat(),
            'season': '2024-2025',
            'leagues': data
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Données sauvegardées dans {output_path}")
    print("\n📊 Résumé:")
    for league, teams in data.items():
        total_players = sum(len(players) for players in teams.values())
        print(f"  - {league}: {len(teams)} équipes, {total_players} joueurs")