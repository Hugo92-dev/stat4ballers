const fs = require('fs');
const path = require('path');
const axios = require('axios');
require('dotenv').config();

// Use the provided API key directly
const API_TOKEN = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';

// League configurations with season IDs and specific club IDs for 2025/2026
const LEAGUES = [
    {
        name: 'Ligue 1',
        slug: 'ligue1',
        seasonId: 25651,
        country: 'France',
        clubIds: [44, 59, 79, 266, 271, 289, 450, 591, 598, 686, 690, 776, 1055, 3513, 3682, 4508, 6789, 9257]
    },
    {
        name: 'Premier League',
        slug: 'premierleague',
        seasonId: 25583,
        country: 'England',
        clubIds: [1, 3, 6, 8, 9, 11, 13, 14, 15, 18, 19, 20, 27, 29, 51, 52, 63, 71, 78, 236]
    },
    {
        name: 'La Liga',
        slug: 'laliga',
        seasonId: 25659,
        country: 'Spain',
        clubIds: [36, 83, 93, 106, 214, 231, 377, 459, 485, 528, 594, 645, 676, 1099, 2975, 3457, 3468, 3477, 7980, 13258]
    },
    {
        name: 'Serie A',
        slug: 'seriea',
        seasonId: 25533,
        country: 'Italy',
        clubIds: [37, 43, 102, 109, 113, 268, 346, 398, 585, 597, 613, 625, 708, 1072, 1123, 2714, 2930, 7790, 8513, 10722]
    },
    {
        name: 'Bundesliga',
        slug: 'bundesliga',
        seasonId: 25646,
        country: 'Germany',
        clubIds: [68, 82, 90, 277, 353, 366, 503, 510, 683, 794, 1079, 2708, 2726, 2831, 3319, 3320, 3321, 3543]
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
        console.log(`   📋 Targeting ${league.clubIds.length} specific clubs`);

        const allPlayers = [];
        let teamCount = 0;
        const teams = [];

        // Fetch team info for each specific club ID
        for (const clubId of league.clubIds) {
            try {
                const teamResponse = await axios.get(
                    `https://api.sportmonks.com/v3/football/teams/${clubId}`,
                    {
                        params: {
                            api_token: API_TOKEN
                        }
                    }
                );
                if (teamResponse.data.data) {
                    teams.push(teamResponse.data.data);
                }
            } catch (error) {
                console.log(`   ⚠️ Could not fetch team with ID ${clubId}`);
            }
        }

        console.log(`✅ Successfully fetched ${teams.length}/${league.clubIds.length} teams for ${league.name}`);

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
        console.log('🚀 Starting synchronization for 2025/2026 season with player names and photos...\n');
        console.log('📅 Season: 2025/2026\n');
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
        let allNewPlayers = [];
        for (const league of LEAGUES) {
            const leaguePlayers = await syncLeaguePlayersWithDetails(league);
            allNewPlayers = allNewPlayers.concat(leaguePlayers);

            // Longer delay between leagues
            if (LEAGUES.indexOf(league) < LEAGUES.length - 1) {
                console.log('⏳ Waiting 3 seconds before next league...');
                await new Promise(resolve => setTimeout(resolve, 3000));
            }
        }

        // DEDUPLICATION: Keep only the last occurrence of each player (by sportmonksId)
        console.log('\n🔍 Checking for transferred players (duplicates)...');
        const playerMap = new Map();
        const duplicates = new Map();

        // Process in reverse order to keep the last occurrence
        for (let i = allNewPlayers.length - 1; i >= 0; i--) {
            const player = allNewPlayers[i];
            if (!playerMap.has(player.sportmonksId)) {
                playerMap.set(player.sportmonksId, player);
            } else {
                // Track duplicates for logging
                if (!duplicates.has(player.sportmonksId)) {
                    duplicates.set(player.sportmonksId, {
                        name: player.name,
                        clubs: [playerMap.get(player.sportmonksId).team.name, player.team.name]
                    });
                } else {
                    duplicates.get(player.sportmonksId).clubs.push(player.team.name);
                }
            }
        }

        // Convert Map back to array
        const deduplicatedPlayers = Array.from(playerMap.values());

        // Log transferred players
        if (duplicates.size > 0) {
            console.log(`\n📋 Found ${duplicates.size} transferred players:`);
            let count = 0;
            for (const [id, info] of duplicates) {
                count++;
                if (count <= 10) {  // Show first 10 transfers
                    console.log(`   • ${info.name}: ${info.clubs.reverse().join(' → ')} (keeping ${info.clubs[info.clubs.length - 1]})`);
                }
            }
            if (duplicates.size > 10) {
                console.log(`   ... and ${duplicates.size - 10} more transfers`);
            }
        } else {
            console.log('   ✅ No transferred players found');
        }

        // Add deduplicated players to existing ones
        existingPlayers = existingPlayers.concat(deduplicatedPlayers);

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
        console.log(`   Total new players (after deduplication): ${deduplicatedPlayers.length}`);
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
console.log('========================================');
console.log('  PLAYERS SYNC 2025/2026 WITH DETAILS  ');
console.log('========================================\n');
syncAllPlayersWithDetails();