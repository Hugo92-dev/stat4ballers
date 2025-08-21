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

# Correspondances des IDs de nationalité vers les noms en français (étendues)
NATIONALITY_MAPPING = {
    614: "Algérie",
    16: "Argentine", 
    1161: "France",
    1569: "Brésil",
    1190: "Italie",
    1280: "Espagne",
    320: "Maroc",
    1004: "Sénégal",
    462: "Côte d'Ivoire",
    1221: "Portugal",
    1073: "Pays-Bas",
    1154: "Belgique",
    1267: "Allemagne",
    1225: "Croatie",
    1228: "Angleterre",
    1072: "Écosse",
    1071: "Pays de Galles",
    1215: "République d'Irlande",
    1251: "Irlande du Nord",
    1243: "Danemark",
    1289: "Suède",
    1273: "Norvège",
    1248: "Finlande",
    1202: "Pologne",
    1230: "République tchèque",
    1257: "Slovaquie",
    1259: "Hongrie",
    1216: "Roumanie",
    1156: "Bulgarie",
    1274: "Serbie",
    1185: "Monténégro",
    1153: "Bosnie-Herzégovine",
    1275: "Slovénie",
    1184: "Macédoine du Nord",
    1065: "Albanie",
    1158: "Grèce",
    1279: "Turquie",
    1213: "Russie",
    1278: "Ukraine",
    1152: "Biélorussie",
    1195: "Lituanie",
    1194: "Lettonie",
    1170: "Estonie",
    1093: "Cameroun",
    1136: "Nigeria",
    1081: "Ghana",
    1277: "Tunisie",
    1172: "Égypte",
    1095: "Afrique du Sud",
    2: "États-Unis",
    1087: "Canada",
    1104: "Mexique",
    1068: "Brésil",
    1197: "Uruguay",
    1176: "Chili",
    1103: "Colombie",
    1173: "Équateur",
    1212: "Pérou",
    1281: "Venezuela",
    1201: "Paraguay",
    1151: "Bolivie",
    1180: "Japon",
    1275: "Corée du Sud",
    1066: "Australie",
    1137: "Nouvelle-Zélande"
}

def get_country_name_from_api(nationality_id):
    """Récupère le nom du pays depuis l'API SportMonks avec gestion des erreurs"""
    if nationality_id in NATIONALITY_MAPPING:
        return NATIONALITY_MAPPING[nationality_id]
    
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
                    'New Zealand': 'Nouvelle-Zélande'
                }
                translated = translations.get(country_name, country_name)
                # Mettre à jour le mapping pour la prochaine fois
                NATIONALITY_MAPPING[nationality_id] = translated
                return translated
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit pour nationality_id {nationality_id}, attente...")
            time.sleep(3)
            return get_country_name_from_api(nationality_id)  # Retry
    except Exception as e:
        print(f"   ❌ Erreur API pour nationality_id {nationality_id}: {e}")
    
    return None

def get_player_sporting_nationality(player_id, player_name):
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
                    nationality = get_country_name_from_api(nationality_id)
                    if nationality:
                        return nationality
                        
                # Fallback sur country_id si nationality_id n'existe pas
                if country_id:
                    country = get_country_name_from_api(country_id)
                    if country:
                        return country
                        
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit pour {player_name}, attente...")
            time.sleep(3)
            return get_player_sporting_nationality(player_id, player_name)  # Retry
            
    except Exception as e:
        print(f"   ❌ Erreur pour {player_name} (ID: {player_id}): {e}")
    
    return None

