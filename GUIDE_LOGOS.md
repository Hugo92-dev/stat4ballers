# Guide d'utilisation des logos

## ✅ Ce qui est déjà fait

### 1. **Configuration Next.js**
Le fichier `next.config.js` est configuré pour accepter les images externes.

### 2. **Base de données des logos**
Le fichier `/data/logos.ts` contient :
- **Logos des championnats** : URLs des logos officiels des 5 ligues
- **Logos des clubs** : URLs pour les 98 clubs

### 3. **Intégration dans les composants**
Les logos sont déjà intégrés dans :
- Page d'accueil (logos des ligues)
- Navigation (logos des ligues)
- Pages championnats (logos des clubs)

## 🌐 Accès au site
Le site est maintenant sur : **http://localhost:3001**

## 🎨 Option 1 : Logos externes (ACTUEL)
Les logos sont chargés depuis des URLs externes (Wikipedia, etc.).

**Avantages :**
- ✅ Pas besoin de télécharger les fichiers
- ✅ Toujours à jour
- ✅ Pas d'espace disque utilisé

**Inconvénients :**
- ⚠️ Dépendance aux sites externes
- ⚠️ Chargement potentiellement plus lent

## 📁 Option 2 : Logos locaux (RECOMMANDÉ pour production)

Si tu veux télécharger les logos localement :

### Étapes :
1. **Créer les dossiers** :
   ```
   public/
     logos/
       leagues/
       clubs/
   ```

2. **Télécharger les logos** :
   - Télécharge les SVG/PNG depuis les URLs dans `/data/logos.ts`
   - Place-les dans les dossiers correspondants
   - Nomme-les selon l'ID (ex: `psg.svg`, `ligue1.svg`)

3. **Modifier le fichier `/data/logos.ts`** :
   ```typescript
   // Au lieu de :
   'psg': 'https://upload.wikimedia.org/...',
   
   // Utiliser :
   'psg': '/logos/clubs/psg.svg',
   ```

## 🔍 Vérification
1. Va sur http://localhost:3001
2. Les logos des ligues apparaissent sur la page d'accueil
3. Clique sur une ligue
4. Les logos des clubs apparaissent dans les cartes

## 🚨 Si les logos ne s'affichent pas
1. Vérifie la console du navigateur (F12)
2. Certains logos Wikipedia peuvent être bloqués par CORS
3. Solution : télécharge-les localement (Option 2)

## 💡 Pour ajouter un nouveau club
1. Ajoute l'URL du logo dans `/data/logos.ts`
2. Ajoute le club dans `/data/leagues.ts`
3. Le logo apparaîtra automatiquement

## 🎯 Prochaines étapes
1. ✅ Logos des ligues et clubs ajoutés
2. ⬜ Créer les pages clubs avec les logos
3. ⬜ Ajouter les photos des joueurs
4. ⬜ Optimiser les performances (lazy loading)