# Todo - Plan d'action du projet Stat4Ballers

## ✅ Phase 1 : Documentation et configuration initiale [COMPLÉTÉE]
- [x] Créer les fichiers de documentation de base
- [x] Documenter les IDs des ligues et clubs pour les 3 saisons
- [x] Documenter les 59 statistiques joueurs avec leurs IDs SportMonks
- [x] Documenter les 54 statistiques équipes avec leurs IDs SportMonks
- [x] Définir le contexte complet du projet avec System Prompt
- [x] Créer le fichier Mémoire pour l'historique du projet

## 🚀 Phase 2 : Architecture et setup technique [PROCHAINE ÉTAPE]
- [ ] Initialiser le projet Node.js avec package.json
- [ ] Configurer Git et connexion au repository GitHub
- [ ] Installer les dépendances principales :
  - [ ] Express.js pour le serveur
  - [ ] Axios pour les appels API
  - [ ] Dotenv pour les variables d'environnement
  - [ ] Node-cron pour les tâches automatisées
- [ ] Créer la structure de dossiers :
  ```
  /src
    /api        (modules API SportMonks)
    /controllers (logique métier)
    /models     (modèles de données)
    /routes     (endpoints)
    /scripts    (scripts de rafraîchissement)
    /utils      (fonctions utilitaires)
  /public
    /css        (styles)
    /js         (scripts frontend)
    /images     (logos, assets)
  /views        (templates HTML)
  /data         (cache et backup)
  ```
- [ ] Configurer le fichier .env avec la clé API
- [ ] Créer le .gitignore

## 📡 Phase 3 : Connexion API SportMonks
- [ ] Créer le module de connexion API de base
- [ ] Implémenter la gestion des limites (3000 req/h)
- [ ] Créer un système de queue pour les requêtes
- [ ] Implémenter le retry automatique si limite atteinte
- [ ] Créer les fonctions de récupération :
  - [ ] getLeagueData(leagueId, seasonId)
  - [ ] getTeamData(teamId, seasonId)
  - [ ] getPlayerData(playerId, seasonId)
  - [ ] getTeamSquad(teamId, seasonId)
- [ ] Implémenter le système de cache local
- [ ] **TEST : Récupérer les données de la Ligue 1 2025/2026**

## 💾 Phase 4 : Base de données et modèles
- [ ] Choisir la base de données (MongoDB ou PostgreSQL)
- [ ] Configurer la connexion à la BDD
- [ ] Créer les schémas/modèles :
  - [ ] League (id, name, country, logo, seasons)
  - [ ] Team (id, name, leagueId, logo, venue, statistics)
  - [ ] Player (id, name, teamId, position, nationality, statistics)
  - [ ] Statistics (playerId/teamId, seasonId, data)
- [ ] Implémenter le système de versioning pour rollback
- [ ] Créer les fonctions CRUD pour chaque modèle

## 🔄 Phase 5 : Scripts de récupération et rafraîchissement
- [ ] Script de récupération initiale complète
- [ ] Scripts de rafraîchissement manuel :
  - [ ] refresh:ligue1
  - [ ] refresh:premierleague
  - [ ] refresh:liga
  - [ ] refresh:seriea
  - [ ] refresh:bundesliga
- [ ] Système de backup avant rafraîchissement
- [ ] Fonction de rollback en cas d'erreur
- [ ] Scripts automatiques avec node-cron :
  - [ ] Ligue 1 : lundi/vendredi 21h
  - [ ] Premier League : lundi/vendredi 20h
  - [ ] La Liga : lundi/vendredi 19h
  - [ ] Serie A : lundi/vendredi 18h
  - [ ] Bundesliga : lundi/vendredi 17h

## 🎨 Phase 6 : Frontend - Structure et design
- [ ] Créer la structure HTML5 de base
- [ ] Implémenter le design system :
  - [ ] Variables CSS (couleurs, typographie)
  - [ ] Grille responsive (mobile-first)
  - [ ] Composants réutilisables
