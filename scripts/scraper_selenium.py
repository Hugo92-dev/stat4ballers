from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import time
from datetime import datetime
import os

class FBrefSeleniumScraper:
    def __init__(self):
        print("🔧 Configuration de Chrome...")
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        self.clubs_ligue1 = {
            'Paris-SG': 'https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats',
        }
    
    def scrape_club(self, club_name, url):
        print(f"\n🔍 Scraping {club_name}...")
        
        try:
            print("⏳ Chargement de la page...")
            self.driver.get(url)
            time.sleep(10)
            
            print("🔍 Recherche de la table...")
            
            # Chercher toutes les tables
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            print(f"📊 {len(tables)} tables trouvées sur la page")
            
            # Chercher la bonne table (celle avec les stats des joueurs)
            players_table = None
            for table in tables:
                try:
                    # Chercher une table qui contient "Player" dans l'en-tête
                    headers = table.find_elements(By.TAG_NAME, "th")
                    for header in headers:
                        if "Player" in header.text or "Joueur" in header.text:
                            players_table = table
                            print("✅ Table des joueurs trouvée!")
                            break
                    if players_table:
                        break
                except:
                    continue
            
            if not players_table:
                print("❌ Table des joueurs non trouvée")
                return []
            
            players = []
            
            # Récupérer toutes les lignes du tbody
            try:
                tbody = players_table.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")
                print(f"📊 {len(rows)} lignes trouvées")
            except:
                print("❌ Pas de tbody trouvé")
                return []
            
            for i, row in enumerate(rows):
                try:
                    # Chercher le nom du joueur dans le th
                    player_th = row.find_elements(By.TAG_NAME, "th")
                    if not player_th:
                        continue
                    
                    # Le premier th contient généralement le nom du joueur
                    player_name = None
                    for th in player_th:
                        text = th.text.strip()
                        if text and text != "" and "Squad Total" not in text:
                            # Essayer de trouver un lien
                            try:
                                link = th.find_element(By.TAG_NAME, "a")
                                player_name = link.text.strip()
                            except:
                                player_name = text
                            break
                    
                    if not player_name:
                        continue
                    
                    print(f"  👤 Joueur trouvé: {player_name}")
                    
                    # Récupérer les stats depuis les td
                    tds = row.find_elements(By.TAG_NAME, "td")
                    
                    # Fonction pour obtenir une stat par index
                    def get_td_value(index, default="0"):
                        try:
                            if index < len(tds):
                                value = tds[index].text.strip()
                                return value if value else default
                            return default
                        except:
                            return default
                    
                    # Créer l'objet joueur avec les stats basiques
                    player_data = {
                        'nom': player_name,
                        'club': club_name,
                        'poste': get_td_value(1, 'N/A'),  # Position est souvent en 2e colonne
                        'age': get_td_value(2, '0'),      # Age en 3e colonne
                        'matchs_joues': int(get_td_value(3, '0') or '0'),
                        'titularisations': int(get_td_value(4, '0') or '0'),
                        'minutes': int(get_td_value(5, '0').replace(',', '') or '0'),
                        'buts': int(get_td_value(7, '0') or '0'),
                        'passes_decisives': int(get_td_value(8, '0') or '0'),
                        'cartons_jaunes': int(get_td_value(13, '0') or '0'),
                        'cartons_rouges': int(get_td_value(14, '0') or '0'),
                        'xg': float(get_td_value(15, '0') or '0'),
                        'xa': float(get_td_value(17, '0') or '0'),
                        
                        # Stats qu'on récupèrera plus tard depuis d'autres pages
                        'points_gagnes_par_match': 0.0,
                        'jours_absents': 0,
                        'valeur_marchande': 0,
                        'total_tirs': 0,
                        'tirs_cadres_pct': 0.0,
                        'ratio_penalty': 0.0,
                        'courses_avant': 0,
                        'interceptions': 0,
                        'tacles_reussis': 0,
                        'duels_aeriens_gagnes': 0,
                        'pressings_reussis': 0,
                        'fautes_subies': 0,
                        'fautes_commises': 0,
                        'touches_balle': 0,
                        'dribbles_reussis': 0,
                        'total_passes': 0,
                        'passes_cles': 0,
                        'passes_avant': 0,
                        'passes_courtes_pct': 0.0,
                        'passes_longues_pct': 0.0,
                        'centres_reussis': 0,
                        
                        'last_update': datetime.now().isoformat()
                    }
                    
                    players.append(player_data)
                    print(f"    ✅ Stats récupérées pour {player_name}")
                    
                except Exception as e:
                    print(f"    ⚠️ Erreur ligne {i}: {str(e)[:50]}")
                    continue
            
            print(f"\n✅ Total: {len(players)} joueurs récupérés")
            return players
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return []
    
    def save_to_json(self, data):
        output_path = os.path.join('public', 'data', 'ligue1_players_real.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'last_update': datetime.now().isoformat(),
                'total_players': len(data),
                'players': data
            }, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Données sauvegardées: {output_path}")
        print(f"📊 {len(data)} joueurs au total")
    
    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    print("🚀 Scraping FBref avec Selenium...")
    print("=" * 50)
    
    scraper = FBrefSeleniumScraper()
    
    try:
        psg_players = scraper.scrape_club('Paris-SG', scraper.clubs_ligue1['Paris-SG'])
        
        if psg_players:
            scraper.save_to_json(psg_players)
            print("\n🎉 SUCCÈS !")
            print(f"Premiers joueurs récupérés:")
            for p in psg_players[:3]:
                print(f"  - {p['nom']} ({p['poste']}) - {p['buts']} buts")
        else:
            print("\n⚠️ Aucun joueur récupéré")
        
        time.sleep(5)
        
    finally:
        scraper.close()
        print("✅ Terminé")