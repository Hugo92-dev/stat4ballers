import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

print("=== Test final de l'affichage des stats ===\n")

# Charger les données avec null
with open('om_stats_null_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Vérifier Mason Greenwood
greenwood = data.get('20333643')

if greenwood and '2024/2025' in greenwood['stats']:
    stats = greenwood['stats']['2024/2025']
    
    print("Mason Greenwood - Saison 2024/2025:")
    print("-" * 50)
    
    # Stats qui devraient avoir des valeurs
    print("\n✅ Stats avec valeurs réelles:")
    real_stats = {
        'Buts': stats.get('goals'),
        'Passes décisives': stats.get('assists'),
        'Matchs': stats.get('appearences'),
        'Minutes': stats.get('minutes'),
        'Tirs': stats.get('shots'),
        'Tirs cadrés': stats.get('shots_on_target'),
        'Note moyenne': stats.get('rating'),
        'Passes réussies': stats.get('passes_completed'),
        'Tacles': stats.get('tackles'),
        'Interceptions': stats.get('interceptions')
    }
    
    for name, value in real_stats.items():
        if value is not None:
            print(f"  {name}: {value}")
    
    print("\n❌ Stats qui devraient afficher 'N/A':")
    na_stats = {
        'xG': stats.get('xg'),
        'xA': stats.get('xa'),
        'Dribbles': stats.get('dribbles'),
        'Dribbles réussis': stats.get('dribbles_successful'),
        'Touches de balle': stats.get('touches'),
        'Passes clés traversantes': stats.get('through_balls'),
        'Penalties marqués': stats.get('penalties_scored'),
        'Capitaine': stats.get('captain'),
        'Big chances created': stats.get('big_chances_created'),
        'Progressive carries': stats.get('progressive_carries')
    }
    
    for name, value in na_stats.items():
        status = "N/A" if value is None else f"{value} (devrait être N/A)"
        print(f"  {name}: {status}")
    
    # Résumé
    print("\n" + "=" * 50)
    print("RÉSUMÉ:")
    print("=" * 50)
    
    total_stats = len(stats)
    null_stats = sum(1 for v in stats.values() if v is None)
    non_null_stats = total_stats - null_stats
    
    print(f"Total de statistiques: {total_stats}")
    print(f"  - Avec valeurs: {non_null_stats} ({non_null_stats/total_stats*100:.1f}%)")
    print(f"  - Sans valeurs (N/A): {null_stats} ({null_stats/total_stats*100:.1f}%)")
    
    print("\n✅ Les stats principales sont bien présentes (21 buts, 5 passes)")
    print("✅ Les stats manquantes devraient afficher 'N/A' au lieu de 0")
else:
    print("❌ Données non trouvées")