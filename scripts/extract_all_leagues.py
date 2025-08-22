import sys
import os
import re
import unicodedata

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

def extract_league_data(filename, league_name, league_var):
    """Extrait les IDs et positions des joueurs d'une ligue"""
    with open(f'../data/{filename}', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire chaque équipe
    teams_pattern = r'\{\s*id:\s*(\d+),\s*name:\s*"([^"]+)",\s*slug:\s*"([^"]+)",\s*players:\s*\[(.*?)\]\s*\}'
    teams = re.findall(teams_pattern, content, re.DOTALL)
    
    # IDs par équipe
    ids_output = []
    ids_output.append(f"// {league_name}")
    ids_output.append(f"export const {league_var}_PLAYER_IDS: Record<string, Record<string, number>> = {{")
    
    # Positions
    all_goalkeepers = []
    all_defenders = []
    all_midfielders = []
    all_forwards = []
    
    for team_id, team_name, team_slug, players_str in teams:
        # Extraire les joueurs de cette équipe
        player_pattern = r'id:\s*(\d+),\s*name:\s*"([^"]+)".*?(?:displayName:\s*"([^"]+)")?.*?position:\s*"([^"]+)"'
        players = re.findall(player_pattern, players_str, re.DOTALL)
        
        ids_output.append(f"  // {team_name}")
        ids_output.append(f"  '{team_slug}': {{")
        
        for player_id, player_name, display_name, position in players:
            # Nettoyer le nom pour en faire une clé valide
            if display_name:
                key_name = display_name
            else:
                key_name = player_name
            
            # Normaliser et nettoyer le nom
            key_name = unicodedata.normalize('NFKD', key_name)
            key_name = ''.join(c for c in key_name if c.isascii())
            key_name = key_name.replace(' ', '').replace('-', '').replace("'", '').replace('.', '').replace(',', '')
            key_name = re.sub(r'[^\w]', '', key_name)
            
            ids_output.append(f"    '{key_name}': {player_id},")
            
            # Classer par position
            if position in ['GK']:
                all_goalkeepers.append(player_id)
            elif position in ['DF', 'DEF']:
                all_defenders.append(player_id)
            elif position in ['MF', 'MID']:
                all_midfielders.append(player_id)
            elif position in ['FW', 'ATT', 'FOR']:
                all_forwards.append(player_id)
        
        ids_output.append("  },")
    
    ids_output.append("};")
    
    # Positions
    positions_output = []
    positions_output.append(f"// {league_name} positions")
    positions_output.append(f"export const {league_var}_PLAYER_POSITIONS = {{")
    positions_output.append(f"  goalkeepers: [{', '.join(all_goalkeepers)}],")
    positions_output.append(f"  defenders: [{', '.join(all_defenders)}],")
    positions_output.append(f"  midfielders: [{', '.join(all_midfielders)}],")
    positions_output.append(f"  forwards: [{', '.join(all_forwards)}]")
    positions_output.append("};")
    
    return '\n'.join(ids_output), '\n'.join(positions_output)

# Extraire toutes les ligues
leagues = [
    ('ligue1Teams.ts', 'Ligue 1', 'LIGUE1'),
    ('premierLeagueTeams.ts', 'Premier League', 'PREMIER_LEAGUE'),
    ('ligaTeams.ts', 'La Liga', 'LIGA'),
    ('serieATeams.ts', 'Serie A', 'SERIE_A'),
    ('bundesligaTeams.ts', 'Bundesliga', 'BUNDESLIGA')
]

all_ids = []
all_positions = []

for filename, league_name, league_var in leagues:
    try:
        ids, positions = extract_league_data(filename, league_name, league_var)
        all_ids.append(ids)
        all_positions.append(positions)
    except Exception as e:
        print(f"// Erreur pour {league_name}: {e}", file=sys.stderr)

# Générer le fichier des IDs
print("// IDs de tous les joueurs des 5 grands championnats")
print()
for ids in all_ids:
    print(ids)
    print()

# Sauvegarder les positions dans un fichier séparé
with open('../services/allPlayerPositions.ts', 'w', encoding='utf-8') as f:
    f.write("// Positions de tous les joueurs des 5 grands championnats\n\n")
    for positions in all_positions:
        f.write(positions)
        f.write("\n\n")

# Message de succès dans stderr uniquement
pass