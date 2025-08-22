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

# IDs des saisons Ligue 1 récentes
LIGUE1_SEASONS = {
    '2024/2025': 23435,
    '2023/2024': 21053, 
    '2022/2023': 19734,
    '2021/2022': 18378,
    '2020/2021': 17420
}

def test_aubameyang_all_seasons():
    """Tester Aubameyang sur toutes les saisons disponibles"""
    
    print("=== TEST AUBAMEYANG - TOUTES SAISONS ===\n")
    
    player_id = 31739
    found_seasons = []
    
    # Tester chaque saison
    for season_name, season_id in LIGUE1_SEASONS.items():
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {
            'api_token': API_TOKEN,
            'filters': f'season_ids:{season_id}'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                stats = data[0] if isinstance(data, list) else data
                
                # Vérifier si il y a des données
                if stats.get('minutes', 0) > 0 or stats.get('appearences', 0) > 0:
                    print(f"✅ {season_name} (ID: {season_id}):")
                    print(f"   • Minutes: {stats.get('minutes', 0)}")
                    print(f"   • Matchs: {stats.get('appearences', 0)}")
                    print(f"   • Buts: {stats.get('goals', 0)}")
                    print(f"   • Passes: {stats.get('assists', 0)}")
                    print(f"   • Team ID: {stats.get('team_id', 'N/A')}")
                    
                    found_seasons.append({
                        'season': season_name,
                        'season_id': season_id,
                        'stats': stats
                    })
                else:
                    print(f"⏸️ {season_name}: Pas de données")
            else:
                print(f"❌ {season_name}: Aucune donnée")
    
    # Essayer d'autres ligues (Premier League, etc.)
    print("\n=== TEST AUTRES LIGUES ===\n")
    
    # IDs de quelques saisons Premier League
    PL_SEASONS = {
        '2023/2024': 21779,
        '2022/2023': 19799,
        '2021/2022': 18462
    }
    
    for season_name, season_id in PL_SEASONS.items():
        url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
        params = {
            'api_token': API_TOKEN,
            'filters': f'season_ids:{season_id}'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                stats = data[0] if isinstance(data, list) else data
                
                if stats.get('minutes', 0) > 0:
                    print(f"✅ Premier League {season_name}:")
                    print(f"   • Minutes: {stats.get('minutes', 0)}")
                    print(f"   • Matchs: {stats.get('appearences', 0)}")
                    print(f"   • Buts: {stats.get('goals', 0)}")
                    
                    found_seasons.append({
                        'season': f"PL {season_name}",
                        'season_id': season_id,
                        'stats': stats
                    })
    
    # Résumé
    if found_seasons:
        print(f"\n📊 RÉSUMÉ: {len(found_seasons)} saisons trouvées avec données")
        total_goals = sum(s['stats'].get('goals', 0) for s in found_seasons)
        total_assists = sum(s['stats'].get('assists', 0) for s in found_seasons)
        total_matches = sum(s['stats'].get('appearences', 0) for s in found_seasons)
        
        print(f"TOTAL CARRIÈRE:")
        print(f"  • Buts: {total_goals}")
        print(f"  • Passes: {total_assists}") 
        print(f"  • Matchs: {total_matches}")
    
    return found_seasons

def test_other_om_players():
    """Tester d'autres joueurs de l'OM"""
    
    print("\n\n=== TEST AUTRES JOUEURS OM ===\n")
    
    # Quelques joueurs avec leurs IDs corrects
    players = [
        {'name': 'Leonardo Balerdi', 'id': 186553},
        {'name': 'Geoffrey Kondogbia', 'id': 906},
        {'name': 'Amine Harit', 'id': 31166}
    ]
    
    # Saison Ligue 1 2023/2024 (la plus récente complète)
    season_id = 21053
    
    for player in players:
        print(f"\n{player['name']} (ID: {player['id']}):")
        
        url = f"{BASE_URL}/statistics/seasons/players/{player['id']}"
        params = {
            'api_token': API_TOKEN,
            'filters': f'season_ids:{season_id}'
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', [])
            if data:
                stats = data[0] if isinstance(data, list) else data
                
                if stats.get('minutes', 0) > 0:
                    print(f"  ✅ Saison 2023/2024:")
                    print(f"     • Minutes: {stats.get('minutes', 0)}")
                    print(f"     • Matchs: {stats.get('appearences', 0)}")
                    print(f"     • Buts: {stats.get('goals', 0)}")
                    print(f"     • Passes: {stats.get('assists', 0)}")
                else:
                    print(f"  ⏸️ Pas de données")
            else:
                print(f"  ❌ Aucune donnée")

if __name__ == "__main__":
    aubameyang_seasons = test_aubameyang_all_seasons()
    test_other_om_players()
    
    print("\n\n💡 CONCLUSION:")
    print("Les données existent dans l'API mais sur des saisons différentes.")
    print("Il faut utiliser les bonnes IDs de saisons pour chaque joueur.")