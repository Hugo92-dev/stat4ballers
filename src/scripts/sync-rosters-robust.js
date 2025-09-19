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

// Detailed position mapping
const DETAILED_POSITION_MAP = {
    148: 'Goalkeeper',
    149: 'Right Back',
    150: 'Center Back',
    151: 'Left Back',
    152: 'Right Wing Back',
    153: 'Left Wing Back',
    154: 'Defensive Midfielder',
    155: 'Central Midfielder',
    156: 'Attacking Midfielder',
    157: 'Right Winger',
    158: 'Left Winger',
    159: 'Center Forward',
    160: 'Striker'
};

class RosterSynchronizer {
    constructor() {
        this.apiToken = API_TOKEN;
        this.playersPath = path.join(__dirname, '../../data/db/players.json');
        this.backupPath = path.join(__dirname, '../../data/db/players.backup.json');
        this.reportPath = path.join(__dirname, '../../data/db/roster-sync-report.json');
        this.existingPlayers = [];
        this.report = {
            timestamp: new Date().toISOString(),
            leagues: {},
            summary: {
                playersAdded: 0,
                playersRemoved: 0,
                playersUpdated: 0,
                totalPlayers: 0
            },
            removedPlayers: [],
            addedPlayers: [],
            updatedPlayers: []
        };
    }

    async initialize() {
        try {
            // Load existing players
            const data = fs.readFileSync(this.playersPath, 'utf8');
            this.existingPlayers = JSON.parse(data);
            console.log(`📂 Loaded ${this.existingPlayers.length} existing players from database`);

            // Create backup
            fs.writeFileSync(this.backupPath, data);
            console.log(`💾 Backup created at ${this.backupPath}`);
        } catch (error) {
            console.log('⚠️  players.json not found, starting with empty database');
            this.existingPlayers = [];
        }
    }

    async fetchCurrentSquad(teamId, seasonId, teamName) {
        try {
            // Fetch current squad with detailed player information
            const squadResponse = await axios.get(
                `https://api.sportmonks.com/v3/football/squads/teams/${teamId}`,
                {
                    params: {
                        api_token: this.apiToken,
                        include: 'player.country,player.position,player.detailedposition',
                        filters: `seasons:${seasonId}`
                    }
                }
            );

            if (!squadResponse.data.data || squadResponse.data.data.length === 0) {
                // Fallback to season-specific endpoint
                const seasonSquadResponse = await axios.get(
                    `https://api.sportmonks.com/v3/football/squads/seasons/${seasonId}/teams/${teamId}`,
                    {
                        params: {
                            api_token: this.apiToken,
                            include: 'player.country,player.position,player.detailedposition'
                        }
                    }
                );
                return seasonSquadResponse.data.data || [];
            }

            return squadResponse.data.data;
        } catch (error) {
            console.log(`      ⚠️  Error fetching squad for ${teamName}: ${error.message}`);
            return [];
        }
    }

    async fetchTransfers(teamId, seasonId) {
        try {
            const transfersResponse = await axios.get(
                `https://api.sportmonks.com/v3/football/transfers`,
                {
                    params: {
                        api_token: this.apiToken,
                        filters: `teams:${teamId};seasons:${seasonId}`,
                        include: 'player,teamIn,teamOut,type'
                    }
                }
            );
            return transfersResponse.data.data || [];
        } catch (error) {
            console.log(`      ⚠️  Error fetching transfers: ${error.message}`);
            return [];
        }
    }

