const fs = require('fs');
const path = require('path');

// Charger les données
const dataPath = path.join(__dirname, '../public/data/ligue1_sportmonks_2025_26.json');
const ligue1Data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

console.log('='.repeat(60));
console.log('CLUBS DISPONIBLES DANS LE FICHIER JSON:');
console.log('='.repeat(60));

ligue1Data.clubs.forEach(club => {
  console.log(`- ${club.nom}: ${club.joueurs.length} joueurs`);
});

console.log('\n' + '='.repeat(60));
console.log('TEST DE MATCHING DES URLS:');
console.log('='.repeat(60));

// Tester le matching pour différentes URLs
const testUrls = [
  'psg',
  'marseille', 
  'lyon',
  'monaco',
  'lille',
  'nice',
  'lens',
  'rennes',
  'reims',
  'toulouse',
  'nantes',
  'montpellier',
  'strasbourg',
  'brest',
  'auxerre',
  'le-havre',
  'angers',
  'saint-etienne'
];

testUrls.forEach(clubId => {
  const club = ligue1Data.clubs.find((c) => {
    const normalizedName = c.nom.toLowerCase().replace(/[\s-]/g, '');
    const normalizedClubId = clubId.toLowerCase().replace(/[\s-]/g, '');
    return normalizedName.includes(normalizedClubId) || normalizedClubId.includes(normalizedName);
  });
  
  if (club) {
    console.log(`✓ "${clubId}" → ${club.nom} (${club.joueurs.length} joueurs)`);
  } else {
    console.log(`✗ "${clubId}" → NON TROUVÉ`);
  }
});

console.log('='.repeat(60));