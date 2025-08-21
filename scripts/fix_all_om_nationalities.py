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

# Cache pour éviter les requêtes répétées
nationality_cache = {}

def get_nationality_from_api(nationality_id):
    """Récupère le nom de la nationalité depuis l'API"""
    if nationality_id in nationality_cache:
        return nationality_cache[nationality_id]
    
    url = f"{BASE_URL}/countries/{nationality_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                country_name = data['data'].get('name', '')
                # Traductions en français
                translations = {
                    'Algeria': 'Algérie', 'Argentina': 'Argentine', 'France': 'France',
                    'Brazil': 'Brésil', 'Italy': 'Italie', 'Spain': 'Espagne',
                    'Morocco': 'Maroc', 'Senegal': 'Sénégal', 'Ivory Coast': 'Côte d\'Ivoire',
                    'Cote d\'Ivoire': 'Côte d\'Ivoire', 'Portugal': 'Portugal',
                    'Netherlands': 'Pays-Bas', 'Belgium': 'Belgique', 'Germany': 'Allemagne',
                    'Croatia': 'Croatie', 'England': 'Angleterre', 'Scotland': 'Écosse',
                    'Wales': 'Pays de Galles', 'Northern Ireland': 'Irlande du Nord',
                    'Republic of Ireland': 'République d\'Irlande', 'Denmark': 'Danemark',
                    'Sweden': 'Suède', 'Norway': 'Norvège', 'Finland': 'Finlande',
                    'Poland': 'Pologne', 'Czech Republic': 'République tchèque',
                    'Slovakia': 'Slovaquie', 'Hungary': 'Hongrie', 'Romania': 'Roumanie',
                    'Bulgaria': 'Bulgarie', 'Serbia': 'Serbie', 'Montenegro': 'Monténégro',
                    'Bosnia and Herzegovina': 'Bosnie-Herzégovine', 'Slovenia': 'Slovénie',
                    'North Macedonia': 'Macédoine du Nord', 'Albania': 'Albanie',
                    'Greece': 'Grèce', 'Turkey': 'Turquie', 'Russia': 'Russie',
                    'Ukraine': 'Ukraine', 'Belarus': 'Biélorussie', 'Lithuania': 'Lituanie',
                    'Latvia': 'Lettonie', 'Estonia': 'Estonie', 'Cameroon': 'Cameroun',
                    'Nigeria': 'Nigeria', 'Ghana': 'Ghana', 'Tunisia': 'Tunisie',
                    'Egypt': 'Égypte', 'South Africa': 'Afrique du Sud',
                    'United States': 'États-Unis', 'Canada': 'Canada', 'Mexico': 'Mexique',
                    'Uruguay': 'Uruguay', 'Chile': 'Chili', 'Colombia': 'Colombie',
                    'Ecuador': 'Équateur', 'Peru': 'Pérou', 'Venezuela': 'Venezuela',
                    'Paraguay': 'Paraguay', 'Bolivia': 'Bolivie', 'Japan': 'Japon',
                    'South Korea': 'Corée du Sud', 'Australia': 'Australie',
                    'New Zealand': 'Nouvelle-Zélande', 'Gabon': 'Gabon', 'Mali': 'Mali',
                    'Burkina Faso': 'Burkina Faso', 'Guinea': 'Guinée', 'Jamaica': 'Jamaïque',
                    'Panama': 'Panama'
                }
                
                translated = translations.get(country_name, country_name)
                nationality_cache[nationality_id] = translated
                return translated
        
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit pour nationality_id {nationality_id}, attente...")
            time.sleep(3)
            return get_nationality_from_api(nationality_id)
            
    except Exception as e:
        print(f"   ❌ Erreur API pour nationality_id {nationality_id}: {e}")
    
    return None

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
                
                print(f"   🔍 {player_name}: nationality_id={nationality_id}, country_id={country_id}")
                
                return nationality_id
        
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit pour {player_name}, attente...")
            time.sleep(3)
            return get_player_nationality_id(player_id, player_name)
            
    except Exception as e:
        print(f"   ❌ Erreur pour {player_name}: {e}")
    
    return None

def extract_all_om_players():
    """Extrait tous les joueurs de l'OM"""
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture fichier: {e}")
        return []
    
    # Trouver la section de l'OM
    om_match = re.search(r'name:\s*["\']Olympique de Marseille["\'].*?players:\s*\[(.*?)\]\s*\}', content, re.DOTALL)
    
    if not om_match:
        print("❌ Impossible de trouver l'OM")
        return []
    
    players_section = om_match.group(1)
    
    # Extraire tous les joueurs
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

def update_all_om_nationalities():
    """Met à jour toutes les nationalités sportives de l'OM"""
    print("="*60)
    print("🇫🇷 MISE À JOUR COMPLÈTE DES NATIONALITÉS SPORTIVES - OM")
    print("="*60)
    
    # Récupérer tous les joueurs
    players = extract_all_om_players()
    
    if not players:
        print("❌ Aucun joueur trouvé")
        return
    
    print(f"📊 {len(players)} joueurs de l'OM trouvés")
    
    updates = []
    
    for i, player in enumerate(players, 1):
        print(f"\n⏳ {i}/{len(players)} - {player['name']} (ID: {player['id']})")
        print(f"   Nationalité actuelle: {player['current_nationality']}")
        
        # Récupérer le nationality_id
        nationality_id = get_player_nationality_id(player['id'], player['name'])
        
        if nationality_id:
            # Récupérer le nom de la nationalité
            sporting_nationality = get_nationality_from_api(nationality_id)
            
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
                print(f"   ❌ Impossible de résoudre nationality_id {nationality_id}")
        else:
            print(f"   ❌ Impossible de récupérer nationality_id")
        
        # Attendre un peu pour éviter le rate limiting
        time.sleep(0.8)
    
    # Appliquer les corrections
    if updates:
        print(f"\n{'='*60}")
        print(f"📝 CORRECTIONS À APPLIQUER ({len(updates)} joueurs)")
        print("="*60)
        
        for update in updates:
            print(f"• {update['name']}: {update['old_nationality']} → {update['new_nationality']}")
        
        apply_nationality_corrections(updates)
    else:
        print(f"\n{'='*60}")
        print("✅ TOUTES LES NATIONALITÉS SONT DÉJÀ CORRECTES")
        print("="*60)

def apply_nationality_corrections(updates):
    """Applique les corrections au fichier"""
    print(f"\n💾 Application des corrections...")
    
    try:
        with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
            content = f.read()
        
        corrections_applied = 0
        
        for update in updates:
            # Pattern pour trouver le joueur spécifique
            pattern = rf'(\{{[^}}]*id:\s*{update["id"]}[^}}]*nationality:\s*["\']){re.escape(update["old_nationality"])}(["\'][^}}]*\}})'
            replacement = rf'\g<1>{update["new_nationality"]}\g<2>'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                print(f"   ✅ {update['name']}: {update['old_nationality']} → {update['new_nationality']}")
                content = new_content
                corrections_applied += 1
            else:
                print(f"   ❌ Impossible de corriger {update['name']}")
        
        # Sauvegarder
        with open('data/ligue1Teams.ts', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   💾 {corrections_applied}/{len(updates)} corrections appliquées et sauvegardées")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'application: {e}")

def main():
    print("="*60)
    print("🔧 CORRECTION COMPLÈTE DES NATIONALITÉS SPORTIVES - OM")
    print("="*60)
    print("   Utilisation du nationality_id pour chaque joueur")
    
    update_all_om_nationalities()

if __name__ == "__main__":
    main()