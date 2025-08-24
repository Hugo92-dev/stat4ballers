#!/usr/bin/env python3
"""
Récupérer les détails de TOUS les clubs (stade, coach, palmarès)
"""

import sys
import requests
import json
import time
from pathlib import Path

# Fix encodage Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "leBzDfKbRE5k9zEg3FuZE3Hh7XbukODNarOXLoVtPAiAtliDZ19wLu1Wnzi2"
BASE_URL = "https://api.sportmonks.com/v3/football"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY,
}

# Configuration des championnats et équipes
LEAGUES_CONFIG = {
    'ligue1': {
        'season_id': 25651,
        'teams': {
            'marseille': 44,
            'psg': 85,
            'lyon': 80,
            'monaco': 91,
            'lille': 79,
            'nice': 72,
            'lens': 78,
            'rennes': 77,
            'strasbourg': 1020,
            'nantes': 92,
            'brest': 83,
            'toulouse': 74,
            'auxerre': 631,
            'angers': 234,
            'le-havre': 73,
            'montpellier': 89,
            'reims': 75,
            'saint-etienne': 82
        }
    },
    'premier-league': {
        'season_id': 25583,
        'teams': {
            'manchester-united': 14,
            'manchester-city': 11,
            'liverpool': 8,
            'chelsea': 18,
            'arsenal': 42,
            'tottenham': 6,
            'newcastle': 13,
            'west-ham': 5,
            'everton': 7,
            'brighton': 397,
            'aston-villa': 9,
            'nottingham-forest': 17,
            'crystal-palace': 3,
            'fulham': 20,
            'brentford': 338,
            'wolves': 22,
            'bournemouth': 43,
            'leicester': 10,
            'southampton': 19,
            'ipswich': 343
        }
    },
    'la-liga': {
        'season_id': 25659,
        'teams': {
            'real-madrid': 3468,
            'barcelona': 83,
            'atletico-madrid': 78,
            'sevilla': 95,
            'valencia': 100,
            'villarreal': 102,
            'athletic-bilbao': 77,
            'real-sociedad': 86,
            'real-betis': 90,
            'osasuna': 93,
            'celta-vigo': 80,
            'rayo-vallecano': 87,
            'getafe': 82,
            'mallorca': 91,
            'alaves': 76,
            'espanyol': 81,
            'las-palmas': 6785,
            'girona': 2394,
            'valladolid': 716,
            'leganes': 719
        }
    },
    'serie-a': {
        'season_id': 25533,
        'teams': {
            'juventus': 496,
            'milan': 113,
            'inter': 108,
            'napoli': 118,
            'roma': 121,
            'lazio': 110,
            'fiorentina': 99,
            'atalanta': 102,
            'bologna': 103,
            'torino': 122,
            'udinese': 492,
            'genoa': 107,
            'como': 117,
            'verona': 504,
            'parma': 119,
            'cagliari': 605,
            'empoli': 98,
            'lecce': 2249,
            'monza': 1189,
            'venezia': 1005
        }
    },
    'bundesliga': {
        'season_id': 25646,
        'teams': {
            'bayern': 21,
            'borussia-dortmund': 25,
            'bayer-leverkusen': 23,
            'leipzig': 173,
            'eintracht-frankfurt': 32,
            'stuttgart': 28,
            'wolfsburg': 30,
            'freiburg': 26,
            'mainz': 37,
            'werder': 38,
            'hoffenheim': 36,
            'augsburg': 31,
            'borussia-monchengladbach': 24,
            'union-berlin': 34,
            'bochum': 40,
            'heidenheim': 14263,
            'holstein-kiel': 658,
            'st-pauli': 656
        }
    }
}

def get_team_details(team_id: int, team_slug: str) -> dict:
    """Récupérer les détails d'une équipe"""
    
    print(f"  Récupération des infos pour {team_slug}...")
    
    # 1. Infos de base avec stade
    url = f"{BASE_URL}/teams/{team_id}"
    params = {'include': 'venue'}
    response = requests.get(url, headers=headers, params=params)
    
    details = {
        'slug': team_slug,
        'id': team_id
    }
    
    if response.status_code == 200:
        data = response.json()['data']
        details['name'] = data.get('name')
        details['founded'] = data.get('founded')
        
        venue = data.get('venue')
        if venue:
            details['stadium'] = venue.get('name')
            details['capacity'] = venue.get('capacity')
    
    time.sleep(0.5)  # Éviter le rate limiting
    
    # 2. Coach actuel
    url = f"{BASE_URL}/coaches/teams/{team_id}/current"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        coaches = data.get('data', [])
        if coaches:
            coach = coaches[0] if isinstance(coaches, list) else coaches
            details['coach'] = coach.get('display_name') or coach.get('name')
    
    return details

def main():
    """Récupérer tous les détails pour tous les clubs"""
    
    all_teams_data = {}
    
    for league_slug, league_config in LEAGUES_CONFIG.items():
        print(f"\n=== {league_slug.upper()} ===")
        league_data = {}
        
        for team_slug, team_id in league_config['teams'].items():
            try:
                team_data = get_team_details(team_id, team_slug)
                league_data[team_slug] = team_data
                print(f"    ✓ {team_data.get('name', team_slug)}")
                time.sleep(0.3)
            except Exception as e:
                print(f"    ✗ Erreur pour {team_slug}: {e}")
        
        all_teams_data[league_slug] = league_data
    
    # Sauvegarder les données
    with open('all_teams_details.json', 'w', encoding='utf-8') as f:
        json.dump(all_teams_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Données sauvegardées dans all_teams_details.json")
    
    # Générer le fichier TypeScript
    generate_typescript(all_teams_data)

def generate_typescript(data: dict):
    """Générer le fichier TypeScript avec toutes les données"""
    
    ts_content = """// Détails complets de toutes les équipes
// Généré automatiquement - NE PAS MODIFIER MANUELLEMENT

export const teamDetails: Record<string, {
  stadium?: string;
  capacity?: number;
  coach?: string;
  founded?: number;
  trophies?: Record<string, number>;
}> = {
"""
    
    for league_slug, teams in data.items():
        ts_content += f"\n  // {league_slug.upper()}\n"
        
        for team_slug, team_data in teams.items():
            ts_content += f"  '{team_slug}': {{\n"
            
            if team_data.get('stadium'):
                ts_content += f"    stadium: '{team_data['stadium']}',\n"
            
            if team_data.get('capacity'):
                ts_content += f"    capacity: {team_data['capacity']},\n"
            
            if team_data.get('coach'):
                ts_content += f"    coach: '{team_data['coach']}',\n"
            
            if team_data.get('founded'):
                ts_content += f"    founded: {team_data['founded']},\n"
            
            # Pour l'instant, on laisse les trophées vides (à remplir manuellement)
            ts_content += "    trophies: {}\n"
            ts_content += "  },\n"
    
    ts_content += "};\n"
    
    output_path = Path(__file__).parent.parent / 'data' / 'teamDetailsComplete.ts'
    output_path.write_text(ts_content, encoding='utf-8')
    
    print(f"✅ Fichier TypeScript généré: {output_path}")

if __name__ == "__main__":
    main()