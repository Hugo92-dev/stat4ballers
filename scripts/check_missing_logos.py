#!/usr/bin/env python3
"""
Script pour identifier les clubs avec des logos manquants
"""

def check_missing_logos():
    """Identifie les clubs mentionnés avec des logos potentiellement manquants"""
    
    missing_logos = {
        'ligue1': ['paris'],  # Paris FC vs PSG confusion
        'premier-league': ['brighton-hove-albion'],  # Changement de slug
        'liga': ['athletic-club', 'deportivo-alaves'],  # Noms spéciaux
        'serie-a': ['parma', 'pisa'],  # Clubs récemment promus
        'bundesliga': ['st-pauli', 'werder-bremen']  # Clubs avec noms spéciaux
    }
    
    print("=== DIAGNOSTIC DES LOGOS MANQUANTS ===\n")
    
    # Solutions recommandées
    solutions = {
        'paris': {
            'issue': 'Confusion entre Paris FC et Paris Saint-Germain',
            'solution': 'Vérifier que le logo correspond à Paris FC (ID probablement 4508)',
            'logo_path': 'logos/paris-fc.png ou logos/4508.png'
        },
        'brighton-hove-albion': {
            'issue': 'Slug changé de brighton-&-hove-albion',
            'solution': 'Renommer le logo ou ajouter un alias',
            'logo_path': 'logos/brighton-hove-albion.png'
        },
        'athletic-club': {
            'issue': 'Nom officiel Athletic Club vs Athletic Bilbao',
            'solution': 'Vérifier le nom exact dans les données',
            'logo_path': 'logos/athletic-bilbao.png ou logos/athletic-club.png'
        },
        'deportivo-alaves': {
            'issue': 'Accents dans le nom original',
            'solution': 'Logo pourrait être sous deportivo-alavés',
            'logo_path': 'logos/deportivo-alaves.png'
        },
        'parma': {
            'issue': 'Club récemment remonté en Serie A',
            'solution': 'Logo peut être manquant dans la base',
            'logo_path': 'logos/parma.png'
        },
        'pisa': {
            'issue': 'Club récemment remonté en Serie A',
            'solution': 'Logo peut être manquant dans la base',
            'logo_path': 'logos/pisa.png'
        },
        'st-pauli': {
            'issue': 'Nom avec trait d\'union spécial',
            'solution': 'Vérifier le format exact du nom',
            'logo_path': 'logos/st-pauli.png ou logos/sankt-pauli.png'
        },
        'werder-bremen': {
            'issue': 'Nom avec trait d\'union',
            'solution': 'Logo pourrait être sous bremen ou werder',
            'logo_path': 'logos/werder-bremen.png'
        }
    }
    
    for league, clubs in missing_logos.items():
        print(f"--- {league.upper()} ---")
        for club in clubs:
            if club in solutions:
                sol = solutions[club]
                print(f"🔍 {club}:")
                print(f"   Issue: {sol['issue']}")
                print(f"   Solution: {sol['solution']}")
                print(f"   Logo: {sol['logo_path']}")
                print()
    
    print("=== ACTIONS RECOMMANDEES ===")
    print("1. Vérifier le dossier public/logos/ pour ces fichiers")
    print("2. Télécharger les logos manquants depuis les sites officiels")
    print("3. Vérifier les mappings de logos dans clubLogosMapping.ts")
    print("4. S'assurer que les IDs correspondent aux bonnes équipes")
    
    print("\n=== URLS A RE-TESTER APRES CORRECTION LOGOS ===")
    for league, clubs in missing_logos.items():
        for club in clubs:
            print(f"  http://localhost:3000/{league}/{club}")

if __name__ == "__main__":
    check_missing_logos()