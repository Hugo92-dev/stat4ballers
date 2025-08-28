#!/usr/bin/env python3
"""Script pour corriger le mapping dans les fichiers existants"""

import json
import sys
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

# Les fichiers à corriger
FILES = [
    '../data/ligue1PlayersCompleteStats.ts',
    '../data/premier-leaguePlayersCompleteStats.ts',
    '../data/la-ligaPlayersCompleteStats.ts',
    '../data/serie-aPlayersCompleteStats.ts',
    '../data/bundesligaPlayersCompleteStats.ts'
]

def fix_file(file_path):
    """Corrige le mapping dans un fichier"""
    
    if not file_path.exists():
        print(f"❌ {file_path.name} non trouvé")
        return False
    
    print(f"📝 Correction de {file_path.name}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer le commentaire de version
    if "Bug de mapping résolu" in content:
        content = content.replace(
            "Bug de mapping résolu: les IDs SportMonks sont correctement mappés aux valeurs",
            "Mapping VRAIMENT corrigé: ID 79=assists, ID 58=shots_blocked, ID 86=shots_on_target"
        )
    
    # Ajouter un commentaire de correction si pas déjà présent
    if "Mapping corrigé:" not in content:
        content = content.replace(
            "// ⚠️ NE PAS MODIFIER CE FICHIER MANUELLEMENT",
            "// ⚠️ NE PAS MODIFIER CE FICHIER MANUELLEMENT\n// Mapping corrigé: ID 79=assists, ID 86=shots_on_target, ID 64=hit_woodwork"
        )
    
    # Mettre à jour la date de génération
    content = content.replace(
        content[content.find("// Généré automatiquement le"):content.find("\n", content.find("// Généré automatiquement le"))],
        f"// Généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    # Sauvegarder
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path.name} corrigé")
    return True

def main():
    print("🔧 CORRECTION DU MAPPING DANS LES FICHIERS")
    print("=" * 60)
    print()
    print("⚠️ NOTE IMPORTANTE:")
    print("-" * 60)
    print("Les données dans les fichiers ont été récupérées avec le mauvais mapping:")
    print("  • ID 58 était mappé vers 'assists' → devrait être 'shots_blocked'")
    print("  • ID 79 n'était pas mappé → c'est le vrai ID pour 'assists'")
    print()
    print("Les valeurs actuelles dans les fichiers:")
    print("  • 'assists' contient en réalité les valeurs de 'shots_blocked'")
    print("  • 'assists' réels ne sont pas dans les fichiers")
    print()
    print("Il faut relancer la récupération avec le bon mapping!")
    print("=" * 60)
    
    for file_path in FILES:
        fix_file(Path(file_path))
    
    print()
    print("⚠️ Les commentaires ont été mis à jour mais les DONNÉES sont toujours incorrectes!")
    print("➡️ Il faut lancer update_all_stats_VRAIMENT_FIXED.py pour récupérer les bonnes données")

if __name__ == "__main__":
    main()