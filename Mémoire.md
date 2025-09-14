# Mémoire du Projet - Historique des discussions

## Session du 14/09/2025

### Initialisation du projet Stat4Ballers
- **Objectif principal** : Créer un site automatisé de statistiques football pour les 5 grands championnats européens
- **Tech Lead** : Assistant Claude configuré comme expert développement web
- **Repository GitHub** : https://github.com/Hugo92-dev/stat4ballers
- **Emplacement local** : C:\Users\hugo\OneDrive\Bureau\stat4ballers

### Configuration API SportMonks
- **Provider** : SportMonks
- **Clé API** : KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ
- **Limitation** : 3000 requêtes par heure (attendre l'heure suivante si limite atteinte)

### Structure de documentation créée
1. **Mémoire.md** : Historique des échanges et décisions
2. **Todo.md** : Plan d'action et suivi des tâches
3. **API_SportMonks.md** : Configuration et clé API
4. **Contexte_projet.md** : System prompt complet avec toutes les spécifications
5. **Stats_Ligue1.md** : IDs des saisons (2023/24: 21779, 2024/25: 23643, 2025/26: 25651) et clubs
6. **Stats_PremierLeague.md** : IDs des saisons (2023/24: 21646, 2024/25: 23614, 2025/26: 25583) et clubs
7. **Stats_Liga.md** : IDs des saisons (2023/24: 21694, 2024/25: 23621, 2025/26: 25659) et clubs
8. **Stats_SerieA.md** : IDs des saisons (2023/24: 21818, 2024/25: 23746, 2025/26: 25533) et clubs
9. **Stats_Bundesliga.md** : IDs des saisons (2023/24: 21795, 2024/25: 23744, 2025/26: 25646) et clubs
10. **Stats_Joueurs.md** : Référentiel complet des 59 statistiques joueurs avec leurs IDs SportMonks
11. **Stats_Équipes.md** : Référentiel complet des 54 statistiques équipes avec leurs IDs SportMonks

### Spécifications techniques définies

#### Architecture du site
- **Frontend** : Site responsive (mobile/desktop), moderne et ergonomique
- **Backend** : Node.js avec Express, connexion API SportMonks
- **Base de données** : À définir (pour cache et stockage des données)
- **Visualisation** : Radar charts (Chart.js ou D3.js)
- **Multilingue** : EN par défaut, traduction FR, ES, PT via sélecteur de drapeaux

#### Fonctionnalités principales
1. **Homepage minimaliste** avec :
   - Barre de recherche avec autocomplétion (championnat, club, joueur)
   - Module de comparaison jusqu'à 4 joueurs
   - Menu avec les 5 championnats et leurs logos officiels

2. **Pages dédiées** :
   - Pages championnats
   - Pages clubs avec statistiques équipe
   - Pages joueurs avec radar charts
   - Page de comparaison multi-joueurs

3. **Radar Charts pour joueurs** :
   - General statistics (8 métriques)
   - Offensive creativity (11 métriques)
   - Defensive commitment (11 métriques)
   - Specific goalkeepers (4 métriques pour gardiens uniquement)

4. **Statistiques clubs** :
   - 12 métriques principales pour la saison 2025/2026

#### Scripts de rafraîchissement
1. **Manuel** : npm run refresh:[championnat] avec rollback
2. **Automatique** : Planification bi-hebdomadaire (lundi et vendredi) à heures françaises différentes selon le championnat

### Contraintes et exigences
- **SEO optimisé** : Balises meta, Hn, schema.org
- **Performance** : Lazy loading, compression, cache intelligent
- **Sécurité** : Code sécurisé et fiable
- **Maintenance** : Code facilement maintenable pour non-développeur
- **Données** : Aucune saisie manuelle, tout automatisé via API
- **UX/UI** : Navigation fluide, recherche rapide, filtres intuitifs

### État d'avancement
- ✅ Phase 1 : Documentation complète créée
- ⏳ Phase 2 : Architecture et setup technique à démarrer
- 📋 Phases suivantes : Connexion API, base de données, backend, frontend, visualisations

### Notes importantes
- Commencer par implémenter la Ligue 1 pour tests
- Respecter strictement les libellés de statistiques fournis
- Penser comme un développeur produit (efficacité, performance, évolutivité)
- Le site doit être production-ready et professionnel

---
*Dernière mise à jour : 14/09/2025 - Session d'initialisation complète*