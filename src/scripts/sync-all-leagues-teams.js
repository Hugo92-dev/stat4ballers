const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

const API_TOKEN = process.env.SPORTMONKS_API_KEY;

// League configurations with season IDs for 2025/2026
const LEAGUES = [
    {
        name: 'Ligue 1',
        slug: 'ligue1',
        seasonId: 25651,
        country: 'France'
    },
    {
        name: 'Premier League',
        slug: 'premierleague',
        seasonId: 25583,
        country: 'England'
    },
    {
        name: 'La Liga',
        slug: 'laliga',
        seasonId: 25659,
        country: 'Spain'
    },
    {
        name: 'Serie A',
        slug: 'seriea',
        seasonId: 25533,
        country: 'Italy'
    },
    {
        name: 'Bundesliga',
        slug: 'bundesliga',
        seasonId: 25646,
        country: 'Germany'
    }
];

async function syncLeagueTeams(league) {
    try {
        console.log(`\n🔄 Fetching ${league.name} teams from Sportmonks API...`);

        // Fetch teams for the season
        const response = await axios.get(
            `https://api.sportmonks.com/v3/football/teams/seasons/${league.seasonId}`,
            {
                params: {
                    api_token: API_TOKEN,
                    include: 'venue'
                }
            }
        );

        const apiTeams = response.data.data;
        console.log(`✅ Found ${apiTeams.length} teams for ${league.name}`);

        // Convert API teams to our format
        const teams = apiTeams.map(apiTeam => ({
            sportmonksId: apiTeam.id,
            name: apiTeam.name,
            slug: apiTeam.name.toLowerCase()
                .replace(/\s+/g, '-')
                .replace(/[éèê]/g, 'e')
                .replace(/[àá]/g, 'a')
                .replace(/[ç]/g, 'c')
                .replace(/[ñ]/g, 'n')
                .replace(/[ü]/g, 'u')
                .replace(/[ö]/g, 'o')
                .replace(/[\.]/g, '')
                .replace(/[&]/g, 'and'),
            shortName: apiTeam.short_code || apiTeam.name.substring(0, 3).toUpperCase(),
            logo: apiTeam.image_path,
            founded: apiTeam.founded,
            league: league.slug,
            country: league.country,
            venue: {
                name: apiTeam.venue?.name || '',
                capacity: apiTeam.venue?.capacity || 0,
                city: apiTeam.venue?.city?.name || ''
            },
            id: Date.now().toString() + Math.floor(Math.random() * 1000),
            lastUpdated: new Date().toISOString()
        }));

        return teams;

    } catch (error) {
        console.error(`❌ Error fetching ${league.name} teams:`, error.message);
        if (error.response) {
            console.error('API Response:', error.response.data);
        }
        return [];
    }
}

async function syncAllLeagues() {
    try {
        console.log('🚀 Starting synchronization of all leagues...\n');

        // Read existing teams (for non-league teams if any)
        const teamsPath = path.join(__dirname, '../../data/db/teams.json');
        let existingTeams = [];

        try {
            const data = fs.readFileSync(teamsPath, 'utf8');
            existingTeams = JSON.parse(data);
        } catch (error) {
            console.log('⚠️ teams.json not found, creating new file');
        }

        // Remove all teams from the 5 main leagues
        const leagueSlugs = LEAGUES.map(l => l.slug);
        existingTeams = existingTeams.filter(team => !leagueSlugs.includes(team.league));

        // Fetch and add teams for each league
        for (const league of LEAGUES) {
            const leagueTeams = await syncLeagueTeams(league);
            existingTeams = existingTeams.concat(leagueTeams);

            // Add a small delay between API calls to avoid rate limiting
            await new Promise(resolve => setTimeout(resolve, 1000));
        }

        // Sort teams by sportmonksId
        existingTeams.sort((a, b) => a.sportmonksId - b.sportmonksId);

        // Write back to file
        fs.writeFileSync(teamsPath, JSON.stringify(existingTeams, null, 2));

        // Print summary
        console.log('\n✅ All leagues synchronized successfully!');
        console.log('\n📊 Summary:');
        for (const league of LEAGUES) {
            const count = existingTeams.filter(t => t.league === league.slug).length;
            console.log(`   ${league.name}: ${count} teams`);
        }
        console.log(`   Total: ${existingTeams.length} teams`);

    } catch (error) {
        console.error('❌ Error during synchronization:', error.message);
        process.exit(1);
    }
}

// Run the sync
syncAllLeagues();