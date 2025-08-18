const fs = require('fs');
const path = require('path');

// Vérifier quels fichiers JSON existent
const dataDir = path.join(__dirname, '../public/data');
const files = [
  'ligue1_sportmonks_2025_26.json',
  'premier-league_sportmonks_2025_26.json',
  'laliga_sportmonks_2025_26.json',
  'serie-a_sportmonks_2025_26.json',
  'bundesliga_sportmonks_2025_26.json'
];

console.log('='.repeat(60));
console.log('CHECKING DATA FILES');
console.log('='.repeat(60));

files.forEach(file => {
  const filePath = path.join(dataDir, file);
  if (fs.existsSync(filePath)) {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    console.log(`\n✓ ${file}`);
    console.log(`  Championship: ${data.championnat}`);
    console.log(`  Clubs: ${data.clubs.length}`);
    
    // Lister les clubs avec des joueurs
    const clubsWithPlayers = data.clubs.filter(c => c.joueurs && c.joueurs.length > 0);
    console.log(`  Clubs with players: ${clubsWithPlayers.length}`);
    
    // Afficher les premiers clubs
    clubsWithPlayers.slice(0, 5).forEach(club => {
      console.log(`    - ${club.nom}: ${club.joueurs.length} players`);
    });
    
    if (clubsWithPlayers.length > 5) {
      console.log(`    ... and ${clubsWithPlayers.length - 5} more clubs`);
    }
  } else {
    console.log(`\n✗ ${file} - NOT FOUND`);
  }
});

console.log('\n' + '='.repeat(60));