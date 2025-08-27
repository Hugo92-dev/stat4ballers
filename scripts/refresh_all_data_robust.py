#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de refresh ROBUSTE et COMPLET pour tous les championnats
Gère les timeouts, les erreurs et les reprises
"""

import subprocess
import sys
import time
from datetime import datetime
import os
import json
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError

# Fix pour l'encodage UTF-8 sur Windows
sys.stdout.reconfigure(encoding='utf-8')

class RefreshManager:
    def __init__(self):
        self.start_time = time.time()
        self.success_count = 0
        self.error_count = 0
        self.skipped_count = 0
        self.results = []
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.scripts_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.project_root, "data")
        self.state_file = os.path.join(self.data_dir, "refresh_state.json")
        
    def log_message(self, message, level="INFO"):
        """Affiche un message horodaté"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
        # Sauvegarder aussi dans un fichier log
        log_dir = os.path.join(self.project_root, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"refresh_{datetime.now().strftime('%Y%m%d')}.log")
        
        try:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] [{level}] {message}\n")
        except:
            pass
    
    def load_state(self):
        """Charge l'état précédent du refresh si disponible"""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return None
    
    def save_state(self, current_script=None, status="in_progress"):
        """Sauvegarde l'état actuel du refresh"""
        state = {
            "timestamp": datetime.now().isoformat(),
            "current_script": current_script,
            "status": status,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "skipped_count": self.skipped_count,
            "results": self.results
        }
        
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.log_message(f"Impossible de sauvegarder l'état: {str(e)}", "WARNING")
    
    def run_script_with_timeout(self, script_name, description, timeout_minutes=10):
        """Exécute un script Python avec timeout et gestion d'erreurs avancée"""
        
        self.log_message(f"🔄 {description}...")
        self.save_state(script_name, "running")
        
        script_path = os.path.join(self.scripts_dir, script_name)
        if not os.path.exists(script_path):
            self.log_message(f"❌ Script introuvable: {script_name}", "ERROR")
            self.error_count += 1
            self.results.append({
                "script": script_name,
                "status": "not_found",
                "duration": 0
            })
            return False
        
        start = time.time()
        timeout_seconds = timeout_minutes * 60
        
        try:
            # Lancer le processus
            process = subprocess.Popen(
                [sys.executable, script_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                cwd=self.scripts_dir
            )
            
            # Attendre avec timeout
            try:
                stdout, stderr = process.communicate(timeout=timeout_seconds)
                
                duration = time.time() - start
                
                if process.returncode == 0:
                    self.log_message(f"✅ {description} - Terminé en {duration:.1f}s", "SUCCESS")
                    if stdout and len(stdout) < 1000:  # Afficher seulement si court
                        print(stdout)
                    self.success_count += 1
                    self.results.append({
                        "script": script_name,
                        "status": "success",
                        "duration": duration
                    })
                    return True
                else:
                    self.log_message(f"❌ {description} - Échec (code {process.returncode})", "ERROR")
                    if stderr:
                        print(f"Erreur: {stderr[:500]}")  # Limiter l'affichage
                    self.error_count += 1
                    self.results.append({
                        "script": script_name,
                        "status": "failed",
                        "duration": duration,
                        "error": stderr[:200] if stderr else None
                    })
                    return False
                    
            except subprocess.TimeoutExpired:
                self.log_message(f"⏱️ {description} - Timeout après {timeout_minutes} minutes", "WARNING")
                process.kill()
                process.wait()
                self.error_count += 1
                self.results.append({
                    "script": script_name,
                    "status": "timeout",
                    "duration": timeout_seconds
                })
                return False
                
        except Exception as e:
            duration = time.time() - start
            self.log_message(f"❌ {description} - Exception: {str(e)}", "ERROR")
            self.error_count += 1
            self.results.append({
                "script": script_name,
                "status": "exception",
                "duration": duration,
                "error": str(e)[:200]
            })
            return False
    
    def refresh_all_data(self, resume=False):
        """Rafraîchit toutes les données avec gestion de reprise"""
        
        self.log_message("=" * 60)
        self.log_message("🚀 DÉBUT DU REFRESH ROBUSTE DES DONNÉES")
        self.log_message("=" * 60)
        
        # Scripts à exécuter avec leurs timeouts personnalisés
        scripts_to_run = [
            ("fetch_all_leagues_all_players_optimized.py", "Récupération de tous les joueurs (5 championnats)", 15),
            ("fetch_all_teams_stats.py", "Récupération des statistiques détaillées", 20),
            ("fetch_complete_all_teams_all_players.py", "Mise à jour complète des effectifs", 20),
        ]
        
        # Vérifier s'il faut reprendre
        start_index = 0
        if resume:
            state = self.load_state()
            if state and state.get('status') == 'in_progress':
                self.log_message("📌 Reprise du refresh précédent...", "INFO")
                self.success_count = state.get('success_count', 0)
                self.error_count = state.get('error_count', 0)
                self.results = state.get('results', [])
                
                # Trouver où reprendre
                last_script = state.get('current_script')
                for i, (script, _, _) in enumerate(scripts_to_run):
                    if script == last_script:
                        start_index = i + 1
                        self.log_message(f"  Reprise après: {last_script}", "INFO")
                        break
        
        # Exécution des scripts
        total_scripts = len(scripts_to_run)
        
        for i in range(start_index, total_scripts):
            script_name, description, timeout = scripts_to_run[i]
            
            self.log_message(f"\n📊 Étape {i+1}/{total_scripts}: {description}")
            self.log_message("-" * 40)
            
            success = self.run_script_with_timeout(script_name, description, timeout)
            
            # Pause entre les scripts pour éviter la surcharge API
            if i < total_scripts - 1:
                pause_seconds = 5
                self.log_message(f"⏳ Pause de {pause_seconds} secondes avant le prochain script...")
                time.sleep(pause_seconds)
            
            # Sauvegarder l'état après chaque script
            self.save_state(script_name, "completed" if success else "failed")
        
        # Finaliser
        self.finalize_refresh()
    
    def finalize_refresh(self):
        """Finalise le refresh et génère le rapport"""
        
        elapsed_time = time.time() - self.start_time
        elapsed_minutes = elapsed_time / 60
        
        self.log_message("\n" + "=" * 60)
        self.log_message("📈 RÉSUMÉ DU REFRESH ROBUSTE")
        self.log_message("=" * 60)
        
        total_scripts = self.success_count + self.error_count + self.skipped_count
        
        self.log_message(f"✅ Scripts réussis: {self.success_count}/{total_scripts}")
        self.log_message(f"❌ Scripts en erreur: {self.error_count}/{total_scripts}")
        if self.skipped_count > 0:
            self.log_message(f"⏭️ Scripts ignorés: {self.skipped_count}/{total_scripts}")
        self.log_message(f"⏱️ Durée totale: {elapsed_minutes:.2f} minutes")
        
        # Détails par script
        if self.results:
            self.log_message("\n📋 Détails par script:")
            for result in self.results:
                status_icon = {
                    "success": "✅",
                    "failed": "❌",
                    "timeout": "⏱️",
                    "exception": "💥",
                    "not_found": "❓",
                    "skipped": "⏭️"
                }.get(result['status'], "❓")
                
                duration_str = f"{result['duration']:.1f}s" if result['duration'] < 60 else f"{result['duration']/60:.1f}m"
                self.log_message(f"  {status_icon} {result['script']}: {result['status']} ({duration_str})")
        
        # Vérifier les fichiers générés
        self.verify_data_files()
        
        # Sauvegarder le rapport final
        self.save_final_report(elapsed_minutes)
        
        # Nettoyer l'état temporaire
        if os.path.exists(self.state_file):
            try:
                os.remove(self.state_file)
            except:
                pass
        
        self.log_message("\n✨ REFRESH TERMINÉ!")
        
        return self.error_count == 0
    
    def verify_data_files(self):
        """Vérifie les fichiers de données générés"""
        
        self.log_message("\n📁 Vérification des fichiers de données:")
        
        leagues = [
            ("ligue1_2025_2026", 18),  # Ligue 1 a normalement 18 équipes
            ("premier-league_2025_2026", 20),
            ("liga_2025_2026", 20),
            ("serie-a_2025_2026", 20),
            ("bundesliga_2025_2026", 18)
        ]
        
        total_teams = 0
        total_players = 0
        
        for league, expected_teams in leagues:
            league_dir = os.path.join(self.data_dir, league)
            if os.path.exists(league_dir):
                files = [f for f in os.listdir(league_dir) if f.endswith('.json')]
                total_teams += len(files)
                
                # Compter les joueurs
                players_count = 0
                for file in files[:3]:  # Vérifier seulement les 3 premiers pour la vitesse
                    try:
                        with open(os.path.join(league_dir, file), 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if 'players' in data:
                                players_count += len(data['players'])
                    except:
                        pass
                
                avg_players = players_count / min(3, len(files)) if files else 0
                estimated_total = int(avg_players * len(files))
                total_players += estimated_total
                
                status = "✅" if len(files) >= expected_teams - 2 else "⚠️"
                self.log_message(f"  {status} {league}: {len(files)}/{expected_teams} équipes (~{estimated_total} joueurs)")
            else:
                self.log_message(f"  ❌ {league}: Dossier manquant", "WARNING")
        
        self.log_message(f"\n📊 Total global: {total_teams} équipes, ~{total_players} joueurs")
    
    def save_final_report(self, elapsed_minutes):
        """Sauvegarde le rapport final du refresh"""
        
        report_file = os.path.join(self.data_dir, "last_refresh.json")
        report = {
            "timestamp": datetime.now().isoformat(),
            "success_count": self.success_count,
            "error_count": self.error_count,
            "skipped_count": self.skipped_count,
            "duration_minutes": round(elapsed_minutes, 2),
            "results": self.results,
            "status": "success" if self.error_count == 0 else "partial"
        }
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            self.log_message(f"\n📝 Rapport de refresh sauvegardé: {report_file}")
        except Exception as e:
            self.log_message(f"⚠️ Impossible de sauvegarder le rapport: {str(e)}", "WARNING")

def main():
    """Point d'entrée principal avec gestion des arguments"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='Refresh robuste des données Stat4Ballers')
    parser.add_argument('--resume', action='store_true', help='Reprendre un refresh interrompu')
    parser.add_argument('--timeout', type=int, default=60, help='Timeout global en minutes (défaut: 60)')
    
    args = parser.parse_args()
    
    manager = RefreshManager()
    
    # Gestion de l'interruption
    def signal_handler(signum, frame):
        manager.log_message("\n⚠️ Refresh interrompu par l'utilisateur", "WARNING")
        manager.save_state(status="interrupted")
        manager.log_message("💾 État sauvegardé. Utilisez --resume pour reprendre.", "INFO")
        sys.exit(1)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        success = manager.refresh_all_data(resume=args.resume)
        sys.exit(0 if success else 1)
    except Exception as e:
        manager.log_message(f"❌ Erreur fatale: {str(e)}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()