    processPlayer(squadEntry, team, league) {
        const player = squadEntry.player;
        if (!player) return null;

        // Get position information
        const positionInfo = POSITION_MAP[squadEntry.position_id] || { name: 'Unknown', short: 'UNK' };

        // Get detailed position if available
        let detailedPosition = positionInfo.name;
        if (player.detailedposition?.data) {
            detailedPosition = player.detailedposition.data.name || detailedPosition;
        } else if (squadEntry.detailed_position_id) {
            detailedPosition = DETAILED_POSITION_MAP[squadEntry.detailed_position_id] || detailedPosition;
        }

        // Get nationality from country data
        let nationality = '';
        if (player.country?.data) {
            nationality = player.country.data.name || '';
        } else if (player.nationality) {
            nationality = player.nationality;
        }

        return {
            sportmonksId: player.id,
            name: player.display_name || player.name || `Player ${squadEntry.jersey_number}`,
            slug: this.generateSlug(player.display_name || player.name || `player-${player.id}`),
            firstName: player.firstname || '',
            lastName: player.lastname || '',
            displayName: player.display_name || player.name || `Player ${squadEntry.jersey_number}`,
            position: positionInfo.name,
            detailedPosition: detailedPosition,
            jerseyNumber: squadEntry.jersey_number,
            nationality: nationality,
            age: player.age || null,
            dateOfBirth: player.date_of_birth || null,
            height: player.height || null,
            weight: player.weight || null,
            image: player.image_path || null,
            isGoalkeeper: squadEntry.position_id === 24,
            isCaptain: squadEntry.captain || false,
            contractStart: squadEntry.start || null,
            contractEnd: squadEntry.end || null,
            transferStatus: 'active', // Will be updated based on transfers
            team: {
                sportmonksId: team.id,
                slug: this.generateSlug(team.name),
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
            id: `${player.id}_${team.id}`, // Unique ID based on player and team
            lastUpdated: new Date().toISOString()
        };
    }

    generateSlug(text) {
        return text.toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[éèêë]/g, 'e')
            .replace(/[àáâä]/g, 'a')
            .replace(/[ç]/g, 'c')
            .replace(/[ñ]/g, 'n')
            .replace(/[üúù]/g, 'u')
            .replace(/[öóò]/g, 'o')
            .replace(/[îï]/g, 'i')
            .replace(/[\.]/g, '')
            .replace(/[&]/g, 'and')
            .replace(/[^a-z0-9-]/g, '');
    }

    async syncLeague(league) {
        console.log(`\n🔄 Processing ${league.name}...`);
        this.report.leagues[league.slug] = {
            name: league.name,
            teams: {},
            playersAdded: [],
            playersRemoved: [],
            playersUpdated: []
        };

        try {
            // Get teams for the season
            const teamsResponse = await axios.get(
                `https://api.sportmonks.com/v3/football/teams/seasons/${league.seasonId}`,
                {
                    params: {
                        api_token: this.apiToken,
                        include: 'venue'
                    }
                }
            );

            const teams = teamsResponse.data.data;
            console.log(`   ✅ Found ${teams.length} teams`);

            const leaguePlayers = [];
            let teamCount = 0;

            for (const team of teams) {
                teamCount++;
                console.log(`   📌 Processing ${team.name} (${teamCount}/${teams.length})`);

                const teamSlug = this.generateSlug(team.name);
                this.report.leagues[league.slug].teams[teamSlug] = {
                    name: team.name,
                    playersAdded: [],
                    playersRemoved: [],
                    playersUpdated: []
                };

                // Get current squad
                const squadPlayers = await this.fetchCurrentSquad(team.id, league.seasonId, team.name);
                console.log(`      Found ${squadPlayers.length} players in current squad`);

                // Get transfers for this team
                const transfers = await this.fetchTransfers(team.id, league.seasonId);
                console.log(`      Found ${transfers.length} transfers`);

                // Process squad players
                const currentPlayerIds = new Set();

                for (const squadEntry of squadPlayers) {
                    const playerData = this.processPlayer(squadEntry, team, league);
                    if (playerData) {
                        // Check if player left in transfers
                        const outTransfer = transfers.find(t =>
                            t.player?.data?.id === playerData.sportmonksId &&
                            t.team_out_id === team.id &&
                            new Date(t.date) < new Date()
                        );

                        if (!outTransfer) {
                            leaguePlayers.push(playerData);
                            currentPlayerIds.add(playerData.sportmonksId);
                        }
                    }
                }

                // Find players that were in this team but are no longer
                const existingTeamPlayers = this.existingPlayers.filter(p =>
                    p.team.slug === teamSlug && p.league === league.slug
                );

                for (const existingPlayer of existingTeamPlayers) {
                    if (!currentPlayerIds.has(existingPlayer.sportmonksId)) {
                        this.report.leagues[league.slug].teams[teamSlug].playersRemoved.push({
                            name: existingPlayer.name,
                            position: existingPlayer.position,
                            jerseyNumber: existingPlayer.jerseyNumber
                        });
                        this.report.removedPlayers.push({
                            name: existingPlayer.name,
                            team: existingPlayer.team.name,
                            league: league.name
                        });
                    }
                }

                // Add delay to avoid rate limiting
                await new Promise(resolve => setTimeout(resolve, 500));
            }

            return leaguePlayers;

        } catch (error) {
            console.error(`   ❌ Error processing ${league.name}: ${error.message}`);
            return [];
        }
    }

