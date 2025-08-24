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

player_id = 186418
season_id = 23643  # 2024/2025

print("RÉCUPÉRATION DES VRAIES VALEURS DE CLEAN SHEETS")
print("=" * 80)

url = f"{BASE_URL}/statistics/seasons/players/{player_id}"
params = {"seasons": season_id}
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    
    for item in data.get("data", []):
        if item.get("season_id") == season_id and item.get("has_values"):
            
            if "details" in item:
                for detail in item["details"]:
                    type_id = detail.get("type_id")
                    
                    # Chercher le type 194 (Cleansheets)
                    if type_id == 194:
                        value = detail.get("value", {})
                        if isinstance(value, dict):
                            cleansheets = value.get("total", value.get("goals", value))
                        else:
                            cleansheets = value
                        
                        print(f"\n✅ TROUVÉ - Type 194 (Cleansheets):")
                        print(f"   Valeur brute: {value}")
                        print(f"   Valeur extraite: {cleansheets}")
                        print(f"\n   Rulli a fait {cleansheets} clean sheets en 2024/2025!")
                        
                        # Si ce n'est pas 5, il y a peut-être une différence entre les données
                        if cleansheets != 5:
                            print(f"   ⚠️ Tu avais dit 5, l'API dit {cleansheets}")

print("\n" + "=" * 80)
print("Vérifions aussi pour les penalties (type 113):")

# Parcourir à nouveau pour chercher le type 113
found_113 = False
for item in data.get("data", []):
    if item.get("season_id") == season_id and item.get("has_values"):
        if "details" in item:
            for detail in item["details"]:
                if detail.get("type_id") == 113:
                    found_113 = True
                    value = detail.get("value", {})
                    print(f"  ✅ Type 113 trouvé avec valeur: {value}")

if not found_113:
    print("  ❌ Type 113 (Penalties Saved) non présent")
    print("     → Rulli n'a probablement pas arrêté de penalty en 2024/2025")
    print("     → L'API ne retourne pas les stats à 0")