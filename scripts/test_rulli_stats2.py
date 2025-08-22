import requests
import json

API_TOKEN = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Authorization": API_TOKEN,
    "Accept": "application/json"
}

# ID de Rulli trouvé : 186418
player_id = 186418

# Méthode alternative : récupérer toutes les stats avec include
print("Récupération des statistiques de Rulli...")
stats_url = f"{BASE_URL}/players/{player_id}?include=statistics.details"
print(f"URL: {stats_url}")

response = requests.get(stats_url, headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    
    # Afficher les infos du joueur
    player_data = data.get('data', {})
    print(f"\nJoueur: {player_data.get('display_name')}")
    print(f"Position: {player_data.get('position_id')} (24=GK)")
    
    # Parcourir toutes les stats
    if player_data.get('statistics'):
        print(f"\nNombre de saisons trouvées: {len(player_data.get('statistics', []))}")
        
        for stat in player_data.get('statistics', []):
            season_id = stat.get('season_id')
            
            # Filtrer seulement les saisons qui nous intéressent
            if season_id in [21646, 23334, 25651]:  # Ligue 1 2023/24, 2024/25, 2025/26
                print(f"\n--- Saison ID: {season_id} ---")
                
                # Afficher les détails
                details = stat.get('details', {})
                print(f"Minutes: {details.get('minutes', 0)}")
                print(f"Matchs: {details.get('appearences', 0)}")
                print(f"Titularisations: {details.get('lineups', 0)}")
                print(f"Arrêts: {details.get('saves', 0)}")
                print(f"Clean sheets: {details.get('clean_sheets', 0)}")
                print(f"Buts encaissés: {details.get('goals_conceded', 0)}")
                print(f"Penalties arrêtés: {details.get('penalties_saved', 0)}")
                print(f"Penalties concédés: {details.get('penalties_committed', 0)}")
                print(f"Erreurs → but: {details.get('mistakes_leading_to_goals', 0)}")
                print(f"Note moyenne: {details.get('rating', 0)}")
                print(f"Cartons jaunes: {details.get('yellow_cards', 0)}")
                print(f"Cartons rouges: {details.get('red_cards', 0)}")
    else:
        print("\nAucune statistique trouvée")
else:
    print(f"Erreur: {response.text[:500]}")