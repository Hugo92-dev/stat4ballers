const fs = require('fs');
const path = require('path');

// Fonction de matching identique à celle dans allLeaguesData.ts
function findClub(clubs, urlId) {
  return clubs.find((c) => {
    const clubNameLower = c.nom.toLowerCase();
    const urlIdLower = urlId.toLowerCase();
    
    // Cas spéciaux d'abord
    const specialMatches = {
      'psg': ['paris saint-germain'],
      'paris-saint-germain': ['paris saint-germain'],
      'om': ['olympique de marseille'],
      'marseille': ['olympique de marseille'],
      'ol': ['olympique lyonnais'],
      'lyon': ['olympique lyonnais'],
      'asse': ['as saint-étienne', 'saint-étienne'],
      'saint-etienne': ['as saint-étienne', 'saint-étienne'],
      'saintetienne': ['as saint-étienne', 'saint-étienne'],
      'rennes': ['stade rennais'],
      'stade-rennais': ['stade rennais'],
      'monaco': ['as monaco'],
      'lille': ['lille osc'],
      'nice': ['ogc nice'],
      'lens': ['rc lens'],
      'reims': ['stade de reims'],
      'toulouse': ['toulouse fc'],
      'nantes': ['fc nantes'],
      'montpellier': ['montpellier hsc'],
      'strasbourg': ['rc strasbourg'],
      'brest': ['stade brestois'],
      'auxerre': ['aj auxerre'],
      'le-havre': ['le havre ac'],
      'lehavre': ['le havre ac'],
      'angers': ['angers sco']
    };
    
    // Vérifier les cas spéciaux d'abord
    if (specialMatches[urlIdLower]) {
      for (const specialName of specialMatches[urlIdLower]) {
        if (clubNameLower === specialName || clubNameLower.includes(specialName)) {
          return true;
        }
      }
    }
    
    // Créer plusieurs variantes du nom pour le matching
    const nameVariants = [
      clubNameLower,
      clubNameLower.replace(/[\s-]/g, ''),
      clubNameLower.replace(/^(as |fc |rc |aj |og[cn] |ud |cd |rcd |ss[cn] |ac[f]? |us |vf[lb] |rb |sc |tsv? |1\. |stade )/, ''),
      clubNameLower.split(' ').pop() || ''
    ];
    
    const idVariants = [
      urlIdLower,
      urlIdLower.replace(/-/g, ''),
      urlIdLower.replace(/-/g, ' ')
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
}

// Charger les données de Ligue 1
const dataPath = path.join(__dirname, '../public/data/ligue1_sportmonks_2025_26.json');
const ligue1Data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

// Test de matching pour différents clubs
const testCases = [
  'psg',
  'paris-saint-germain',
  'marseille',
  'om',
  'lyon',
  'ol',
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
  'saint-etienne',
  'asse'
];

console.log('='.repeat(60));
console.log('TESTING IMPROVED CLUB NAME MATCHING');
console.log('='.repeat(60));

testCases.forEach(testId => {
  const club = findClub(ligue1Data.clubs, testId);
  
  if (club) {
    console.log(`✓ "${testId}" → ${club.nom} (${club.joueurs.length} players)`);
  } else {
    console.log(`✗ "${testId}" → NOT FOUND`);
  }
});

console.log('\n' + '='.repeat(60));