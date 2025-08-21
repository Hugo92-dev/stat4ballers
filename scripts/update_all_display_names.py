#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import re
import os
from datetime import datetime

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def get_player_info(player_id):
    """Récupère les informations d'un joueur depuis l'API"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                return data['data']
    except Exception as e:
        print(f"   ❌ Erreur pour joueur {player_id}: {e}")
    
    return None

def extract_players_from_file(file_path):
    """Extrait tous les IDs de joueurs d'un fichier"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver tous les blocs de joueurs
    players = []
    pattern = r'{[^}]*id:\s*(\d+)[^}]*}'
    
    for match in re.finditer(pattern, content):
        player_id = int(match.group(1))
        player_block = match.group(0)
        
        # Extraire le nom actuel
        name_match = re.search(r'name:\s*"([^"]+)"', player_block)
        name = name_match.group(1) if name_match else "Unknown"
        
        players.append({
            'id': player_id,
            'name': name,
            'block': player_block,
            'start': match.start(),
            'end': match.end()
        })
    
    return players, content

def update_file_with_display_names(file_path, league_name):
    """Met à jour un fichier avec les display_name depuis l'API"""
    
    print(f"\n{'='*60}")
    print(f"📁 Traitement de {league_name}")
    print(f"   Fichier: {file_path}")
    print(f"{'='*60}")
    
    # Extraire les joueurs
    players, content = extract_players_from_file(file_path)
    print(f"   📊 {len(players)} joueurs trouvés")
    
    # Récupérer les display_name depuis l'API
    updates = []
    for i, player in enumerate(players):
        if i % 10 == 0:
            print(f"   ⏳ Progression: {i}/{len(players)} joueurs...")
        
        # Récupérer les infos du joueur
        player_data = get_player_info(player['id'])
        
        if player_data:
            display_name = player_data.get('display_name', '')
            if not display_name:
                display_name = player_data.get('name', '')
            
            if display_name:
                updates.append({
                    'player': player,
                    'display_name': display_name
                })
        
        # Rate limiting
        time.sleep(0.03)  # 30ms entre chaque requête
    
    print(f"   ✅ {len(updates)} display_name récupérés")
    
    # Appliquer les mises à jour
    new_content = content
    offset = 0
    
    for update in updates:
        player = update['player']
        display_name = update['display_name']
        
        # Créer le nouveau bloc avec displayName
        old_block = player['block']
        
        # Vérifier si displayName existe déjà
        if 'displayName:' in old_block:
            # Remplacer l'existant
            new_block = re.sub(
                r'displayName:\s*"[^"]*"',
                f'displayName: "{display_name}"',
                old_block
            )
        else:
            # Ajouter displayName après fullName ou name
            lines = old_block.split('\n')
            new_lines = []
            added = False
            
            for line in lines:
                new_lines.append(line)
                if not added and ('fullName:' in line or ('name:' in line and 'displayName' not in line)):
                    # Ajouter displayName avec la même indentation
                    indent = len(line) - len(line.lstrip())
                    new_lines.append(' ' * indent + f'displayName: "{display_name}",')
                    added = True
            
            new_block = '\n'.join(new_lines)
        
        # Remplacer dans le contenu
        start = player['start'] + offset
        end = player['end'] + offset
        new_content = new_content[:start] + new_block + new_content[end:]
        offset += len(new_block) - len(old_block)
    
    # Sauvegarder le fichier
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"   💾 Fichier sauvegardé avec {len(updates)} mises à jour")
    
    # Afficher quelques exemples
    if updates:
        print(f"\n   📝 Exemples de display_name:")
        for update in updates[:5]:
            player_name = update['player']['name']
            display_name = update['display_name']
            if player_name != display_name:
                print(f"      {player_name:30} → {display_name}")

def main():
    """Traite tous les fichiers de données"""
    
    print("\n" + "="*60)
    print("🚀 MISE À JOUR DES DISPLAY_NAME DEPUIS L'API SPORTMONKS")
    print("="*60)
    print(f"   Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   Environ 2800 joueurs à traiter")
    print()
    
    leagues = [
        ('data/ligue1Teams.ts', 'Ligue 1'),
        ('data/premierLeagueTeams.ts', 'Premier League'),
        ('data/ligaTeams.ts', 'La Liga'),
        ('data/serieATeams.ts', 'Serie A'),
        ('data/bundesligaTeams.ts', 'Bundesliga')
    ]
    
    start_time = time.time()
    
    for file_path, league_name in leagues:
        if os.path.exists(file_path):
            try:
                update_file_with_display_names(file_path, league_name)
            except Exception as e:
                print(f"❌ Erreur avec {league_name}: {e}")
        else:
            print(f"❌ Fichier non trouvé: {file_path}")
    
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    
    print(f"\n{'='*60}")
    print(f"✅ TERMINÉ en {minutes}m {seconds}s")
    print(f"   Tous les display_name ont été mis à jour depuis l'API")
    print(f"{'='*60}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--ligue1':
        # Traiter seulement la Ligue 1
        print("\n🇫🇷 Traitement de la Ligue 1 uniquement...")
        update_file_with_display_names('data/ligue1Teams.ts', 'Ligue 1')
    else:
        # Traiter tous les championnats
        main()