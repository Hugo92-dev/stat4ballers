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

response = requests.get(stats_url, headers=headers)

if response.status_code == 200:
    data = response.json()
    
    # Sauvegarder la réponse complète pour analyse
    with open('rulli_stats.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print("Données sauvegardées dans rulli_stats.json")
    
    # Afficher les infos du joueur
    player_data = data.get('data', {})
    print(f"\nJoueur: {player_data.get('display_name')}")
    
    # Parcourir toutes les stats
    if player_data.get('statistics'):
        print(f"\nNombre de saisons trouvées: {len(player_data.get('statistics', []))}")
        
        season_names = {
            21646: "2023/2024",
            23334: "2024/2025", 
            25651: "2025/2026"
        }
        
        stats_found = {}
        
        for stat in player_data.get('statistics', []):
            season_id = stat.get('season_id')
            
            # Filtrer seulement les saisons Ligue 1 qui nous intéressent
            if season_id in [21646, 23334, 25651]:
                season_name = season_names.get(season_id, f"Saison {season_id}")
                print(f"\n--- {season_name} (ID: {season_id}) ---")
                
                # Gérer les détails (peut être une liste ou un dict)
                details = stat.get('details', [])
                
                # Si c'est une liste, prendre le premier élément
                if isinstance(details, list) and len(details) > 0:
                    detail = details[0]
                elif isinstance(details, dict):
                    detail = details
                else:
                    detail = {}
                
                # Extraire les stats qui nous intéressent
                stats_dict = {
                    'minutes': detail.get('minutes', 0),
                    'appearences': detail.get('appearences', 0),
                    'lineups': detail.get('lineups', 0),
                    'captain': detail.get('captain', 0),
                    'saves': detail.get('saves', 0),
                    'inside_box_saves': detail.get('inside_box_saves', 0),
                    'clean_sheets': detail.get('clean_sheets', 0),
                    'goals_conceded': detail.get('goals_conceded', 0),
                    'penalties_saved': detail.get('penalties_saved', 0),
                    'penalties_committed': detail.get('penalties_committed', 0),
                    'mistakes_leading_to_goals': detail.get('mistakes_leading_to_goals', 0),
                    'rating': detail.get('rating', 0),
                    'yellow_cards': detail.get('yellow_cards', 0),
                    'red_cards': detail.get('red_cards', 0),
                    'passes': detail.get('passes', 0),
                    'passes_accuracy': detail.get('passes_accuracy', 0)
                }
                
                stats_found[season_name] = stats_dict
                
                # Afficher un résumé
                print(f"Minutes jouées: {stats_dict['minutes']}")
                print(f"Matchs joués: {stats_dict['appearences']}")
                print(f"Titularisations: {stats_dict['lineups']}")
                print(f"Arrêts: {stats_dict['saves']}")
                print(f"Clean sheets: {stats_dict['clean_sheets']}")
                print(f"Buts encaissés: {stats_dict['goals_conceded']}")
        
        # Créer un fichier avec juste les stats nécessaires
        with open('rulli_stats_clean.json', 'w', encoding='utf-8') as f:
            json.dump(stats_found, f, indent=2, ensure_ascii=False)
        
        print(f"\n\nStatistiques nettoyées sauvegardées dans rulli_stats_clean.json")
else:
    print(f"Erreur: {response.status_code}")