    async syncAll() {
        console.log('🚀 Starting ROBUST roster synchronization...\n');
        console.log('📋 Features:');
        console.log('   ✓ Current squad validation');
        console.log('   ✓ Transfer tracking');
        console.log('   ✓ Removed players detection');
        console.log('   ✓ Detailed reporting\n');

        await this.initialize();

        // Remove all players from the 5 main leagues (we'll re-add current ones)
        const leagueSlugs = LEAGUES.map(l => l.slug);
        const otherPlayers = this.existingPlayers.filter(player => !leagueSlugs.includes(player.league));

        const allNewPlayers = [...otherPlayers];

        // Process each league
        for (const league of LEAGUES) {
            const leaguePlayers = await this.syncLeague(league);

            // Track added players
            for (const player of leaguePlayers) {
                const existingPlayer = this.existingPlayers.find(p => p.sportmonksId === player.sportmonksId);
                if (!existingPlayer) {
                    this.report.addedPlayers.push({
                        name: player.name,
                        team: player.team.name,
                        league: league.name
                    });
                    this.report.summary.playersAdded++;
                } else if (existingPlayer.team.slug !== player.team.slug) {
                    this.report.updatedPlayers.push({
                        name: player.name,
                        oldTeam: existingPlayer.team.name,
                        newTeam: player.team.name,
                        league: league.name
                    });
                    this.report.summary.playersUpdated++;
                }
            }

            allNewPlayers.push(...leaguePlayers);

            if (LEAGUES.indexOf(league) < LEAGUES.length - 1) {
                console.log('   ⏳ Waiting before next league...\n');
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        // Count removed players
        this.report.summary.playersRemoved = this.report.removedPlayers.length;
        this.report.summary.totalPlayers = allNewPlayers.length;

        // Sort players
        allNewPlayers.sort((a, b) => a.sportmonksId - b.sportmonksId);

        // Save updated players
        fs.writeFileSync(this.playersPath, JSON.stringify(allNewPlayers, null, 2));

        // Save report
        fs.writeFileSync(this.reportPath, JSON.stringify(this.report, null, 2));

        // Print summary
        this.printSummary(allNewPlayers);
    }

    printSummary(allPlayers) {
        console.log('\n' + '='.repeat(50));
        console.log('📊 SYNCHRONIZATION COMPLETE');
        console.log('='.repeat(50));

        console.log('\n📈 Summary:');
        console.log(`   ✅ Players added: ${this.report.summary.playersAdded}`);
        console.log(`   ❌ Players removed: ${this.report.summary.playersRemoved}`);
        console.log(`   🔄 Players updated: ${this.report.summary.playersUpdated}`);
        console.log(`   📁 Total players: ${this.report.summary.totalPlayers}`);

        console.log('\n📋 League breakdown:');
        for (const league of LEAGUES) {
            const count = allPlayers.filter(p => p.league === league.slug).length;
            console.log(`   ${league.name}: ${count} players`);
        }

        if (this.report.removedPlayers.length > 0) {
            console.log('\n❌ Players removed (first 10):');
            this.report.removedPlayers.slice(0, 10).forEach((player, i) => {
                console.log(`   ${i + 1}. ${player.name} (${player.team} - ${player.league})`);
            });
        }

        if (this.report.addedPlayers.length > 0) {
            console.log('\n✅ Players added (first 10):');
            this.report.addedPlayers.slice(0, 10).forEach((player, i) => {
                console.log(`   ${i + 1}. ${player.name} (${player.team} - ${player.league})`);
            });
        }

        if (this.report.updatedPlayers.length > 0) {
            console.log('\n🔄 Players transferred (first 10):');
            this.report.updatedPlayers.slice(0, 10).forEach((player, i) => {
                console.log(`   ${i + 1}. ${player.name}: ${player.oldTeam} → ${player.newTeam}`);
            });
        }

        console.log(`\n📄 Full report saved to: ${this.reportPath}`);
        console.log(`💾 Backup saved to: ${this.backupPath}`);
    }
}

// Run the synchronization
async function main() {
    const syncer = new RosterSynchronizer();

    try {
        await syncer.syncAll();
        console.log('\n✅ Synchronization completed successfully!');
    } catch (error) {
        console.error('\n❌ Fatal error during synchronization:', error.message);
        console.error(error.stack);
        process.exit(1);
    }
}

// Execute if run directly
if (require.main === module) {
    main();
}

module.exports = RosterSynchronizer;