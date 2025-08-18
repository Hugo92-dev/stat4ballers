const http = require('http');

const testUrls = [
  '/ligue1/angers',
  '/ligue1/auxerre',
  '/ligue1/psg',
  '/ligue1/marseille',
  '/ligue1/lyon',
  '/ligue1/monaco',
  '/laliga/real-madrid',
  '/premier-league/arsenal'
];

async function testUrl(path) {
  return new Promise((resolve) => {
    const options = {
      hostname: 'localhost',
      port: 3001,
      path: path,
      method: 'GET'
    };

    const req = http.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => {
        data += chunk;
      });
      res.on('end', () => {
        // Chercher si on a des joueurs dans la page
        const hasPlayers = data.includes('Effectif professionnel');
        const hasNoPlayersMessage = data.includes('Aucun joueur disponible');
        const playerCount = (data.match(/class="bg-white rounded-xl shadow-lg/g) || []).length;
        
        resolve({
          path,
          status: res.statusCode,
          hasPlayers,
          hasNoPlayersMessage,
          playerCount
        });
      });
    });

    req.on('error', (e) => {
      resolve({
        path,
        status: 0,
        error: e.message
      });
    });

    req.end();
  });
}

async function main() {
  console.log('='.repeat(60));
  console.log('TESTING CLUB URLS');
  console.log('='.repeat(60));
  
  for (const url of testUrls) {
    const result = await testUrl(url);
    if (result.status === 200) {
      if (result.playerCount > 0) {
        console.log(`✓ ${url} → ${result.playerCount} players found`);
      } else if (result.hasNoPlayersMessage) {
        console.log(`✗ ${url} → "Aucun joueur disponible" message shown`);
      } else {
        console.log(`? ${url} → Page loads but unclear status`);
      }
    } else {
      console.log(`✗ ${url} → Status: ${result.status} ${result.error || ''}`);
    }
  }
  
  console.log('='.repeat(60));
}

main();