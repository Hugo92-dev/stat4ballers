#!/usr/bin/env python3
"""
Régénère tous les playerSlugs dans les fichiers Teams.ts
pour qu'ils correspondent à la nouvelle fonction slugify
"""

import re
import json
from pathlib import Path

def slugify_player(name):
    """Convertit un nom en slug URL-friendly"""
    if not name:
        return ''
    
    # Convertir en minuscules
    slug = name.lower()
    
    # Normaliser les caractères spéciaux
    replacements = {
        'à': 'a', 'â': 'a', 'ä': 'a', 'á': 'a', 'ã': 'a', 'å': 'a', 'æ': 'ae',
        'ç': 'c', 'č': 'c', 'ć': 'c',
        'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ě': 'e', 'ė': 'e',
        'î': 'i', 'ï': 'i', 'í': 'i', 'ì': 'i', 'į': 'i',
        'ñ': 'n', 'ň': 'n',
        'ô': 'o', 'ö': 'o', 'ò': 'o', 'ó': 'o', 'õ': 'o', 'ø': 'o',
        'š': 's', 'ś': 's', 'ß': 's',
        'ù': 'u', 'û': 'u', 'ü': 'u', 'ú': 'u', 'ů': 'u',
        'ý': 'y', 'ÿ': 'y',
        'ž': 'z', 'ź': 'z', 'ż': 'z',
        'đ': 'd',
        "'": '', '"': '', '.': '', ',': '', '!': '', '?': '', ':': '', ';': ''
    }
    
    for old, new in replacements.items():
        slug = slug.replace(old, new)
    
    # Remplacer les espaces par des tirets
    slug = re.sub(r'\s+', '-', slug)
    
    # Garder seulement lettres, chiffres et tirets
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    # Réduire les tirets multiples
    slug = re.sub(r'-+', '-', slug)
    
    # Supprimer les tirets au début et à la fin
    slug = slug.strip('-')
    
    return slug

def update_player_slugs_in_file(filepath):
    """Met à jour les playerSlugs dans un fichier Teams.ts"""
    print(f"\nTraitement de {filepath.name}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern pour trouver les joueurs
        player_pattern = r'(\{[^}]*?displayName:\s*"([^"]+)"[^}]*?\})'
        
        updated_count = 0
        
        def replace_player(match):
            nonlocal updated_count
            player_block = match.group(1)
            display_name = match.group(2)
            
            # Générer le nouveau slug
            new_slug = slugify_player(display_name)
            
            # Chercher si playerSlug existe déjà
            slug_pattern = r'playerSlug:\s*"[^"]+"'
            
            if re.search(slug_pattern, player_block):
                # Remplacer le slug existant
                new_block = re.sub(slug_pattern, f'playerSlug: "{new_slug}"', player_block)
            else:
                # Ajouter playerSlug avant la fermeture
                new_block = player_block.rstrip('}') + f',\n        playerSlug: "{new_slug}"\n      }}'
            
            if new_block != player_block:
                updated_count += 1
                print(f"  OK: {display_name} -> {new_slug}")
            
            return new_block
        
        # Remplacer tous les joueurs
        new_content = re.sub(player_pattern, replace_player, content)
        
        if updated_count > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  Total: {updated_count} joueurs mis à jour")
        else:
            print(f"  Aucune mise à jour nécessaire")
            
        return True
    except Exception as e:
        print(f"  ERREUR: {e}")
        return False

def main():
    print("="*50)
    print("RÉGÉNÉRATION DES PLAYER SLUGS")
    print("="*50)
    
    data_path = Path(__file__).parent.parent / 'data'
    
    # Liste des fichiers à traiter
    team_files = [
        'ligue1Teams.ts',
        'premierLeagueTeams.ts',
        'ligaTeams.ts',
        'serieATeams.ts',
        'bundesligaTeams.ts'
    ]
    
    success_count = 0
    for filename in team_files:
        filepath = data_path / filename
        if filepath.exists():
            if update_player_slugs_in_file(filepath):
                success_count += 1
        else:
            print(f"\nFichier non trouvé: {filename}")
    
    print("\n" + "="*50)
    print(f"Terminé: {success_count}/{len(team_files)} fichiers traités avec succès")
    print("\nIMPORTANT: Redémarrez le serveur de développement pour appliquer les changements")

if __name__ == "__main__":
    main()