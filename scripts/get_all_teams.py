import requests
import json

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
base_url = "https://api.sportmonks.com/v3/football"

def get_teams_by_league(league_id, league_name):
    """Récupère toutes les équipes d'un championnat"""
    print(f"\n{'='*60}")
    print(f"Fetching teams for {league_name} (ID: {league_id})")
    print(f"{'='*60}")
    
    # Récupérer la saison actuelle
    season_response = requests.get(
        f"{base_url}/seasons",
        params={
            'api_token': API_KEY,
            'filters': f'league_id:{league_id};is_current:true'
        }
    )
    
    if season_response.status_code == 200:
        season_data = season_response.json()
        if season_data['data']:
            current_season = season_data['data'][0]
            season_id = current_season['id']
            print(f"Current season ID: {season_id}")
            
            # Récupérer les équipes de la saison
            teams_response = requests.get(
                f"{base_url}/teams/seasons/{season_id}",
                params={'api_token': API_KEY}
            )
            
            if teams_response.status_code == 200:
                teams_data = teams_response.json()
                teams = []
                for team in teams_data['data']:
                    teams.append({
                        'id': team['id'],
                        'name': team['name'],
                        'short_code': team.get('short_code', ''),
                        'venue_id': team.get('venue_id')
                    })
                print(f"Found {len(teams)} teams")
                return teams
    
    return []

def main():
    # IDs des championnats (vérifiés)
    leagues = {
        'ligue1': {'id': 301, 'name': 'Ligue 1'},
        'premier-league': {'id': 8, 'name': 'Premier League'},
        'laliga': {'id': 564, 'name': 'La Liga'},
        'serie-a': {'id': 384, 'name': 'Serie A'},
        'bundesliga': {'id': 82, 'name': 'Bundesliga'}
    }
    
    all_teams = {}
    
    for league_key, league_info in leagues.items():
        teams = get_teams_by_league(league_info['id'], league_info['name'])
        all_teams[league_key] = {
            'league_id': league_info['id'],
            'league_name': league_info['name'],
            'teams': teams
        }
        
        # Afficher les équipes trouvées
        print("\nTeams found:")
        for team in teams:
            print(f"  - {team['name']}: ID={team['id']}")
    
    # Sauvegarder dans un fichier
    with open('all_teams_ids.json', 'w', encoding='utf-8') as f:
        json.dump(all_teams, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("Teams data saved to all_teams_ids.json")
    print(f"{'='*60}")
    
    # Résumé
    for league_key, data in all_teams.items():
        print(f"{data['league_name']}: {len(data['teams'])} teams")

if __name__ == "__main__":
    main()