const axios = require('axios');

const API_TOKEN = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';

async function debugPlayers() {
  // First get Marseille squad to see who's really there
  console.log('🔍 Getting Marseille squad...');

  try {
    const squadResponse = await axios.get(
      `https://api.sportmonks.com/v3/football/squads/seasons/25651/teams/44`,
      {
        params: {
          api_token: API_TOKEN,
          include: 'player'
        }
      }
    );

    const squadPlayers = squadResponse.data.data;
    console.log(`📋 Found ${squadPlayers.length} players in Marseille squad`);

    // Look for players named like O'Riley, Murillo, Gouiri
    const targets = ['Riley', 'Murillo', 'Gouiri'];

    targets.forEach(name => {
      const found = squadPlayers.filter(p =>
        p.player && p.player.name && p.player.name.includes(name)
      );

      console.log(`\n🔎 Players with "${name}" in name:`);
      found.forEach(p => {
        console.log(`   • ${p.player.display_name || p.player.name} (ID: ${p.player.id})`);
      });
    });

  } catch (error) {
    console.error('Error:', error.message);
  }
}

debugPlayers();