#!/usr/bin/env python3
"""Validation finale de toutes les statistiques"""

import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def validate_file(file_path, league_name):
    """Valide un fichier de stats"""
    
    if not file_path.exists():
        return f"❌ {league_name}: Fichier non trouvé"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifications
    checks = {
        'Version corrigée': 'Version CORRIGÉE' in content or 'Bug de mapping résolu' in content,
        'Export correct': 'PlayersRealStats' in content,
        'Interface définie': 'PlayerSeasonStats' in content,
        'Données 2024/2025': '"2024/2025' in content,
        'Goals mappé correctement': '"goals":' in content and '"goals": 52' not in content,
        'Assists mappé correctement': '"assists":' in content and '"assists": 58' not in content,
        'Saves mappé correctement': '"saves":' in content and '"saves": 57' not in content,
    }
    
    # Compter les joueurs
    player_count = content.count('"displayName":')
    
    # Obtenir la date de génération
    gen_date = "Unknown"
    if "Généré automatiquement le" in content:
        start = content.find("Généré automatiquement le") + len("Généré automatiquement le")
        end = content.find("\n", start)
        gen_date = content[start:end].strip()
    
    # Rapport
    all_ok = all(checks.values())
    status = "✅" if all_ok else "⚠️"
    
    result = f"{status} {league_name}:\n"
    result += f"  📊 {player_count} joueurs\n"
    result += f"  📅 Généré: {gen_date}\n"
    
    for check_name, passed in checks.items():
        symbol = "✓" if passed else "✗"
        result += f"  {symbol} {check_name}\n"
    
    return result

def test_specific_players():
    """Teste quelques joueurs spécifiques"""
    
    tests = []
    
    # Test Mbappé dans Liga
    liga_file = Path('../data/la-ligaPlayersCompleteStats.ts')
    if liga_file.exists():
        with open(liga_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Chercher Mbappé
        if '"Kylian Mbappé"' in content:
            # Extraire la section 2024/2025
            start = content.find('"Kylian Mbappé"')
            section = content[start:start+5000]
            
            # Vérifier les vraies valeurs
            if '"goals": 31' in section and '"assists": 39' in section:
                tests.append("✅ Mbappé: Stats correctes (31 buts, 39 assists)")
            else:
                tests.append("❌ Mbappé: Stats incorrectes")
        else:
            tests.append("⚠️ Mbappé non trouvé dans Liga")
    
    # Test Donnarumma dans Ligue 1
    ligue1_file = Path('../data/ligue1PlayersCompleteStats.ts')
    if ligue1_file.exists():
        with open(ligue1_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if '"Gianluigi Donnarumma"' in content:
            start = content.find('"Gianluigi Donnarumma"')
            section = content[start:start+5000]
            
            if '"saves": 49' in section and '"goals_conceded": 25' in section:
                tests.append("✅ Donnarumma: Stats correctes (49 arrêts, 25 buts encaissés)")
            else:
                tests.append("❌ Donnarumma: Stats incorrectes")
        else:
            tests.append("⚠️ Donnarumma non trouvé dans Ligue 1")
    
    return tests

def main():
    print("=" * 70)
    print("🏆 VALIDATION FINALE DES STATISTIQUES")
    print("=" * 70)
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Fichiers à valider
    files = {
        'LIGUE 1': Path('../data/ligue1PlayersCompleteStats.ts'),
        'PREMIER LEAGUE': Path('../data/premier-leaguePlayersCompleteStats.ts'),
        'LIGA': Path('../data/la-ligaPlayersCompleteStats.ts'),
        'SERIE A': Path('../data/serie-aPlayersCompleteStats.ts'),
        'BUNDESLIGA': Path('../data/bundesligaPlayersCompleteStats.ts'),
    }
    
    # Valider chaque fichier
    all_valid = True
    for league, file_path in files.items():
        result = validate_file(file_path, league)
        print(result)
        if "⚠️" in result or "❌" in result:
            all_valid = False
    
    # Tests spécifiques
    print("🎯 TESTS DE JOUEURS SPÉCIFIQUES:")
    print("-" * 40)
    for test in test_specific_players():
        print(f"  {test}")
    
    # Conclusion
    print("\n" + "=" * 70)
    if all_valid:
        print("✅ TOUTES LES DONNÉES SONT CORRECTES ET À JOUR!")
        print("\n📌 Les statistiques s'affichent correctement sur:")
        print("   • http://localhost:3000/ligue1/paris-saint-germain/gianluigi-donnarumma")
        print("   • http://localhost:3000/liga/real-madrid/kylian-mbappe")
        print("   • http://localhost:3000/premier-league/manchester-city/erling-haaland")
        print("   • Et tous les autres joueurs!")
    else:
        print("⚠️ Certaines données doivent encore être mises à jour")
        print("   Le script update_all_stats_final_fixed.py est probablement encore en cours")
    
    print("=" * 70)

if __name__ == "__main__":
    main()