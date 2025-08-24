import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données
with open('om_complete_stats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Récupérer les stats de Greenwood
greenwood = data.get('28575687')

if greenwood:
    print(f"=== Stats de {greenwood['displayName']} ===\n")
    print(f"Position: {greenwood['position']}")
    print(f"Numéro: {greenwood.get('jersey', 'N/A')}\n")
    
    print("Saisons avec stats:\n")
    
    # Parcourir toutes les saisons
    for season_name, stats in greenwood['stats'].items():
        # Chercher les stats importantes
        apps = stats.get('appearences', 0)
        goals = stats.get('goals', 0)
        assists = stats.get('assists', 0)
        minutes = stats.get('minutes', 0)
        
        # Afficher seulement les saisons avec des matchs
        if apps > 0:
            print(f"{season_name}:")
            print(f"  Matchs: {int(apps)}")
            print(f"  Buts: {int(goals)}")
            print(f"  Passes décisives: {int(assists)}")
            print(f"  Minutes: {int(minutes)}")
            
            # Si c'est une saison importante
            if goals > 5:
                print(f"  >>> SAISON IMPORTANTE - {goals} buts! <<<")
            
            print()
    
    # Chercher spécifiquement la saison avec 21 buts
    print("\nRecherche de la saison avec 21 buts...")
    for season_name, stats in greenwood['stats'].items():
        if stats.get('goals', 0) >= 20:
            print(f"TROUVÉ! Saison {season_name}: {stats.get('goals')} buts")
            print(f"  Matchs: {stats.get('appearences')}")
            print(f"  Minutes: {stats.get('minutes')}")
            print(f"  xG: {stats.get('xg', 0)}")
            print(f"  Tirs: {stats.get('shots', 0)}")
            print(f"  Tirs cadrés: {stats.get('shots_on_target', 0)}")
else:
    print("Greenwood non trouvé dans les données")