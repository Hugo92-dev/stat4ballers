#!/usr/bin/env python3
"""
Récupérer automatiquement les détails de TOUTES les équipes depuis l'API SportMonks
Inclut: stade, capacité, année de fondation
"""

import requests
import json
import time
from pathlib import Path

# Configuration API
API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

# Headers pour les requêtes
headers = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}

# IDs des saisons 2025/2026 pour chaque championnat
SEASON_IDS = {
    'ligue1': 25651,
    'premier-league': 25583,
    'la-liga': 25659,
    'serie-a': 25533,
    'bundesliga': 25646
}

def get_teams_by_season(season_id, league_name):
    """Récupérer toutes les équipes d'une saison"""
    url = f"{BASE_URL}/teams/seasons/{season_id}"
    params = {
        "api_token": API_KEY,
        "include": "venue",  # Inclure les infos du stade
        "per_page": 50
    }
    
    all_teams = []
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        teams = data.get('data', [])
        
        print(f"\n{league_name.upper()}: {len(teams)} équipes trouvées")
        
        for team in teams:
            all_teams.append(team)
            venue = team.get('venue', {})
            try:
                if venue:
                    print(f"  {team.get('name')}: {venue.get('name')} ({venue.get('capacity')} places)")
                else:
                    print(f"  {team.get('name')}: Pas de stade")
            except:
                # Ignorer les erreurs d'encodage
                pass
    else:
        print(f"Erreur pour la saison {season_id}: {response.status_code}")
        if response.text:
            print(f"Message: {response.text[:200]}")
    
    return all_teams

def extract_team_details(team_data):
    """Extraire les détails d'une équipe"""
    details = {
        'id': team_data.get('id'),
        'name': team_data.get('name'),
        'founded': team_data.get('founded'),
        'stadium': None,
        'capacity': None
    }
    
    # Récupérer les infos du stade si disponibles
    venue = team_data.get('venue')
    if venue:
        details['stadium'] = venue.get('name')
        details['capacity'] = venue.get('capacity')
    
    return details

def generate_typescript_file(all_teams_details):
    """Générer le fichier TypeScript avec les détails des équipes"""
    
    # Début du fichier TypeScript
    ts_content = """// Détails complets de toutes les équipes des 5 grands championnats
// Généré automatiquement depuis l'API SportMonks
// NE PAS MODIFIER MANUELLEMENT - Utiliser fetch_all_teams_details.py

export const teamDetails: Record<string, {
  stadium?: string;
  capacity?: number;
  founded?: number;
}> = {
"""
    
    # Ajouter chaque équipe
    for slug, details in sorted(all_teams_details.items()):
        ts_content += f"  '{slug}': {{\n"
        
        if details.get('stadium'):
            # Échapper les apostrophes dans les noms de stades
            stadium = details['stadium'].replace("'", "\\'")
            ts_content += f"    stadium: '{stadium}',\n"
        
        if details.get('capacity'):
            ts_content += f"    capacity: {details['capacity']},\n"
            
        if details.get('founded'):
            ts_content += f"    founded: {details['founded']},\n"
        
        ts_content += "  },\n"
    
    ts_content += "};\n"
    
    return ts_content

