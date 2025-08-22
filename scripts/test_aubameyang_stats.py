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

# Aubameyang
PLAYER_ID = 31739

# Saisons Ligue 1
CURRENT_SEASON = 25651  # 2025/2026
PREVIOUS_SEASONS = [23435, 21053]  # 2024/2025, 2023/2024

def test_aubameyang_stats():
    """Tester les statistiques d'Aubameyang"""
    
    print("=== TEST STATISTIQUES AUBAMEYANG ===\n")
    
    # 1. Saison actuelle 2025/2026
    print("1. SAISON 2025/2026 (ID: 25651)")
    print("-" * 40)
    
    url = f"{BASE_URL}/statistics/seasons/players/{PLAYER_ID}"
    params = {
        'api_token': API_TOKEN,
        'filters': f'season_ids:{CURRENT_SEASON}'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            stats = data[0] if isinstance(data, list) else data
            print(f"✅ Données trouvées:")
            print(f"   • Minutes: {stats.get('minutes', 0)}")
            print(f"   • Matchs: {stats.get('appearences', 0)}")
            print(f"   • Buts: {stats.get('goals', 0)}")
            print(f"   • Passes décisives: {stats.get('assists', 0)}")
            
            # Afficher toutes les stats disponibles
            print("\nToutes les statistiques disponibles:")
            for key, value in stats.items():
                if key not in ['id', 'player_id', 'team_id', 'season_id']:
                    if value and value != 0:
                        print(f"   • {key}: {value}")
        else:
            print("❌ Pas de données pour cette saison")
    else:
        print(f"❌ Erreur API: {response.status_code}")
    
    # 2. Saison précédente 2024/2025
    print("\n2. SAISON 2024/2025 (ID: 23435)")
    print("-" * 40)
    
    params['filters'] = f'season_ids:{PREVIOUS_SEASONS[0]}'
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            stats = data[0] if isinstance(data, list) else data
            if stats.get('minutes', 0) > 0 or stats.get('appearences', 0) > 0:
                print(f"✅ Données trouvées:")
                print(f"   • Minutes: {stats.get('minutes', 0)}")
                print(f"   • Matchs: {stats.get('appearences', 0)}")
                print(f"   • Buts: {stats.get('goals', 0)}")
                print(f"   • Passes décisives: {stats.get('assists', 0)}")
                print(f"   • xG: {stats.get('expected_goals', 0)}")
                print(f"   • xA: {stats.get('expected_assists', 0)}")
                print(f"   • Note moyenne: {stats.get('rating', 0)}")
            else:
                print("❌ Pas de données (joueur n'a pas joué)")
        else:
            print("❌ Pas de données pour cette saison")
    else:
        print(f"❌ Erreur API: {response.status_code}")
    
    # 3. Saison 2023/2024
    print("\n3. SAISON 2023/2024 (ID: 21053)")
    print("-" * 40)
    
    params['filters'] = f'season_ids:{PREVIOUS_SEASONS[1]}'
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json().get('data', [])
        if data:
            stats = data[0] if isinstance(data, list) else data
            if stats.get('minutes', 0) > 0 or stats.get('appearences', 0) > 0:
                print(f"✅ Données trouvées:")
                print(f"   • Minutes: {stats.get('minutes', 0)}")
                print(f"   • Matchs: {stats.get('appearences', 0)}")
                print(f"   • Buts: {stats.get('goals', 0)}")
                print(f"   • Passes décisives: {stats.get('assists', 0)}")
                print(f"   • xG: {stats.get('expected_goals', 0)}")
                print(f"   • xA: {stats.get('expected_assists', 0)}")
                print(f"   • Note moyenne: {stats.get('rating', 0)}")
            else:
                print("❌ Pas de données (joueur n'a pas joué)")
        else:
            print("❌ Pas de données pour cette saison")
    else:
        print(f"❌ Erreur API: {response.status_code}")

if __name__ == "__main__":
    test_aubameyang_stats()