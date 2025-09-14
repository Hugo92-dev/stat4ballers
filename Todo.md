# Todo - Plan d'action du projet Stat4Ballers

## ✅ Phase 1 : Documentation et configuration initiale [COMPLÉTÉE]
- [x] Créer les fichiers de documentation de base
- [x] Documenter les IDs des ligues et clubs pour les 3 saisons
- [x] Documenter les 59 statistiques joueurs avec leurs IDs SportMonks
- [x] Documenter les 54 statistiques équipes avec leurs IDs SportMonks
- [x] Définir le contexte complet du projet avec System Prompt
- [x] Créer le fichier Mémoire pour l'historique du projet

## ✅ Phase 2 : Architecture et setup technique [COMPLÉTÉ]
- [x] Initialiser le projet Node.js avec package.json
- [x] Configurer Git et connexion au repository GitHub
- [x] Installer les dépendances principales :
  - [x] Express.js pour le serveur
  - [x] Axios pour les appels API
  - [x] Dotenv pour les variables d'environnement
  - [x] Node-cron pour les tâches automatisées
- [x] Créer la structure de dossiers complète
- [x] Configurer le fichier .env avec la clé API
- [x] Créer le .gitignore

## ✅ Phase 3 : Connexion API SportMonks [COMPLÉTÉ]
- [x] Créer le module de connexion API de base
- [x] Implémenter la gestion des limites (3000 req/h)
- [x] Créer un système de queue pour les requêtes
- [x] Implémenter le retry automatique si limite atteinte
- [x] Créer les fonctions de récupération :
  - [x] getLeagueData(leagueId, seasonId)
  - [x] getTeamData(teamId, seasonId)
  - [x] getPlayerData(playerId, seasonId)
  - [x] getTeamSquad(teamId, seasonId)
- [x] Implémenter le système de cache local
- [ ] **TEST : Récupérer les données de la Ligue 1 2025/2026** (À faire)

## ✅ Phase 4 : Base de données et modèles [COMPLÉTÉ]
- [x] Choisir la base de données (MongoDB)
- [x] Configurer la connexion à la BDD
- [x] Créer les schémas/modèles :
  - [x] League (id, name, country, logo, seasons)
  - [x] Team (id, name, leagueId, logo, venue, statistics)
  - [x] Player (id, name, teamId, position, nationality, statistics)
  - [x] Statistics intégrées dans les modèles Player et Team
- [x] Implémenter le système de versioning pour rollback
- [x] Créer les méthodes pour générer les données des radar charts

## ✅ Phase 5 : Scripts de récupération et rafraîchissement [COMPLÉTÉ]
- [x] Script de récupération initiale complète
- [x] Scripts de rafraîchissement manuel :
  - [x] refresh:ligue1
  - [x] refresh:premierleague
  - [x] refresh:liga
  - [x] refresh:seriea
  - [x] refresh:bundesliga
- [x] Système de backup avant rafraîchissement
- [x] Fonction de rollback en cas d'erreur
- [ ] Scripts automatiques avec node-cron (À configurer)

## 🔄 Phase 6 : Frontend - Structure et design [EN COURS]
- [x] Créer la structure HTML5 de base
- [x] Implémenter le design system :
  - [x] Variables CSS (couleurs, typographie)
  - [x] Grille responsive (mobile-first)
  - [x] Composants réutilisables
- [x] Créer la homepage minimaliste :
  - [x] Header avec logo et navigation
  - [x] Barre de recherche avec autocomplétion
  - [x] Module de comparaison (jusqu'à 4 joueurs)
  - [x] Menu des 5 championnats avec logos
  - [x] Footer avec liens utiles
- [ ] Créer les templates de pages (À compléter) :
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