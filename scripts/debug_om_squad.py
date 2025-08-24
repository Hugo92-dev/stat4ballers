import requests
import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

OM_TEAM_ID = 44
SEASON_ID = 25651  # 2025/2026

print("TEST RÉCUPÉRATION EFFECTIF OM")
print("=" * 80)

# Essayer différents endpoints
endpoints = [
    f"/squads/teams/{OM_TEAM_ID}/extended",
    f"/squads/seasons/{SEASON_ID}/teams/{OM_TEAM_ID}",
    f"/teams/{OM_TEAM_ID}/squad",
]

for endpoint in endpoints:
    print(f"\n📍 Test endpoint: {endpoint}")
    url = BASE_URL + endpoint
    params = {"season_id": SEASON_ID} if "extended" in endpoint else {}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "data" in data:
                if isinstance(data["data"], list):
                    print(f"   ✅ {len(data['data'])} éléments trouvés")
                    if len(data["data"]) > 0:
                        print(f"   Premier élément: {json.dumps(data['data'][0], indent=2)[:500]}...")
                else:
                    print(f"   Type de data: {type(data['data'])}")
        else:
            print(f"   Erreur: {response.text[:200]}")
    except Exception as e:
        print(f"   Exception: {e}")

# Essayer avec l'endpoint players directement
print("\n📍 Test direct avec l'endpoint players pour l'équipe OM")
url = f"{BASE_URL}/players"
params = {"filters": f"teamIds:{OM_TEAM_ID}"}

try:
    response = requests.get(url, headers=headers, params=params)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if "data" in data and isinstance(data["data"], list):
            print(f"   ✅ {len(data['data'])} joueurs trouvés")
            if len(data["data"]) > 0:
                for i, player in enumerate(data["data"][:5]):
                    print(f"   - {player.get('display_name', 'Unknown')} (ID: {player.get('id')})")
    else:
        print(f"   Erreur: {response.text[:200]}")
except Exception as e:
    print(f"   Exception: {e}")