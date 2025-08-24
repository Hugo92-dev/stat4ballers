import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données originales
with open('om_complete_stats.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

# Analyser Mason Greenwood spécifiquement
greenwood_id = '20333643'
greenwood = raw_data.get(greenwood_id)

if greenwood:
    print("=== Analyse des stats disponibles pour Mason Greenwood ===\n")
    
    # Regarder la saison 2024/25 (Season_23643)
    season_23643 = None
    for season_key, stats in greenwood['stats'].items():
        if 'Season_23643' in season_key:
            season_23643 = stats
            break
    
    if season_23643:
        print("Saison 2024/25 (21 buts) - Stats disponibles vs manquantes:\n")
        
        # Catégoriser les stats
        categories = {
            'Général': ['rating', 'minutes', 'appearences', 'lineups', 'captain', 'substitutions', 'touches'],
            'Gardien': ['saves', 'punches', 'clean_sheets', 'goals_conceded'],
            'Offensif': ['goals', 'assists', 'shots', 'shots_on_target', 'xg', 'xa', 'offsides', 'penalties', 'penalties_scored', 'penalties_missed', 'hit_woodwork'],
            'Défensif': ['tackles', 'blocks', 'interceptions', 'clearances', 'aerial_duels', 'aerial_duels_won', 'ground_duels', 'ground_duels_won', 'fouls', 'fouls_drawn', 'yellow_cards', 'red_cards'],
            'Créatif': ['passes', 'passes_completed', 'passes_accuracy', 'key_passes', 'crosses', 'crosses_accurate', 'long_balls', 'long_balls_accurate', 'through_balls', 'through_balls_accurate', 'dribbles', 'dribbles_successful', 'progressive_carries', 'big_chances_created']
        }
        
        for category, stat_names in categories.items():
            print(f"\n{category}:")
            available = []
            missing = []
            
            for stat in stat_names:
                value = season_23643.get(stat, 0)
                if value != 0:
                    available.append(f"{stat}={value}")
                else:
                    missing.append(stat)
            
            if available:
                print(f"  ✅ Disponibles: {', '.join(available[:5])}")
                if len(available) > 5:
                    print(f"      ... et {len(available)-5} autres")
            
            if missing:
                print(f"  ❌ Manquantes (affichées comme 0): {', '.join(missing[:10])}")
                if len(missing) > 10:
                    print(f"      ... et {len(missing)-10} autres")

# Analyser tous les joueurs pour voir quelles stats sont généralement disponibles
print("\n\n=== Stats généralement disponibles pour TOUS les joueurs ===\n")

all_stats_count = {}
total_players = 0

for player_id, player_data in raw_data.items():
    for season_key, season_stats in player_data.get('stats', {}).items():
        if season_stats.get('appearences', 0) > 0:  # Seulement les saisons avec des matchs
            total_players += 1
            for stat_key, stat_value in season_stats.items():
                if stat_value and stat_value != 0:
                    if stat_key not in all_stats_count:
                        all_stats_count[stat_key] = 0
                    all_stats_count[stat_key] += 1

# Trier par fréquence
sorted_stats = sorted(all_stats_count.items(), key=lambda x: x[1], reverse=True)

print(f"Total de joueurs-saisons analysés: {total_players}\n")
print("Stats les plus fréquentes:")
for stat, count in sorted_stats[:20]:
    percentage = (count / total_players) * 100
    print(f"  {stat}: {count}/{total_players} ({percentage:.1f}%)")

print("\n\nStats rarement disponibles (< 10% des joueurs):")
rare_stats = [s for s, c in sorted_stats if (c/total_players) < 0.1]
print(f"  {', '.join(rare_stats[:15])}")
if len(rare_stats) > 15:
    print(f"  ... et {len(rare_stats)-15} autres")