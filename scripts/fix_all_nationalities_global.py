#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import sys
import time
import re
import os

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'replace')

API_KEY = "j28l04KZC0LGFAdbxIzdyb8zz253K1YegT5vEUN5taw0dxuNr6U3jtRMmS6C"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Cache pour éviter les requêtes répétées
nationality_cache = {}

def get_player_sporting_nationality(player_id, player_name):
    """Récupère automatiquement la nationalité sportive via l'include nationality"""
    url = f"{BASE_URL}/players/{player_id}"
    params = {
        'api_token': API_KEY,
        'include': 'nationality'
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'nationality' in data['data'] and data['data']['nationality']:
                nationality_data = data['data']['nationality']
                country_name = nationality_data.get('name', '')
                
                # Cache the result
                nationality_cache[player_id] = country_name
                
                # Traduction en français
                translations = {
                    'Algeria': 'Algérie', 'Argentina': 'Argentine', 'France': 'France',
                    'Brazil': 'Brésil', 'Italy': 'Italie', 'Spain': 'Espagne',
                    'Morocco': 'Maroc', 'Senegal': 'Sénégal', 'Ivory Coast': 'Côte d\'Ivoire',
                    'Portugal': 'Portugal', 'Netherlands': 'Pays-Bas', 'Belgium': 'Belgique', 
                    'Germany': 'Allemagne', 'Croatia': 'Croatie', 'England': 'Angleterre',
                    'Scotland': 'Écosse', 'Wales': 'Pays de Galles', 'Northern Ireland': 'Irlande du Nord',
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
                    'Panama': 'Panama', 'Switzerland': 'Suisse', 'Central African Republic': 'République centrafricaine',
                    'Austria': 'Autriche', 'Israel': 'Israël', 'Iran': 'Iran', 'Iraq': 'Irak',
                    'Saudi Arabia': 'Arabie saoudite', 'Qatar': 'Qatar', 'Kuwait': 'Koweït',
                    'United Arab Emirates': 'Émirats arabes unis', 'Jordan': 'Jordanie',
                    'Lebanon': 'Liban', 'Syria': 'Syrie', 'Yemen': 'Yémen', 'Oman': 'Oman',
                    'Bahrain': 'Bahreïn', 'Afghanistan': 'Afghanistan', 'Pakistan': 'Pakistan',
                    'Bangladesh': 'Bangladesh', 'India': 'Inde', 'Sri Lanka': 'Sri Lanka',
                    'Nepal': 'Népal', 'Bhutan': 'Bhoutan', 'Maldives': 'Maldives',
                    'China': 'Chine', 'Mongolia': 'Mongolie', 'North Korea': 'Corée du Nord',
                    'Thailand': 'Thaïlande', 'Vietnam': 'Vietnam', 'Laos': 'Laos',
                    'Cambodia': 'Cambodge', 'Myanmar': 'Myanmar', 'Malaysia': 'Malaisie',
                    'Singapore': 'Singapour', 'Indonesia': 'Indonésie', 'Philippines': 'Philippines',
                    'Iceland': 'Islande', 'Luxembourg': 'Luxembourg', 'Liechtenstein': 'Liechtenstein',
                    'Monaco': 'Monaco', 'San Marino': 'Saint-Marin', 'Vatican City': 'Vatican',
                    'Malta': 'Malte', 'Cyprus': 'Chypre', 'Kosovo': 'Kosovo',
                    'Cape Verde': 'Cap-Vert', 'Guinea-Bissau': 'Guinée-Bissau', 'Gambia': 'Gambie',
                    'Sierra Leone': 'Sierra Leone', 'Liberia': 'Liberia', 'Mauritania': 'Mauritanie',
                    'Chad': 'Tchad', 'Niger': 'Niger', 'Sudan': 'Soudan', 'South Sudan': 'Soudan du Sud',
                    'Ethiopia': 'Éthiopie', 'Eritrea': 'Érythrée', 'Djibouti': 'Djibouti',
                    'Somalia': 'Somalie', 'Kenya': 'Kenya', 'Uganda': 'Ouganda',
                    'Tanzania': 'Tanzanie', 'Rwanda': 'Rwanda', 'Burundi': 'Burundi',
                    'Democratic Republic of the Congo': 'République démocratique du Congo',
                    'Republic of the Congo': 'République du Congo', 'Angola': 'Angola',
                    'Zambia': 'Zambie', 'Malawi': 'Malawi', 'Mozambique': 'Mozambique',
                    'Zimbabwe': 'Zimbabwe', 'Botswana': 'Botswana', 'Namibia': 'Namibie',
                    'Lesotho': 'Lesotho', 'Eswatini': 'Eswatini', 'Madagascar': 'Madagascar',
                    'Mauritius': 'Maurice', 'Seychelles': 'Seychelles', 'Comoros': 'Comores'
                }
                
                french_name = translations.get(country_name, country_name)
                return french_name
                
        elif response.status_code == 429:
            print(f"   ⏳ Rate limit pour {player_name}, attente...")
            time.sleep(3)
            return get_player_sporting_nationality(player_id, player_name)
        elif response.status_code == 404:
            print(f"   ❌ Joueur {player_name} non trouvé dans l'API")
            return None
            
    except Exception as e:
        print(f"   ❌ Erreur pour {player_name}: {e}")
    
    return None

def extract_players_from_file(file_path, championship_name):
    """Extrait tous les joueurs d'un fichier de championnat"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Erreur lecture {file_path}: {e}")
        return []
    
    players = []
    
    # Rechercher toutes les équipes
    team_pattern = r'name:\s*["\']([^"\']+)["\'].*?players:\s*\[(.*?)\]\s*\}'
    team_matches = re.finditer(team_pattern, content, re.DOTALL)
    
    for team_match in team_matches:
        team_name = team_match.group(1)
        players_section = team_match.group(2)
        
        # Extraire les joueurs de cette équipe
        player_blocks = re.findall(r'\{([^}]+)\}', players_section)
        
        for block in player_blocks:
            id_match = re.search(r'id:\s*(\d+)', block)
            name_match = re.search(r'name:\s*["\']([^"\']+)["\']', block)
            nationality_match = re.search(r'nationality:\s*["\']([^"\']*)["\']', block)
            
            if id_match and name_match:
                players.append({
                    'id': int(id_match.group(1)),
                    'name': name_match.group(1),
                    'team': team_name,
                    'current_nationality': nationality_match.group(1) if nationality_match else 'Unknown'
                })
    
    return players

def process_championship(file_path, championship_name):
    """Traite un championnat complet"""
    print(f"\n{'='*80}")
    print(f"🏆 {championship_name.upper()}")
    print("="*80)
    
    if not os.path.exists(file_path):
        print(f"❌ Fichier {file_path} non trouvé")
        return []
    
    # Extraire tous les joueurs
    players = extract_players_from_file(file_path, championship_name)
    
    if not players:
        print(f"❌ Aucun joueur trouvé dans {championship_name}")
        return []
    
    print(f"📊 {len(players)} joueurs trouvés")
    
    # Traiter par batch pour éviter le rate limiting
    batch_size = 25
    all_updates = []
    
    for i in range(0, len(players), batch_size):
        batch = players[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(players) + batch_size - 1) // batch_size
        
        print(f"\n📦 Batch {batch_num}/{total_batches} ({len(batch)} joueurs)")
        
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
            time.sleep(0.7)
        
        all_updates.extend(batch_updates)
        
        # Pause entre les batches
        if i + batch_size < len(players):
            print(f"⏸️ Pause de 5 secondes avant le prochain batch...")
            time.sleep(5)
    
    # Appliquer les corrections
    if all_updates:
        print(f"\n📝 {len(all_updates)} corrections à appliquer pour {championship_name}")
        apply_corrections_to_file(file_path, all_updates)
    else:
        print(f"\n✅ Toutes les nationalités de {championship_name} sont déjà correctes")
    
    return all_updates

def apply_corrections_to_file(file_path, updates):
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
                print(f"   ❌ Pattern non trouvé pour {update['name']}")
        
        # Sauvegarder le fichier
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   💾 {corrections_applied}/{len(updates)} corrections appliquées et sauvegardées")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'application des corrections: {e}")

def main():
    print("="*80)
    print("🌍 CORRECTION AUTOMATIQUE GLOBALE DES NATIONALITÉS SPORTIVES")
    print("="*80)
    print("   Tous les championnats européens - Solution 100% automatique")
    print("   Utilisation de l'include 'nationality' de l'API SportMonks")
    
    # Configuration des championnats
    championships = [
        {
            'name': 'Ligue 1',
            'file': 'data/ligue1Teams.ts'
        },
        {
            'name': 'Premier League', 
            'file': 'data/premierLeagueTeams.ts'
        },
        {
            'name': 'La Liga',
            'file': 'data/ligaTeams.ts'
        },
        {
            'name': 'Serie A',
            'file': 'data/serieATeams.ts'
        },
        {
            'name': 'Bundesliga',
            'file': 'data/bundesligaTeams.ts'
        }
    ]
    
    total_corrections = 0
    start_time = time.time()
    
    # Traiter chaque championnat
    for championship in championships:
        updates = process_championship(championship['file'], championship['name'])
        total_corrections += len(updates)
    
    # Résumé final
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*80}")
    print(f"📊 RÉSUMÉ GLOBAL")
    print("="*80)
    print(f"   🏆 5 championnats traités")
    print(f"   ✅ {total_corrections} corrections appliquées au total")
    print(f"   ⏱️ Durée totale: {duration/60:.1f} minutes")
    print(f"   🎯 Toutes les nationalités sportives sont maintenant correctes !")
    print("="*80)

if __name__ == "__main__":
    main()