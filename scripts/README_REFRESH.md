# 🔄 Guide du système de refresh des données

## 📋 Vue d'ensemble

Le système de refresh permet de maintenir à jour les effectifs et statistiques des joueurs pour les 5 grands championnats européens :
- Ligue 1
- Premier League  
- La Liga
- Serie A
- Bundesliga

## 🎯 Commandes disponibles

### 1. Refresh Manuel Interactif
```bash
npm run refresh
```
Lance un assistant interactif qui vous guide à travers le processus de refresh. Idéal pour les mises à jour ponctuelles.

### 2. Refresh Manuel Direct
```bash
npm run refresh:now
```
Lance directement le refresh sans interaction. Utile pour les scripts ou automatisations personnalisées.

### 3. Scheduler Automatique
```bash
npm run refresh:auto
```
Démarre le scheduler qui exécutera automatiquement le refresh :
- **Tous les lundis à 21h00**
- **Tous les vendredis à 21h00**
- Heure française (Europe/Paris)

Pour lancer le scheduler en arrière-plan (Windows) :
```bash
start /B npm run refresh:auto
```

## 📂 Structure des scripts

- `scripts/refresh_all_data.py` : Script principal de refresh
- `scripts/manual_refresh.js` : Interface interactive pour le refresh manuel
- `scripts/scheduler.js` : Scheduler automatique avec node-cron

## 📊 Données rafraîchies

Le refresh met à jour :
1. **Les effectifs complets** de chaque club
2. **Les statistiques détaillées** de chaque joueur
3. **Les photos et informations** des joueurs

Les données sont sauvegardées dans :
```
data/
├── ligue1_2025_2026/
├── premier-league_2025_2026/
├── liga_2025_2026/
├── serie-a_2025_2026/
└── bundesliga_2025_2026/
```

## 📝 Logs et suivi

### Logs du scheduler
Les logs du scheduler automatique sont sauvegardés dans :
```
logs/scheduler.log
```

### Dernier refresh
Les informations du dernier refresh sont dans :
```
data/last_refresh.json
```

## 🚀 Démarrage rapide

1. **Pour un refresh immédiat :**
   ```bash
   npm run refresh
   ```

2. **Pour automatiser les refreshs :**
   ```bash
   npm run refresh:auto
   # Laisser tourner en arrière-plan
   ```

## ⚙️ Configuration avancée

### Modifier les horaires du scheduler
Éditer `scripts/scheduler.js` et modifier la ligne :
```javascript
const SCHEDULE = '0 21 * * 1,5'; // Format cron
```

### Personnaliser les scripts exécutés
Éditer `scripts/refresh_all_data.py` et modifier la liste `scripts_to_run`.

## 🔧 Dépannage

### Le scheduler ne se lance pas
Vérifier que node-cron est installé :
```bash
npm install node-cron --legacy-peer-deps
```

### Erreurs Python
Vérifier que Python est installé et dans le PATH :
```bash
python --version
```

### Problèmes d'encodage
Les scripts sont configurés pour UTF-8. En cas de problème sur Windows, vérifier que la variable d'environnement `PYTHONIOENCODING` est définie à `utf-8`.

## 📌 Notes importantes

- Le refresh complet peut prendre **5-10 minutes**
- Une pause de 5 secondes est appliquée entre chaque script pour éviter la surcharge de l'API
- Les données sont écrasées à chaque refresh (pas d'historique conservé)