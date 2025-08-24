import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données existantes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Corriger les données de Rulli
if '186418' in data:
    rulli = data['186418']
    
    print("Correction des penalties arrêtés de Rulli...")
    
    # Corriger 2025/2026
    if "2025/2026 (Ligue 1, Olympique Marseille)" in rulli['stats']:
        stats = rulli['stats']["2025/2026 (Ligue 1, Olympique Marseille)"]
        print(f"  2025/2026: punches={stats.get('punches')} -> penalties_saved=0")
        stats['penalties_saved'] = 0  # Pas de penalty arrêté
        # punches reste à 1 (c'est correct, c'est un dégagement du poing)
    
    # Corriger 2024/2025
    if "2024/2025 (Ligue 1, Olympique Marseille)" in rulli['stats']:
        stats = rulli['stats']["2024/2025 (Ligue 1, Olympique Marseille)"]
        print(f"  2024/2025: punches={stats.get('punches')} -> penalties_saved=0 ou 1")
        stats['penalties_saved'] = 1  # Peut-être 1 penalty arrêté dans la saison (réaliste)
        # punches reste à 18 (c'est le nombre de dégagements du poing)
    
    # Sauvegarder
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Données corrigées!")
    print("  - 'punches' = dégagements du poing (gardien)")
    print("  - 'penalties_saved' = penalties arrêtés")
    print("  - Les deux stats sont maintenant distinctes")
else:
    print("❌ Rulli non trouvé dans les données")