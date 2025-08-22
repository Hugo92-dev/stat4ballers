import sys
import os
import re
import unicodedata

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Lire le fichier ligue1Teams.ts
with open('../data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# Extraire chaque équipe
teams_pattern = r'\{\s*id:\s*(\d+),\s*name:\s*"([^"]+)",\s*slug:\s*"([^"]+)",\s*players:\s*\[(.*?)\]\s*\}'
teams = re.findall(teams_pattern, content, re.DOTALL)

print("// IDs des joueurs pour tous les clubs de Ligue 1")
print("export const LIGUE1_PLAYER_IDS: Record<string, Record<string, number>> = {")

for team_id, team_name, team_slug, players_str in teams:
    # Extraire les joueurs de cette équipe
    player_pattern = r'id:\s*(\d+),\s*name:\s*"([^"]+)".*?(?:displayName:\s*"([^"]+)")?.*?position:\s*"([^"]+)"'
    players = re.findall(player_pattern, players_str, re.DOTALL)
    
    print(f"  // {team_name}")
    print(f"  '{team_slug}': {{")
    
    for player_id, player_name, display_name, position in players:
        # Nettoyer le nom pour en faire une clé valide
        if display_name:
            # Utiliser le displayName s'il existe
            key_name = display_name
        else:
            # Sinon utiliser le name
            key_name = player_name
        
        # Normaliser et nettoyer le nom
        key_name = unicodedata.normalize('NFKD', key_name)
        key_name = ''.join(c for c in key_name if c.isascii())
        key_name = key_name.replace(' ', '').replace('-', '').replace("'", '').replace('.', '').replace(',', '')
        key_name = re.sub(r'[^\w]', '', key_name)
        
        print(f"    '{key_name}': {player_id},")
    
    print("  },")

print("};")
print()

# Compter le total
total = sum(len(players) for _, _, _, players_str in teams for _ in re.findall(r'id:\s*(\d+)', players_str))
print(f"// Total: {len(teams)} équipes, ~{total} joueurs")