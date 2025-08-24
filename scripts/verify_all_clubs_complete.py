#!/usr/bin/env python3
"""
Vérifier que TOUS les clubs ont des données complètes comme Marseille
"""

import re
import json
from pathlib import Path

data_dir = Path(__file__).parent.parent / 'data'

# Lire teamDetails.ts pour vérifier les infos stade/fondation
team_details_path = data_dir / 'teamDetails.ts'
team_details_content = team_details_path.read_text(encoding='utf-8')

# Extraire toutes les clés de teamDetails
details_pattern = r"'([^']+)':\s*\{"
team_details_slugs = set(re.findall(details_pattern, team_details_content))

# Lire les fichiers teams pour avoir la liste complète
files = {
    'ligue1': 'ligue1Teams.ts',
    'premier-league': 'premierLeagueTeams.ts',
    'la-liga': 'ligaTeams.ts',
    'serie-a': 'serieATeams.ts',
    'bundesliga': 'bundesligaTeams.ts'
}

print("VÉRIFICATION COMPLÈTE DE TOUS LES CLUBS")
print("="*80)

issues = []
total_clubs = 0
clubs_without_details = []
clubs_with_incomplete_players = []

for league, filename in files.items():
    filepath = data_dir / filename
    if filepath.exists():
        content = filepath.read_text(encoding='utf-8')
        
        # Parser les équipes
        teams_pattern = r'\{\s*id:\s*\d+,\s*name:\s*"([^"]+)",\s*slug:\s*"([^"]+)",\s*players:\s*\[(.*?)\]\s*\}'
        teams = re.findall(teams_pattern, content, re.DOTALL)
        
        print(f"\n{league.upper()}")
        print("-"*80)
        
        for name, slug, players_str in teams:
            total_clubs += 1
            issues_for_club = []
            
            # 1. Vérifier si le club a des détails (stade, fondation)
            if slug not in team_details_slugs:
                issues_for_club.append("Pas de détails (stade/fondation)")
                clubs_without_details.append(f"{league}/{slug}")
            
            # 2. Compter les joueurs
            player_count = players_str.count('id:')
            if player_count < 20:
                issues_for_club.append(f"Seulement {player_count} joueurs")
                clubs_with_incomplete_players.append(f"{league}/{slug}: {player_count} joueurs")
            
            # 3. Vérifier les photos des joueurs (au moins quelques-uns devraient avoir des photos)
            photo_count = players_str.count('image:')
            if photo_count < player_count * 0.8:  # Au moins 80% devraient avoir des photos
                issues_for_club.append(f"Photos manquantes ({photo_count}/{player_count})")
            
            # 4. Vérifier que les joueurs ont des numéros
            numero_count = players_str.count('numero:')
            if numero_count < player_count * 0.5:  # Au moins 50% devraient avoir des numéros
                issues_for_club.append(f"Numéros manquants ({numero_count}/{player_count})")
            
            # Afficher le statut
            if issues_for_club:
                print(f"PROBLEME: {name:30} ({slug})")
                for issue in issues_for_club:
                    print(f"   - {issue}")
                    issues.append(f"{league}/{slug}: {issue}")
            else:
                print(f"OK: {name:30} ({slug}) - Complet")

print("\n" + "="*80)
print("RÉSUMÉ")
print("="*80)
print(f"Total: {total_clubs} clubs vérifiés")

if clubs_without_details:
    print(f"\nPROBLEME: {len(clubs_without_details)} clubs sans détails (stade/fondation):")
    for club in clubs_without_details[:10]:  # Afficher les 10 premiers
        print(f"  - {club}")
    if len(clubs_without_details) > 10:
        print(f"  ... et {len(clubs_without_details) - 10} autres")

if clubs_with_incomplete_players:
    print(f"\nPROBLEME: {len(clubs_with_incomplete_players)} clubs avec moins de 20 joueurs:")
    for club in clubs_with_incomplete_players:
        print(f"  - {club}")

if not issues:
    print("\nPARFAIT! Tous les clubs ont des données complètes comme Marseille!")
else:
    print(f"\nATTENTION: {len(set([i.split(':')[0] for i in issues]))} clubs ont des problèmes à corriger")

# Vérifier aussi les logos
print("\n" + "="*80)
print("VÉRIFICATION DES LOGOS")
print("="*80)

logos_mapping_path = data_dir / 'clubLogosMapping.ts'
if logos_mapping_path.exists():
    logos_content = logos_mapping_path.read_text(encoding='utf-8')
    
    # Vérifier spécifiquement West Ham
    if "'west-ham'" in logos_content and "'west-ham-united'" not in logos_content:
        print("ATTENTION: West Ham utilise 'west-ham' dans les logos mais 'west-ham-united' dans les données")
        print("   -> La fonction getClubLogoPath doit gérer cet alias")