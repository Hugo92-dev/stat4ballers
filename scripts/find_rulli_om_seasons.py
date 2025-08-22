import json

# Charger les données
with open('rulli_stats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

player_data = data['data']
stats = player_data.get('statistics', [])

print(f"Joueur: {player_data.get('display_name')}")
print(f"Total saisons: {len(stats)}")

# Chercher les saisons avec l'OM (team_id de l'OM = 85)
om_seasons = []

for stat in stats:
    # Si il y a un team_id, regarder si c'est l'OM
    details = stat.get('details', [])
    if isinstance(details, list) and len(details) > 0:
        detail = details[0]
    elif isinstance(details, dict):
        detail = details
    else:
        detail = {}
    
    # Récupérer les minutes pour voir si le joueur a joué
    minutes = detail.get('minutes', 0) if detail else 0
    appearences = detail.get('appearences', 0) if detail else 0
    
    if minutes > 0 or appearences > 0:
        season_info = {
            'season_id': stat.get('season_id'),
            'team_id': stat.get('team_id'),
            'minutes': minutes,
            'appearences': appearences,
            'saves': detail.get('saves', 0) if detail else 0,
            'clean_sheets': detail.get('clean_sheets', 0) if detail else 0
        }
        
        # Filtrer les saisons récentes (IDs > 19000 environ)
        if season_info['season_id'] > 19000:
            om_seasons.append(season_info)

# Trier par season_id décroissant (plus récent en premier)
om_seasons.sort(key=lambda x: x['season_id'], reverse=True)

print("\n=== Saisons récentes avec des stats ===")
for season in om_seasons[:10]:  # Afficher les 10 plus récentes
    print(f"\nSeason ID: {season['season_id']}")
    print(f"  Team ID: {season['team_id']}")
    print(f"  Minutes: {season['minutes']}")
    print(f"  Matchs: {season['appearences']}")
    print(f"  Arrêts: {season['saves']}")
    print(f"  Clean sheets: {season['clean_sheets']}")