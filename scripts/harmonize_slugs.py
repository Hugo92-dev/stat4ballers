#!/usr/bin/env python3
"""
Harmoniser les slugs entre les fichiers teamDetails et les fichiers Teams
pour que les URLs correspondent exactement
"""

import re
import json
from pathlib import Path

# Mapping des fichiers
FILES_TO_UPDATE = {
    'ligue1Teams.ts': {
        'olympique-marseille': 'marseille',
        'paris-saint-germain': 'psg',
        'olympique-lyonnais': 'lyon',
        'losc-lille': 'lille',
        'angers-sco': 'angers',
        'le-havre': 'le-havre',
        'paris-fc': 'paris-fc'
    },
    'premierLeagueTeams.ts': {
        'manchester-united': 'manchester-united',
        'manchester-city': 'manchester-city', 
        'liverpool': 'liverpool',
        'chelsea': 'chelsea',
        'arsenal': 'arsenal',
        'tottenham-hotspur': 'tottenham',
        'west-ham-united': 'west-ham',
        'newcastle-united': 'newcastle',
        'aston-villa': 'aston-villa',
        'brighton-and-hove-albion': 'brighton',
        'wolverhampton-wanderers': 'wolves',
        'crystal-palace': 'crystal-palace',
        'nottingham-forest': 'nottingham-forest',
        'everton': 'everton',
        'fulham': 'fulham',
        'afc-bournemouth': 'bournemouth',
        'brentford': 'brentford',
        'burnley': 'burnley',
        'leeds-united': 'leeds',
        'sunderland': 'sunderland'
    },
    'ligaTeams.ts': {
        'real-madrid': 'real-madrid',
        'fc-barcelona': 'barcelona',
        'atletico-madrid': 'atletico-madrid',
        'sevilla': 'sevilla',
        'real-betis': 'real-betis',
        'real-sociedad': 'real-sociedad',
        'athletic-club': 'athletic-bilbao',
        'valencia': 'valencia',
        'villarreal': 'villarreal',
        'getafe': 'getafe',
        'espanyol': 'espanyol',
        'osasuna': 'osasuna',
        'rayo-vallecano': 'rayo-vallecano',
        'mallorca': 'mallorca',
        'celta-de-vigo': 'celta-vigo',
        'deportivo-alaves': 'alaves',
        'elche': 'elche',
        'levante': 'levante',
        'girona': 'girona',
        'real-oviedo': 'real-oviedo'
    },
    'serieATeams.ts': {
        'juventus': 'juventus',
        'milan': 'milan',
        'inter': 'inter',
        'napoli': 'napoli',
        'roma': 'roma',
        'lazio': 'lazio',
        'atalanta': 'atalanta',
        'fiorentina': 'fiorentina',
        'torino': 'torino',
        'bologna': 'bologna',
        'udinese': 'udinese',
        'sassuolo': 'sassuolo',
        'genoa': 'genoa',
        'hellas-verona': 'verona',
        'cagliari': 'cagliari',
        'parma': 'parma',
        'lecce': 'lecce',
        'cremonese': 'cremonese',
        'pisa': 'pisa',
        'como': 'como'
    },
    'bundesligaTeams.ts': {
        'fc-bayern-münchen': 'bayern-munich',
        'borussia-dortmund': 'dortmund',
        'rb-leipzig': 'leipzig',
        'bayer-04-leverkusen': 'leverkusen',
        'borussia-mönchengladbach': 'monchengladbach',
        'eintracht-frankfurt': 'frankfurt',
        'vfl-wolfsburg': 'wolfsburg',
        'sc-freiburg': 'freiburg',
        'tsg-hoffenheim': 'hoffenheim',
        'vfb-stuttgart': 'stuttgart',
        'fc-köln': 'koln',
        'fc-union-berlin': 'union-berlin',
        'fc-augsburg': 'augsburg',
        'werder-bremen': 'bremen',
        'fsv-mainz-05': 'mainz',
        'heidenheim': 'heidenheim',
        'st-pauli': 'st-pauli',
        'hamburger-sv': 'hamburg'
    }
}

def update_team_file(filepath, slug_mapping):
    """Mettre à jour les slugs dans un fichier d'équipes"""
    print(f"\nTraitement de {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = 0
        for old_slug, new_slug in slug_mapping.items():
            # Chercher et remplacer le slug
            pattern = f'slug: "{old_slug}"'
            replacement = f'slug: "{new_slug}"'
            
            if pattern in content:
                content = content.replace(pattern, replacement)
                changes_made += 1
                print(f"  OK: {old_slug} -> {new_slug}")
        
        if changes_made > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Total: {changes_made} slugs mis à jour")
        else:
            print(f"  Aucun changement nécessaire")
            
        return True
    except Exception as e:
        print(f"  ERREUR: {e}")
        return False

def main():
    print("="*50)
    print("HARMONISATION DES SLUGS")
    print("="*50)
    
    data_path = Path(__file__).parent.parent / 'data'
    
    success_count = 0
    for filename, slug_mapping in FILES_TO_UPDATE.items():
        filepath = data_path / filename
        if filepath.exists():
            if update_team_file(filepath, slug_mapping):
                success_count += 1
        else:
            print(f"\nFichier non trouve: {filename}")
    
    print("\n" + "="*50)
    print(f"Terminé: {success_count}/{len(FILES_TO_UPDATE)} fichiers traités avec succès")

if __name__ == "__main__":
    main()