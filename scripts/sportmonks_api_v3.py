import requests
import json
import time
from typing import Dict, List, Optional
from datetime import datetime

class SportMonksAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.sportmonks.com/v3/football"
        self.headers = {
            'Accept': 'application/json'
        }
        
        # IDs des 5 grands championnats européens (confirmés via l'API)
        self.league_ids = {
            "Ligue 1": 301,        # France Ligue 1
            "Premier League": 8,   # England Premier League
            "La Liga": 564,        # Spain La Liga
            "Serie A": 384,        # Italy Serie A
            "Bundesliga": 82       # Germany Bundesliga
        }
        
        self.fetched_data = {
            "ligue1": [],
            "premier_league": [],
            "la_liga": [],
            "serie_a": [],
            "bundesliga": []
        }
        
    def make_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Effectue une requête à l'API SportMonks"""
        if params is None:
            params = {}
        
        params['api_token'] = self.api_key
        
        try:
            url = f"{self.base_url}{endpoint}"
            print(f"Calling: {endpoint}")
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            
            # Vérifier la limite de rate
            if isinstance(data, dict) and 'subscription' in data:
                subscription = data['subscription']
                if isinstance(subscription, dict):
                    remaining = subscription.get('rate_limit', {}).get('remaining', 'N/A')
                    print(f"  Rate limit remaining: {remaining}")
            
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None
    
    def get_current_season(self, league_id: int) -> Optional[int]:
        """Récupère l'ID de la saison actuelle pour une ligue"""
        data = self.make_request(f"/leagues/{league_id}", {"include": "currentSeason"})
        
        if data and 'data' in data:
            current_season = data['data'].get('currentSeason')
            if current_season:
                season_id = current_season.get('id')
                print(f"  Season ID: {season_id} ({current_season.get('name', 'N/A')})")
                return season_id
        
        return None
    
    def get_teams_in_season(self, season_id: int) -> List[Dict]:
        """Récupère toutes les équipes d'une saison"""
        data = self.make_request(f"/seasons/{season_id}/teams")
        
        teams = []
        if data and 'data' in data:
            for team in data['data']:
                teams.append({
                    'id': team.get('id'),
                    'name': team.get('name'),
                    'short_code': team.get('short_code')
                })
            print(f"  Found {len(teams)} teams")
        
        return teams
    
    def get_team_squad(self, team_id: int, team_name: str) -> List[Dict]:
        """Récupère l'effectif complet d'une équipe"""
        # Utiliser l'endpoint squad/extended pour avoir plus d'infos
        data = self.make_request(f"/teams/{team_id}/squad/extended")
        
        players = []
        if data and 'data' in data:
            for player_data in data['data']:
                player = player_data.get('player', {})
                
                # Extraire les informations du joueur
                player_info = {
                    'id': player.get('id'),
                    'nom': player.get('display_name') or player.get('name', 'Unknown'),
                    'position': self.map_position(player_data.get('position', {}).get('name')),
                    'numero': player_data.get('jersey_number'),
                    'age': self.calculate_age(player.get('date_of_birth')),
                    'nationalite': player.get('nationality', {}).get('name', 'Unknown'),
                    'valeur_marchande': player.get('market_value'),
                    # Stats de base (seront mises à jour avec l'endpoint statistics)
                    'minutes': 0,
                    'buts': 0,
                    'passes_decisives': 0,
                    'tirs_par_match': 0,
                    'passes_par_match': 0,
                    'tacles_par_match': 0,
                    'interceptions_par_match': 0
                }
                
                players.append(player_info)
            
            print(f"    {team_name}: {len(players)} players")
        
        return players
    
    def get_player_statistics(self, player_id: int, season_id: int) -> Dict:
        """Récupère les statistiques détaillées d'un joueur pour une saison"""
        # Inclure les statistiques dans la requête
        params = {
            "include": "statistics",
            "filters": f"statisticSeasons:{season_id}"
        }
        
        data = self.make_request(f"/players/{player_id}", params)
        
        stats = {
            'minutes': 0,
            'buts': 0,
            'passes_decisives': 0,
            'tirs_par_match': 0,
            'passes_par_match': 0,
            'tacles_par_match': 0,
            'interceptions_par_match': 0
        }
        
        if data and 'data' in data:
            player_stats = data['data'].get('statistics', [])
            
            # Parcourir les stats pour la saison
            for stat in player_stats:
                if stat.get('season_id') == season_id:
                    details = stat.get('details', [])
                    
                    for detail in details:
                        type_name = detail.get('type', {}).get('name', '')
                        value = detail.get('value', {})
                        
                        # Mapper les stats SportMonks vers notre format
                        if 'Minutes Played' in type_name:
                            stats['minutes'] = value.get('total', 0)
                        elif 'Goals' in type_name:
                            stats['buts'] = value.get('total', 0)
                        elif 'Assists' in type_name:
                            stats['passes_decisives'] = value.get('total', 0)
                        elif 'Shots' in type_name:
                            games = value.get('count', 1) or 1
                            stats['tirs_par_match'] = round(value.get('total', 0) / games, 1)
                        elif 'Passes' in type_name:
                            games = value.get('count', 1) or 1
                            stats['passes_par_match'] = round(value.get('total', 0) / games, 1)
                        elif 'Tackles' in type_name:
                            games = value.get('count', 1) or 1
                            stats['tacles_par_match'] = round(value.get('total', 0) / games, 1)
                        elif 'Interceptions' in type_name:
                            games = value.get('count', 1) or 1
                            stats['interceptions_par_match'] = round(value.get('total', 0) / games, 1)
        
        return stats
    
    def map_position(self, position: Optional[str]) -> str:
        """Convertit les positions SportMonks vers notre format"""
        if not position:
            return "Milieu"
        
        position_lower = position.lower()
        
        if 'goalkeeper' in position_lower or 'keeper' in position_lower:
            return "Gardien"
        elif 'defender' in position_lower or 'back' in position_lower:
            return "Défenseur"
        elif 'midfielder' in position_lower or 'midfield' in position_lower:
            return "Milieu"
        elif 'attacker' in position_lower or 'forward' in position_lower or 'striker' in position_lower:
            return "Attaquant"
        else:
            return "Milieu"
    
    def calculate_age(self, date_of_birth: Optional[str]) -> int:
        """Calcule l'âge à partir de la date de naissance"""
        if not date_of_birth:
            return 25  # Âge par défaut
        
        try:
            birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                age -= 1
            return age
        except:
            return 25
    
    def fetch_league_data(self, league_name: str, league_id: int, limit_teams: Optional[int] = None) -> Dict:
        """Récupère toutes les données d'une ligue"""
        print(f"\n{'='*50}")
        print(f"Fetching {league_name} data...")
        print(f"{'='*50}")
        
        # Étape 1: Obtenir la saison actuelle
        season_id = self.get_current_season(league_id)
        if not season_id:
            print(f"Could not get current season for {league_name}")
            return None
        
        # Étape 2: Obtenir toutes les équipes
        teams = self.get_teams_in_season(season_id)
        
        if limit_teams:
            teams = teams[:limit_teams]
            print(f"  Limiting to {limit_teams} teams for testing")
        
        # Étape 3: Pour chaque équipe, obtenir l'effectif
        league_data = {
            "championnat": league_name,
            "saison": "2025-2026",
            "clubs": []
        }
        
        for team in teams:
            print(f"\n  Fetching squad for {team['name']}...")
            
            # Obtenir l'effectif
            players = self.get_team_squad(team['id'], team['name'])
            
            # Pour les tests, limiter les stats détaillées aux premiers joueurs
            if len(players) > 0:
                print(f"    Fetching statistics for players...")
                # Limiter à 5 joueurs pour les tests
                for i, player in enumerate(players[:5]):
                    if player['id']:
                        stats = self.get_player_statistics(player['id'], season_id)
                        player.update(stats)
                        print(f"      Player {i+1}/5: {player['nom']}")
                    
                    # Pause pour respecter les limites de l'API
                    time.sleep(0.5)
            
            club_data = {
                "nom": team['name'],
                "logo": f"/logos/{team['name'].lower().replace(' ', '_')}.png",
                "stade": "Stadium",  # À compléter si nécessaire
                "joueurs": players
            }
            
            league_data["clubs"].append(club_data)
            
            # Pause entre les équipes
            time.sleep(1)
        
        return league_data
    
    def test_connection(self):
        """Test la connexion à l'API"""
        print("Testing SportMonks API connection...")
        data = self.make_request("/leagues", {"per_page": 1})
        
        if data:
            print("[OK] API connection successful!")
            if isinstance(data, dict) and 'subscription' in data:
                sub = data['subscription']
                if isinstance(sub, dict):
                    print(f"  Plan: {sub.get('plan', {}).get('name', 'N/A')}")
                    print(f"  Rate limit: {sub.get('rate_limit', {}).get('remaining', 'N/A')}/{sub.get('rate_limit', {}).get('limit', 'N/A')}")
            return True
        else:
            print("[ERROR] API connection failed!")
            return False

def main():
    # Votre clé API SportMonks
    API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
    
    api = SportMonksAPI(API_KEY)
    
    # Tester la connexion
    if not api.test_connection():
        print("Cannot proceed without API connection")
        return
    
    # Pour les tests, on commence avec la Ligue 1 et seulement 4 équipes
    print("\n" + "="*50)
    print("STARTING DATA COLLECTION FOR LIGUE 1 (TEST)")
    print("="*50)
    
    # Récupérer les données de la Ligue 1 (limité à 4 équipes pour le test)
    ligue1_data = api.fetch_league_data("Ligue 1", api.league_ids["Ligue 1"], limit_teams=4)
    
    if ligue1_data:
        # Sauvegarder les données
        output_file = "../public/data/ligue1_sportmonks_2025_26.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(ligue1_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*50}")
        print(f"Data saved to {output_file}")
        print(f"Total clubs: {len(ligue1_data['clubs'])}")
        
        for club in ligue1_data['clubs']:
            print(f"  - {club['nom']}: {len(club['joueurs'])} players")
    
    print("\n" + "="*50)
    print("DATA COLLECTION COMPLETE")
    print("="*50)

if __name__ == "__main__":
    main()