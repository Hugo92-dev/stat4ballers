#!/usr/bin/env python3
"""Script de mise à jour rapide sans compilation"""

import sys
import os
from pathlib import Path

# Importer le script principal
sys.path.append('.')
from safe_update_all_data import *

def main_no_compile():
    """Version sans test de compilation"""
    logging.info("=" * 60)
    logging.info("[START] DÉBUT DE LA MISE À JOUR RAPIDE")
    logging.info("=" * 60)
    
    start_time = time.time()
    backup_path = None
    success = True
    
    try:
        # ÉTAPE 1: Créer un backup
        backup_path = create_backup()
        
        # ÉTAPE 2: Traiter chaque ligue
        for league_id, league_info in TOP_5_LEAGUES.items():
            logging.info(f"\n--- Traitement de {league_info['name']} ---")
            
            league_data = {
                'teams': {},
                'stats': {}
            }
            
            # Récupérer la saison actuelle
            current_season_id = league_info['seasons']['2025/2026']
            
            # Récupérer les effectifs
            teams = get_team_squads_safe(league_id, current_season_id, league_info)
            
            if teams is None:
                logging.error(f"[ERREUR] Échec pour {league_info['name']}")
                continue
            
            league_data['teams'] = teams
            
            # Générer les fichiers TypeScript
            if not generate_typescript_files_safe(league_data, league_info):
                logging.error(f"[ERREUR] Génération échouée pour {league_info['name']}")
                success = False
                break
        
        # PAS DE TEST DE COMPILATION
        logging.info("[INFO] Compilation skippée - mise à jour rapide")
        
        if not success and backup_path:
            restore_backup(backup_path)
            logging.error("[ATTENTION] Mise à jour annulée, backup restauré")
        else:
            logging.info("[SUCCESS] Mise à jour réussie!")
        
    except Exception as e:
        logging.error(f"[ERREUR CRITIQUE]: {e}")
        if backup_path:
            restore_backup(backup_path)
        success = False
    
    elapsed_time = time.time() - start_time
    logging.info("\n" + "=" * 60)
    if success:
        logging.info(f"[SUCCESS] MISE À JOUR TERMINÉE EN {elapsed_time:.2f} SECONDES")
    else:
        logging.info(f"[FAIL] MISE À JOUR ÉCHOUÉE APRÈS {elapsed_time:.2f} SECONDES")
    logging.info("=" * 60)
    
    # Créer un fichier de statut
    status_file = SCRIPT_DIR / 'last_update.json'
    status_file.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'duration': elapsed_time,
        'success': success
    }, indent=2))
    
    return success

if __name__ == "__main__":
    sys.exit(0 if main_no_compile() else 1)