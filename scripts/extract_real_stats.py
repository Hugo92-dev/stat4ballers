import json

# Charger les données
with open('rulli_stats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

player_data = data['data']
stats = player_data.get('statistics', [])

print(f"Joueur: {player_data.get('display_name')}")
print(f"Total saisons: {len(stats)}")

# Chercher les saisons avec has_values=True
seasons_with_data = []

for stat in stats:
    if stat.get('has_values', False):
        season_info = {
            'season_id': stat.get('season_id'),
            'team_id': stat.get('team_id'),
            'jersey_number': stat.get('jersey_number'),
            'details': stat.get('details', [])
        }
        seasons_with_data.append(season_info)

print(f"\nSaisons avec données: {len(seasons_with_data)}")

# Afficher les premières saisons avec données
for i, season in enumerate(seasons_with_data[:5]):
    print(f"\n=== Saison {i+1} ===")
    print(f"Season ID: {season['season_id']}")
    print(f"Team ID: {season['team_id']}")
    print(f"Jersey: {season['jersey_number']}")
    
    # Afficher les détails si disponibles
    details = season['details']
    if isinstance(details, list) and len(details) > 0:
        detail = details[0]
    elif isinstance(details, dict):
        detail = details
    else:
        detail = {}
    
    if detail:
        print("\nStatistiques disponibles:")
        # Afficher quelques stats clés
        for key in ['minutes', 'appearences', 'lineups', 'saves', 'clean_sheets', 'goals_conceded']:
            if key in detail:
                print(f"  {key}: {detail[key]}")

# Sauvegarder les stats formatées pour l'OM (team_id = 85)
om_stats = {}
for season in seasons_with_data:
    if season['team_id'] == 85:  # OM
        details = season['details']
        if isinstance(details, list) and len(details) > 0:
            detail = details[0]
        elif isinstance(details, dict):
            detail = details
        else:
            continue
            
        # Mapper le season_id à une saison lisible
        season_name = None
        if season['season_id'] == 21646:
            season_name = "2024/2025"
        elif season['season_id'] == 19686:
            season_name = "2023/2024"
        elif season['season_id'] == 23490:
            season_name = "2025/2026"
            
        if season_name and detail:
            om_stats[season_name] = detail

if om_stats:
    with open('rulli_stats_clean.json', 'w', encoding='utf-8') as f:
        json.dump(om_stats, f, indent=2, ensure_ascii=False)
    print(f"\nStats OM sauvegardées dans rulli_stats_clean.json")
    print(f"Saisons trouvées: {list(om_stats.keys())}")
else:
    print("\nAucune statistique trouvée pour l'OM (team_id=85)")