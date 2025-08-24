# 🔄 Système de Mise à Jour Automatique des Données

## Vue d'ensemble

Ce système permet de maintenir à jour automatiquement :
- **Les effectifs des équipes** (nouveaux joueurs, transferts)
- **Les statistiques des joueurs** (après chaque match)
- **Les fiches joueurs** (création automatique pour les nouveaux)
- **La base de données de recherche**

## 🚀 Mise en place

### Option 1: GitHub Actions (Recommandé)

1. **Configurer le secret API** :
   - Aller dans Settings > Secrets and variables > Actions
   - Créer un nouveau secret `SPORTMONKS_API_KEY` avec votre clé API

2. **Le workflow se déclenchera automatiquement** :
   - Tous les lundis à 21h
   - Tous les vendredis à 21h
   - Ou manuellement via l'onglet Actions

### Option 2: Windows Task Scheduler (Local)

1. **Installer la tâche planifiée** :
   ```powershell
   # Ouvrir PowerShell en tant qu'administrateur
   cd C:\Users\hugo\stat4ballers\scripts
   .\setup_task_scheduler.ps1
   ```

2. **Vérifier l'installation** :
   - Ouvrir le Planificateur de tâches Windows
   - Naviguer vers le dossier "Stat4Ballers"
   - Vous devriez voir 2 tâches (Monday et Friday)

### Option 3: Exécution manuelle

```bash
cd scripts
python update_all_data.py
```

## 📊 Ce que fait le script

### 1. Récupération des effectifs
- Interroge l'API SportMonks pour chaque championnat
- Récupère tous les joueurs actuels de chaque équipe
- Détecte automatiquement les nouveaux joueurs

### 2. Mise à jour des statistiques
- Récupère les stats des 3 dernières saisons
- Stats détaillées : buts, passes, cartons, etc.
- Stats spécifiques par position (gardiens, défenseurs, etc.)

### 3. Génération des fichiers TypeScript
Pour chaque championnat, génère :
- `data/{league}Teams.ts` : Effectifs complets
- `data/{league}PlayersCompleteStats.ts` : Statistiques détaillées

### 4. Intégration des nouveaux joueurs
- Création automatique de la fiche joueur
- Ajout dans la base de recherche
- Génération du slug URL
- Récupération de la photo officielle

## 🔍 Monitoring

### Logs
Les logs sont créés dans `scripts/` :
- `update_YYYYMMDD_HHMMSS.log` : Log détaillé de chaque exécution
- `last_update.json` : Statut de la dernière mise à jour

### Vérification du statut
```python
# Voir la dernière mise à jour
import json
with open('scripts/last_update.json', 'r') as f:
    status = json.load(f)
    print(f"Dernière mise à jour: {status['timestamp']}")
    print(f"Durée: {status['duration']}s")
    print(f"Succès: {status['success']}")
```

## ⚠️ Gestion des erreurs

### Limites de l'API
- Le script gère automatiquement les erreurs 429 (rate limiting)
- Retry automatique avec backoff exponentiel
- Parallélisation limitée à 5 requêtes simultanées

### Nouveaux joueurs sans stats
- Les nouveaux joueurs sont ajoutés même sans statistiques
- Les stats seront mises à jour lors de la prochaine exécution

### Échec de compilation TypeScript
- Le script continue même si la compilation échoue
- Les erreurs sont loggées pour correction manuelle

## 🛠️ Personnalisation

### Modifier les horaires
**GitHub Actions** : Éditer `.github/workflows/update-data.yml`
```yaml
schedule:
  - cron: '0 20 * * 1'  # Lundi 21h
  - cron: '0 20 * * 5'  # Vendredi 21h
```

**Windows** : Réexécuter `setup_task_scheduler.ps1` avec les nouveaux horaires

### Ajouter un championnat
Éditer `update_all_data.py` et ajouter dans `TOP_5_LEAGUES` :
```python
NEW_LEAGUE_ID: {
    "name": "League Name",
    "slug": "league-slug",
    "dataFile": "leagueTeams",
    "seasons": {
        "2025/2026": SEASON_ID,
        # ...
    }
}
```

## 📈 Performance

- **Durée moyenne** : 10-15 minutes pour tous les championnats
- **Données traitées** : ~2500 joueurs, ~15000 statistiques
- **Taille des fichiers** : ~5-10 MB au total

## 🔒 Sécurité

- La clé API n'est jamais commitée dans le code
- Utiliser les secrets GitHub Actions ou variables d'environnement
- Les logs ne contiennent pas d'informations sensibles

## 📞 Support

En cas de problème :
1. Vérifier les logs dans `scripts/update_*.log`
2. Vérifier le statut de l'API SportMonks
3. S'assurer que la clé API est valide et a les bonnes permissions