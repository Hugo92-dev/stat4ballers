const axios = require('axios');

const API_TOKEN = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';

async function checkPlayers() {
  const playersToCheck = [
    { name: "Matt O'Riley", id: 10196 },
    { name: 'Amir Murillo', id: 317379 },
    { name: 'Amine Harit', id: 96691 }
  ];

  for (const player of playersToCheck) {
    try {
      const response = await axios.get(
        `https://api.sportmonks.com/v3/football/players/${player.id}`,
        {
          params: {
            api_token: API_TOKEN,
            include: 'teams'
          }
        }
      );

      const data = response.data.data;
      console.log(`\n👤 ${player.name} (ID: ${player.id})`);
      console.log('Teams:', JSON.stringify(data.teams.map(t => ({
        team_id: t.team_id,
        start: t.start,
        end: t.end,
        jersey: t.jersey_number
      })), null, 2));

      const activeTeam = data.teams.find(t => !t.end || new Date(t.end) > new Date());
      if (activeTeam) {
        console.log(`✅ Active team: ${activeTeam.team_id} (Marseille = 44)`);
        if (activeTeam.team_id === 44) {
          console.log('   → SHOULD KEEP in Marseille');
        } else {
          console.log('   → SHOULD REMOVE from Marseille');
        }
      }

    } catch (error) {
      console.error(`Error checking ${player.name}:`, error.message);
    }
  }
}

checkPlayers();