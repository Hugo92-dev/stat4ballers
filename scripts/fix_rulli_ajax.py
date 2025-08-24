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
    
    print("Correction des données de Rulli...")
    print("Avant:", list(rulli['stats'].keys()))
    
    # Supprimer les fausses données de Villarreal
    if "2023/2024 (Liga, Villarreal)" in rulli['stats']:
        del rulli['stats']["2023/2024 (Liga, Villarreal)"]
    
    # Ajouter une entrée null pour Ajax (hors de notre périmètre)
    # On ne met pas de données car Ajax n'est pas dans nos championnats
    # L'utilisateur comprendra que les données ne sont pas disponibles
    
    print("Après:", list(rulli['stats'].keys()))
    
    # Sauvegarder
    with open('om_complete_stats_v2.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Données corrigées!")
    print("  - Supprimé: fausses données de Villarreal 2023/2024")
    print("  - Rulli était à l'Ajax Amsterdam en 2023/2024 (Eredivisie - non couvert)")
    print("  - Les stats 2025/2026 et 2024/2025 à l'OM sont conservées")
else:
    print("❌ Rulli non trouvé dans les données")