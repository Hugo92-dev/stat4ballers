import json
import sys
import re

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

def identify_season_year(season_id, team_id, matches, goals, player_name):
    """
    Identifie l'année de la saison basé sur les indices disponibles
    """
    # Mapping manuel basé sur notre analyse
    # Pour Mason Greenwood spécifiquement
    if player_name == "Mason Greenwood":
        if season_id == "Season_23643" and matches >= 30 and goals >= 20:
            return "2024/2025"  # Saison avec 21 buts à l'OM
        elif season_id == "Season_21694" and matches >= 30 and goals >= 5:
            return "2023/2024"  # Saison à Getafe avec 8 buts
        elif season_id == "Season_24893":
            return "2025/2026"  # Saison actuelle (quelques matchs)
        elif season_id == "Season_25651":
            return "2025/2026"  # Saison actuelle alternative
    
    # Mapping général pour l'OM (team_id = 44)
    if team_id == 44:
        # Saisons avec beaucoup de matchs = saisons complètes
        if matches >= 25:
            if season_id == "Season_23643":
                return "2024/2025"
            elif season_id == "Season_21792":
                return "2023/2024"
            elif season_id == "Season_19735":
                return "2022/2023"
        # Saisons en cours
        elif matches < 10:
            if season_id in ["Season_24893", "Season_25651"]:
                return "2025/2026"
    
    # Retourner l'ID original si on ne peut pas identifier
    return season_id

def fix_om_stats():
    """Corrige le mapping des saisons dans les stats de l'OM"""
    
    print("Chargement des données existantes...")
    with open('om_complete_stats.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Nombre de joueurs: {len(data)}\n")
    
    # Nouveau dictionnaire avec les saisons corrigées
    fixed_data = {}
    
    # Statistiques de correction
    seasons_fixed = 0
    players_with_fixes = 0
    
    for player_id, player_data in data.items():
        player_name = player_data.get('displayName', player_data.get('name', 'Unknown'))
        fixed_player = {
            'id': player_data['id'],
            'name': player_data['name'],
            'displayName': player_data.get('displayName'),
            'position': player_data['position'],
            'jersey': player_data.get('jersey'),
            'stats': {}
        }
        
        player_had_fixes = False
        
        # Traiter chaque saison
        for season_id, stats in player_data.get('stats', {}).items():
            # Extraire les infos clés
            matches = stats.get('appearences', 0)
            goals = stats.get('goals', 0)
            
            # Identifier la bonne année
            if matches > 0:  # Seulement pour les saisons avec des matchs
                # Assumer que c'est l'OM (team_id = 44) pour toutes les stats
                correct_year = identify_season_year(season_id, 44, matches, goals, player_name)
                
                if correct_year != season_id:
                    seasons_fixed += 1
                    player_had_fixes = True
                    
                    if player_name == "Mason Greenwood":
                        print(f"  {player_name}: {season_id} -> {correct_year} ({matches} matchs, {goals} buts)")
                
                # Éviter les doublons - garder la saison avec le plus de matchs
                if correct_year in fixed_player['stats']:
                    existing_matches = fixed_player['stats'][correct_year].get('appearences', 0)
                    if matches > existing_matches:
                        fixed_player['stats'][correct_year] = stats
                else:
                    fixed_player['stats'][correct_year] = stats
        
        if player_had_fixes:
            players_with_fixes += 1
        
        fixed_data[player_id] = fixed_player
    
    print(f"\n✅ Corrections appliquées:")
    print(f"  - {seasons_fixed} saisons corrigées")
    print(f"  - {players_with_fixes} joueurs affectés")
    
    # Sauvegarder les données corrigées
    with open('om_stats_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Données sauvegardées dans om_stats_fixed.json")
    
    # Créer le fichier TypeScript
    create_typescript_file(fixed_data)

def create_typescript_file(all_stats):
    """Crée un fichier TypeScript avec les stats corrigées"""
    
    ts_content = """// Stats réelles des joueurs de l'OM depuis SportMonks API
// Généré automatiquement - CORRIGÉ avec le bon mapping des saisons

export interface PlayerSeasonStats {
  // Général
  rating: number;
  minutes: number;
  appearences: number;
  lineups: number;
  captain: number;
  substitutions: number;
  touches: number;
  saves: number;
  punches: number;
  
  // Offensif
  goals: number;
  assists: number;
  shots: number;
  shots_on_target: number;
  xg: number;
  xa: number;
  offsides: number;
  penalties: number;
  penalties_scored: number;
  penalties_missed: number;
  hit_woodwork: number;
  
  // Défensif
  tackles: number;
  blocks: number;
  interceptions: number;
  clearances: number;
  aerial_duels: number;
  aerial_duels_won: number;
  ground_duels: number;
  ground_duels_won: number;
  fouls: number;
  fouls_drawn: number;
  yellow_cards: number;
  red_cards: number;
  clean_sheets: number;
  goals_conceded: number;
  
  // Créatif
  passes: number;
  passes_completed: number;
  passes_accuracy: number;
  key_passes: number;
  crosses: number;
  crosses_accurate: number;
  long_balls: number;
  long_balls_accurate: number;
  through_balls: number;
  through_balls_accurate: number;
  dribbles: number;
  dribbles_successful: number;
  progressive_carries: number;
  big_chances_created: number;
}

export interface PlayerRealStats {
  id: number;
  name: string;
  displayName?: string;
  position: string;
  jersey?: number;
  stats: {
    [season: string]: PlayerSeasonStats;
  };
}

export const omPlayersRealStats: { [playerId: number]: PlayerRealStats } = """
    
    ts_content += json.dumps(all_stats, indent=2, ensure_ascii=False)
    ts_content += ";\n"
    
    # Sauvegarder
    with open('../data/omPlayersRealStatsFixed.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript créé: data/omPlayersRealStatsFixed.ts")

if __name__ == "__main__":
    print("🚀 Correction du mapping des saisons...\n")
    fix_om_stats()
    
    # Vérifier spécifiquement Mason Greenwood
    print("\n=== Vérification de Mason Greenwood ===")
    with open('om_stats_fixed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    greenwood = data.get('20333643')
    if greenwood:
        print(f"Nom: {greenwood['displayName']}")
        print(f"Saisons disponibles: {list(greenwood['stats'].keys())}")
        
        for season, stats in greenwood['stats'].items():
            if '2024' in season or '2025' in season:
                print(f"\n{season}:")
                print(f"  Matchs: {stats.get('appearences', 0)}")
                print(f"  Buts: {stats.get('goals', 0)}")
                print(f"  Passes: {stats.get('assists', 0)}")