- [ ] Créer la homepage minimaliste :
  - [ ] Header avec logo et navigation
  - [ ] Barre de recherche avec autocomplétion
  - [ ] Module de comparaison (jusqu'à 4 joueurs)
  - [ ] Menu des 5 championnats avec logos
  - [ ] Footer avec liens utiles
- [ ] Créer les templates de pages :
  - [ ] Page championnat
  - [ ] Page club
  - [ ] Page joueur
  - [ ] Page de comparaison

## 📊 Phase 7 : Visualisation des données
- [ ] Intégrer Chart.js pour les radar charts
- [ ] Créer les composants de visualisation :
  - [ ] Radar chart "General statistics"
  - [ ] Radar chart "Offensive creativity"
  - [ ] Radar chart "Defensive commitment"
  - [ ] Radar chart "Specific goalkeepers"
- [ ] Implémenter la logique de sélection (gardien vs joueur)
- [ ] Créer la vue comparative (4 joueurs côte à côte)
- [ ] Ajouter la vue cumulative 3 saisons
- [ ] Optimiser les performances des graphiques

## 🌍 Phase 8 : Système multilingue
- [ ] Installer et configurer i18n
- [ ] Créer les fichiers de traduction :
  - [ ] en.json (anglais - par défaut)
  - [ ] fr.json (français)
  - [ ] es.json (espagnol)
  - [ ] pt.json (portugais)
- [ ] Traduire tous les labels et textes
- [ ] Implémenter le sélecteur de langue (drapeaux)
- [ ] Sauvegarder la préférence utilisateur

## 🔍 Phase 9 : SEO et optimisation
- [ ] Implémenter les balises meta dynamiques
- [ ] Ajouter les structured data (schema.org) :
  - [ ] SportsTeam
  - [ ] Person (pour les joueurs)
  - [ ] SportsEvent
- [ ] Optimiser les URLs (slugs SEO-friendly)
- [ ] Créer le sitemap.xml dynamique
- [ ] Implémenter le robots.txt
- [ ] Optimiser les performances :
  - [ ] Lazy loading des images
  - [ ] Compression des assets
  - [ ] Mise en cache côté client
  - [ ] Minification CSS/JS

## 🔧 Phase 10 : Fonctionnalités avancées
- [ ] Système de recherche avancée avec filtres
- [ ] Autocomplétion intelligente (ElasticSearch ?)
- [ ] Historique de navigation utilisateur
- [ ] Favoris (joueurs/équipes)
- [ ] Notifications de mise à jour des stats
- [ ] Export des données (PDF/CSV)
- [ ] API publique avec documentation

## ✅ Phase 11 : Tests et qualité
- [ ] Tests unitaires (Jest)
- [ ] Tests d'intégration API
- [ ] Tests E2E (Cypress)
- [ ] Tests de performance
- [ ] Tests responsive (mobile/tablet/desktop)
- [ ] Tests cross-browser
- [ ] Audit SEO
- [ ] Audit accessibilité (WCAG)

## 🚀 Phase 12 : Déploiement et maintenance
- [ ] Choisir l'hébergeur (Vercel, Netlify, AWS ?)
- [ ] Configurer le CI/CD (GitHub Actions)
- [ ] Mise en place du monitoring (Sentry)
- [ ] Documentation technique complète
- [ ] Documentation utilisateur
- [ ] Plan de backup automatique
- [ ] Procédures de maintenance
- [ ] Support et mises à jour

## 📝 Notes importantes
- **Priorité 1** : Commencer par la Ligue 1 pour valider l'architecture
- **Priorité 2** : Homepage et système de recherche
- **Priorité 3** : Pages joueurs avec radar charts
- Respecter strictement les libellés des statistiques
- Maintenir un code propre et documenté
- Faire des commits réguliers et descriptifs

---
*Dernière mise à jour : 14/09/2025*
*Prochaine action : Démarrer la Phase 2 - Setup technique*