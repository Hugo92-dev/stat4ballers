#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import re

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

def get_full_player_data(player_id, player_name):
    """Récupère TOUTES les données d'un joueur pour analyse complète"""
    print(f"\n🔍 {player_name} (ID: {player_id})")
    
    url = f"{BASE_URL}/players/{player_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                player_data = data['data']
                
                # Extraire les informations importantes
                name = player_data.get('name', 'N/A')
                display_name = player_data.get('display_name', 'N/A')
                common_name = player_data.get('common_name', 'N/A')
                nationality_id = player_data.get('nationality_id')
                country_id = player_data.get('country_id')
                
                print(f"   Name: {name}")
                print(f"   Display name: {display_name}")
                print(f"   Common name: {common_name}")
                print(f"   Nationality ID: {nationality_id}")
                print(f"   Country ID: {country_id}")
                
                return {
                    'player_id': player_id,
                    'name': player_name,
                    'api_name': name,
                    'display_name': display_name,
                    'common_name': common_name,
                    'nationality_id': nationality_id,
                    'country_id': country_id
                }
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit, attente...")
            time.sleep(3)
            return get_full_player_data(player_id, player_name)
        else:
            print(f"   ❌ Erreur API: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
    
    return None

def extract_all_om_players():
    """Extrait tous les joueurs de l'OM du fichier"""
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture: {e}")
        return []
    
    om_match = re.search(r'name:\s*["\']Olympique de Marseille["\'].*?players:\s*\[(.*?)\]\s*\}', content, re.DOTALL)
    
    if not om_match:
        print("❌ OM non trouvé")
        return []
    
    players_section = om_match.group(1)
    players = []
    player_blocks = re.findall(r'\{([^}]+)\}', players_section)
    
    for block in player_blocks:
        id_match = re.search(r'id:\s*(\d+)', block)
        name_match = re.search(r'name:\s*["\']([^"\']+)["\']', block)
        nationality_match = re.search(r'nationality:\s*["\']([^"\']*)["\']', block)
        
        if id_match and name_match:
            players.append({
                'id': int(id_match.group(1)),
                'name': name_match.group(1),
                'current_nationality': nationality_match.group(1) if nationality_match else 'Unknown'
            })
    
    return players

def main():
    print("="*80)
    print("🔍 RÉCUPÉRATION COMPLÈTE DES NATIONALITÉS SPORTIVES - OM")
    print("="*80)
    
    # Récupérer tous les joueurs de l'OM
    players = extract_all_om_players()
    if not players:
        return
    
    print(f"📊 {len(players)} joueurs trouvés")
    
    all_data = []
    
    # Récupérer les données complètes pour chaque joueur
    for i, player in enumerate(players, 1):
        print(f"\n{'='*50}")
        print(f"⏳ {i}/{len(players)} - Analyse complète")
        print("="*50)
        
        player_data = get_full_player_data(player['id'], player['name'])
        if player_data:
            player_data['current_nationality'] = player['current_nationality']
            all_data.append(player_data)
        
        # Attendre pour éviter le rate limiting
        time.sleep(1)
    
    # Sauvegarder toutes les données pour analyse
    print(f"\n{'='*80}")
    print("💾 SAUVEGARDE DES DONNÉES COMPLÈTES")
    print("="*80)
    
    with open('om_players_complete_data.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Données sauvegardées dans om_players_complete_data.json")
    
    # Afficher un résumé des nationality_id uniques
    nationality_ids = set()
    for data in all_data:
        if data['nationality_id']:
            nationality_ids.add(data['nationality_id'])
    
    print(f"\n📋 {len(nationality_ids)} nationality_id uniques trouvés:")
    for nid in sorted(nationality_ids):
        players_with_id = [d for d in all_data if d['nationality_id'] == nid]
        names = [d['name'] for d in players_with_id]
        print(f"   {nid}: {', '.join(names)}")
    
    print(f"\n{'='*80}")
    print("✅ ANALYSE TERMINÉE")
    print("   Maintenant, veuillez me donner les vraies nationalités pour chaque nationality_id")
    print("="*80)

if __name__ == "__main__":
    main()