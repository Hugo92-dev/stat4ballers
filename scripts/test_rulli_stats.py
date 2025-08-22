import requests
import json

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Authorization": API_TOKEN,
    "Accept": "application/json"
}

# D'abord, chercher Gerónimo Rulli
search_url = f"{BASE_URL}/players/search/Rulli"
print(f"URL: {search_url}")
response = requests.get(search_url, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

# Si on trouve son ID, récupérer ses stats
if response.status_code == 200 and response.text:
    try:
        data = response.json()
        print("\nRecherche de Rulli:")
        print(json.dumps(data, indent=2))
        
        if data.get('data'):
            for player in data['data']:
                if 'Gerónimo' in player.get('display_name', '') or 'Geronimo' in player.get('display_name', ''):
                    player_id = player['id']
                    print(f"\n\nID de Rulli trouvé: {player_id}")
                    print(f"Nom complet: {player.get('display_name')}")
                    
                    # IDs des saisons (corrigés)
                    seasons = {
                        '2023/2024': 21646,  # Ligue 1 2023/24
                        '2024/2025': 23334,  # Ligue 1 2024/25  
                        '2025/2026': 25651   # Ligue 1 2025/26
                    }
                    
                    for season_name, season_id in seasons.items():
                        print(f"\n\n--- Statistiques {season_name} ---")
                        stats_url = f"{BASE_URL}/players/{player_id}?include=statistics.details&filters[statistics][season_id]={season_id}"
                        stats_response = requests.get(stats_url, headers=headers)
                        
                        if stats_response.status_code == 200:
                            stats_data = stats_response.json()
                            if stats_data.get('data', {}).get('statistics'):
                                for stat in stats_data['data']['statistics']:
                                    if stat.get('season_id') == season_id:
                                        print(f"Minutes: {stat.get('details', {}).get('minutes', 0)}")
                                        print(f"Matchs: {stat.get('details', {}).get('appearences', 0)}")
                                        print(f"Arrêts: {stat.get('details', {}).get('saves', 0)}")
                                        print(f"Clean sheets: {stat.get('details', {}).get('clean_sheets', 0)}")
                                        print(f"Buts encaissés: {stat.get('details', {}).get('goals_conceded', 0)}")
                        else:
                            print(f"Erreur {stats_response.status_code}")
                    
                    break
    except Exception as e:
        print(f"Erreur: {e}")