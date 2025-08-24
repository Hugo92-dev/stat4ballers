import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données complètes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

greenwood = data.get('20333643')

if greenwood:
    print("=" * 80)
    print("VÉRIFICATION COMPLÈTE DES STATS DE MASON GREENWOOD")
    print("=" * 80)
    
    # Stats à vérifier selon les nouvelles cartes
    stats_categories = {
        "Carte Générale": [
            'rating', 'minutes', 'lineups', 'appearences', 'captain', 
            'touches', 'shots', 'shots_on_target', 'passes', 'passes_completed', 'passes_accuracy'
        ],
        "Carte Offensive": [
            'goals', 'xg', 'assists', 'xa', 'shots', 'penalties_won', 
            'penalties_scored', 'penalties_missed', 'hit_woodwork', 'offsides'
        ],
        "Carte Créative": [
            'passes', 'key_passes', 'crosses', 'crosses_accurate', 
            'dribbles', 'dribbles_successful'
        ],
        "Carte Défensive": [
            'tackles', 'interceptions', 'ground_duels', 'ground_duels_won',
            'aerial_duels', 'aerial_duels_won', 'fouls', 'fouls_drawn',
            'yellow_cards', 'red_cards'
        ]
    }
    
    # Analyser chaque saison
    for season_key in sorted(greenwood['stats'].keys(), reverse=True):
        stats = greenwood['stats'][season_key]
        
        # Ne montrer que les saisons avec des matchs
        if stats.get('appearences', 0) > 0:
            print(f"\n{'='*60}")
            print(f"📅 {season_key}")
            print(f"{'='*60}")
            
            for category, stat_names in stats_categories.items():
                print(f"\n{category}:")
                print("-" * 40)
                
                for stat_name in stat_names:
                    value = stats.get(stat_name)
                    
                    # Calculer les pourcentages si nécessaire
                    if stat_name == 'shots' and category == "Carte Générale":
                        # Précision des tirs
                        if value and value > 0:
                            on_target = stats.get('shots_on_target', 0)
                            accuracy = (on_target / value * 100) if on_target else 0
                            print(f"  Précision des tirs: {accuracy:.1f}%")
                    elif stat_name == 'passes' and category == "Carte Générale":
                        # Précision des passes
                        if value and value > 0:
                            completed = stats.get('passes_completed', 0)
                            accuracy = stats.get('passes_accuracy')
                            if accuracy:
                                print(f"  Précision des passes: {accuracy:.1f}%")
                            elif completed:
                                accuracy = (completed / value * 100)
                                print(f"  Précision des passes: {accuracy:.1f}%")
                    elif stat_name == 'crosses' and category == "Carte Créative":
                        # Précision des centres
                        if value and value > 0:
                            accurate = stats.get('crosses_accurate', 0)
                            accuracy = (accurate / value * 100) if accurate else 0
                            print(f"  Précision des centres: {accuracy:.1f}%")
                    elif stat_name == 'dribbles' and category == "Carte Créative":
                        # Précision des dribbles
                        if value and value > 0:
                            successful = stats.get('dribbles_successful', 0)
                            accuracy = (successful / value * 100) if successful else 0
                            print(f"  Précision des dribbles: {accuracy:.1f}%")
                    elif stat_name == 'penalties_won' and category == "Carte Offensive":
                        # Précision des penalties
                        if value and value > 0:
                            scored = stats.get('penalties_scored', 0) or 0
                            accuracy = (scored / value * 100) if scored else 0
                            print(f"  Précision des penalties: {accuracy:.1f}%")
                    else:
                        # Afficher la valeur normale
                        if value is not None:
                            if value == 0:
                                print(f"  {stat_name}: 0 (vraie valeur)")
                            else:
                                print(f"  {stat_name}: {value}")
                        else:
                            print(f"  {stat_name}: N/A (pas de donnée)")
    
    # Résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ:")
    print("=" * 80)
    
    for season_key in sorted(greenwood['stats'].keys(), reverse=True):
        stats = greenwood['stats'][season_key]
        if stats.get('appearences', 0) > 0:
            print(f"\n{season_key}:")
            
            # Compter les stats disponibles
            total_stats = len(stats)
            non_null = sum(1 for v in stats.values() if v is not None)
            zeros = sum(1 for v in stats.values() if v == 0)
            nulls = sum(1 for v in stats.values() if v is None)
            
            print(f"  - Total de stats: {total_stats}")
            print(f"  - Avec valeurs non-null: {non_null} ({non_null/total_stats*100:.1f}%)")
            print(f"  - Valeurs = 0: {zeros}")
            print(f"  - Valeurs = N/A: {nulls}")
            
            # Stats clés
            print(f"  - Buts: {stats.get('goals', 'N/A')}")
            print(f"  - Penalties gagnés: {stats.get('penalties_won', 'N/A')}")
            print(f"  - xG: {stats.get('xg', 'N/A')}")
            print(f"  - Dribbles: {stats.get('dribbles', 'N/A')}")
            
else:
    print("❌ Mason Greenwood non trouvé dans les données!")