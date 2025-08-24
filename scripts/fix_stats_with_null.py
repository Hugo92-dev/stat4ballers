import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

def identify_season_year(season_id, matches, goals, player_name):
    """Identifie l'année de la saison basé sur les indices disponibles"""
    
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
    
    # Mapping général pour l'OM
    if matches >= 25:
        if season_id == "Season_23643":
            return "2024/2025"
        elif season_id == "Season_21792":
            return "2023/2024"
        elif season_id == "Season_19735":
            return "2022/2023"
    elif matches < 10:
        if season_id in ["Season_24893", "Season_25651"]:
            return "2025/2026"
    
    return season_id

def map_stats_from_existing(existing_stats):
    """Convertit les stats existantes en remplaçant les 0 par null"""
    
    # Créer un nouveau dictionnaire avec null pour les valeurs 0
    stats = {}
    
    # Parcourir toutes les stats existantes
    for key, value in existing_stats.items():
        # Remplacer 0 par null, garder les autres valeurs
        if value == 0:
            stats[key] = None
        else:
            stats[key] = value
    
    return stats

def fix_om_stats():
    """Corrige le mapping des saisons et les valeurs null"""
    
    print("Chargement des données originales...")
    with open('om_complete_stats.json', 'r', encoding='utf-8') as f:
        raw_data = json.load(f)
    
    print(f"Nombre de joueurs: {len(raw_data)}\n")
    
    # Nouveau dictionnaire avec les saisons corrigées
    fixed_data = {}
    
    for player_id, player_data in raw_data.items():
        player_name = player_data.get('displayName', player_data.get('name', 'Unknown'))
        
        fixed_player = {
            'id': player_data['id'],
            'name': player_data['name'],
            'displayName': player_data.get('displayName'),
            'position': player_data['position'],
            'jersey': player_data.get('jersey'),
            'stats': {}
        }
        
        # Traiter chaque saison
        for season_id, stat_data in player_data.get('stats', {}).items():
            # Re-mapper les stats avec null au lieu de 0
            mapped_stats = map_stats_from_existing(stat_data)
            
            # Identifier la bonne année
            matches = mapped_stats.get('appearences') or 0
            goals = mapped_stats.get('goals') or 0
            
            if matches > 0:  # Seulement pour les saisons avec des matchs
                correct_year = identify_season_year(season_id, matches, goals, player_name)
                
                if player_name == "Mason Greenwood" and goals > 10:
                    print(f"  {player_name}: {season_id} -> {correct_year} ({matches} matchs, {goals} buts)")
                
                # Éviter les doublons
                if correct_year in fixed_player['stats']:
                    existing_matches = fixed_player['stats'][correct_year].get('appearences', 0) or 0
                    if matches > existing_matches:
                        fixed_player['stats'][correct_year] = mapped_stats
                else:
                    fixed_player['stats'][correct_year] = mapped_stats
        
        fixed_data[player_id] = fixed_player
    
    # Sauvegarder les données corrigées
    with open('om_stats_null_fixed.json', 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Données sauvegardées dans om_stats_null_fixed.json")
    
    # Créer le fichier TypeScript
    create_typescript_file(fixed_data)

def create_typescript_file(all_stats):
    """Crée un fichier TypeScript avec les stats corrigées"""
    
    ts_content = """// Stats réelles des joueurs de l'OM depuis SportMonks API
// Généré automatiquement - Version avec null pour les valeurs manquantes

export interface PlayerSeasonStats {
  // Général
  rating: number | null;
  minutes: number | null;
  appearences: number | null;
  lineups: number | null;
  captain: number | null;
  substitutions: number | null;
  touches: number | null;
  saves: number | null;
  punches: number | null;
  
  // Offensif
  goals: number | null;
  assists: number | null;
  shots: number | null;
  shots_on_target: number | null;
  xg: number | null;
  xa: number | null;
  offsides: number | null;
  penalties: number | null;
  penalties_scored: number | null;
  penalties_missed: number | null;
  hit_woodwork: number | null;
  
  // Défensif
  tackles: number | null;
  blocks: number | null;
  interceptions: number | null;
  clearances: number | null;
  aerial_duels: number | null;
  aerial_duels_won: number | null;
  ground_duels: number | null;
  ground_duels_won: number | null;
  fouls: number | null;
  fouls_drawn: number | null;
  yellow_cards: number | null;
  red_cards: number | null;
  clean_sheets: number | null;
  goals_conceded: number | null;
  
  // Créatif
  passes: number | null;
  passes_completed: number | null;
  passes_accuracy: number | null;
  key_passes: number | null;
  crosses: number | null;
  crosses_accurate: number | null;
  long_balls: number | null;
  long_balls_accurate: number | null;
  through_balls: number | null;
  through_balls_accurate: number | null;
  dribbles: number | null;
  dribbles_successful: number | null;
  progressive_carries: number | null;
  big_chances_created: number | null;
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
    with open('../data/omPlayersRealStatsNull.ts', 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print("✅ Fichier TypeScript créé: data/omPlayersRealStatsNull.ts")

if __name__ == "__main__":
    print("🚀 Correction des stats avec null pour les valeurs manquantes...\n")
    fix_om_stats()
    
    # Vérifier Mason Greenwood
    print("\n=== Vérification de Mason Greenwood ===")
    with open('om_stats_null_fixed.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    greenwood = data.get('20333643')
    if greenwood and '2024/2025' in greenwood['stats']:
        stats = greenwood['stats']['2024/2025']
        print(f"\nSaison 2024/2025:")
        print(f"  Buts: {stats.get('goals')}")
        print(f"  xG: {stats.get('xg')}")
        print(f"  Dribbles: {stats.get('dribbles')}")
        print(f"  Through balls: {stats.get('through_balls')}")
        print("\nStats avec valeurs null (au lieu de 0):")
        null_stats = [k for k, v in stats.items() if v is None]
        print(f"  {', '.join(null_stats[:10])}")
        if len(null_stats) > 10:
            print(f"  ... et {len(null_stats)-10} autres")