import sys
import os
import re
import unicodedata

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Lire le fichier ligue1Teams.ts
with open('../data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraire tous les joueurs avec leurs positions
# Pattern plus précis pour éviter de capturer les team ids
player_pattern = r'players:\s*\[.*?\]'
teams_blocks = re.findall(player_pattern, content, re.DOTALL)

players = []
for block in teams_blocks:
    # Extraire chaque joueur dans le bloc
    player_items = re.findall(r'\{\s*id:\s*(\d+).*?position:\s*"([^"]+)".*?\}', block, re.DOTALL)
    players.extend(player_items)

# Grouper par position
goalkeepers = []
defenders = []
midfielders = []
forwards = []

for player_id, position in players:
    if position in ['GK']:
        goalkeepers.append(player_id)
    elif position in ['DF', 'DEF']:
        defenders.append(player_id)
    elif position in ['MF', 'MID']:
        midfielders.append(player_id)
    elif position in ['FW', 'ATT', 'FOR']:
        forwards.append(player_id)

print("// Positions des joueurs de Ligue 1")
print("export const LIGUE1_PLAYER_POSITIONS = {")
print(f"  goalkeepers: [{', '.join(goalkeepers)}],")
print(f"  defenders: [{', '.join(defenders)}],")
print(f"  midfielders: [{', '.join(midfielders)}],")
print(f"  forwards: [{', '.join(forwards)}]")
print("};")