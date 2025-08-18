// Test de chargement des données comme dans l'application

console.log('='.repeat(60));
console.log('TESTING DATA LOADING LIKE IN THE APP');
console.log('='.repeat(60));

// Simuler le chargement comme dans allLeaguesData.ts
let ligue1Data = null;
let premierLeagueData = null;
let laligaData = null;
let serieAData = null;
let bundesligaData = null;

try {
  // Utiliser le chemin relatif depuis scripts/
  ligue1Data = require('../public/data/ligue1_sportmonks_2025_26.json');
  console.log('✓ Ligue 1 data loaded:', ligue1Data.clubs.length, 'clubs');
} catch (e) {
  console.log('✗ Ligue 1 data error:', e.message);
}

try {
  premierLeagueData = require('../public/data/premier-league_sportmonks_2025_26.json');
  console.log('✓ Premier League data loaded:', premierLeagueData.clubs.length, 'clubs');
} catch (e) {
  console.log('✗ Premier League data error:', e.message);
}

try {
  laligaData = require('../public/data/laliga_sportmonks_2025_26.json');
  console.log('✓ La Liga data loaded:', laligaData.clubs.length, 'clubs');
} catch (e) {
  console.log('✗ La Liga data error:', e.message);
}

try {
  serieAData = require('../public/data/serie-a_sportmonks_2025_26.json');
  console.log('✓ Serie A data loaded:', serieAData.clubs.length, 'clubs');
} catch (e) {
  console.log('✗ Serie A data error:', e.message);
}

try {
  bundesligaData = require('../public/data/bundesliga_sportmonks_2025_26.json');
  console.log('✓ Bundesliga data loaded:', bundesligaData.clubs.length, 'clubs');
} catch (e) {
  console.log('✗ Bundesliga data error:', e.message);
}

console.log('\n' + '='.repeat(60));

// Tester quelques clubs spécifiques
const testClubs = [
  { league: 'ligue1', id: 'angers', data: ligue1Data },
  { league: 'ligue1', id: 'auxerre', data: ligue1Data },
  { league: 'ligue1', id: 'psg', data: ligue1Data },
  { league: 'laliga', id: 'real-madrid', data: laligaData },
  { league: 'premier-league', id: 'arsenal', data: premierLeagueData }
];

console.log('TESTING SPECIFIC CLUBS:');
console.log('='.repeat(60));

testClubs.forEach(test => {
  if (test.data && test.data.clubs) {
    const club = test.data.clubs.find(c => {
      const clubNameLower = c.nom.toLowerCase();
      const urlIdLower = test.id.toLowerCase();
      
      // Cas spéciaux
      const specialMatches = {
        'psg': ['paris saint-germain'],
        'angers': ['angers sco'],
        'auxerre': ['aj auxerre'],
        'real-madrid': ['real madrid'],
        'arsenal': ['arsenal']
      };
      
      if (specialMatches[urlIdLower]) {
        for (const specialName of specialMatches[urlIdLower]) {
          if (clubNameLower === specialName || clubNameLower.includes(specialName)) {
            return true;
          }
        }
      }
      
      return clubNameLower.includes(urlIdLower);
    });
    
    if (club) {
      console.log(`✓ ${test.league}/${test.id} → ${club.nom} (${club.joueurs.length} players)`);
    } else {
      console.log(`✗ ${test.league}/${test.id} → NOT FOUND`);
    }
  } else {
    console.log(`✗ ${test.league}/${test.id} → NO DATA`);
  }
});

console.log('='.repeat(60));