import requests
import json
import time

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
base_url = "https://api.sportmonks.com/v3/football"

def get_league_teams(league_id, league_name):
    """Récupère toutes les équipes d'un championnat pour la saison 2024/2025"""
    print(f"\n{'='*60}")
    print(f"Fetching teams for {league_name} (ID: {league_id})")
    print(f"{'='*60}")
    
    # D'abord essayer de récupérer directement les équipes du championnat
    standings_response = requests.get(
        f"{base_url}/standings/live/leagues/{league_id}",
        params={'api_token': API_KEY, 'include': 'participant'}
    )
    
    if standings_response.status_code == 200:
        standings_data = standings_response.json()
        if standings_data.get('data'):
            teams = []
            team_ids = set()  # Pour éviter les doublons
            
            for standing in standings_data['data']:
                if 'participant' in standing and standing['participant']:
                    team = standing['participant']
                    if team['id'] not in team_ids:
                        team_ids.add(team['id'])
                        teams.append({
                            'id': team['id'],
                            'name': team.get('name', 'Unknown'),
                            'short_code': team.get('short_code', '')
                        })
            
            print(f"Found {len(teams)} teams from standings")
            return teams
    
    # Si ça ne marche pas, essayer une autre approche
    print("Trying alternative approach...")
    
    # Rechercher les équipes par championnat
    teams_response = requests.get(
        f"{base_url}/teams",
        params={
            'api_token': API_KEY,
            'filters': f'current_league_id:{league_id}'
        }
    )
    
    if teams_response.status_code == 200:
        teams_data = teams_response.json()
        teams = []
        for team in teams_data.get('data', []):
            teams.append({
                'id': team['id'],
                'name': team.get('name', 'Unknown'),
                'short_code': team.get('short_code', '')
            })
        print(f"Found {len(teams)} teams from teams endpoint")
        return teams
    
    return []

def main():
    # IDs des championnats (vérifiés)
    leagues = {
        'ligue1': {'id': 301, 'name': 'Ligue 1', 'country': 'France'},
        'premier-league': {'id': 8, 'name': 'Premier League', 'country': 'England'},
        'laliga': {'id': 564, 'name': 'La Liga', 'country': 'Spain'},
        'serie-a': {'id': 384, 'name': 'Serie A', 'country': 'Italy'},
        'bundesliga': {'id': 82, 'name': 'Bundesliga', 'country': 'Germany'}
    }
    
    all_teams = {}
    
    for league_key, league_info in leagues.items():
        teams = get_league_teams(league_info['id'], league_info['name'])
        
        if not teams:
            # Si pas de résultats, essayer avec les équipes connues
            print(f"No teams found via API for {league_info['name']}, using known teams...")
            
            if league_key == 'ligue1':
                # Équipes de Ligue 1 connues
                known_teams = [
                    {'id': 591, 'name': 'Paris Saint-Germain'},
                    {'id': 44, 'name': 'Olympique de Marseille'},
                    {'id': 79, 'name': 'Olympique Lyonnais'},
                    {'id': 6789, 'name': 'AS Monaco'},
                    {'id': 65, 'name': 'Lille OSC'},
                    {'id': 85, 'name': 'Nice'},
                    {'id': 77, 'name': 'RC Lens'},
                    {'id': 69, 'name': 'Stade Rennais'},
                    {'id': 1020, 'name': 'Stade de Reims'},
                    {'id': 82, 'name': 'Toulouse FC'},
                    {'id': 88, 'name': 'FC Nantes'},
                    {'id': 57, 'name': 'Montpellier HSC'},
                    {'id': 106, 'name': 'RC Strasbourg'},
                    {'id': 66, 'name': 'Stade Brestois'},
                    {'id': 334, 'name': 'AJ Auxerre'},
                    {'id': 75, 'name': 'Le Havre AC'},
                    {'id': 674, 'name': 'Angers SCO'},
                    {'id': 58, 'name': 'AS Saint-Étienne'}
                ]
                teams = known_teams
        
        all_teams[league_key] = {
            'league_id': league_info['id'],
            'league_name': league_info['name'],
            'country': league_info['country'],
            'teams': teams
        }
        
        # Afficher les équipes trouvées
        if teams:
            print("\nTeams found:")
            for team in teams[:20]:  # Limiter l'affichage
                print(f"  - {team['name']}: ID={team['id']}")
            if len(teams) > 20:
                print(f"  ... and {len(teams) - 20} more teams")
        
        time.sleep(1)  # Pause entre les requêtes
    
    # Sauvegarder dans un fichier
    with open('all_teams_ids.json', 'w', encoding='utf-8') as f:
        json.dump(all_teams, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*60}")
    print("Teams data saved to all_teams_ids.json")
    print(f"{'='*60}")
    
    # Résumé
    total_teams = 0
    for league_key, data in all_teams.items():
        count = len(data['teams'])
        total_teams += count
        print(f"{data['league_name']}: {count} teams")
    print(f"\nTotal: {total_teams} teams across all leagues")

if __name__ == "__main__":
    main()