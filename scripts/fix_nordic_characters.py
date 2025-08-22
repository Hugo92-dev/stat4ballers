import os
import re
import sys

# Forcer l'encodage UTF-8 pour Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def fix_nordic_characters(content):
    """Remplace les caractères nordiques par leurs équivalents"""
    # Remplacer ø par o et Ø par O
    content = content.replace('ø', 'o')
    content = content.replace('Ø', 'O')
    # Aussi remplacer æ et Æ si présents
    content = content.replace('æ', 'ae')
    content = content.replace('Æ', 'Ae')
    # Et å/Å
    content = content.replace('å', 'a')
    content = content.replace('Å', 'A')
    return content

def process_file(filepath):
    """Traite un fichier TypeScript pour corriger les caractères nordiques"""
    print(f"Traitement de {os.path.basename(filepath)}...")
    
    # Lire le fichier
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Compter les remplacements
    count_o = content.count('ø') + content.count('Ø')
    count_ae = content.count('æ') + content.count('Æ')
    count_a = content.count('å') + content.count('Å')
    
    if count_o + count_ae + count_a == 0:
        print(f"  ✅ Aucun caractère nordique trouvé")
        return 0
    
    # Appliquer les corrections
    new_content = fix_nordic_characters(content)
    
    # Écrire le fichier corrigé
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✅ Corrigé: {count_o} ø/Ø, {count_ae} æ/Æ, {count_a} å/Å")
    return count_o + count_ae + count_a

def main():
    """Parcourt tous les fichiers de données des équipes"""
    data_dir = 'C:/Users/hugo/stat4ballers/data'
    
    files_to_process = [
        'ligue1Teams.ts',
        'premierLeagueTeams.ts',
        'ligaTeams.ts',
        'serieATeams.ts',
        'bundesligaTeams.ts'
    ]
    
    total_corrections = 0
    
    print("=== Correction des caractères nordiques ===\n")
    
    for filename in files_to_process:
        filepath = os.path.join(data_dir, filename)
        if os.path.exists(filepath):
            corrections = process_file(filepath)
            total_corrections += corrections
        else:
            print(f"❌ Fichier non trouvé: {filename}")
    
    print(f"\n=== Terminé ===")
    print(f"Total de corrections: {total_corrections}")

if __name__ == "__main__":
    main()