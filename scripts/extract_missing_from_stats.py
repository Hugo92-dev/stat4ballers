#!/usr/bin/env python3
"""
Script pour extraire tous les joueurs manquants depuis omPlayersCompleteStats.ts
"""

import re
import json

def extract_player_ids_from_stats_file():
    """Extrait tous les IDs de joueurs depuis omPlayersCompleteStats.ts"""
    
    with open('data/omPlayersCompleteStats.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Chercher tous les IDs de joueurs (format: "  12345: {")
    pattern = r'^\s*(\d+):\s*\{'
    matches = re.findall(pattern, content, re.MULTILINE)
    
    player_ids = [int(match) for match in matches]
    print(f"IDs de joueurs trouvés dans omPlayersCompleteStats.ts: {len(player_ids)}")
    
    return player_ids

def extract_player_details():
    """Extrait les détails des joueurs depuis le fichier stats"""
    
    with open('data/omPlayersCompleteStats.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern pour extraire ID, displayName et jersey
    pattern = r'(\d+):\s*\{\s*displayName:\s*"([^"]*)",\s*position:\s*"([^"]*)",\s*jersey:\s*(\d+|null)'
    matches = re.findall(pattern, content)
    
    players = []
    for match in matches:
        player_id = int(match[0])
        display_name = match[1]
        position = match[2] if match[2] else "Unknown"
        jersey = int(match[3]) if match[3] != 'null' else None
        
        players.append({
            'id': player_id,
            'display_name': display_name,
            'position': position,
            'jersey': jersey
        })
    
    return players

def main():
    print("=== Extraction des joueurs manquants ===\\n")
    
    # 1. Extraire tous les joueurs des stats
    stats_players = extract_player_details()
    print(f"Joueurs dans omPlayersCompleteStats.ts: {len(stats_players)}")
    
    # 2. Charger nos données actuelles
    with open('om_complete_squad_final.json', 'r', encoding='utf-8') as f:
        our_data = json.load(f)
    
    our_player_ids = {p['id'] for p in our_data['players']}
    print(f"Nos données actuelles: {len(our_player_ids)} joueurs")
    
    # 3. Trouver les joueurs manquants
    stats_player_ids = {p['id'] for p in stats_players}
    missing_player_ids = stats_player_ids - our_player_ids
    
    print(f"\\n=== JOUEURS MANQUANTS ({len(missing_player_ids)}) ===")
    
    missing_players = []
    for player in stats_players:
        if player['id'] in missing_player_ids:
            missing_players.append(player)
            jersey_info = f"#{player['jersey']}" if player['jersey'] else "N/A"
            print(f"  - {player['display_name']} (ID: {player['id']}, Pos: {player['position']}, Jersey: {jersey_info})")
    
    # 4. Sauvegarder les joueurs manquants
    if missing_players:
        output = {
            'missing_count': len(missing_players),
            'missing_players': missing_players,
            'missing_ids': list(missing_player_ids)
        }
        
        with open('missing_om_players_from_stats.json', 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\\nDonnées sauvegardées dans missing_om_players_from_stats.json")
        
        # 5. Afficher quelques détails supplémentaires
        print(f"\\n=== RÉSUMÉ ===")
        print(f"Total dans stats: {len(stats_players)}")
        print(f"Total dans nos données: {len(our_player_ids)}")
        print(f"Manquants: {len(missing_player_ids)}")
        
        # Grouper les manquants par position
        positions = {}
        for player in missing_players:
            pos = player['position'] or 'Unknown'
            if pos not in positions:
                positions[pos] = []
            positions[pos].append(player['display_name'])
        
        print(f"\\nRépartition des manquants:")
        for pos, names in positions.items():
            print(f"  {pos}: {len(names)} joueurs")
            for name in names:
                print(f"    - {name}")
    else:
        print("Aucun joueur manquant trouvé!")

if __name__ == "__main__":
    main()