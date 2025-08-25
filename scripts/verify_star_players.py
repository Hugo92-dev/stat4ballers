#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour vérifier que les joueurs vedettes ont les bons noms
"""

import json
import os
import sys

# Forcer l'encodage UTF-8 pour Windows
sys.stdout.reconfigure(encoding='utf-8')

def search_player_in_file(filepath, player_names):
    """Cherche un joueur dans un fichier"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for name in player_names:
                if name.lower() in content.lower():
                    return True
        return False
    except:
        return False

def check_star_players():
    """Vérifie la présence et les noms des joueurs vedettes"""
    
    # Dictionnaire des joueurs vedettes et leurs équipes attendues
    star_players = {
        'Kylian Mbappé': {
            'team': 'real-madrid',
            'league': 'liga',
            'alt_names': ['Kylian Mbappe', 'Mbappé', 'Mbappe'],
            'position': 'FW'
        },
        'Erling Haaland': {
            'team': 'manchester-city',
            'league': 'premier-league',
            'alt_names': ['Erling Braut Haaland', 'Haaland'],
            'position': 'FW'
        },
        'Mohamed Salah': {
            'team': 'liverpool',
            'league': 'premier-league',
            'alt_names': ['Mo Salah', 'M. Salah'],
            'position': 'FW'
        },
        'Robert Lewandowski': {
            'team': 'barcelona',
            'league': 'liga',
            'alt_names': ['Lewandowski', 'R. Lewandowski'],
            'position': 'FW'
        },
        'Harry Kane': {
            'team': 'bayern-munich',
            'league': 'bundesliga',
            'alt_names': ['Kane', 'H. Kane'],
            'position': 'FW'
        },
        'Vinícius Júnior': {
            'team': 'real-madrid',
            'league': 'liga',
            'alt_names': ['Vinicius Junior', 'Vinicius Jr', 'Vinícius Jr', 'Vini Jr'],
            'position': 'FW'
        },
        'Jude Bellingham': {
            'team': 'real-madrid',
            'league': 'liga',
            'alt_names': ['Bellingham', 'J. Bellingham'],
            'position': 'MF'
        },
        'Bukayo Saka': {
            'team': 'arsenal',
            'league': 'premier-league',
            'alt_names': ['Saka', 'B. Saka'],
            'position': 'FW'
        },
        'Pedri': {
            'team': 'barcelona',
            'league': 'liga',
            'alt_names': ['Pedri González', 'Pedro González'],
            'position': 'MF'
        },
        'Gavi': {
            'team': 'barcelona',
            'league': 'liga',
            'alt_names': ['Pablo Páez Gavira', 'Pablo Gavi'],
            'position': 'MF'
        },
        'Lamine Yamal': {
            'team': 'barcelona',
            'league': 'liga',
            'alt_names': ['Yamal', 'L. Yamal'],
            'position': 'FW'
        },
        'Victor Osimhen': {
            'team': 'napoli',
            'league': 'serie-a',
            'alt_names': ['Osimhen', 'V. Osimhen'],
            'position': 'FW'
        },
        'Khvicha Kvaratskhelia': {
            'team': 'napoli',
            'league': 'serie-a',
            'alt_names': ['Kvaratskhelia', 'Kvara'],
            'position': 'FW'
        },
        'Marcus Rashford': {
            'team': 'manchester-united',
            'league': 'premier-league',
            'alt_names': ['Rashford', 'M. Rashford'],
            'position': 'FW'
        },
        'Bruno Fernandes': {
            'team': 'manchester-united',
            'league': 'premier-league',
            'alt_names': ['B. Fernandes', 'Bruno Miguel'],
            'position': 'MF'
        },
        'Kevin De Bruyne': {
            'team': 'manchester-city',
            'league': 'premier-league',
            'alt_names': ['De Bruyne', 'KDB'],
            'position': 'MF'
        },
        'Thibaut Courtois': {
            'team': 'real-madrid',
            'league': 'liga',
            'alt_names': ['Courtois', 'T. Courtois'],
            'position': 'GK'
        },
        'Marc-André ter Stegen': {
            'team': 'barcelona',
            'league': 'liga',
            'alt_names': ['Ter Stegen', 'Marc ter Stegen', 'MATS'],
            'position': 'GK'
        },
        'Gianluigi Donnarumma': {
            'team': 'paris-saint-germain',
            'league': 'ligue1',
            'alt_names': ['Donnarumma', 'G. Donnarumma', 'Gigio'],
            'position': 'GK'
        },
        'Alisson': {
            'team': 'liverpool',
            'league': 'premier-league',
            'alt_names': ['Alisson Becker', 'Alisson Ramses Becker'],
            'position': 'GK'
        }
    }
    
    data_folder = "C:\\Users\\hugo\\stat4ballers\\data"
    results = {
        'found': [],
        'not_found': [],
        'wrong_team': []
    }
    
    print("=== VÉRIFICATION DES JOUEURS VEDETTES ===\n")
    
    for player_name, info in star_players.items():
        league_folder = os.path.join(data_folder, f"{info['league']}_2025_2026")
        team_file = os.path.join(league_folder, f"{info['team']}.json")
        
        # Vérifier si le fichier de l'équipe existe
        if not os.path.exists(team_file):
            print(f"❌ Fichier non trouvé: {team_file}")
            results['not_found'].append({
                'player': player_name,
                'issue': f"Fichier équipe non trouvé: {info['team']}.json"
            })
            continue
        
        # Chercher le joueur
        all_names = [player_name] + info['alt_names']
        found = search_player_in_file(team_file, all_names)
        
        if found:
            print(f"✅ {player_name} - {info['team']} ({info['position']})")
            results['found'].append(player_name)
        else:
            # Chercher dans d'autres équipes de la même ligue
            found_elsewhere = False
            for other_file in os.listdir(league_folder):
                if other_file.endswith('.json') and other_file != f"{info['team']}.json":
                    other_path = os.path.join(league_folder, other_file)
                    if search_player_in_file(other_path, all_names):
                        team_name = other_file.replace('.json', '')
                        print(f"⚠️  {player_name} - Trouvé dans {team_name} au lieu de {info['team']}")
                        results['wrong_team'].append({
                            'player': player_name,
                            'expected': info['team'],
                            'found_in': team_name
                        })
                        found_elsewhere = True
                        break
            
            if not found_elsewhere:
                print(f"❌ {player_name} - NON TROUVÉ dans {info['team']}")
                results['not_found'].append({
                    'player': player_name,
                    'issue': f"Non trouvé dans {info['team']}"
                })
    
    # Résumé
    print(f"\n=== RÉSUMÉ ===")
    print(f"✅ Joueurs trouvés: {len(results['found'])}/{len(star_players)}")
    print(f"⚠️  Mauvaise équipe: {len(results['wrong_team'])}")
    print(f"❌ Non trouvés: {len(results['not_found'])}")
    
    if results['not_found']:
        print(f"\n=== JOUEURS MANQUANTS OU MAL NOMMÉS ===")
        for item in results['not_found']:
            print(f"  • {item['player']}: {item['issue']}")
    
    if results['wrong_team']:
        print(f"\n=== JOUEURS DANS LA MAUVAISE ÉQUIPE ===")
        for item in results['wrong_team']:
            print(f"  • {item['player']}: attendu dans {item['expected']}, trouvé dans {item['found_in']}")
    
    return results

if __name__ == "__main__":
    check_star_players()