def extract_players_from_file(file_path, team_pattern):
    """Extrait tous les joueurs d'un fichier de championnat"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture {file_path}: {e}")
        return []
    
    players = []
    
    # Trouver toutes les équipes
    team_matches = re.finditer(team_pattern, content, re.DOTALL)
    
    for team_match in team_matches:
        team_name = team_match.group(1)
        players_section = team_match.group(2)
        
        # Extraire les joueurs de cette équipe
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
                    'team': team_name,
                    'current_nationality': nationality_match.group(1) if nationality_match else 'Unknown'
                }
                players.append(player)
    
    return players

def process_championship(file_path, championship_name, team_pattern):
    """Traite un championnat complet"""
    print(f"\n{'='*60}")
    print(f"🏆 {championship_name.upper()}")
    print("="*60)
    
    # Extraire tous les joueurs
    players = extract_players_from_file(file_path, team_pattern)
    
    if not players:
        print("❌ Aucun joueur trouvé")
        return []
    
    print(f"📊 {len(players)} joueurs trouvés")
    
    # Traiter par batch pour éviter le rate limiting
    batch_size = 20
    all_updates = []
    
    for i in range(0, len(players), batch_size):
        batch = players[i:i + batch_size]
        print(f"\n📦 Batch {i//batch_size + 1}/{(len(players) + batch_size - 1)//batch_size}")
        
        batch_updates = []
        for j, player in enumerate(batch, 1):
            global_index = i + j
            print(f"⏳ {global_index}/{len(players)} - {player['name']} ({player['team']})")
            print(f"   Nationalité actuelle: {player['current_nationality']}")
            
            # Récupérer la nationalité sportive
            sporting_nationality = get_player_sporting_nationality(player['id'], player['name'])
            
            if sporting_nationality:
                if sporting_nationality != player['current_nationality']:
                    print(f"   ✅ {player['current_nationality']} → {sporting_nationality}")
                    batch_updates.append({
                        'id': player['id'],
                        'name': player['name'],
                        'team': player['team'],
                        'old_nationality': player['current_nationality'],
                        'new_nationality': sporting_nationality
                    })
                else:
                    print(f"   ✓ Nationalité déjà correcte")
            else:
                print(f"   ❌ Impossible de récupérer")
            
            # Attendre entre chaque joueur
            time.sleep(0.8)
        
        all_updates.extend(batch_updates)
        
        # Pause entre les batches
        if i + batch_size < len(players):
            print(f"⏸️ Pause de 5 secondes avant le prochain batch...")
            time.sleep(5)
    
    # Appliquer les corrections si il y en a
    if all_updates:
        print(f"\n📝 {len(all_updates)} corrections à appliquer pour {championship_name}")
        apply_nationality_corrections_to_file(file_path, all_updates)
    else:
        print(f"\n✅ Toutes les nationalités de {championship_name} sont déjà correctes")
    
    return all_updates

def apply_nationality_corrections_to_file(file_path, updates):
    """Applique les corrections à un fichier spécifique"""
    print(f"💾 Application des corrections à {file_path}...")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        corrections_applied = 0
        
        for update in updates:
            # Pattern pour trouver le joueur spécifique
            pattern = rf'(\{{[^}}]*id:\s*{update["id"]}[^}}]*nationality:\s*["\']){re.escape(update["old_nationality"])}(["\'][^}}]*\}})'
            replacement = rf'\g<1>{update["new_nationality"]}\g<2>'
            
            new_content = re.sub(pattern, replacement, content)
            
            if new_content != content:
                print(f"   ✅ {update['name']} ({update['team']}): {update['old_nationality']} → {update['new_nationality']}")
                content = new_content
                corrections_applied += 1
            else:
                print(f"   ❌ Impossible de corriger {update['name']}")
        
        # Sauvegarder le fichier
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   💾 {corrections_applied}/{len(updates)} corrections appliquées et sauvegardées")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'application des corrections: {e}")

def main():
    print("="*60)
    print("🌍 CORRECTION GLOBALE DES NATIONALITÉS SPORTIVES")
    print("="*60)
    print("   Objectif: Remplacer toutes les nationalités de naissance par les nationalités sportives")
    
    # Configuration des championnats
    championships = [
        {
            'name': 'Ligue 1',
            'file': 'data/ligue1Teams.ts',
            'pattern': r'name:\s*["\']([^"\']+)["\'].*?players:\s*\[(.*?)\]\s*\}'
        },
        {
            'name': 'Premier League', 
            'file': 'data/premierLeagueTeams.ts',
            'pattern': r'name:\s*["\']([^"\']+)["\'].*?players:\s*\[(.*?)\]\s*\}'
        },
        {
            'name': 'La Liga',
            'file': 'data/ligaTeams.ts', 
            'pattern': r'name:\s*["\']([^"\']+)["\'].*?players:\s*\[(.*?)\]\s*\}'
        },
        {
            'name': 'Serie A',
            'file': 'data/serieATeams.ts',
            'pattern': r'name:\s*["\']([^"\']+)["\'].*?players:\s*\[(.*?)\]\s*\}'
        },
        {
            'name': 'Bundesliga',
            'file': 'data/bundesligaTeams.ts',
            'pattern': r'name:\s*["\']([^"\']+)["\'].*?players:\s*\[(.*?)\]\s*\}'
        }
    ]
    
    total_corrections = 0
    
    # Traiter chaque championnat
    for championship in championships:
        if os.path.exists(championship['file']):
            updates = process_championship(
                championship['file'], 
                championship['name'], 
                championship['pattern']
            )
            total_corrections += len(updates)
        else:
            print(f"❌ Fichier {championship['file']} non trouvé")
    
    # Résumé final
    print(f"\n{'='*60}")
    print(f"📊 RÉSUMÉ GLOBAL")
    print("="*60)
    print(f"   Total des corrections appliquées: {total_corrections}")
    print(f"   Tous les championnats ont été traités")
    print("="*60)

if __name__ == "__main__":
    main()