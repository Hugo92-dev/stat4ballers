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

# Correspondances des IDs de nationalité vers les noms en français
NATIONALITY_MAPPING = {
    614: "Algérie",  # Amine Gouiri
    16: "Argentine", 
    1161: "France",
    1569: "Brésil",
    1190: "Italie",
    1280: "Espagne",
    1569: "Brésil",
    320: "Maroc",
    16: "Argentine",
    1004: "Sénégal",
    462: "Côte d'Ivoire",
    1221: "Portugal",
    1073: "Pays-Bas",
    1154: "Belgique",
    1267: "Allemagne",
    1225: "Croatie",
    1228: "Angleterre",
    1004: "Sénégal",
    1161: "France",
    1569: "Brésil",
    1267: "Allemagne",
    1280: "Espagne"
    # On complétera au fur et à mesure
}

def get_country_name_from_api(nationality_id):
    """Récupère le nom du pays depuis l'API SportMonks"""
    url = f"{BASE_URL}/countries/{nationality_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                country_name = data['data'].get('name', '')
                # Traduire en français si nécessaire
                translations = {
                    'Algeria': 'Algérie',
                    'Argentina': 'Argentine',
                    'France': 'France',
                    'Brazil': 'Brésil',
                    'Italy': 'Italie',
                    'Spain': 'Espagne',
                    'Morocco': 'Maroc',
                    'Senegal': 'Sénégal',
                    'Ivory Coast': 'Côte d\'Ivoire',
                    'Cote d\'Ivoire': 'Côte d\'Ivoire',
                    'Portugal': 'Portugal',
                    'Netherlands': 'Pays-Bas',
                    'Belgium': 'Belgique',
                    'Germany': 'Allemagne',
                    'Croatia': 'Croatie',
                    'England': 'Angleterre'
                }
                return translations.get(country_name, country_name)
    except Exception as e:
        print(f"   ❌ Erreur API pour nationality_id {nationality_id}: {e}")
    
    return None

def get_player_sporting_nationality(player_id):
    """Récupère la nationalité sportive d'un joueur depuis l'API"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {'api_token': API_KEY}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data:
                nationality_id = data['data'].get('nationality_id')
                country_id = data['data'].get('country_id')
                
                if nationality_id:
                    # Essayer d'abord le mapping local
                    if nationality_id in NATIONALITY_MAPPING:
                        return NATIONALITY_MAPPING[nationality_id]
                    
                    # Sinon récupérer depuis l'API
                    nationality = get_country_name_from_api(nationality_id)
                    if nationality:
                        return nationality
                        
                # Fallback sur country_id si nationality_id n'existe pas
                if country_id:
                    country = get_country_name_from_api(country_id)
                    if country:
                        return country
                        
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit atteint, attente...")
            time.sleep(2)
            return get_player_sporting_nationality(player_id)  # Retry
            
    except Exception as e:
        print(f"   ❌ Erreur pour joueur {player_id}: {e}")
    
    return None

def extract_om_players():
    """Extrait tous les joueurs de l'OM depuis le fichier de données"""
    with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Trouver la section de l'OM
    om_match = re.search(r'name:\s*["\']Olympique de Marseille["\'].*?players:\s*\[(.*?)\]\s*\}', content, re.DOTALL)
    
    if not om_match:
        print("❌ Impossible de trouver l'OM dans le fichier")
        return []
    
    players_section = om_match.group(1)
    
    # Extraire les joueurs avec regex
    players = []
    player_blocks = re.findall(r'\{([^}]+)\}', players_section)
    
    for block in player_blocks:
        # Extraire les infos du joueur
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

def update_om_nationalities():
    """Met à jour les nationalités sportives des joueurs de l'OM"""
    print("="*60)
    print("🇫🇷 CORRECTION DES NATIONALITÉS SPORTIVES - OLYMPIQUE DE MARSEILLE")
    print("="*60)
    
    # Récupérer les joueurs de l'OM
    players = extract_om_players()
    
    if not players:
        print("❌ Aucun joueur trouvé")
        return
    
    print(f"📊 {len(players)} joueurs de l'OM trouvés")
    
    # Traiter chaque joueur
    updates = []
    
    for i, player in enumerate(players, 1):
        print(f"\n⏳ {i}/{len(players)} - {player['name']} (ID: {player['id']})")
        print(f"   Nationalité actuelle: {player['current_nationality']}")
        
        # Récupérer la nationalité sportive
        sporting_nationality = get_player_sporting_nationality(player['id'])
        
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
            print(f"   ❌ Impossible de récupérer la nationalité sportive")
        
        # Attendre un peu pour éviter le rate limiting
        time.sleep(0.5)
    
    # Afficher le résumé
    if updates:
        print(f"\n{'='*60}")
        print(f"📝 CORRECTIONS À APPORTER ({len(updates)} joueurs)")
        print("="*60)
        
        for update in updates:
            print(f"• {update['name']}: {update['old_nationality']} → {update['new_nationality']}")
        
        # Appliquer les corrections au fichier
        apply_nationality_corrections(updates)
    else:
        print(f"\n{'='*60}")
        print("✅ TOUTES LES NATIONALITÉS SONT DÉJÀ CORRECTES")
        print("="*60)

def apply_nationality_corrections(updates):
    """Applique les corrections au fichier ligue1Teams.ts"""
    print(f"\n💾 Application des corrections au fichier...")
    
    # Lire le fichier
    with open('data/ligue1Teams.ts', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Appliquer chaque correction
    for update in updates:
        # Pattern pour trouver le joueur spécifique
        pattern = rf'(\{{[^}}]*id:\s*{update["id"]}[^}}]*nationality:\s*["\']){re.escape(update["old_nationality"])}(["\'][^}}]*\}})'
        replacement = rf'\g<1>{update["new_nationality"]}\g<2>'
        
        new_content = re.sub(pattern, replacement, content)
        
        if new_content != content:
            print(f"   ✅ {update['name']}: {update['old_nationality']} → {update['new_nationality']}")
            content = new_content
        else:
            print(f"   ❌ Impossible de corriger {update['name']}")
    
    # Sauvegarder le fichier
    with open('data/ligue1Teams.ts', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   💾 Fichier sauvegardé avec {len(updates)} corrections")

def main():
    print("="*60)
    print("🔧 CORRECTION DES NATIONALITÉS SPORTIVES")
    print("="*60)
    print("   Cible: Olympique de Marseille")
    print("   Objectif: Remplacer les nationalités de naissance par les nationalités sportives")
    
    # Traiter l'OM
    update_om_nationalities()

if __name__ == "__main__":
    main()