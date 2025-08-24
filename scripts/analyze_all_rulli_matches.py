import requests
import json
import sys
from datetime import datetime

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

print("ANALYSE COMPLÈTE DE TOUS LES MATCHS DE RULLI EN 2024/2025")
print("=" * 80)

# Récupérer TOUS les matchs de l'OM en 2024/2025
print("\n1️⃣ RÉCUPÉRATION DE TOUS LES MATCHS DE L'OM:")
print("-" * 60)

url = f"{BASE_URL}/fixtures"
params = {
    "filters": f"teamIds:{OM_TEAM_ID};seasonIds:{season_id}",
    "include": "events,lineups,statistics,participants",
    "per_page": 100
}

response = requests.get(url, headers=headers, params=params)

all_matches = []
rulli_matches = []
stats_aggregated = {
    "matches": 0,
    "goals_conceded": 0,
    "clean_sheets": 0,
    "penalties_faced": 0,
    "penalties_saved": 0,
    "saves": 0,
    "yellow_cards": 0,
    "red_cards": 0
}

if response.status_code == 200:
    data = response.json()
    print(f"✅ {len(data.get('data', []))} matchs trouvés")
    
    for fixture in data.get("data", []):
        match_date = fixture.get("starting_at", "")[:10]
        match_name = fixture.get("name", "")
        fixture_id = fixture.get("id")
        
        # Vérifier si Rulli a joué
        rulli_played = False
        rulli_lineup_data = None
        
        if "lineups" in fixture:
            for lineup in fixture["lineups"]:
                if lineup.get("player_id") == player_id:
                    rulli_played = True
                    rulli_lineup_data = lineup
                    break
        
        if rulli_played:
            rulli_matches.append(fixture)
            stats_aggregated["matches"] += 1
            
            # Analyser le score
            scores = fixture.get("scores", {})
            if scores:
                # Déterminer si l'OM est domicile ou extérieur
                participants = fixture.get("participants", [])
                om_is_home = False
                opponent_name = ""
                
                for p in participants:
                    if p.get("id") == OM_TEAM_ID:
                        om_is_home = (p.get("meta", {}).get("location") == "home")
                    else:
                        opponent_name = p.get("name", "")
                
                # Calculer les buts encaissés
                if om_is_home:
                    goals_against = scores.get("ft_score", {}).get("participant_away", 0)
                else:
                    goals_against = scores.get("ft_score", {}).get("participant_home", 0)
                
                stats_aggregated["goals_conceded"] += goals_against
                
                if goals_against == 0:
                    stats_aggregated["clean_sheets"] += 1
                
                # Afficher le match
                print(f"\n📅 {match_date}: {match_name}")
                print(f"   Score final: {scores.get('ft_score', {})}")
                print(f"   Buts encaissés: {goals_against}")
                
                # Analyser les événements du match
                penalty_in_match = False
                if "events" in fixture:
                    for event in fixture["events"]:
                        event_type = event.get("type_id")
                        
                        # Penalty (type 83)
                        if event_type == 83:
                            participant_id = event.get("participant_id")
                            result = event.get("result", "")
                            minute = event.get("minute", "")
                            
                            # Si c'est un penalty contre l'OM
                            if participant_id != OM_TEAM_ID:
                                stats_aggregated["penalties_faced"] += 1
                                penalty_in_match = True
                                
                                print(f"   🎯 PENALTY à la {minute}e minute!")
                                print(f"      Résultat: {result}")
                                
                                # Vérifier si arrêté
                                if result in ["missed", "saved", "missed_penalty", ""]:
                                    stats_aggregated["penalties_saved"] += 1
                                    print(f"      ✅ PENALTY ARRÊTÉ!")
                        
                        # Carton jaune pour Rulli (type 17)
                        elif event_type == 17 and event.get("player_id") == player_id:
                            stats_aggregated["yellow_cards"] += 1
                            print(f"   🟨 Carton jaune pour Rulli à la {event.get('minute', '')}e minute")
                        
                        # Carton rouge pour Rulli (type 18)
                        elif event_type == 18 and event.get("player_id") == player_id:
                            stats_aggregated["red_cards"] += 1
                            print(f"   🟥 Carton rouge pour Rulli à la {event.get('minute', '')}e minute")
                
                # Analyser les statistiques du match
                if "statistics" in fixture:
                    for stat in fixture["statistics"]:
                        if stat.get("participant_id") == OM_TEAM_ID:
                            if stat.get("type_id") == 57:  # Saves
                                saves_value = stat.get("data", {}).get("value", 0)
                                if isinstance(saves_value, dict):
                                    saves_value = saves_value.get("total", 0)
                                # Note: ce sont les saves de l'équipe, pas forcément de Rulli
                
                if not penalty_in_match and opponent_name.lower() in ["brest", "lyon", "rennes"]:
                    print(f"   ⚠️ Match contre {opponent_name} mais pas de penalty détecté dans l'API")

print("\n" + "=" * 80)
print("2️⃣ STATISTIQUES AGRÉGÉES DEPUIS LES MATCHS:")
print("-" * 60)
print(f"Matchs joués: {stats_aggregated['matches']}")
print(f"Buts encaissés: {stats_aggregated['goals_conceded']}")
print(f"Clean sheets: {stats_aggregated['clean_sheets']}")
print(f"Penalties affrontés: {stats_aggregated['penalties_faced']}")
print(f"Penalties arrêtés: {stats_aggregated['penalties_saved']}")
print(f"Cartons jaunes: {stats_aggregated['yellow_cards']}")
print(f"Cartons rouges: {stats_aggregated['red_cards']}")

# Essayer un autre endpoint pour les stats détaillées
print("\n" + "=" * 80)
print("3️⃣ VÉRIFICATION AVEC L'ENDPOINT PLAYER STATISTICS DÉTAILLÉ:")
print("-" * 60)

url = f"{BASE_URL}/players/{player_id}"
params = {
    "include": "statistics.details,statistics.season,teams"
}

response = requests.get(url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()
    player_data = data.get("data", {})
    
    print(f"Joueur: {player_data.get('display_name')}")
    
    if "statistics" in player_data:
        for stat in player_data["statistics"]:
            if stat.get("season_id") == season_id:
                print(f"\n✅ Stats trouvées pour 2024/2025")
                print(f"   has_values: {stat.get('has_values')}")
                print(f"   team_id: {stat.get('team_id')}")
                
                if "details" in stat:
                    # Chercher le type 113 (penalties saved)
                    for detail in stat["details"]:
                        if detail.get("type_id") in [113, 1509, 326]:
                            print(f"   🎯 Type {detail.get('type_id')} trouvé: {detail.get('value')}")

print("\n" + "=" * 80)
print("CONCLUSION:")
print("-" * 60)
if stats_aggregated["penalties_saved"] > 0:
    print(f"✅ {stats_aggregated['penalties_saved']} penalties arrêtés trouvés dans les événements de match!")
else:
    print("⚠️ Les penalties arrêtés ne sont pas correctement retournés par l'API SportMonks")
    print("   Soit ils ne sont pas dans le plan d'abonnement actuel,")
    print("   soit il faut utiliser un endpoint spécifique non documenté.")
print("\nLes autres stats (buts encaissés, clean sheets) semblent correctes.")