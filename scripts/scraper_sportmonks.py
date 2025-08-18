import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Any

class SportMonksScraper:
    """
    Scraper utilisant l'API SportMonks (compte premium requis)
    Documentation: https://docs.sportmonks.com/football/
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportmonks.com/v3/football"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        
        # IDs des ligues dans SportMonks
        self.league_ids = {
            "ligue1": 301,      # Ligue 1 France
            "premier-league": 237,  # Premier League
            "liga": 564,        # La Liga
            "serie-a": 384,     # Serie A
            "bundesliga": 271   # Bundesliga
        }
        
        # Saison actuelle 2025-2026
        self.current_season_id = None  # À récupérer dynamiquement
    
    def get_current_season(self, league_id: int) -> int:
        """Récupère l'ID de la saison actuelle pour une ligue"""
        url = f"{self.base_url}/seasons"
        params = {
            "filters[league_id]": league_id,
            "filters[is_current]": "true"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                if data.get("data") and len(data["data"]) > 0:
                    return data["data"][0]["id"]
        except Exception as e:
            print(f"Erreur récupération saison: {e}")
        
        return None
    
    def get_teams_by_league(self, league_id: int) -> List[Dict]:
        """Récupère toutes les équipes d'une ligue"""
        season_id = self.get_current_season(league_id)
        if not season_id:
            print(f"Impossible de trouver la saison actuelle pour la ligue {league_id}")
            return []
        
        url = f"{self.base_url}/teams/seasons/{season_id}"
        params = {
            "include": "players"  # Inclure les joueurs
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"Erreur API: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Erreur récupération équipes: {e}")
        
        return []
    
    def get_team_squad(self, team_id: int, season_id: int) -> List[Dict]:
        """Récupère l'effectif complet d'une équipe avec stats détaillées"""
        url = f"{self.base_url}/squads/teams/{team_id}/seasons/{season_id}"
        params = {
            "include": "player.position,player.statistics.details,player.transfers"
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"Erreur API squad: {response.status_code}")
        except Exception as e:
            print(f"Erreur récupération effectif: {e}")
        
        return []
    
    def get_player_stats(self, player_id: int, season_id: int) -> Dict:
        """Récupère les statistiques détaillées d'un joueur pour la saison"""
        url = f"{self.base_url}/players/{player_id}"
        params = {
            "include": f"statistics.details:filter(season_id:{season_id})",
            "filters[season_id]": season_id
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                return data.get("data", {})
        except Exception as e:
            print(f"Erreur stats joueur: {e}")
        
        return {}
    
    def format_player_data(self, player_data: Dict, team_name: str) -> Dict:
        """Formate les données du joueur pour notre structure"""
        player = player_data.get("player", {})
        stats = player.get("statistics", {}).get("data", [{}])[0] if player.get("statistics") else {}
        
        # Calculer la valeur marchande (si disponible via transfermarkt ID)
        market_value = 0
        if player.get("market_value"):
            market_value = player["market_value"]
        
        return {
            "id": player.get("common_name", "").lower().replace(" ", "-"),
            "nom": player.get("display_name", player.get("common_name", "")),
            "club": team_name,
            "poste": player.get("position", {}).get("name", "N/A") if player.get("position") else "N/A",
            "numero": player_data.get("jersey_number", 0),
            "age": self.calculate_age(player.get("date_of_birth", "")),
            "nationalite": player.get("nationality", {}).get("name", "") if player.get("nationality") else "",
            "photo": player.get("image_path", ""),
            
            # Stats de base
            "matchs_joues": stats.get("appearances", 0),
            "titularisations": stats.get("lineups", 0),
            "minutes": stats.get("minutes", 0),
            "note_moyenne": stats.get("rating", 0),
            
            # Stats offensives
            "buts": stats.get("goals", 0),
            "passes_decisives": stats.get("assists", 0),
            "xg": stats.get("xg", {}).get("total", 0) if stats.get("xg") else 0,
            "xa": stats.get("xg", {}).get("assists", 0) if stats.get("xg") else 0,
            "tirs_total": stats.get("shots", {}).get("total", 0) if stats.get("shots") else 0,
            "tirs_cadres": stats.get("shots", {}).get("on_target", 0) if stats.get("shots") else 0,
            "penalties_marques": stats.get("penalties", {}).get("scored", 0) if stats.get("penalties") else 0,
            
            # Stats créatives
            "passes_cles": stats.get("passes", {}).get("key", 0) if stats.get("passes") else 0,
            "passes_reussies_pct": stats.get("passes", {}).get("accuracy", 0) if stats.get("passes") else 0,
            "dribbles_reussis": stats.get("dribbles", {}).get("success", 0) if stats.get("dribbles") else 0,
            "centres_reussis": stats.get("crosses", {}).get("accurate", 0) if stats.get("crosses") else 0,
            
            # Stats défensives
            "tacles_reussis": stats.get("tackles", 0),
            "interceptions": stats.get("interceptions", 0),
            "duels_aeriens_gagnes": stats.get("duels", {}).get("aerial_won", 0) if stats.get("duels") else 0,
            "cleansheets": stats.get("clean_sheets", 0),
            
            # Discipline
            "cartons_jaunes": stats.get("cards", {}).get("yellow", 0) if stats.get("cards") else 0,
            "cartons_rouges": stats.get("cards", {}).get("red", 0) if stats.get("cards") else 0,
            
            # Autres
            "valeur_marchande": market_value,
            "last_update": datetime.now().isoformat()
        }
    
    def calculate_age(self, date_of_birth: str) -> int:
        """Calcule l'âge à partir de la date de naissance"""
        if not date_of_birth:
            return 0
        
        try:
            birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
            return age
        except:
            return 0
    
    def scrape_ligue1_clubs(self, club_names: List[str] = ["psg", "marseille", "lyon", "monaco"]):
        """Récupère les données des clubs spécifiés de Ligue 1"""
        league_id = self.league_ids["ligue1"]
        season_id = self.get_current_season(league_id)
        
        if not season_id:
            print("Impossible de récupérer la saison actuelle")
            return {}
        
        print(f"Saison actuelle ID: {season_id}")
        
        # Récupérer toutes les équipes de Ligue 1
        teams = self.get_teams_by_league(league_id)
        
        result = {}
        
        for team in teams:
            team_name_normalized = team.get("name", "").lower().replace(" ", "-")
            
            # Mapping des noms d'équipes
            team_mapping = {
                "paris-saint-germain": "psg",
                "olympique-marseille": "marseille",
                "olympique-lyonnais": "lyon",
                "as-monaco": "monaco"
            }
            
            team_key = team_mapping.get(team_name_normalized, team_name_normalized)
            
            if team_key in club_names:
                print(f"\nRécupération de {team.get('name')}...")
                team_id = team.get("id")
                
                # Récupérer l'effectif
                squad = self.get_team_squad(team_id, season_id)
                
                players = []
                for player_data in squad:
                    formatted_player = self.format_player_data(player_data, team_key)
                    players.append(formatted_player)
                    print(f"  - {formatted_player['nom']} ({formatted_player['poste']})")
                
                result[team_key] = players
        
        return result
    
    def save_to_json(self, data: Dict, filename: str = "ligue1_sportmonks.json"):
        """Sauvegarde les données en JSON"""
        output_path = os.path.join('public', 'data', filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'league': 'ligue1',
                'season': '2025-2026',
                'last_update': datetime.now().isoformat(),
                'teams': data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] Données sauvegardées: {output_path}")
        
        # Calculer les statistiques
        total_players = sum(len(players) for players in data.values())
        print(f"Total: {len(data)} clubs, {total_players} joueurs")

# Configuration et test
if __name__ == "__main__":
    print("="*50)
    print("SportMonks API Scraper - Saison 2025-2026")
    print("="*50)
    
    # IMPORTANT: Remplace par ta clé API SportMonks
    API_KEY = "YOUR_SPORTMONKS_API_KEY"
    
    print("\n[!] IMPORTANT: Ajoute ta clé API SportMonks dans le fichier")
    print("    Remplace 'YOUR_SPORTMONKS_API_KEY' par ta vraie clé")
    print("\nAvec SportMonks tu auras:")
    print("  - Effectifs exacts et à jour")
    print("  - Stats complètes de chaque joueur")
    print("  - Valeurs marchandes")
    print("  - Photos des joueurs")
    print("  - Historique des transferts")
    
    # Si tu as une clé API, décommente les lignes suivantes:
    # scraper = SportMonksScraper(API_KEY)
    # data = scraper.scrape_ligue1_clubs(["psg", "marseille", "lyon", "monaco"])
    # if data:
    #     scraper.save_to_json(data)
    
    print("\n[i] Documentation SportMonks: https://docs.sportmonks.com/football/")
    print("[i] Endpoints utiles:")
    print("    - /teams/seasons/{id} : Équipes d'une saison")
    print("    - /squads/teams/{id} : Effectif d'une équipe")
    print("    - /players/{id} : Stats détaillées d'un joueur")