const fs = require('fs');
const path = require('path');

// Charger les données de Ligue 1
const dataPath = path.join(__dirname, '../public/data/ligue1_sportmonks_2025_26.json');
const ligue1Data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// Test de matching pour différents clubs
const testCases = [
  'psg',
  'paris-saint-germain',
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

console.log('='.repeat(60));
console.log('TESTING CLUB NAME MATCHING');
console.log('='.repeat(60));

testCases.forEach(testId => {
  const club = ligue1Data.clubs.find((c) => {
    const clubNameLower = c.nom.toLowerCase();
    
    // Créer plusieurs variantes du nom pour le matching
    const nameVariants = [
      clubNameLower,
      clubNameLower.replace(/[\s-]/g, ''), // sans espaces ni tirets
      clubNameLower.replace(/^(as |fc |rc |aj |og[cn] |ud |cd |rcd |ss[cn] |ac[f]? |us |vf[lb] |rb |sc |tsv? |1\. )/, ''), // sans préfixes
      clubNameLower.split(' ').pop() || '', // dernier mot seulement
    ];
    
    // Normaliser l'ID depuis l'URL
    const urlIdLower = testId.toLowerCase();
    const idVariants = [
      urlIdLower,
      urlIdLower.replace(/-/g, ''), // sans tirets
      urlIdLower.replace(/-/g, ' '), // tirets remplacés par espaces
    ];
    
    // Tester toutes les combinaisons
    for (const nameVar of nameVariants) {
      for (const idVar of idVariants) {
        if (nameVar === idVar) return true;
        if (nameVar.includes(idVar) && idVar.length > 3) return true;
      }
    }
    
    return false;
  });
  
  if (club) {
    console.log(`✓ "${testId}" → ${club.nom} (${club.joueurs.length} players)`);
  } else {
    console.log(`✗ "${testId}" → NOT FOUND`);
  }
});

console.log('\n' + '='.repeat(60));