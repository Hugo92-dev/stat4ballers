import json
import sys

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

# Charger les données complètes
with open('om_complete_stats_v2.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Génération du fichier TypeScript avec {len(data)} joueurs...")

# Générer le contenu TypeScript
typescript_content = """// Stats COMPLÈTES des joueurs de l'OM depuis SportMonks API
// Inclut TOUTES les saisons dans TOUS les clubs (pas seulement l'OM)
// Généré automatiquement

export interface PlayerSeasonStats {
  // Métadonnées
  team?: string;
  team_id?: number;
  league?: string;
  
  // Stats générales
  rating?: number | null;
  minutes?: number | null;
  appearences?: number | null;
  lineups?: number | null;
  captain?: number | null;
  substitutions?: number | null;
  touches?: number | null;
  
  // Stats offensives
  goals?: number | null;
  assists?: number | null;
  xg?: number | null;
  xa?: number | null;
  shots?: number | null;
  shots_on_target?: number | null;
  penalties_won?: number | null;
  penalties?: number | null;
  penalties_scored?: number | null;
  penalties_missed?: number | null;
  hit_woodwork?: number | null;
  offsides?: number | null;
  
  // Stats de passes
  passes?: number | null;
  passes_completed?: number | null;
  passes_accuracy?: number | null;
  key_passes?: number | null;
  crosses?: number | null;
  crosses_accurate?: number | null;
  
  // Stats de dribbles
  dribbles?: number | null;
  dribbles_successful?: number | null;
  
  // Stats défensives
  tackles?: number | null;
  blocks?: number | null;
  interceptions?: number | null;
  clearances?: number | null;
  ground_duels?: number | null;
  ground_duels_won?: number | null;
  aerial_duels?: number | null;
  aerial_duels_won?: number | null;
  
  // Discipline
  fouls?: number | null;
  fouls_drawn?: number | null;
  yellow_cards?: number | null;
  red_cards?: number | null;
  yellowred_cards?: number | null;
  penalties_committed?: number | null;
  
  // Autres
  ball_losses?: number | null;
  ball_recoveries?: number | null;
  mistakes_leading_to_goals?: number | null;
  
  // Stats gardien
  saves?: number | null;
  punches?: number | null;
  inside_box_saves?: number | null;
  clean_sheets?: number | null;
  goals_conceded?: number | null;
  
  // Calculé
  crosses_accuracy?: number | null;
}

export interface PlayerRealStats {
  displayName: string;
  position: string;
  jersey?: number;
  stats: {
    [seasonKey: string]: PlayerSeasonStats | null;
  };
}

export const omPlayersRealStats: { [playerId: number]: PlayerRealStats } = {
"""

# Ajouter chaque joueur
for player_id, player_data in data.items():
    typescript_content += f"  {player_id}: {{\n"
    typescript_content += f"    displayName: \"{player_data.get('displayName', '')}\",\n"
    typescript_content += f"    position: \"{player_data.get('position', '')}\",\n"
    
    if player_data.get('jersey'):
        typescript_content += f"    jersey: {player_data.get('jersey')},\n"
    
    typescript_content += "    stats: {\n"
    
    # Ajouter chaque saison
    for season_key, stats in player_data.get('stats', {}).items():
        typescript_content += f"      \"{season_key}\": "
        
        if stats is None:
            typescript_content += "null,\n"
        else:
            typescript_content += "{\n"
            for stat_key, stat_value in stats.items():
                if stat_value is None:
                    typescript_content += f"        {stat_key}: null,\n"
                elif isinstance(stat_value, (int, float)):
                    typescript_content += f"        {stat_key}: {stat_value},\n"
                elif isinstance(stat_value, str):
                    typescript_content += f"        {stat_key}: \"{stat_value}\",\n"
            typescript_content += "      },\n"
    
    typescript_content += "    }\n"
    typescript_content += "  },\n"

typescript_content += "};\n"

# Sauvegarder le fichier TypeScript
output_path = '../data/omPlayersCompleteStats.ts'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(typescript_content)

print(f"✅ Fichier TypeScript généré: {output_path}")
print(f"   Contient {len(data)} joueurs dont Rulli (ID: 186418)")