def main():
    print("="*50)
    print("RÉCUPÉRATION DES DÉTAILS DES ÉQUIPES")
    print("="*50)
    
    all_teams_details = {}
    all_teams = []
    
    # Récupérer les équipes pour chaque championnat
    for league_name, season_id in SEASON_IDS.items():
        teams = get_teams_by_season(season_id, league_name)
        all_teams.extend(teams)
        time.sleep(1)  # Pause entre les requêtes
    
    print(f"\nTotal global: {len(all_teams)} équipes récupérées")
    
    # Traiter chaque équipe
    for team_data in all_teams:
        details = extract_team_details(team_data)
        
        # Créer le slug (simplification du nom)
        name = details['name']
        slug = name.lower()
        slug = slug.replace(' ', '-')
        slug = slug.replace('é', 'e').replace('è', 'e')
        slug = slug.replace('à', 'a').replace('â', 'a')
        slug = slug.replace('ç', 'c')
        slug = slug.replace('ô', 'o')
        slug = slug.replace('&', 'and')
        slug = slug.replace('.', '')
        slug = slug.replace("'", '')
        
        # Corrections pour harmoniser avec les slugs des fichiers Teams.ts
        slug_corrections = {
                # Ligue 1
                'olympique-de-marseille': 'marseille',
                'olympique-marseille': 'marseille',
                'paris-saint-germain-fc': 'psg',
                'paris-saint-germain': 'psg',
                'olympique-lyonnais': 'lyon',
                'losc-lille': 'lille',
                'ogc-nice': 'nice',
                'rc-lens': 'lens',
                'stade-rennais-fc': 'rennes',
                'rc-strasbourg-alsace': 'strasbourg',
                'fc-nantes': 'nantes',
                'aj-auxerre': 'auxerre',
                'stade-brestois-29': 'brest',
                'angers-sco': 'angers',
                'le-havre-ac': 'le-havre',
                'toulouse-fc': 'toulouse',
                'fc-metz': 'metz',
                'metz': 'metz',
                'fc-lorient': 'lorient',
                'lorient': 'lorient',
                'paris-fc': 'paris-fc',
                'as-monaco': 'monaco',
                'monaco': 'monaco',
                'montpellier-hsc': 'montpellier',
                'stade-de-reims': 'reims',
                'as-saint-etienne': 'saint-etienne',
                # Premier League
                'manchester-united-fc': 'manchester-united',
                'manchester-city-fc': 'manchester-city',
                'liverpool-fc': 'liverpool',
                'chelsea-fc': 'chelsea',
                'arsenal-fc': 'arsenal',
                'tottenham-hotspur-fc': 'tottenham',
                'west-ham-united-fc': 'west-ham',
                'newcastle-united-fc': 'newcastle',
                'aston-villa-fc': 'aston-villa',
                'brighton-and-hove-albion-fc': 'brighton',
                'brighton-hove-albion': 'brighton',
                'wolverhampton-wanderers-fc': 'wolves',
                'crystal-palace-fc': 'crystal-palace',
                'nottingham-forest-fc': 'nottingham-forest',
                'everton-fc': 'everton',
                'fulham-fc': 'fulham',
                'afc-bournemouth': 'bournemouth',
                'brentford-fc': 'brentford',
                'burnley-fc': 'burnley',
                'leeds-united-fc': 'leeds',
                'sunderland-afc': 'sunderland',
                'leicester-city-fc': 'leicester',
                'southampton-fc': 'southampton',
                'ipswich-town-fc': 'ipswich',
                # La Liga
                'real-madrid-cf': 'real-madrid',
                'fc-barcelona': 'barcelona',
                'atletico-de-madrid': 'atletico-madrid',
                'sevilla-fc': 'sevilla',
                'real-betis-balompie': 'real-betis',
                'real-sociedad': 'real-sociedad',
                'athletic-club': 'athletic-bilbao',
                'valencia-cf': 'valencia',
                'villarreal-cf': 'villarreal',
                'getafe-cf': 'getafe',
                'rcd-espanyol': 'espanyol',
                'ca-osasuna': 'osasuna',
                'rayo-vallecano': 'rayo-vallecano',
                'rcd-mallorca': 'mallorca',
                'rc-celta': 'celta-vigo',
                'deportivo-alaves': 'alaves',
                'elche-cf': 'elche',
                'levante-ud': 'levante',
                'girona-fc': 'girona',
                'real-oviedo': 'real-oviedo',
                'real-valladolid-cf': 'valladolid',
                # Serie A
                'juventus-fc': 'juventus',
                'ac-milan': 'milan',
                'inter-milan': 'inter',
                'ssc-napoli': 'napoli',
                'as-roma': 'roma',
                'ss-lazio': 'lazio',
                'atalanta-bc': 'atalanta',
                'acf-fiorentina': 'fiorentina',
                'torino-fc': 'torino',
                'bologna-fc-1909': 'bologna',
                'udinese-calcio': 'udinese',
                'us-sassuolo': 'sassuolo',
                'genoa-cfc': 'genoa',
                'hellas-verona-fc': 'verona',
                'cagliari-calcio': 'cagliari',
                'parma-calcio-1913': 'parma',
                'us-lecce': 'lecce',
                'us-cremonese': 'cremonese',
                'pisa-sc': 'pisa',
                'como-1907': 'como',
                'empoli-fc': 'empoli',
                # Bundesliga
                'fc-bayern-munchen': 'bayern-munich',
                'borussia-dortmund': 'dortmund',
                'rb-leipzig': 'leipzig',
                'bayer-04-leverkusen': 'leverkusen',
                'borussia-monchengladbach': 'monchengladbach',
                'eintracht-frankfurt': 'frankfurt',
                'vfl-wolfsburg': 'wolfsburg',
                'sc-freiburg': 'freiburg',
                'tsg-1899-hoffenheim': 'hoffenheim',
                'vfb-stuttgart': 'stuttgart',
                '1-fc-koln': 'koln',
                '1-fc-union-berlin': 'union-berlin',
                'fc-augsburg': 'augsburg',
                'sv-werder-bremen': 'bremen',
                '1-fsv-mainz-05': 'mainz',
                '1-fc-heidenheim-1846': 'heidenheim',
                'fc-st-pauli': 'st-pauli',
                'hamburger-sv': 'hamburg',
                'holstein-kiel': 'holstein-kiel',
        }
        
        # Appliquer les corrections
        if slug in slug_corrections:
            slug = slug_corrections[slug]
        
        # Stocker les détails
        all_teams_details[slug] = {
            'stadium': details['stadium'],
            'capacity': details['capacity'],
            'founded': details['founded']
        }
    
    # Sauvegarder les données JSON pour backup
    json_path = Path(__file__).parent / 'teams_details_api.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_teams_details, f, ensure_ascii=False, indent=2)
    print(f"\nDonnees sauvegardees: {json_path}")
    
    # Générer le fichier TypeScript
    ts_content = generate_typescript_file(all_teams_details)
    ts_path = Path(__file__).parent.parent / 'data' / 'teamDetailsFromAPI.ts'
    
    with open(ts_path, 'w', encoding='utf-8') as f:
        f.write(ts_content)
    
    print(f"Fichier TypeScript genere: {ts_path}")
    print(f"\nTotal: {len(all_teams_details)} équipes avec leurs détails")
    
    # Statistiques
    with_stadium = sum(1 for d in all_teams_details.values() if d.get('stadium'))
    with_capacity = sum(1 for d in all_teams_details.values() if d.get('capacity'))
    with_founded = sum(1 for d in all_teams_details.values() if d.get('founded'))
    
    print(f"\nStatistiques:")
    print(f"  - {with_stadium} équipes avec stade")
    print(f"  - {with_capacity} équipes avec capacité")
    print(f"  - {with_founded} équipes avec année de fondation")

if __name__ == "__main__":
    main()