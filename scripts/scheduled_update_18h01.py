import schedule
import time
import subprocess
import sys
from datetime import datetime

# Fix pour l'encodage UTF-8 sur Windows  
sys.stdout.reconfigure(encoding='utf-8')

def run_update():
    """Lance la mise à jour complète des statistiques"""
    print("🚀 DÉBUT DE LA MISE À JOUR PROGRAMMÉE")
    print("=" * 50)
    current_time = datetime.now().strftime("%H:%M:%S")
    print(f"⏰ Heure: {current_time}")
    
    try:
        # D'abord les clubs problématiques
        print("\n📋 ÉTAPE 1: Clubs problématiques")
        result = subprocess.run([
            'python', 'scripts/update_missing_clubs.py'
        ], capture_output=True, text=True, encoding='utf-8')
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        # Ensuite scan complet pour vérifier les autres clubs
        print("\n📋 ÉTAPE 2: Scan complet des autres clubs")
        result2 = subprocess.run([
            'python', 'scripts/complete_automated_update.py'
        ], capture_output=True, text=True, encoding='utf-8')
        
        print("STDOUT:", result2.stdout)
        if result2.stderr:
            print("STDERR:", result2.stderr)
            
        print(f"\n✅ TERMINÉ À {datetime.now().strftime('%H:%M:%S')}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")

def main():
    print("⏰ PROGRAMMATION DE LA MISE À JOUR")
    print("=" * 40)
    print("🎯 Mise à jour programmée pour 18:01")
    print("📊 Clubs prioritaires: Lyon, Bayern, Mainz, Union Berlin, Hoffenheim, Köln")
    print("🔄 Puis scan complet des autres clubs")
    print("\n⌛ En attente...")
    
    # Programmer pour 18:01
    schedule.every().day.at("18:01").do(run_update)
    
    while True:
        schedule.run_pending()
        time.sleep(30)  # Vérifier toutes les 30 secondes
        
        # Afficher l'heure actuelle toutes les 5 minutes
        if datetime.now().second == 0 and datetime.now().minute % 5 == 0:
            current = datetime.now().strftime("%H:%M:%S")
            print(f"⏰ {current} - En attente de 18:01...")

if __name__ == "__main__":
    main()