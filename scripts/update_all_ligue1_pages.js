const fs = require('fs');
const path = require('path');

// Configuration des clubs de Ligue 1
const clubs = [
  { folder: 'nice', id: 'nice', name: 'OGC Nice', primary: '#dc2626', secondary: '#000000' },
  { folder: 'reims', id: 'reims', name: 'Stade de Reims', primary: '#dc2626', secondary: '#ffffff' },
  { folder: 'toulouse', id: 'toulouse', name: 'Toulouse FC', primary: '#663399', secondary: '#ffffff' },
  { folder: 'nantes', id: 'nantes', name: 'FC Nantes', primary: '#ffc72c', secondary: '#064e3b' },
  { folder: 'montpellier', id: 'montpellier', name: 'Montpellier HSC', primary: '#ff6600', secondary: '#003366' },
  { folder: 'strasbourg', id: 'strasbourg', name: 'RC Strasbourg', primary: '#0066cc', secondary: '#ffffff' },
  { folder: 'brest', id: 'brest', name: 'Stade Brestois', primary: '#dc2626', secondary: '#ffffff' },
  { folder: 'auxerre', id: 'auxerre', name: 'AJ Auxerre', primary: '#ffffff', secondary: '#87ceeb' },
  { folder: 'angers', id: 'angers', name: 'Angers SCO', primary: '#000000', secondary: '#ffffff' },
  // Clubs qui n'existent plus ou ont été relégués, on va les ignorer
  { folder: 'clermont', id: 'clermont', name: 'Clermont Foot', primary: '#dc2626', secondary: '#003366' },
  { folder: 'lorient', id: 'lorient', name: 'FC Lorient', primary: '#ff6600', secondary: '#000000' },
  { folder: 'metz', id: 'metz', name: 'FC Metz', primary: '#800020', secondary: '#ffffff' }
];

const template = (club) => `import ClubPageNew from '@/components/ClubPageNew';

export default function ${club.name.replace(/[^a-zA-Z]/g, '')}Page() {
  return (
    <ClubPageNew 
      clubId="${club.id}"
      clubName="${club.name}"
      leagueId="ligue1"
      leagueName="Ligue 1"
      primaryColor="${club.primary}"
      secondaryColor="${club.secondary}"
    />
  );
}`;

// Mettre à jour chaque club
clubs.forEach(club => {
  const filePath = path.join(__dirname, `../app/ligue1/${club.folder}/page.tsx`);
  
  // Vérifier si le dossier existe
  if (fs.existsSync(path.dirname(filePath))) {
    fs.writeFileSync(filePath, template(club));
    console.log(`✓ Updated ${club.folder}/page.tsx`);
  } else {
    console.log(`✗ Folder not found: ${club.folder}`);
  }
});

// Créer aussi le Havre s'il n'existe pas déjà
const lehavreFolder = path.join(__dirname, '../app/ligue1/le-havre');
if (!fs.existsSync(lehavreFolder)) {
  fs.mkdirSync(lehavreFolder, { recursive: true });
}

const lehavreTemplate = `import ClubPageNew from '@/components/ClubPageNew';

export default function LeHavrePage() {
  return (
    <ClubPageNew 
      clubId="le-havre"
      clubName="Le Havre AC"
      leagueId="ligue1"
      leagueName="Ligue 1"
      primaryColor="#87ceeb"
      secondaryColor="#003366"
    />
  );
}`;

fs.writeFileSync(path.join(lehavreFolder, 'page.tsx'), lehavreTemplate);
console.log('✓ Created le-havre/page.tsx');

// Créer Saint-Étienne s'il n'existe pas
const saintEtienneFolder = path.join(__dirname, '../app/ligue1/saint-etienne');
if (!fs.existsSync(saintEtienneFolder)) {
  fs.mkdirSync(saintEtienneFolder, { recursive: true });
}

const saintEtienneTemplate = `import ClubPageNew from '@/components/ClubPageNew';

export default function SaintEtiennePage() {
  return (
    <ClubPageNew 
      clubId="saint-etienne"
      clubName="AS Saint-Étienne"
      leagueId="ligue1"
      leagueName="Ligue 1"
      primaryColor="#064e3b"
      secondaryColor="#ffffff"
    />
  );
}`;

fs.writeFileSync(path.join(saintEtienneFolder, 'page.tsx'), saintEtienneTemplate);
console.log('✓ Created saint-etienne/page.tsx');

console.log('\nAll Ligue 1 club pages updated!');