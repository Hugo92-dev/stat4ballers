const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const API_TOKEN = process.env.SPORTMONKS_API_KEY;
const SEASON_ID = 25651; // Ligue 1 2025/2026

async function syncLigue1Teams() {
    try {
        console.log('🔄 Fetching Ligue 1 teams from Sportmonks API...');

        // Fetch teams for Ligue 1 season 2025/2026
        const response = await axios.get(
            `https://api.sportmonks.com/v3/football/teams/seasons/${SEASON_ID}`,
            {
                params: {
                    api_token: API_TOKEN,
                    include: 'venue'
                }
            }
        );

        const apiTeams = response.data.data;
        console.log(`✅ Found ${apiTeams.length} teams from API`);

        // Read existing teams
        const teamsPath = path.join(__dirname, '../../data/db/teams.json');
        let existingTeams = [];

        try {
            const data = fs.readFileSync(teamsPath, 'utf8');
            existingTeams = JSON.parse(data);
        } catch (error) {
            console.log('⚠️ teams.json not found, creating new file');
        }

        // Remove old Ligue 1 teams
        existingTeams = existingTeams.filter(team => team.league !== 'ligue1');

        // Add new teams from API
        apiTeams.forEach(apiTeam => {
            const team = {
                sportmonksId: apiTeam.id,
                name: apiTeam.name,
                slug: apiTeam.name.toLowerCase()
                    .replace(/\s+/g, '-')
                    .replace(/[éè]/g, 'e')
                    .replace(/[à]/g, 'a')
                    .replace(/[ç]/g, 'c'),
                shortName: apiTeam.short_code || apiTeam.name.substring(0, 3).toUpperCase(),
                logo: apiTeam.image_path,
                founded: apiTeam.founded,
                league: 'ligue1',
                country: apiTeam.country?.name || 'France',
                venue: {
                    name: apiTeam.venue?.name || '',
                    capacity: apiTeam.venue?.capacity || 0,
                    city: apiTeam.venue?.city?.name || ''
                },
                id: Date.now().toString() + Math.floor(Math.random() * 1000),
                lastUpdated: new Date().toISOString()
            };

            existingTeams.push(team);
            console.log(`✅ Added ${team.name}`);
        });

        // Sort teams by sportmonksId
        existingTeams.sort((a, b) => a.sportmonksId - b.sportmonksId);

        // Write back to file
        fs.writeFileSync(teamsPath, JSON.stringify(existingTeams, null, 2));
        console.log('\n✅ Teams database synchronized with API successfully!');
        console.log(`📊 Total teams in database: ${existingTeams.length}`);
        console.log(`📊 Ligue 1 teams: ${existingTeams.filter(t => t.league === 'ligue1').length}`);

    } catch (error) {
        console.error('❌ Error syncing teams:', error.message);
        if (error.response) {
            console.error('API Response:', error.response.data);
        }
        process.exit(1);
    }
}

// Run the sync
syncLigue1Teams();