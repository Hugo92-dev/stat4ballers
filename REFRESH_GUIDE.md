# 🔄 Guide Complet du Système de Refresh Stat4Ballers

## 📋 Vue d'ensemble

Le système de refresh permet de maintenir à jour les effectifs et statistiques des joueurs pour les 5 grands championnats européens. Il propose des modes automatiques et manuels avec des horaires optimisés par championnat.

## 🎯 Commandes de Refresh Manuel par Championnat

### Refresh individuel par championnat
```bash
# 🇫🇷 Ligue 1
npm run refresh:ligue1

# 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League
npm run refresh:premier

# 🇪🇸 La Liga
npm run refresh:liga

# 🇮🇹 Serie A
npm run refresh:serie

# 🇩🇪 Bundesliga
npm run refresh:bundesliga
```

### Refresh de tous les championnats
```bash
# Refresh complet robuste avec gestion d'erreurs
npm run refresh:now

# Reprendre un refresh interrompu
npm run refresh:resume
```

## 🤖 Scheduler Automatique avec Horaires Décalés

### Démarrer le scheduler avancé
```bash
npm run refresh:auto
```

### Planning automatique
Le scheduler exécute automatiquement les refresh aux horaires suivants (heure française) :

| Championnat | Lundi | Vendredi |
|------------|-------|----------|
| 🇩🇪 Bundesliga | 17h00 | 17h00 |
| 🇮🇹 Serie A | 18h00 | 18h00 |
| 🇪🇸 La Liga | 19h00 | 19h00 |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League | 20h00 | 20h00 |
| 🇫🇷 Ligue 1 | 21h00 | 21h00 |

### Pourquoi ces horaires décalés ?
- **Optimisation des performances** : Évite la surcharge du serveur
- **Respect des limites API** : Étale les requêtes dans le temps
- **Maintenance simplifiée** : Permet d'identifier facilement les problèmes par championnat

## 🧪 Mode Test

### Tester le refresh d'un championnat via le scheduler
```bash
# Test Ligue 1
npm run refresh:test:ligue1

# Test Premier League  
npm run refresh:test:premier

# Test La Liga
npm run refresh:test:liga

# Test Serie A
npm run refresh:test:serie

# Test Bundesliga
npm run refresh:test:bundesliga
```

### Test rapide sur un club (Lyon)
```bash
npm run refresh:test
```

## 📊 Données Rafraîchies

Chaque refresh met à jour :
- ✅ **Effectifs complets** : Nouveaux transferts, départs, arrivées
- 📈 **Statistiques des joueurs** : Buts, passes, cartons, temps de jeu
- 🖼️ **Photos et informations** : Images, âge, nationalité, position
- 📍 **Informations du club** : Stade, capacité, année de fondation

## 📂 Structure des Données

Les données sont organisées par championnat et saison :
```
data/
├── ligue1_2025_2026/
│   ├── paris-saint-germain.json
│   ├── olympique-marseille.json
│   ├── olympique-lyonnais.json
│   └── ...
├── premier-league_2025_2026/
├── liga_2025_2026/
├── serie-a_2025_2026/
└── bundesliga_2025_2026/
```

## 📝 Logs et Monitoring

### Emplacement des logs
```
logs/
├── scheduler_advanced.log     # Log principal du scheduler
├── refresh_20250827.log       # Logs quotidiens
├── last_refresh_ligue1.log    # Dernier refresh Ligue 1
├── last_refresh_premier_league.log
├── last_refresh_liga.log
├── last_refresh_serie_a.log
└── last_refresh_bundesliga.log
```

### Fichier de statut
```
data/last_refresh.json  # Informations sur le dernier refresh global
```

## 🚀 Démarrage Rapide

### Pour un refresh manuel immédiat de la Ligue 1
```bash
npm run refresh:ligue1
```

### Pour automatiser tous les refresh
```bash
npm run refresh:auto
# Laisser tourner en arrière-plan
```

### Pour lancer en arrière-plan (Windows)
```bash
start /B npm run refresh:auto
```

### Pour lancer en arrière-plan (Linux/Mac)
```bash
nohup npm run refresh:auto > refresh.log 2>&1 &
```

## ⚙️ Configuration Avancée

### Modifier les horaires du scheduler
Éditer `scripts/scheduler_advanced.js` et modifier les horaires dans `LEAGUE_SCHEDULES`.

### Ajouter/Retirer des équipes
Éditer les scripts `refresh_[championnat].py` et modifier les dictionnaires `[LEAGUE]_TEAMS`.

## 🔧 Dépannage

### Le refresh échoue avec une erreur 404
- Vérifier que les IDs des équipes sont corrects
- S'assurer que la saison est active sur l'API

### Problèmes d'encodage sur Windows
Les scripts sont configurés pour UTF-8. Si problème :
```bash
set PYTHONIOENCODING=utf-8
```

### Le scheduler ne se lance pas
Vérifier que node-cron est installé :
```bash
npm install node-cron --legacy-peer-deps
```

## 📌 Exemples d'Usage

### Scénario 1 : Mise à jour avant le weekend
```bash
# Vendredi 16h30 - Rafraîchir tous les championnats manuellement
npm run refresh:bundesliga  # 5 min
npm run refresh:serie       # 5 min  
npm run refresh:liga        # 5 min
npm run refresh:premier     # 5 min
npm run refresh:ligue1      # 5 min
```

### Scénario 2 : Automatisation complète
```bash
# Une seule fois, lancer le scheduler
npm run refresh:auto
# Le laisser tourner, il s'occupera de tout
```

### Scénario 3 : Mise à jour urgente d'un championnat
```bash
# Mise à jour immédiate de la Premier League
npm run refresh:premier
```

## 💡 Conseils

1. **Ne pas exécuter plusieurs refresh simultanément** pour éviter les limites API
2. **Vérifier les logs après chaque refresh** pour détecter les problèmes
3. **Faire un backup régulier** du dossier `data/`
4. **Tester d'abord sur un championnat** avant de lancer un refresh global

## 📊 Statistiques Moyennes

| Championnat | Temps moyen | Nombre d'équipes | Joueurs |
|------------|------------|------------------|---------|
| 🇩🇪 Bundesliga | ~4-5 min | 18 | ~450 |
| 🇮🇹 Serie A | ~5-6 min | 20 | ~500 |
| 🇪🇸 La Liga | ~5-6 min | 20 | ~500 |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League | ~5-6 min | 20 | ~500 |
| 🇫🇷 Ligue 1 | ~4-5 min | 18-19 | ~450 |

## 🆘 Support

En cas de problème, vérifier :
1. Les logs dans `logs/`
2. La connexion internet
3. Les limites API (max 3000 requêtes/heure)
4. L'espace disque disponible