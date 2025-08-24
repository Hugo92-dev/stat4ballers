import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données corrigées
with open('om_stats_fixed.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# ID de Mason Greenwood
greenwood_id = '20333643'

if greenwood_id in data:
    greenwood = data[greenwood_id]
    
    print(f"=== {greenwood['displayName']} - Stats Corrigées ===\n")
    print(f"Position: {greenwood['position']}")
    print(f"Numéro: {greenwood.get('jersey', 'N/A')}")
    print("\n" + "="*50 + "\n")
    
    # Afficher les saisons principales
    seasons_to_check = ['2025/2026', '2024/2025', '2023/2024']
    
    for season in seasons_to_check:
        if season in greenwood['stats']:
            stats = greenwood['stats'][season]
            print(f"📅 Saison {season}:")
            print(f"   Matchs: {int(stats.get('appearences', 0))}")
            print(f"   Buts: {int(stats.get('goals', 0))}")
            print(f"   Passes décisives: {int(stats.get('assists', 0))}")
            print(f"   Minutes: {int(stats.get('minutes', 0))}")
            
            # Vérifier s'il y a des valeurs non-nulles
            non_zero_stats = {k: v for k, v in stats.items() if v and v != 0}
            print(f"   Stats non-nulles: {len(non_zero_stats)}/{len(stats)}")
            
            # Afficher quelques stats importantes
            if stats.get('xg'):
                print(f"   xG: {stats.get('xg', 0):.2f}")
            if stats.get('shots'):
                print(f"   Tirs: {int(stats.get('shots', 0))}")
            if stats.get('rating'):
                print(f"   Note moyenne: {stats.get('rating', 0):.2f}")
            
            print()
    
    # Vérifier spécifiquement la saison 2024/2025
    print("\n" + "="*50)
    print("✅ VÉRIFICATION FINALE:")
    print("="*50)
    
    if '2024/2025' in greenwood['stats']:
        s2425 = greenwood['stats']['2024/2025']
        print(f"\n🎯 Saison 2024/2025 (celle avec 21 buts):")
        print(f"   - Buts: {int(s2425.get('goals', 0))} {'✅' if s2425.get('goals', 0) == 21 else '❌'}")
        print(f"   - Matchs: {int(s2425.get('appearences', 0))}")
        print(f"   - Passes: {int(s2425.get('assists', 0))}")
    else:
        print("❌ Saison 2024/2025 non trouvée!")
    
    if '2023/2024' in greenwood['stats']:
        s2324 = greenwood['stats']['2023/2024']
        print(f"\n🎯 Saison 2023/2024 (Getafe, 8 buts):")
        print(f"   - Buts: {int(s2324.get('goals', 0))} {'✅' if s2324.get('goals', 0) == 8 else '❌'}")
        print(f"   - Matchs: {int(s2324.get('appearences', 0))}")
    else:
        print("❌ Saison 2023/2024 non trouvée!")
        
else:
    print(f"❌ Mason Greenwood (ID: {greenwood_id}) non trouvé dans les données!")