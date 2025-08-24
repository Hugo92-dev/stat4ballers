import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données
with open('om_complete_stats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Récupérer les stats de Greenwood avec le bon ID
greenwood = data.get('20333643')

if greenwood:
    print(f"=== Stats de {greenwood['displayName']} ===\n")
    print(f"Position: {greenwood['position']}")
    print(f"Numéro: {greenwood.get('jersey', 'N/A')}\n")
    
    print("Toutes les saisons avec stats:\n")
    
    # Parcourir toutes les saisons
    for season_name, stats in greenwood['stats'].items():
        # Chercher les stats importantes
        apps = stats.get('appearences', 0)
        goals = stats.get('goals', 0)
        assists = stats.get('assists', 0)
        minutes = stats.get('minutes', 0)
        xg = stats.get('xg', 0)
        shots = stats.get('shots', 0)
        
        # Afficher toutes les saisons avec des matchs
        if apps > 0:
            print(f"{season_name}:")
            print(f"  Matchs: {int(apps)}")
            print(f"  Buts: {int(goals)}")
            print(f"  Passes décisives: {int(assists)}")
            print(f"  Minutes: {int(minutes)}")
            if xg > 0:
                print(f"  xG: {xg:.2f}")
            if shots > 0:
                print(f"  Tirs: {int(shots)}")
            
            # Si c'est une saison importante
            if goals > 10:
                print(f"  >>> SAISON IMPORTANTE - {int(goals)} buts! <<<")
            
            print()
    
    # Chercher spécifiquement la saison avec 21 buts
    print("\n=== Recherche de la saison avec 20+ buts ===")
    for season_name, stats in greenwood['stats'].items():
        if stats.get('goals', 0) >= 20:
            print(f"\n✅ TROUVÉ! Saison {season_name}:")
            print(f"  Buts: {int(stats.get('goals'))}")
            print(f"  Matchs: {int(stats.get('appearences'))}")
            print(f"  Passes décisives: {int(stats.get('assists'))}")
            print(f"  Minutes: {int(stats.get('minutes'))}")
            print(f"  xG: {stats.get('xg', 0):.2f}")
            print(f"  Tirs: {int(stats.get('shots', 0))}")
            print(f"  Tirs cadrés: {int(stats.get('shots_on_target', 0))}")
            print(f"  Rating: {stats.get('rating', 0)}")
else:
    print("Greenwood (ID: 20333643) non trouvé dans les données")