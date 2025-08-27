#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de refresh complet des données pour tous les championnats
Récupère les effectifs à jour et les statistiques des joueurs
"""

import subprocess
import sys
import time
from datetime import datetime
import os
import json

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

def log_message(message, level="INFO"):
    """Affiche un message horodaté"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

def run_script(script_name, description):
    """Exécute un script Python et gère les erreurs"""
    log_message(f"🔄 {description}...")
    
    # Le répertoire scripts où se trouvent tous les scripts
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=scripts_dir  # Exécuter depuis le dossier scripts
        )
        
        if result.returncode == 0:
            log_message(f"✅ {description} - Terminé avec succès", "SUCCESS")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            log_message(f"❌ {description} - Échec", "ERROR")
            if result.stderr:
                print(f"Erreur: {result.stderr}")
            return False
            
    except Exception as e:
        log_message(f"❌ {description} - Exception: {str(e)}", "ERROR")
        return False

def refresh_all_data():
    """Rafraîchit toutes les données des 5 grands championnats"""
    
    log_message("=" * 60)
    log_message("🚀 DÉBUT DU REFRESH COMPLET DES DONNÉES")
    log_message("=" * 60)
    
    start_time = time.time()
    success_count = 0
    error_count = 0
    
    # Scripts à exécuter dans l'ordre (juste les noms, sans le chemin)
    scripts_to_run = [
        ("fetch_all_leagues_all_players_optimized.py", "Récupération de tous les joueurs (5 championnats)"),
        ("fetch_all_teams_stats.py", "Récupération des statistiques détaillées"),
        ("fetch_complete_all_teams_all_players.py", "Mise à jour complète des effectifs"),
    ]
    
    # Exécution séquentielle des scripts
    for script_name, description in scripts_to_run:
        log_message(f"\n📊 Étape: {description}")
        log_message("-" * 40)
        
        if run_script(script_name, description):
            success_count += 1
        else:
            error_count += 1
            log_message(f"⚠️ Continuer malgré l'erreur...", "WARNING")
        
        # Pause entre les scripts pour éviter la surcharge API
        if script_name != scripts_to_run[-1][0]:
            log_message("⏳ Pause de 5 secondes avant le prochain script...")
            time.sleep(5)
    
    # Résumé final
    elapsed_time = time.time() - start_time
    elapsed_minutes = elapsed_time / 60
    
    log_message("\n" + "=" * 60)
    log_message("📈 RÉSUMÉ DU REFRESH")
    log_message("=" * 60)
    log_message(f"✅ Scripts réussis: {success_count}/{len(scripts_to_run)}")
    log_message(f"❌ Scripts en erreur: {error_count}/{len(scripts_to_run)}")
    log_message(f"⏱️ Durée totale: {elapsed_minutes:.2f} minutes")
    
    # Vérifier les fichiers générés
    log_message("\n📁 Vérification des fichiers de données:")
    # Trouver le répertoire data depuis le dossier scripts
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(project_root, "data")
    
    leagues = ["ligue1_2025_2026", "premier-league_2025_2026", "liga_2025_2026", 
               "serie-a_2025_2026", "bundesliga_2025_2026"]
    
    for league in leagues:
        league_dir = os.path.join(data_dir, league)
        if os.path.exists(league_dir):
            files = [f for f in os.listdir(league_dir) if f.endswith('.json')]
            log_message(f"  📂 {league}: {len(files)} équipes")
        else:
            log_message(f"  ⚠️ {league}: Dossier manquant", "WARNING")
    
    # Sauvegarder le log de refresh
    log_file = os.path.join(data_dir, "last_refresh.json")
    refresh_info = {
        "timestamp": datetime.now().isoformat(),
        "success_count": success_count,
        "error_count": error_count,
        "duration_minutes": round(elapsed_minutes, 2),
        "scripts_executed": [s[0] for s in scripts_to_run]
    }
    
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(refresh_info, f, ensure_ascii=False, indent=2)
        log_message(f"\n📝 Log de refresh sauvegardé: {log_file}")
    except Exception as e:
        log_message(f"⚠️ Impossible de sauvegarder le log: {str(e)}", "WARNING")
    
    log_message("\n✨ REFRESH TERMINÉ!")
    
    return success_count == len(scripts_to_run)

if __name__ == "__main__":
    try:
        success = refresh_all_data()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        log_message("\n⚠️ Refresh interrompu par l'utilisateur", "WARNING")
        sys.exit(1)
    except Exception as e:
        log_message(f"❌ Erreur fatale: {str(e)}", "ERROR")
        sys.exit(1)