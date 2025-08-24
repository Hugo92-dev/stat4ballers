import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Tester différentes méthodes d'authentification
API_KEY = "C3Wid19g74gH2DUPrtoJPpRx8w7obNSgSWpBD8rIoq66HJCEjxFSe3OwCJHF"
BASE_URL = "https://api.sportmonks.com/v3/football"

print("Test de différentes méthodes d'authentification SportMonks API")
print("=" * 80)

# Méthode 1: Authorization header (comme avant)
def test_auth_header():
    print("\n1. Test avec Authorization header:")
    headers = {
        "Accept": "application/json",
        "Authorization": API_KEY,
    }
    url = f"{BASE_URL}/leagues"
    params = {"per_page": 1}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Succès!")
            return True
        else:
            print(f"   ❌ Erreur: {response.json().get('message', response.text[:100])}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    return False

# Méthode 2: Bearer token
def test_bearer_token():
    print("\n2. Test avec Bearer token:")
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }
    url = f"{BASE_URL}/leagues"
    params = {"per_page": 1}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Succès!")
            return True
        else:
            print(f"   ❌ Erreur: {response.json().get('message', response.text[:100])}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    return False

# Méthode 3: API key dans les paramètres
def test_api_key_param():
    print("\n3. Test avec api_token dans les paramètres:")
    headers = {
        "Accept": "application/json",
    }
    url = f"{BASE_URL}/leagues"
    params = {
        "api_token": API_KEY,
        "per_page": 1
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Succès!")
            return True
        else:
            print(f"   ❌ Erreur: {response.json().get('message', response.text[:100])}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    return False

# Méthode 4: X-API-KEY header
def test_x_api_key():
    print("\n4. Test avec X-API-KEY header:")
    headers = {
        "Accept": "application/json",
        "X-API-KEY": API_KEY,
    }
    url = f"{BASE_URL}/leagues"
    params = {"per_page": 1}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Succès!")
            return True
        else:
            print(f"   ❌ Erreur: {response.json().get('message', response.text[:100])}")
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    return False

# Tester toutes les méthodes
methods = [
    test_auth_header,
    test_bearer_token,
    test_api_key_param,
    test_x_api_key
]

working_method = None
for method in methods:
    if method():
        working_method = method.__name__
        break

if working_method:
    print(f"\n✅ Méthode qui fonctionne: {working_method}")
    print("\nMaintenant, récupérons les stats de Rulli...")
    
    # Utiliser la méthode qui fonctionne
    if working_method == "test_api_key_param":
        # Récupérer les stats avec api_token dans params
        player_id = 186418
        season_id = 25651
        
        url = f"{BASE_URL}/players/{player_id}"
        params = {
            "api_token": API_KEY,
            "include": "statistics.details",
            "filters": f"playerStatisticSeasons:{season_id}"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            print(json.dumps(data, indent=2, ensure_ascii=False)[:1000])
else:
    print("\n❌ Aucune méthode d'authentification ne fonctionne")
    print("\nL'API key fournie semble invalide ou expirée.")
    print("Il faut une API key valide pour récupérer les vraies stats.")