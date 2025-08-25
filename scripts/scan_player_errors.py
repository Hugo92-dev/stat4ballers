#!/usr/bin/env python3
"""
Script pour détecter les erreurs potentielles dans les noms de joueurs
"""

import json
import os
import re
from collections import defaultdict

def load_json_file(filepath):
    """Charge un fichier JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erreur lors du chargement de {filepath}: {e}")
        return None

def check_suspicious_names(player_data, team_name, league):
    """Vérifie les noms suspects dans les données des joueurs"""
    suspicious_patterns = []
    
    # Patterns pour détecter les erreurs potentielles
    if isinstance(player_data, dict):
        name = player_data.get('display_name', player_data.get('nom', ''))
        player_id = player_data.get('id', '')
        position = player_data.get('position', '')
        nationality = player_data.get('nationality', player_data.get('nationalite', ''))
        age = player_data.get('age', 0)
        
        # Vérifier les noms trop courts ou trop longs
        if len(name) < 3 or len(name) > 40:
            suspicious_patterns.append({
                'team': team_name,
                'league': league,
                'player': name,
                'id': player_id,
                'issue': f'Nom suspect (longueur: {len(name)})',
                'details': f'{position}, {nationality}, {age} ans'
            })
        
        # Vérifier les patterns inhabituels
        if re.search(r'\d{3,}', name):  # Plus de 3 chiffres consécutifs
            suspicious_patterns.append({
                'team': team_name,
                'league': league,
                'player': name,
                'id': player_id,
                'issue': 'Contient des chiffres suspects',
                'details': f'{position}, {nationality}, {age} ans'
            })
        
        # Vérifier les noms qui ressemblent à des slugs
        if name.count('-') > 2 or name.count('_') > 0:
            suspicious_patterns.append({
                'team': team_name,
                'league': league,
                'player': name,
                'id': player_id,
                'issue': 'Format de nom inhabituel',
                'details': f'{position}, {nationality}, {age} ans'
            })
        
        # Vérifier les espaces en fin de nom
        if name != name.strip():
            suspicious_patterns.append({
                'team': team_name,
                'league': league,
                'player': name,
                'id': player_id,
                'issue': 'Espaces en début/fin de nom',
                'details': f'{position}, {nationality}, {age} ans'
            })
    
    return suspicious_patterns

def scan_league_data(league_name, data_folder):
    """Scan les données d'une ligue"""
    league_folder = os.path.join(data_folder, f"{league_name}_2025_2026")
    suspicious_players = []
    
    if not os.path.exists(league_folder):
        print(f"Dossier non trouvé: {league_folder}")
        return suspicious_players
    
    for filename in os.listdir(league_folder):
        if filename.endswith('.json'):
            filepath = os.path.join(league_folder, filename)
            team_data = load_json_file(filepath)
            
            if team_data and 'players' in team_data:
                team_name = filename.replace('.json', '')
                for player in team_data['players']:
                    issues = check_suspicious_names(player, team_name, league_name)
                    suspicious_players.extend(issues)
    
    return suspicious_players

def check_known_players():
    """Vérifie les joueurs connus qui pourraient avoir des noms incorrects"""
    known_players = {
        # Gardiens célèbres
        'Thibaut Courtois': {'team': 'real-madrid', 'nationality': 'Belgium'},
        'Gianluigi Donnarumma': {'team': 'paris-saint-germain', 'nationality': 'Italy'},
        'Manuel Neuer': {'team': 'bayern-munich', 'nationality': 'Germany'},
        'Alisson': {'team': 'liverpool', 'nationality': 'Brazil'},
        'Ederson': {'team': 'manchester-city', 'nationality': 'Brazil'},
        
        # Défenseurs célèbres
        'Virgil van Dijk': {'team': 'liverpool', 'nationality': 'Netherlands'},
        'Sergio Ramos': {'team': 'sevilla', 'nationality': 'Spain'},
        'Raphaël Varane': {'team': 'manchester-united', 'nationality': 'France'},
        
        # Milieux célèbres
        'Kevin De Bruyne': {'team': 'manchester-city', 'nationality': 'Belgium'},
        'Luka Modrić': {'team': 'real-madrid', 'nationality': 'Croatia'},
        'Bruno Fernandes': {'team': 'manchester-united', 'nationality': 'Portugal'},
        
        # Attaquants célèbres
        'Kylian Mbappé': {'team': 'real-madrid', 'nationality': 'France'},
        'Erling Haaland': {'team': 'manchester-city', 'nationality': 'Norway'},
        'Robert Lewandowski': {'team': 'barcelona', 'nationality': 'Poland'},
        'Mohamed Salah': {'team': 'liverpool', 'nationality': 'Egypt'},
        'Harry Kane': {'team': 'bayern-munich', 'nationality': 'England'},
        'Vinicius Junior': {'team': 'real-madrid', 'nationality': 'Brazil'},
    }
    
    return known_players

def main():
    print("=== SCAN DES ERREURS DE NOMS DE JOUEURS ===\n")
    
    data_folder = "C:\\Users\\hugo\\stat4ballers\\data"
    
    leagues = {
        'ligue1': 'Ligue 1',
        'premier-league': 'Premier League',
        'liga': 'La Liga',
        'serie-a': 'Serie A',
        'bundesliga': 'Bundesliga'
    }
    
    all_suspicious = []
    
    for league_slug, league_name in leagues.items():
        print(f"Scanning {league_name}...")
        suspicious = scan_league_data(league_slug, data_folder)
        all_suspicious.extend(suspicious)
        print(f"  Trouvé {len(suspicious)} noms suspects")
    
    print(f"\n=== RÉSUMÉ ===")
    print(f"Total de noms suspects trouvés: {len(all_suspicious)}\n")
    
    if all_suspicious:
        print("=== DÉTAILS DES NOMS SUSPECTS ===\n")
        
        # Grouper par type d'erreur
        by_issue = defaultdict(list)
        for item in all_suspicious:
            by_issue[item['issue']].append(item)
        
        for issue, players in by_issue.items():
            print(f"\n--- {issue} ({len(players)} cas) ---")
            for p in players[:10]:  # Limiter à 10 exemples par type
                print(f"  • {p['league']}/{p['team']}: {p['player']} (ID: {p['id']})")
                print(f"    {p['details']}")
            
            if len(players) > 10:
                print(f"  ... et {len(players) - 10} autres cas")
    
    # Vérifier les joueurs connus
    print("\n=== VÉRIFICATION DES JOUEURS CÉLÈBRES ===")
    print("(Vérifier manuellement que ces joueurs sont bien présents avec les bons noms)")
    
    known = check_known_players()
    for player_name, info in known.items():
        print(f"  • {player_name} - {info['team']} ({info['nationality']})")
    
    # Sauvegarder les résultats
    output_file = os.path.join(data_folder, '..', 'scripts', 'player_errors_report.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'suspicious_players': all_suspicious,
            'known_players_to_check': known
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nRapport sauvegardé dans: {output_file}")

if __name__ == "__main__":
    main()