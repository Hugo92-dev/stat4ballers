import json

# Charger les données
with open('rulli_stats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

player_data = data['data']
stats = player_data.get('statistics', [])

print(f"Joueur: {player_data.get('display_name')}")

# Chercher les saisons les plus récentes avec has_values=True
recent_seasons = []

for stat in stats:
    if stat.get('has_values', False):
        details = stat.get('details', [])
        if isinstance(details, list) and len(details) > 0:
            detail = details[0]
        elif isinstance(details, dict):
            detail = details
        else:
            continue
            
        # Vérifier qu'il y a vraiment des stats
        if detail and (detail.get('minutes', 0) > 0 or detail.get('appearences', 0) > 0):
            season_info = {
                'season_id': stat.get('season_id'),
                'team_id': stat.get('team_id'),
                'stats': detail
            }
            recent_seasons.append(season_info)

# Trier par season_id décroissant
recent_seasons.sort(key=lambda x: x['season_id'], reverse=True)

print(f"\nSaisons récentes avec vraies stats: {len(recent_seasons)}")

# Afficher la saison la plus récente avec des stats complètes
if recent_seasons:
    latest = recent_seasons[0]
    print(f"\n=== Saison la plus récente (Season ID: {latest['season_id']}, Team ID: {latest['team_id']}) ===")
    
    stats_detail = latest['stats']
    print("\nStatistiques détaillées:")
    
    # Afficher toutes les stats disponibles
    important_stats = [
        'minutes', 'appearences', 'lineups', 'captain',
        'saves', 'inside_box_saves', 'clean_sheets', 'goals_conceded',
        'penalties_saved', 'penalties_committed', 'mistakes_leading_to_goals',
        'rating', 'yellow_cards', 'red_cards', 'yellowred_cards',
        'passes', 'passes_accuracy', 'passes_total'
    ]
    
    for key in important_stats:
        if key in stats_detail:
            value = stats_detail[key]
            if value is not None:
                print(f"  {key}: {value}")
    
    # Sauvegarder un exemple de stats pour utiliser comme modèle
    example_stats = {
        "2024/2025": stats_detail
    }
    
    with open('example_goalkeeper_stats.json', 'w', encoding='utf-8') as f:
        json.dump(example_stats, f, indent=2, ensure_ascii=False)
    print("\nExemple de stats sauvegardé dans example_goalkeeper_stats.json")