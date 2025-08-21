#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import os
import re
from datetime import datetime

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def get_player_info(player_id):
    """Récupère les infos d'un joueur incluant display_name"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'api_token': API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                player_data = data['data']
                return {
                    'display_name': player_data.get('display_name', ''),
                    'common_name': player_data.get('common_name', ''),
                    'name': player_data.get('name', ''),
                    'firstname': player_data.get('firstname', ''),
                    'lastname': player_data.get('lastname', '')
                }
        return None
    except Exception as e:
        print(f"Erreur API pour joueur {player_id}: {e}")
        return None

def update_team_file(file_path, output_path):
    """Met à jour un fichier de données d'équipe avec les display_name"""
    
    # Lire le fichier TypeScript
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extraire les données des joueurs
    import re
    
    # Pattern pour trouver les IDs des joueurs
    player_ids = re.findall(r'id:\s*(\d+)', content)
    
    print(f"\n📁 Traitement de {file_path}")
    print(f"   Nombre de joueurs trouvés: {len(player_ids)}")
    
    # Créer un mapping ID -> display_name
    display_names = {}
    
    for i, player_id in enumerate(player_ids):
        if i % 10 == 0:
            print(f"   Progression: {i}/{len(player_ids)}")
        
        player_info = get_player_info(player_id)
        if player_info:
            display_names[player_id] = player_info['display_name']
            time.sleep(0.1)  # Rate limiting
    
    # Maintenant, mettre à jour le contenu
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        new_lines.append(line)
        
        # Si on trouve un ID de joueur
        match = re.search(r'id:\s*(\d+)', line)
        if match:
            player_id = match.group(1)
            
            # Ajouter display_name après l'ID si on l'a
            if player_id in display_names and display_names[player_id]:
                # Vérifier si display_name n'existe pas déjà
                next_line_idx = lines.index(line) + 1
                if next_line_idx < len(lines):
                    next_line = lines[next_line_idx]
                    if 'displayName:' not in next_line and 'name:' in next_line:
                        # Ajouter displayName après l'ID
                        indent = len(line) - len(line.lstrip())
                        new_lines.append(' ' * indent + f'displayName: "{display_names[player_id]}",')
    
    # Écrire le nouveau fichier
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))
    
    print(f"   ✅ Fichier mis à jour: {output_path}")
    return len(display_names)

def update_all_leagues():
    """Met à jour tous les fichiers de données des ligues"""
    
    print("=" * 80)
    print("MISE À JOUR DES DISPLAY_NAME POUR TOUS LES JOUEURS")
    print("=" * 80)
    
    data_files = [
        'data/ligue1Teams.ts',
        'data/premierLeagueTeams.ts',
        'data/ligaTeams.ts',
        'data/serieATeams.ts',
        'data/bundesligaTeams.ts'
    ]
    
    total_updated = 0
    
    for file_path in data_files:
        if os.path.exists(file_path):
            # Créer une sauvegarde
            backup_path = file_path.replace('.ts', '_backup.ts')
            
            # Copier le fichier original
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            
            # Mettre à jour le fichier
            count = update_team_file(file_path, file_path)
            total_updated += count
        else:
            print(f"❌ Fichier non trouvé: {file_path}")
    
    print("\n" + "=" * 80)
    print(f"✅ TERMINÉ - {total_updated} joueurs mis à jour au total")
    print("=" * 80)

def quick_fix_display_names():
    """Solution rapide: modifier directement les fichiers TypeScript existants"""
    
    print("=" * 80)
    print("AJOUT RAPIDE DES DISPLAY_NAME AUX DONNÉES EXISTANTES")
    print("=" * 80)
    
    # Pour chaque fichier de données
    data_files = [
        'data/ligue1Teams.ts',
        'data/premierLeagueTeams.ts', 
        'data/ligaTeams.ts',
        'data/serieATeams.ts',
        'data/bundesligaTeams.ts'
    ]
    
    for file_path in data_files:
        if not os.path.exists(file_path):
            print(f"❌ Fichier non trouvé: {file_path}")
            continue
            
        print(f"\n📁 Traitement de {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Ajouter displayName au type Player si nécessaire
        if 'displayName?' not in content:
            content = content.replace(
                'export interface Player {',
                'export interface Player {\n  displayName?: string;'
            )
        
        # Pour chaque joueur, ajouter displayName basé sur le fullName
        # On va simplifier en utilisant fullName comme displayName pour l'instant
        lines = content.split('\n')
        new_lines = []
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            # Si on trouve fullName, ajouter displayName juste après
            if 'fullName:' in line and i > 0:
                # Vérifier si la ligne précédente n'a pas déjà displayName
                if i > 0 and 'displayName' not in lines[i-1]:
                    # Extraire le fullName
                    match = re.search(r'fullName:\s*"([^"]+)"', line)
                    if match:
                        full_name = match.group(1)
                        # Pour display_name, on garde juste prénom + premier nom de famille
                        parts = full_name.split()
                        if len(parts) >= 2:
                            # Garder prénom + premier nom de famille
                            display_name = f"{parts[0]} {parts[1]}"
                        else:
                            display_name = full_name
                        
                        # Ajouter displayName avec la même indentation
                        indent = len(line) - len(line.lstrip())
                        new_lines.append(' ' * indent + f'displayName: "{display_name}",')
        
        # Écrire le fichier modifié
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        print(f"   ✅ Fichier mis à jour")
    
    print("\n✅ Tous les fichiers ont été mis à jour avec displayName")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        # Solution rapide sans appels API
        quick_fix_display_names()
    else:
        # Solution complète avec appels API (plus lent)
        print("⚠️ Ce script va faire de nombreux appels API (environ 2800 joueurs)")
        print("   Cela prendra environ 5-10 minutes.")
        print("   Pour une solution rapide sans API, utilisez: python update_display_names.py --quick")
        response = input("\nContinuer avec les appels API? (o/n): ")
        
        if response.lower() == 'o':
            update_all_leagues()
        else:
            print("Annulé. Utilisation de la solution rapide...")
            quick_fix_display_names()