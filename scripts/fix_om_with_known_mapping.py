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

# Mapping manuel basé sur les patterns observés et la logique
NATIONALITY_ID_TO_COUNTRY = {
    # Connus avec certitude
    614: "Algérie",      # Gouiri - confirmé par vous
    
    # Déductions logiques basées sur les patterns
    17: "France",        # Plusieurs joueurs français
    44: "Argentine",     # Rulli, Balerdi, etc.
    462: "Angleterre",   # Egan Riley, Rowe, Greenwood selon vous
    
    # Autres mappings probables
    32: "Espagne",       # Lirola, Blanco
    38: "Pays-Bas",      # de Lange
    1004: "Sénégal",     # Cornelius
    5: "Brésil",         # Barbosa da Paixão
    593: "Cameroun",     # Mughe, Moumbagna
    320: "Maroc",        # Højbjerg (étrange mais c'est ce qui était marqué)
    1424: "Maroc",       # Harit, Ounahi
    1247: "République centrafricaine", # Kondogbia
    3483: "États-Unis",  # Weah
    556: "Belgique",     # Van Neck
    65437: "Panama",     # Murillo
    3662: "Gabon",       # Aubameyang
    62: "Portugal",      # Garcia selon le country_id différent
}

def get_player_nationality_id(player_id, player_name):
    """Récupère le nationality_id d'un joueur"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                nationality_id = data['data'].get('nationality_id')
                country_id = data['data'].get('country_id')
                return nationality_id, country_id
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit pour {player_name}, attente...")
            time.sleep(3)
            return get_player_nationality_id(player_id, player_name)
    except Exception as e:
        print(f"   ❌ Erreur pour {player_name}: {e}")
    
    return None, None

def extract_all_om_players():
    """Extrait tous les joueurs de l'OM"""
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return []
    
    om_match = re.search(r'name:\s*["\']Olympique de Marseille["\'].*?players:\s*\[(.*?)\]\s*\}', content, re.DOTALL)
    
    if not om_match:
        print("❌ Impossible de trouver l'OM")
        return []
    
    players_section = om_match.group(1)
    players = []
    player_blocks = re.findall(r'\{([^}]+)\}', players_section)
    
    for block in player_blocks:
        id_match = re.search(r'id:\s*(\d+)', block)
        name_match = re.search(r'name:\s*["\']([^"\']+)["\']', block)
        nationality_match = re.search(r'nationality:\s*["\']([^"\']*)["\']', block)
        
        if id_match and name_match:
            player = {
                'id': int(id_match.group(1)),
                'name': name_match.group(1),
                'current_nationality': nationality_match.group(1) if nationality_match else 'Unknown'
            }
            players.append(player)
    
    return players

def update_om_nationalities_with_mapping():
    """Met à jour les nationalités avec le mapping manuel"""
    print("="*60)
    print("🇫🇷 CORRECTION DES NATIONALITÉS OM - MAPPING MANUEL")
    print("="*60)
    
    players = extract_all_om_players()
    if not players:
        return
    
    print(f"📊 {len(players)} joueurs trouvés")
    updates = []
    
    for i, player in enumerate(players, 1):
        print(f"\n⏳ {i}/{len(players)} - {player['name']} (ID: {player['id']})")
        print(f"   Nationalité actuelle: {player['current_nationality']}")
        
        # Récupérer les IDs
        nationality_id, country_id = get_player_nationality_id(player['id'], player['name'])
        
        if nationality_id:
            print(f"   🔍 nationality_id: {nationality_id}, country_id: {country_id}")
            
            # Chercher dans le mapping
            sporting_nationality = NATIONALITY_ID_TO_COUNTRY.get(nationality_id)
            
            if sporting_nationality:
                if sporting_nationality != player['current_nationality']:
                    print(f"   ✅ Correction: {player['current_nationality']} → {sporting_nationality}")
                    updates.append({
                        'id': player['id'],
                        'name': player['name'],
                        'old_nationality': player['current_nationality'],
                        'new_nationality': sporting_nationality
                    })
                else:
                    print(f"   ✓ Nationalité déjà correcte: {sporting_nationality}")
            else:
                print(f"   ❌ nationality_id {nationality_id} non trouvé dans le mapping")
                # Utiliser country_id comme fallback si différent
                if country_id and country_id != nationality_id:
                    fallback_nationality = NATIONALITY_ID_TO_COUNTRY.get(country_id)
                    if fallback_nationality:
                        print(f"   🔄 Fallback sur country_id {country_id}: {fallback_nationality}")
                        if fallback_nationality != player['current_nationality']:
                            updates.append({
                                'id': player['id'],
                                'name': player['name'],
                                'old_nationality': player['current_nationality'],
                                'new_nationality': fallback_nationality
                            })
        else:
            print(f"   ❌ Impossible de récupérer les IDs")
        
        time.sleep(0.8)
    
    # Appliquer les corrections
    if updates:
        print(f"\n{'='*60}")
        print(f"📝 CORRECTIONS À APPLIQUER ({len(updates)} joueurs)")
        print("="*60)
        
        for update in updates:
            print(f"• {update['name']}: {update['old_nationality']} → {update['new_nationality']}")
        
        apply_corrections(updates)
    else:
        print(f"\n{'='*60}")
        print("✅ AUCUNE CORRECTION NÉCESSAIRE")
        print("="*60)

def apply_corrections(updates):
    """Applique les corrections au fichier"""
    print(f"\n💾 Application des corrections...")
    
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
        
        corrections_applied = 0
        
        for update in updates:
            pattern = rf'(\{{[^}}]*id:\s*{update["id"]}[^}}]*nationality:\s*["\']){re.escape(update["old_nationality"])}(["\'][^}}]*\}})'
            replacement = rf'\g<1>{update["new_nationality"]}\g<2>'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                print(f"   ✅ {update['name']}: {update['old_nationality']} → {update['new_nationality']}")
                content = new_content
                corrections_applied += 1
            else:
                print(f"   ❌ Pattern non trouvé pour {update['name']}")
        
        with open('data/ligue1Teams.ts', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   💾 {corrections_applied}/{len(updates)} corrections appliquées")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def main():
    update_om_nationalities_with_mapping()

if __name__ == "__main__":
    main()