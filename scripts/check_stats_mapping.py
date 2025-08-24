import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Vérifier Rulli
rulli = data.get('186418', {})
stats_2024 = rulli.get('stats', {}).get('2024/2025 (Ligue 1, Olympique Marseille)', {})

print("CLÉS DISPONIBLES DANS LES STATS DE RULLI 2024/2025:")
print("=" * 60)
for key in sorted(stats_2024.keys()):
    value = stats_2024[key]
    print(f"  {key:30} : {value}")

print("\n" + "=" * 60)
print("MAPPING ATTENDU DANS L'INTERFACE:")
print("=" * 60)

# Ce qui est attendu dans StatsCards.tsx
expected_fields = [
    # Général
    "rating", "minutes", "lineups", "appearences", "captain", "touches", "passes_accuracy",
    # Gardien
    "saves", "inside_box_saves", "penalties_saved", "clean_sheets", "goals_conceded",
    # Passes
    "passes_total", "key_passes", "crosses_total", "crosses_accuracy",
    # Défense
    "ball_recoveries", "tackles", "interceptions", "duels", "duels_won", 
    "aerial_duels", "aerial_duels_won",
    # Discipline
    "fouls", "fouls_drawn", "yellow_cards", "red_cards", "yellowred_cards",
    "penalties_committed", "mistakes_leading_to_goals"
]

print("\nCHAMPS MANQUANTS:")
for field in expected_fields:
    if field not in stats_2024:
        print(f"  ❌ {field}")

print("\nCHAMPS EN TROP (non utilisés):")
for key in stats_2024.keys():
    if key not in expected_fields and key not in ["team", "team_id", "league"]:
        print(f"  ⚠️ {key}")

# Vérifier un joueur de champ aussi
greenwood = data.get('20333643', {})
if greenwood:
    stats_greenwood = greenwood.get('stats', {}).get('2024/2025 (Ligue 1, Olympique Marseille)', {})
    
    print("\n" + "=" * 60)
    print("EXEMPLE JOUEUR DE CHAMP (Greenwood):")
    print("=" * 60)
    
    offensive_fields = ["goals", "assists", "expected_goals", "expected_assists", "shots", 
                       "shots_on_target", "penalties", "penalties_scored", "hit_woodwork", "offsides"]
    
    for field in offensive_fields:
        value = stats_greenwood.get(field, "NON TROUVÉ")
        print(f"  {field:25} : {value}")