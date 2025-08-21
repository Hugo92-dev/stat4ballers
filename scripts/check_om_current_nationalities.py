#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

def extract_om_nationalities():
    """Extrait toutes les nationalités actuelles des joueurs de l'OM"""
    
    print("="*60)
    print("🔍 ÉTAT ACTUEL DES NATIONALITÉS - OM")
    print("="*60)
    
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return
    
    # Trouver la section de l'OM
    om_match = re.search(r'name:\s*["\']Olympique de Marseille["\'].*?players:\s*\[(.*?)\]\s*\}', content, re.DOTALL)
    
    if not om_match:
        print("❌ Impossible de trouver l'OM dans le fichier")
        return
    
    players_section = om_match.group(1)
    
    # Extraire tous les joueurs
    player_blocks = re.findall(r'\{([^}]+)\}', players_section)
    
    players = []
    for block in player_blocks:
        # Extraire les infos du joueur
        id_match = re.search(r'id:\s*(\d+)', block)
        name_match = re.search(r'name:\s*["\']([^"\']+)["\']', block)
        nationality_match = re.search(r'nationality:\s*["\']([^"\']*)["\']', block)
        
        if id_match and name_match:
            player = {
                'id': int(id_match.group(1)),
                'name': name_match.group(1),
                'nationality': nationality_match.group(1) if nationality_match else 'Unknown'
            }
            players.append(player)
    
    # Afficher tous les joueurs
    print(f"📊 {len(players)} joueurs trouvés dans l'OM:")
    print()
    
    # Joueurs problématiques mentionnés
    problematic_names = ['Egan Riley', 'Garcia', 'Cornelius', 'Aubameyang', 'Rowe', 'Greenwood', 'Gouiri']
    
    for i, player in enumerate(players, 1):
        name_parts = player['name'].split()
        is_problematic = any(part in ' '.join(name_parts) for part in problematic_names)
        
        marker = "🔴" if is_problematic else "  "
        print(f"{marker} {i:2d}. {player['name']:<30} (ID: {player['id']:<8}) → {player['nationality']}")
    
    print(f"\n{'='*60}")
    print("🔴 = Joueurs potentiellement problématiques")
    print("="*60)
    
    return players

def main():
    extract_om_nationalities()

if __name__ == "__main__":
    main()