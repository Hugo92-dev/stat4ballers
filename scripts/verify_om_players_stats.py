import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données complètes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("VÉRIFICATION DES STATS DE TOUS LES JOUEURS DE L'OM")
print("=" * 80)

# Statistiques globales
total_players = len(data)
players_with_multiple_clubs = 0
total_seasons = 0
total_stats_available = 0
total_stats_null = 0

# Analyser chaque joueur
for player_id, player_data in data.items():
    player_name = player_data.get('displayName', player_data.get('name'))
    position = player_data.get('position')
    
    # Compter les clubs différents
    clubs = set()
    seasons_count = 0
    
    for season_key, stats in player_data['stats'].items():
        if stats and stats.get('appearences', 0) and stats.get('appearences', 0) > 0:
            seasons_count += 1
            if 'team' in stats:
                clubs.add(stats['team'])
            
            # Compter les stats disponibles
            for key, value in stats.items():
                if key not in ['team', 'team_id', 'league']:
                    if value is not None:
                        total_stats_available += 1
                    else:
                        total_stats_null += 1
    
    total_seasons += seasons_count
    
    if len(clubs) > 1:
        players_with_multiple_clubs += 1

# Afficher quelques exemples détaillés
print("\n📊 EXEMPLES DÉTAILLÉS DE JOUEURS:\n")

# Joueurs à analyser en détail
sample_players = [
    '95776',   # Neal Maupay
    '96691',   # Amine Harit
    '608285',  # Angel Gomes
    '186418',  # Rulli (gardien)
]

for player_id in sample_players:
    if player_id in data:
        player = data[player_id]
        print(f"\n{'='*60}")
        print(f"👤 {player['displayName']} ({player['position']})")
        print(f"{'='*60}")
        
        for season_key, stats in player['stats'].items():
            if stats and stats.get('appearences', 0) and stats.get('appearences', 0) > 0:
                print(f"\n📅 {season_key}")
                
                # Stats principales
                print(f"  ⚽ Performance:")
                print(f"     - Matchs: {stats.get('appearences', 'N/A')}")
                print(f"     - Minutes: {stats.get('minutes', 'N/A')}")
                print(f"     - Note: {stats.get('rating', 'N/A')}")
                print(f"     - Buts: {stats.get('goals', 'N/A')}")
                print(f"     - Passes déc.: {stats.get('assists', 'N/A')}")
                
                # Pour les gardiens
                if player['position'] == 'GK':
                    print(f"  🥅 Stats Gardien:")
                    print(f"     - Arrêts: {stats.get('saves', 'N/A')}")
                    print(f"     - Clean sheets: {stats.get('clean_sheets', 'N/A')}")
                    print(f"     - Buts encaissés: {stats.get('goals_conceded', 'N/A')}")
                
                # Compter les stats disponibles
                non_null = sum(1 for k, v in stats.items() if v is not None and k not in ['team', 'team_id', 'league'])
                total = len([k for k in stats.keys() if k not in ['team', 'team_id', 'league']])
                print(f"  📊 Complétude: {non_null}/{total} stats ({non_null/total*100:.1f}%)")

print("\n" + "=" * 80)
print("RÉSUMÉ GLOBAL")
print("=" * 80)

print(f"\n✅ Statistiques générales:")
print(f"  - Total joueurs OM: {total_players}")
print(f"  - Joueurs avec plusieurs clubs: {players_with_multiple_clubs}")
print(f"  - Total saisons analysées: {total_seasons}")
print(f"  - Moyenne saisons/joueur: {total_seasons/total_players:.1f}")

print(f"\n📊 Qualité des données:")
print(f"  - Stats avec valeurs: {total_stats_available}")
print(f"  - Stats manquantes (N/A): {total_stats_null}")
print(f"  - Taux de complétude: {total_stats_available/(total_stats_available+total_stats_null)*100:.1f}%")

# Vérifier spécifiquement les penalties et autres stats importantes
print(f"\n🎯 Vérification des stats clés sur l'équipe:")
players_with_goals = 0
players_with_penalties = 0
players_with_xg = 0
players_with_dribbles = 0

for player_id, player_data in data.items():
    for season_key, stats in player_data['stats'].items():
        if stats and stats.get('appearences', 0) and stats.get('appearences', 0) > 0:
            if stats.get('goals', 0) > 0:
                players_with_goals += 1
                break
                
for player_id, player_data in data.items():
    for season_key, stats in player_data['stats'].items():
        if stats and stats.get('appearences', 0) and stats.get('appearences', 0) > 0:
            if stats.get('penalties_won', 0) > 0:
                players_with_penalties += 1
                break
                
for player_id, player_data in data.items():
    for season_key, stats in player_data['stats'].items():
        if stats and stats.get('appearences', 0) and stats.get('appearences', 0) > 0:
            if stats.get('xg') is not None:
                players_with_xg += 1
                break
                
for player_id, player_data in data.items():
    for season_key, stats in player_data['stats'].items():
        if stats and stats.get('appearences', 0) and stats.get('appearences', 0) > 0:
            if stats.get('dribbles', 0) > 0:
                players_with_dribbles += 1
                break

print(f"  - Joueurs avec buts: {players_with_goals}/{total_players}")
print(f"  - Joueurs avec penalties: {players_with_penalties}/{total_players}")
print(f"  - Joueurs avec xG: {players_with_xg}/{total_players}")
print(f"  - Joueurs avec dribbles: {players_with_dribbles}/{total_players}")

print("\n✅ Les données sont prêtes pour être utilisées sur le site!")