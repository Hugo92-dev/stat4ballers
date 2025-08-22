import requests
import sys
import json

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

API_TOKEN = 'leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2'
BASE_URL = 'https://api.sportmonks.com/v3/football'

def find_player_real_stats(player_name, player_id):
    """Trouver les vraies statistiques d'un joueur sur plusieurs saisons"""
    
    print(f"\n{'='*60}")
    print(f"📊 {player_name} (ID: {player_id})")
    print('='*60)
    
    # Récupérer toutes les statistiques du joueur
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'api_token': API_TOKEN,
        'include': 'statistics'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"❌ Erreur API: {response.status_code}")
        return None
    
    data = response.json()['data']
    
    if 'statistics' not in data:
        print("❌ Pas de statistiques trouvées")
        return None
    
    # Récupérer toutes les saisons où le joueur a joué
    all_stats = data['statistics']
    seasons_with_data = []
    
    for stat in all_stats:
        if stat.get('has_values'):
            season_id = stat.get('season_id')
            team_id = stat.get('team_id')
            
            # Récupérer les détails de cette saison
            url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
            params = {
                'api_token': API_TOKEN,
                'filters': f'season_ids:{season_id}'
            }
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                season_data = response.json().get('data', [])
                if season_data:
                    stats = season_data[0] if isinstance(season_data, list) else season_data
                    if stats.get('minutes', 0) > 0 or stats.get('appearences', 0) > 0:
                        seasons_with_data.append({
                            'season_id': season_id,
                            'team_id': team_id,
                            'minutes': stats.get('minutes', 0),
                            'matches': stats.get('appearences', 0),
                            'goals': stats.get('goals', 0),
                            'assists': stats.get('assists', 0),
                            'yellow_cards': stats.get('yellow_cards', 0),
                            'red_cards': stats.get('red_cards', 0),
                            'rating': stats.get('rating', 0)
                        })
    
    if seasons_with_data:
        print(f"\n✅ {len(seasons_with_data)} saisons avec des données trouvées")
        print("\nDernières saisons (IDs):")
        for i, season in enumerate(seasons_with_data[:5]):
            print(f"  {i+1}. Season ID: {season['season_id']}, Team ID: {season['team_id']}")
            print(f"     • Minutes: {season['minutes']}, Matchs: {season['matches']}")
            print(f"     • Buts: {season['goals']}, Passes: {season['assists']}")
    else:
        print("❌ Aucune saison avec des données")
    
    return seasons_with_data

def main():
    print("=== RECHERCHE DES VRAIES STATISTIQUES DES JOUEURS OM ===")
    
    # Joueurs clés de l'OM avec leurs vrais IDs
    om_players = [
        {'name': 'Pierre-Emerick Aubameyang', 'id': 31739},
        {'name': 'Mason Greenwood', 'id': 184465},
        {'name': 'Amine Harit', 'id': 31166},
        {'name': 'Leonardo Balerdi', 'id': 186553},
        {'name': 'Geoffrey Kondogbia', 'id': 906},
        {'name': 'Adrien Rabiot', 'id': 37824},
        {'name': 'Pierre-Emile Højbjerg', 'id': 2584},
        {'name': 'Luis Henrique', 'id': 85513},
        {'name': 'Jonathan Rowe', 'id': 316465},
        {'name': 'Neal Maupay', 'id': 3263}
    ]
    
    # Trouver les stats pour chaque joueur
    all_player_stats = {}
    
    for player in om_players:
        stats = find_player_real_stats(player['name'], player['id'])
        if stats:
            all_player_stats[player['name']] = stats
    
    # Résumé
    print(f"\n\n{'='*60}")
    print("📋 RÉSUMÉ DES SAISONS TROUVÉES")
    print('='*60)
    
    for player_name, seasons in all_player_stats.items():
        print(f"\n{player_name}: {len(seasons)} saisons avec données")
        total_goals = sum(s['goals'] for s in seasons)
        total_assists = sum(s['assists'] for s in seasons)
        total_matches = sum(s['matches'] for s in seasons)
        print(f"  Total: {total_goals} buts, {total_assists} passes, {total_matches} matchs")
    
    print("\n💡 CONCLUSION:")
    print("Les joueurs ont des historiques sur différentes saisons.")
    print("Il faut récupérer les bonnes IDs de saisons pour chaque joueur.")

if __name__ == "__main__":
    main()