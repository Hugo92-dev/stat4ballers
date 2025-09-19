const axios = require('axios');

const API_TOKEN = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';

async function testFixedLogic() {
    console.log('🔧 Testing FIXED logic for Marseille players...\n');

    const testPlayers = [
        { name: "Matt O'Riley", id: 1494712 },
        { name: 'Amir Murillo', id: 512560 },
        { name: 'Amine Gouiri', id: 433458 }
    ];

    for (const player of testPlayers) {
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
            const teams = data.teams || [];
            const MARSEILLE_ID = 44;

            console.log(`👤 ${player.name} (ID: ${player.id})`);

            // NEW LOGIC: Look specifically for Marseille relationship
            const marseilleRelationship = teams.find(t => t.team_id === MARSEILLE_ID);

            if (marseilleRelationship) {
                console.log(`   Found Marseille relationship: start=${marseilleRelationship.start}, end=${marseilleRelationship.end}`);

                if (!marseilleRelationship.end || new Date(marseilleRelationship.end) > new Date()) {
                    console.log(`   ✅ KEEP: Active relationship with Marseille`);
                } else {
                    console.log(`   ❌ REMOVE: Expired relationship with Marseille`);
                }
            } else {
                console.log(`   ❌ REMOVE: No relationship with Marseille found`);
            }
            console.log('');

        } catch (error) {
            console.error(`Error checking ${player.name}:`, error.message);
        }
    }
}

testFixedLogic();