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

// Position mapping based on position_id
const POSITION_MAP = {
    24: { name: 'Goalkeeper', short: 'GK' },
    25: { name: 'Defender', short: 'DEF' },
    26: { name: 'Midfielder', short: 'MID' },
    27: { name: 'Forward', short: 'FWD' },
    28: { name: 'Attacker', short: 'ATT' }
};

async function syncLeaguePlayersWithDetails(league) {
    try {
        console.log(`\n🔄 Fetching ${league.name} teams and players with full details...`);

        // Get teams for the season
        const teamsResponse = await axios.get(
            `https://api.sportmonks.com/v3/football/teams/seasons/${league.seasonId}`,
            {
                params: {
                    api_token: API_TOKEN
                }
            }
        );

        const teams = teamsResponse.data.data;
        console.log(`✅ Found ${teams.length} teams for ${league.name}`);

        const allPlayers = [];
        let teamCount = 0;

        // Process each team to get squad with player details
        for (const team of teams) {
            teamCount++;
            console.log(`   📌 Processing ${team.name} (${teamCount}/${teams.length})`);

            try {
                // Use the squad endpoint that includes player details
                const squadResponse = await axios.get(
                    `https://api.sportmonks.com/v3/football/squads/seasons/${league.seasonId}/teams/${team.id}`,
                    {
                        params: {
                            api_token: API_TOKEN,
                            include: 'player'
                        }
                    }
                );

                const squadPlayers = squadResponse.data.data;
                console.log(`      Found ${squadPlayers.length} players`);

                // Process each player with full details
                squadPlayers.forEach(squadEntry => {
                    const player = squadEntry.player;

                    if (player) {
                        // Get position info
                        const positionInfo = POSITION_MAP[squadEntry.position_id] || { name: 'Unknown', short: 'UNK' };

                        // Build player data with all details
                        const playerData = {
                            sportmonksId: player.id,
                            name: player.display_name || player.name || `Player ${squadEntry.jersey_number}`,
                            slug: (player.display_name || player.name || `player-${player.id}`).toLowerCase()
                                .replace(/\s+/g, '-')
                                .replace(/[éèêë]/g, 'e')
                                .replace(/[àáâä]/g, 'a')
                                .replace(/[ç]/g, 'c')
                                .replace(/[ñ]/g, 'n')
                                .replace(/[üú]/g, 'u')
                                .replace(/[öó]/g, 'o')
                                .replace(/[^a-z0-9-]/g, ''),
                            firstName: player.firstname || '',
                            lastName: player.lastname || '',
                            displayName: player.display_name || player.name || `Player ${squadEntry.jersey_number}`,
                            position: positionInfo.name,
                            detailedPosition: positionInfo.name, // Could be enhanced with detailed position mapping
                            jerseyNumber: squadEntry.jersey_number,
                            nationality: player.nationality || '',
                            age: player.age || null,
                            dateOfBirth: player.date_of_birth || null,
                            height: player.height || null,
                            weight: player.weight || null,
                            image: player.image_path || null,
                            isGoalkeeper: squadEntry.position_id === 24,
                            isCaptain: squadEntry.captain || false,
                            contractStart: squadEntry.start,
                            contractEnd: squadEntry.end,
                            team: {
                                sportmonksId: team.id,
                                slug: team.name.toLowerCase()
                                    .replace(/\s+/g, '-')
                                    .replace(/[éèêë]/g, 'e')
                                    .replace(/[àáâä]/g, 'a')
                                    .replace(/[ç]/g, 'c')
                                    .replace(/[ñ]/g, 'n')
                                    .replace(/[üú]/g, 'u')
                                    .replace(/[öó]/g, 'o')
                                    .replace(/[\.]/g, '')
                                    .replace(/[&]/g, 'and'),
                                name: team.name
                            },
                            league: league.slug,
                            country: league.country,
                            statistics: {
                                rating: 0,
                                appearances: 0,
                                goals: 0,
                                assists: 0,
                                minutesPlayed: 0,
                                yellowCards: 0,
                                redCards: 0
                            },
                            id: Date.now().toString() + Math.floor(Math.random() * 10000),
                            lastUpdated: new Date().toISOString()
                        };

                        allPlayers.push(playerData);
                    }
                });

                // Small delay to avoid rate limiting
                await new Promise(resolve => setTimeout(resolve, 300));

            } catch (error) {
                console.log(`      ❌ Error fetching squad for ${team.name}:`, error.message);
                // Continue with next team
                continue;
            }
        }

        console.log(`   ✅ Processed ${allPlayers.length} players for ${league.name}`);
        return allPlayers;

    } catch (error) {
        console.error(`❌ Error fetching ${league.name} players:`, error.message);
        return [];
    }
}

async function syncAllPlayersWithDetails() {
    try {
        console.log('🚀 Starting FINAL synchronization with player names and photos...\n');
        console.log('⚠️  This will take 10-15 minutes to fetch all details...\n');

        // Read existing players (if any)
        const playersPath = path.join(__dirname, '../../data/db/players.json');
        let existingPlayers = [];

        try {
            const data = fs.readFileSync(playersPath, 'utf8');
            existingPlayers = JSON.parse(data);
            console.log(`📂 Found ${existingPlayers.length} existing players in database`);
        } catch (error) {
            console.log('⚠️  players.json not found, creating new file');
        }

        // Remove all players from the 5 main leagues
        const leagueSlugs = LEAGUES.map(l => l.slug);
        existingPlayers = existingPlayers.filter(player => !leagueSlugs.includes(player.league));
        console.log(`🗑️  Removed old players from main leagues, keeping ${existingPlayers.length} other players\n`);

        // Fetch and add players for each league
        let totalNewPlayers = 0;
        for (const league of LEAGUES) {
            const leaguePlayers = await syncLeaguePlayersWithDetails(league);
            existingPlayers = existingPlayers.concat(leaguePlayers);
            totalNewPlayers += leaguePlayers.length;

            // Longer delay between leagues
            if (LEAGUES.indexOf(league) < LEAGUES.length - 1) {
                console.log('⏳ Waiting 3 seconds before next league...');
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
        }

        // Sort players by sportmonksId
        existingPlayers.sort((a, b) => a.sportmonksId - b.sportmonksId);

        // Write back to file
        fs.writeFileSync(playersPath, JSON.stringify(existingPlayers, null, 2));

        // Print summary
        console.log('\n🎉 All players synchronized successfully with names and photos!');
        console.log('\n📊 Final Summary:');
        for (const league of LEAGUES) {
            const count = existingPlayers.filter(p => p.league === league.slug).length;
            console.log(`   ${league.name}: ${count} players`);
        }
        console.log(`   Total new players: ${totalNewPlayers}`);
        console.log(`   Total in database: ${existingPlayers.length} players`);

        // Show sample players to verify
        console.log('\n📋 Sample players (first 3):');
        existingPlayers.slice(0, 3).forEach((player, i) => {
            console.log(`   ${i + 1}. ${player.name} (#${player.jerseyNumber}) - ${player.position} - ${player.team.name}`);
            if (player.image) {
                console.log(`      Photo: ${player.image}`);
            }
        });

    } catch (error) {
        console.error('❌ Error during synchronization:', error.message);
        process.exit(1);
    }
}

// Run the sync
console.log('====================================');
console.log('  FINAL PLAYERS SYNC WITH DETAILS  ');
console.log('====================================\n');
syncAllPlayersWithDetails();