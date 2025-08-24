import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Essayons avec l'API key correcte
API_KEY = "C3Wid19g74gH2DUPrtoJPpRx8w7obNSgSWpBD8rIoq66HJCEjxFSe3OwCJHF"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

print("Test de l'API SportMonks...")
print("=" * 80)

# Test 1: Vérifier l'accès de base
def test_basic_access():
    url = f"{BASE_URL}/leagues"
    params = {"per_page": 1}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Test accès API: Status {response.status_code}")
        if response.status_code == 200:
            print("✅ API accessible")
            return True
        else:
            print(f"❌ Erreur: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

# Test 2: Récupérer les stats de Rulli pour 2025/2026
def get_rulli_stats_current():
    # Rulli ID = 186418
    # Saison 2025/2026 Ligue 1 = 25651
    player_id = 186418
    season_id = 25651
    
    url = f"{BASE_URL}/players/{player_id}/statistics/seasons/{season_id}"
    
    print(f"\nTentative de récupération des stats de Rulli (ID: {player_id})")
    print(f"Saison 2025/2026 (ID: {season_id})")
    
    try:
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data and "data" in data:
                stats = data["data"]
                print("\n✅ STATS TROUVÉES:")
                print(json.dumps(stats, indent=2, ensure_ascii=False)[:500])
                return stats
        else:
            print(f"Erreur: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")
    
    return None

# Test 3: Essayer un autre endpoint
def get_player_season_stats():
    player_id = 186418
    season_id = 25651
    
    url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
    params = {
        "filters": f"seasons:{season_id}",
        "include": "details"
    }
    
    print(f"\nAutre tentative avec endpoint statistics...")
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data and "data" in data and len(data["data"]) > 0:
                stats = data["data"][0]
                if "details" in stats and len(stats["details"]) > 0:
                    detail = stats["details"][0]
                    print("\n✅ STATS TROUVÉES (détails):")
                    print(f"  Matchs: {detail.get('games', {}).get('appearences')}")
                    print(f"  Minutes: {detail.get('minutes')}")
                    print(f"  Buts encaissés: {detail.get('goalkeeper', {}).get('goals_conceded')}")
                    print(f"  Clean sheets: {detail.get('goalkeeper', {}).get('cleansheets')}")
                    print(f"  Arrêts: {detail.get('goalkeeper', {}).get('saves')}")
                    return detail
        else:
            print(f"Erreur: {response.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")
    
    return None

# Exécuter les tests
if test_basic_access():
    print("\nRecherche des vraies stats de Rulli...")
    stats = get_player_season_stats()
    
    if not stats:
        print("\n⚠️ Impossible de récupérer les stats depuis l'API")
        print("L'API semble avoir un problème ou les données ne sont pas encore disponibles")
        print("\nDonnées connues pour 2025/2026:")
        print("  - 1 seul match joué (vs Rennes)")
        print("  - Score: 0-1 (défaite)")
        print("  - Buts encaissés: 1 (pas 2)")
else:
    print("\n❌ L'API n'est pas accessible avec cette clé")