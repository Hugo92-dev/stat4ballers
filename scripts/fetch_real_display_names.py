#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import re
from datetime import datetime

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Cache pour éviter les requêtes multiples pour le même joueur
player_cache = {}

def get_player_display_name(player_id):
    """Récupère le display_name officiel depuis l'API SportMonks"""
    
    # Vérifier le cache
    if player_id in player_cache:
        return player_cache[player_id]
    
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
                display_name = player_data.get('display_name', '')
                # Si pas de display_name, utiliser name
                if not display_name:
                    display_name = player_data.get('name', '')
                
                player_cache[player_id] = display_name
                return display_name
        else:
            print(f"   ⚠️ Erreur API {response.status_code} pour joueur {player_id}")
    except Exception as e:
        print(f"   ❌ Erreur pour joueur {player_id}: {e}")
    
    return None

def update_file_with_real_display_names(file_path):
    """Met à jour un fichier avec les vrais display_name de l'API"""
    
    print(f"\n📁 Traitement de {file_path}")
    
    # Lire le fichier
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver tous les joueurs avec leur ID
    pattern = r'{\s*id:\s*(\d+),.*?}'
    matches = re.finditer(pattern, content, re.DOTALL)
    
    players_updated = 0
    total_players = 0
    
    # Pour chaque joueur trouvé
    for match in matches:
        total_players += 1
        player_block = match.group(0)
        player_id = match.group(1)
        
        # Afficher la progression
        if total_players % 10 == 0:
            print(f"   Progression: {total_players} joueurs traités...")
        
        # Récupérer le display_name depuis l'API
        display_name = get_player_display_name(player_id)
        
        if display_name:
            # Chercher si displayName existe déjà
            if 'displayName:' in player_block:
                # Remplacer le displayName existant
                old_pattern = r'displayName:\s*"[^"]*"'
                new_display = f'displayName: "{display_name}"'
                new_block = re.sub(old_pattern, new_display, player_block)
            else:
                # Ajouter displayName après fullName
                if 'fullName:' in player_block:
                    # Insérer après fullName
                    lines = player_block.split('\n')
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if 'fullName:' in line:
                            # Calculer l'indentation
                            indent = len(line) - len(line.lstrip())
                            new_lines.append(' ' * indent + f'displayName: "{display_name}",')
                    new_block = '\n'.join(new_lines)
                else:
                    # Insérer après name
                    lines = player_block.split('\n')
                    new_lines = []
                    for line in lines:
                        new_lines.append(line)
                        if 'name:' in line and 'displayName' not in line:
                            # Calculer l'indentation
                            indent = len(line) - len(line.lstrip())
                            new_lines.append(' ' * indent + f'displayName: "{display_name}",')
                    new_block = '\n'.join(new_lines)
            
            # Remplacer dans le contenu
            content = content.replace(player_block, new_block)
            players_updated += 1
        
        # Rate limiting pour éviter de surcharger l'API
        time.sleep(0.05)  # 50ms entre chaque requête
    
    # Écrire le fichier mis à jour
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ {players_updated}/{total_players} joueurs mis à jour")
    return players_updated, total_players

def main():
    """Met à jour tous les fichiers avec les vrais display_name"""
    
    print("=" * 80)
    print("RÉCUPÉRATION DES VRAIS DISPLAY_NAME DEPUIS L'API SPORTMONKS")
    print("=" * 80)
    print("⚠️ Ce processus va prendre plusieurs minutes...")
    print("   Environ 2800 joueurs à traiter")
    print()
    
    files = [
        'data/ligue1Teams.ts',
        'data/premierLeagueTeams.ts',
        'data/ligaTeams.ts',
        'data/serieATeams.ts',
        'data/bundesligaTeams.ts'
    ]
    
    total_updated = 0
    total_players = 0
    
    for file_path in files:
        try:
            updated, total = update_file_with_real_display_names(file_path)
            total_updated += updated
            total_players += total
        except Exception as e:
            print(f"❌ Erreur avec {file_path}: {e}")
    
    print("\n" + "=" * 80)
    print(f"✅ TERMINÉ - {total_updated}/{total_players} joueurs mis à jour")
    print("=" * 80)
    
    # Afficher quelques exemples depuis le cache
    if player_cache:
        print("\n📝 Exemples de display_name récupérés:")
        examples = list(player_cache.items())[:10]
        for player_id, display_name in examples:
            print(f"   ID {player_id}: {display_name}")

if __name__ == "__main__":
    # Lancer directement ou avec --confirm pour demander
    import sys
    
    if '--confirm' in sys.argv:
        print("Ce script va faire environ 2800 requêtes API.")
        print("Temps estimé: 3-5 minutes")
        response = input("\nVoulez-vous continuer? (o/n): ")
        
        if response.lower() != 'o':
            print("Annulé.")
            sys.exit(0)
    
    main()