#!/usr/bin/env python3
"""
Script de diagnostic pour vérifier tous les clubs
"""

import json
import os
from typing import Dict, List

def load_teams_data() -> Dict[str, Dict]:
    """Charge toutes les données des équipes"""
    leagues = {
        'ligue1': 'data/ligue1Teams.ts',
        'premier-league': 'data/premierLeagueTeams.ts', 
        'liga': 'data/ligaTeams.ts',
        'serie-a': 'data/serieATeams.ts',
        'bundesliga': 'data/bundesligaTeams.ts'
    }
    
    teams_data = {}
    
    for league, filepath in leagues.items():
        print(f"\n=== {league.upper()} ===")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract teams count
            teams_count = content.count('id:') - content.count('position_id:')
            print(f"  Fichier: {filepath} ✅")
            print(f"  Équipes trouvées: {teams_count}")
            
            # Extract some team names for verification
            lines = content.split('\n')
            team_names = []
            for line in lines:
                if 'nom:' in line and 'displayName' not in line:
                    name = line.split('nom: "')[1].split('"')[0]
                    team_names.append(name)
            
            print(f"  Quelques équipes: {team_names[:3]}...")
            teams_data[league] = {
                'file': filepath,
                'teams_count': teams_count,
                'sample_names': team_names[:5]
            }
        else:
            print(f"  ❌ MANQUANT: {filepath}")
            teams_data[league] = {'file': filepath, 'exists': False}
    
    return teams_data

def check_slug_consistency() -> List[str]:
    """Vérifie la cohérence des slugs entre les fichiers JSON et TypeScript"""
    print(f"\n{'='*60}")
    print("VÉRIFICATION DE LA COHÉRENCE DES SLUGS")
    print(f"{'='*60}")
    
    issues = []
    
    leagues = {
        'ligue1': 'data/ligue1_2025_2026',
        'premier-league': 'data/premier-league_2025_2026',
        'liga': 'data/liga_2025_2026', 
        'serie-a': 'data/serie-a_2025_2026',
        'bundesliga': 'data/bundesliga_2025_2026'
    }
    
    for league, json_dir in leagues.items():
        print(f"\n--- {league.upper()} ---")
        
        if os.path.exists(json_dir):
            json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
            json_slugs = [f.replace('.json', '') for f in json_files]
            
            print(f"  Fichiers JSON: {len(json_slugs)}")
            
            # Vérifier quelques slugs problématiques connus
            problematic_slugs = []
            for slug in json_slugs:
                if ' ' in slug or 'é' in slug or 'ü' in slug or '&' in slug:
                    problematic_slugs.append(slug)
            
            if problematic_slugs:
                print(f"  ⚠️  Slugs problématiques: {problematic_slugs}")
                issues.extend([f"{league}: {slug}" for slug in problematic_slugs])
            else:
                print(f"  ✅ Slugs corrects")
                
            # Afficher quelques exemples
            print(f"  Exemples de slugs: {json_slugs[:3]}...")
        else:
            print(f"  ❌ Dossier manquant: {json_dir}")
            issues.append(f"{league}: dossier JSON manquant")
    
    return issues

def check_missing_logos():
    """Vérifie les logos manquants"""
    print(f"\n{'='*60}")
    print("VÉRIFICATION DES LOGOS")
    print(f"{'='*60}")
    
    # Cette fonction serait plus complexe, pour l'instant on fait un check basique
    print("  🔍 Logos à vérifier manuellement sur le front-end")
    print("  Clubs qui pourraient avoir des logos manquants:")
    print("  - Clubs avec noms spéciaux (accents, espaces)")
    print("  - Nouveaux clubs promus")
    print("  - Clubs avec changements de nom")

def main():
    print("="*80)
    print("🔍 DIAGNOSTIC COMPLET DES CLUBS")
    print("="*80)
    
    # 1. Vérifier les fichiers TypeScript
    teams_data = load_teams_data()
    
    # 2. Vérifier la cohérence des slugs
    slug_issues = check_slug_consistency()
    
    # 3. Vérifier les logos
    check_missing_logos()
    
    # 4. Résumé final
    print(f"\n{'='*80}")
    print("📊 RÉSUMÉ DU DIAGNOSTIC")
    print(f"{'='*80}")
    
    total_teams = sum(data.get('teams_count', 0) for data in teams_data.values() if 'teams_count' in data)
    print(f"Total équipes dans les fichiers TS: {total_teams}")
    
    print(f"\nPar championnat:")
    for league, data in teams_data.items():
        if 'teams_count' in data:
            print(f"  {league}: {data['teams_count']} équipes")
        else:
            print(f"  {league}: ❌ Fichier manquant")
    
    if slug_issues:
        print(f"\n⚠️  PROBLÈMES DÉTECTÉS:")
        for issue in slug_issues:
            print(f"  - {issue}")
        
        print(f"\n🔧 SOLUTIONS RECOMMANDÉES:")
        print("  1. Corriger les slugs avec accents/espaces/caractères spéciaux")
        print("  2. Régénérer les fichiers TypeScript si nécessaire")
        print("  3. Vérifier les pages qui affichent 'Club non trouvé'")
    else:
        print(f"\n✅ AUCUN PROBLÈME MAJEUR DÉTECTÉ")
    
    print(f"\n🌐 PAGES À TESTER:")
    print("  Ligue 1: http://localhost:3000/ligue1")
    print("  Premier League: http://localhost:3000/premier-league") 
    print("  Liga: http://localhost:3000/liga")
    print("  Serie A: http://localhost:3000/serie-a")
    print("  Bundesliga: http://localhost:3000/bundesliga")

if __name__ == "__main__":
    main()