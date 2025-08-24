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

player_id = 186418  # Rulli
OM_TEAM_ID = 44
season_id = 23643  # 2024/2025

print("RECHERCHE DES PENALTIES ARRÊTÉS PAR RULLI EN 2024/2025")
print("=" * 80)
print("Vous avez dit: Brest, Lyon et Rennes")
print()

# Méthode 1: Chercher les matchs spécifiques contre ces équipes
print("1️⃣ RECHERCHE DES MATCHS CONTRE BREST, LYON ET RENNES:")
print("-" * 60)

# D'abord, obtenir les IDs des équipes
team_names = ["Brest", "Lyon", "Rennes"]
team_ids = {}

url = f"{BASE_URL}/teams"
params = {"filters": f"countryIds:320", "per_page": 100}  # France
response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    for team in data.get("data", []):
        name = team.get("name", "")
        for target in team_names:
            if target.lower() in name.lower():
                team_ids[target] = team.get("id")
                print(f"✅ {target}: ID {team.get('id')} ({name})")

# Maintenant chercher les matchs contre ces équipes
print("\n2️⃣ ANALYSE DES MATCHS:")
print("-" * 60)

penalties_saved_count = 0
matches_with_penalties = []

for team_name, team_id in team_ids.items():
    if not team_id:
        continue
        
    # Chercher les matchs OM vs cette équipe en 2024/2025
    url = f"{BASE_URL}/fixtures"
    params = {
        "filters": f"teamIds:{OM_TEAM_ID},{team_id};seasonIds:{season_id}",
        "include": "events,lineups.player,statistics"
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        
        for fixture in data.get("data", []):
            # Vérifier que c'est bien OM vs l'équipe
            participants = fixture.get("participants", [])
            if len(participants) >= 2:
                team1_id = participants[0].get("id")
                team2_id = participants[1].get("id")
                
                if (team1_id == OM_TEAM_ID and team2_id == team_id) or (team2_id == OM_TEAM_ID and team1_id == team_id):
                    match_date = fixture.get("starting_at", "")[:10]
                    match_name = fixture.get("name", "")
                    
                    print(f"\n📅 {match_date}: {match_name}")
                    
                    # Vérifier si Rulli a joué
                    rulli_played = False
                    if "lineups" in fixture:
                        for lineup in fixture["lineups"]:
                            if lineup.get("player_id") == player_id:
                                rulli_played = True
                                print(f"   ✅ Rulli a joué")
                                break
                    
                    if not rulli_played:
                        print(f"   ⚫ Rulli n'a pas joué")
                        continue
                    
                    # Analyser les événements
                    if "events" in fixture:
                        for event in fixture["events"]:
                            event_type = event.get("type_id")
                            event_type_name = event.get("type", {}).get("name", "")
                            
                            # Chercher les penalties
                            if event_type == 83 or "penalty" in str(event_type_name).lower():
                                player_event_id = event.get("player_id")
                                participant_id = event.get("participant_id")
                                result = event.get("result", "")
                                
                                print(f"   🎯 Penalty trouvé!")
                                print(f"      Type: {event_type} ({event_type_name})")
                                print(f"      Joueur: {player_event_id}")
                                print(f"      Équipe: {participant_id}")
                                print(f"      Résultat: {result}")
                                
                                # Si c'est un penalty contre l'OM et qu'il est raté/arrêté
                                if participant_id != OM_TEAM_ID and (result in ["missed", "saved", "missed_penalty"]):
                                    penalties_saved_count += 1
                                    matches_with_penalties.append({
                                        "match": match_name,
                                        "date": match_date,
                                        "opponent": team_name
                                    })
                                    print(f"      ✅ PENALTY ARRÊTÉ PAR RULLI!")

print("\n" + "=" * 80)
print("3️⃣ RECHERCHE ALTERNATIVE - STATISTIQUES PAR JOUEUR/MATCH:")
print("-" * 60)

# Essayer l'endpoint player/fixtures
url = f"{BASE_URL}/players/{player_id}/fixtures"
params = {
    "filters": f"seasonIds:{season_id}",
    "include": "statistics"
}

response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    print("✅ Endpoint player/fixtures disponible")
    data = response.json()
    fixtures_count = len(data.get("data", []))
    print(f"   {fixtures_count} matchs trouvés pour Rulli")
else:
    print(f"❌ Endpoint non disponible: {response.status_code}")

# Essayer l'endpoint statistics/fixtures/players
print("\n4️⃣ ENDPOINT STATISTICS/FIXTURES/PLAYERS:")
print("-" * 60)

url = f"{BASE_URL}/statistics/fixtures/players"
params = {
    "filters": f"playerIds:{player_id};seasonIds:{season_id}",
}

response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    print("✅ Endpoint disponible")
    data = response.json()
    stats_count = len(data.get("data", []))
    print(f"   {stats_count} entrées de statistiques")
else:
    print(f"❌ Endpoint non disponible: {response.status_code}")

print("\n" + "=" * 80)
print("RÉSUMÉ:")
print("-" * 60)
print(f"Penalties arrêtés trouvés: {penalties_saved_count}")
if matches_with_penalties:
    print("\nMatchs où Rulli a arrêté un penalty:")
    for match in matches_with_penalties:
        print(f"  - {match['date']}: {match['match']} (vs {match['opponent']})")
else:
    print("\n⚠️ L'API SportMonks ne semble pas retourner les penalties arrêtés")
    print("   Il faudrait peut-être:")
    print("   1. Un abonnement API supérieur")
    print("   2. Un endpoint spécialisé non documenté")
    print("   3. Analyser match par match manuellement")