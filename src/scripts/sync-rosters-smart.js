const fs = require('fs');
const path = require('path');
const axios = require('axios');

const API_TOKEN = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';

// Complete league and team configurations
const LEAGUES = [
    {
        name: 'Ligue 1',
        slug: 'ligue1',
        seasonId: 25651,
        country: 'France',
        teams: [
            { id: 44, name: 'Olympique Marseille' },
            { id: 59, name: 'Nantes' },
            { id: 79, name: 'Olympique Lyonnais' },
            { id: 266, name: 'Brest' },
            { id: 271, name: 'Lens' },
            { id: 289, name: 'Toulouse' },
            { id: 450, name: 'Nice' },
            { id: 591, name: 'Paris Saint Germain' },
            { id: 598, name: 'Rennes' },
            { id: 686, name: 'Strasbourg' },
            { id: 690, name: 'LOSC Lille' },
            { id: 776, name: 'Angers SCO' },
            { id: 1055, name: 'Le Havre' },
            { id: 3513, name: 'Metz' },
            { id: 3682, name: 'Auxerre' },
            { id: 4508, name: 'Paris' },
            { id: 6789, name: 'Monaco' },
            { id: 9257, name: 'Lorient' }
        ]
    },
    {
        name: 'Premier League',
        slug: 'premierleague',
        seasonId: 25583,
        country: 'England',
        teams: [
            { id: 1, name: 'West Ham United' },
            { id: 3, name: 'Sunderland' },
            { id: 6, name: 'Tottenham Hotspur' },
            { id: 8, name: 'Liverpool' },
            { id: 9, name: 'Manchester City' },
            { id: 11, name: 'Fulham' },
            { id: 13, name: 'Everton' },
            { id: 14, name: 'Manchester United' },
            { id: 15, name: 'Aston Villa' },
            { id: 18, name: 'Chelsea' },
            { id: 19, name: 'Arsenal' },
            { id: 20, name: 'Newcastle United' },
            { id: 27, name: 'Burnley' },
            { id: 29, name: 'Wolverhampton Wanderers' },
            { id: 51, name: 'Crystal Palace' },
            { id: 52, name: 'AFC Bournemouth' }
        ]
    },
    {
        name: 'La Liga',
        slug: 'laliga',
        seasonId: 25659,
        country: 'Spain',
        teams: [
            { id: 36, name: 'Celta de Vigo' },
            { id: 83, name: 'FC Barcelona' },
            { id: 93, name: 'Real Oviedo' },
            { id: 106, name: 'Getafe' },
            { id: 214, name: 'Valencia' },
            { id: 231, name: 'Girona' },
            { id: 377, name: 'Rayo Vallecano' },
            { id: 459, name: 'Osasuna' },
            { id: 485, name: 'Real Betis' },
            { id: 528, name: 'Espanyol' },
            { id: 594, name: 'Real Sociedad' },
            { id: 645, name: 'Mallorca' },
            { id: 676, name: 'Sevilla' },
            { id: 1099, name: 'Elche' },
            { id: 2975, name: 'Deportivo Alavés' },
            { id: 3457, name: 'Levante' },
            { id: 3468, name: 'Real Madrid' },
            { id: 3477, name: 'Villarreal' },
            { id: 7980, name: 'Atlético Madrid' },
            { id: 13258, name: 'Athletic Club' }
        ]
    },
    {
        name: 'Serie A',
        slug: 'seriea',
        seasonId: 25533,
        country: 'Italy',
        teams: [
            { id: 37, name: 'Roma' },
            { id: 43, name: 'Lazio' },
            { id: 102, name: 'Genoa' },
            { id: 109, name: 'Fiorentina' },
            { id: 113, name: 'Milan' },
            { id: 268, name: 'Como' },
            { id: 346, name: 'Udinese' },
            { id: 398, name: 'Parma' },
            { id: 585, name: 'Cagliari' },
            { id: 597, name: 'Napoli' },
            { id: 613, name: 'Torino' },
            { id: 625, name: 'Juventus' },
            { id: 708, name: 'Atalanta' },
            { id: 1072, name: 'Pisa' },
            { id: 1123, name: 'Hellas Verona' },
            { id: 2714, name: 'Sassuolo' },
            { id: 2930, name: 'Inter' },
            { id: 7790, name: 'Lecce' },
            { id: 8513, name: 'Bologna' },
            { id: 10722, name: 'Cremonese' }
        ]
    },
    {
        name: 'Bundesliga',
        slug: 'bundesliga',
        seasonId: 25646,
        country: 'Germany',
        teams: [
            { id: 68, name: 'Borussia Dortmund' },
            { id: 82, name: 'Werder Bremen' },
            { id: 90, name: 'FC Augsburg' },
            { id: 277, name: 'RB Leipzig' },
            { id: 353, name: 'St. Pauli' },
            { id: 366, name: 'Eintracht Frankfurt' },
            { id: 503, name: 'FC Bayern München' },
            { id: 510, name: 'VfL Wolfsburg' },
            { id: 683, name: 'Borussia Mönchengladbach' },
            { id: 794, name: 'FSV Mainz 05' },
            { id: 1079, name: 'FC Union Berlin' },
            { id: 2708, name: 'Hamburger SV' },
            { id: 2726, name: 'TSG Hoffenheim' },
            { id: 2831, name: 'Heidenheim' },
            { id: 3319, name: 'VfB Stuttgart' },
            { id: 3320, name: 'FC Köln' },
            { id: 3321, name: 'Bayer 04 Leverkusen' },
            { id: 3543, name: 'SC Freiburg' }
        ]
    }
];

// Position mapping
const POSITION_MAP = {
    24: { name: 'Goalkeeper', short: 'GK' },
    25: { name: 'Defender', short: 'DEF' },
    26: { name: 'Midfielder', short: 'MID' },
    27: { name: 'Forward', short: 'FWD' },
    28: { name: 'Attacker', short: 'ATT' }
};

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

class SmartRosterSync {
    constructor() {
        this.apiToken = API_TOKEN;
        this.playersPath = path.join(__dirname, '../../data/db/players.json');
        this.backupPath = path.join(__dirname, '../../data/db/players.backup.json');
        this.reportPath = path.join(__dirname, '../../data/db/sync-smart-report-' + new Date().toISOString().split('T')[0] + '.json');
        this.existingPlayers = [];
        this.allFetchedPlayers = [];
        this.playerCurrentClubs = new Map(); // Map playerId -> current teamId
        this.duplicatePlayers = new Map();
        this.report = {
            timestamp: new Date().toISOString(),
            leagues: {},
            summary: {
                playersAdded: 0,
                playersRemoved: 0,
                playersUpdated: 0,
                loanedPlayersExcluded: 0,
                duplicatesResolved: 0,
                totalPlayers: 0,
                errors: []
            },
            loanedPlayers: [],
            duplicatesFound: [],
            failedTeams: []
        };
    }

    generateSlug(text) {
        if (!text) return '';
        return text.toLowerCase()
            .replace(/\s+/g, '-')
            .replace(/[éèêë]/g, 'e')
            .replace(/[àáâä]/g, 'a')
            .replace(/[ç]/g, 'c')
            .replace(/[ñ]/g, 'n')
            .replace(/[üúùû]/g, 'u')
            .replace(/[öóòô]/g, 'o')
            .replace(/[îï]/g, 'i')
            .replace(/[\.]/g, '')
            .replace(/[&]/g, 'and')
            .replace(/[^a-z0-9-]/g, '');
    }

    async initialize() {
        try {
            const data = fs.readFileSync(this.playersPath, 'utf8');
            this.existingPlayers = JSON.parse(data);
            console.log(`📂 Loaded ${this.existingPlayers.length} existing players`);

            fs.writeFileSync(this.backupPath, data);
            console.log(`💾 Backup created: ${this.backupPath}`);
        } catch (error) {
            console.log('⚠️  No existing players.json, starting fresh');
            this.existingPlayers = [];
        }
    }

    async fetchPlayerCurrentTeam(playerId) {
        try {
            // Fetch player details to get current team
            const url = `https://api.sportmonks.com/v3/football/players/${playerId}`;
            const response = await axios.get(url, {
                params: {
                    api_token: this.apiToken,
                    include: 'team'
                }
            });

            if (response.data?.data?.team?.data) {
                return response.data.data.team.data.id;
            } else if (response.data?.data?.team_id) {
                return response.data.data.team_id;
            }

            return null;
        } catch (error) {
            // Silent fail - player might not have current team data
            return null;
        }
    }

    async fetchTeamSquad(teamId, seasonId, teamName) {
        try {
            const url = `https://api.sportmonks.com/v3/football/squads/seasons/${seasonId}/teams/${teamId}`;
            const response = await axios.get(url, {
                params: {
                    api_token: this.apiToken,
                    include: 'player'
                }
            });

            if (response.data && response.data.data) {
                return response.data.data;
            }
            return [];
        } catch (error) {
            console.log(`\n      ⚠️  Error fetching squad for ${teamName}: ${error.message}`);
            this.report.failedTeams.push({ team: teamName, teamId, error: error.message });
            return [];
        }
    }

    async processPlayer(squadEntry, team, league) {
        const player = squadEntry.player;
        if (!player) return null;

        // Check if player's current team matches the squad team
        let currentTeamId = this.playerCurrentClubs.get(player.id);

        if (!currentTeamId) {
            // Fetch current team if not cached
            currentTeamId = await this.fetchPlayerCurrentTeam(player.id);
            if (currentTeamId) {
                this.playerCurrentClubs.set(player.id, currentTeamId);
            }
        }

        // If player's current team is different, they're on loan
        if (currentTeamId && currentTeamId !== team.id) {
            this.report.loanedPlayers.push({
                name: player.display_name || player.name,
                squadTeam: team.name,
                currentTeamId: currentTeamId,
                playerId: player.id
            });
            this.report.summary.loanedPlayersExcluded++;
            return null; // Skip this player
        }

        // Get position
        const positionInfo = POSITION_MAP[squadEntry.position_id] || { name: 'Unknown', short: 'UNK' };
        let detailedPosition = positionInfo.name;
        if (squadEntry.detailed_position_id) {
            detailedPosition = DETAILED_POSITION_MAP[squadEntry.detailed_position_id] || detailedPosition;
        }

        const playerData = {
            sportmonksId: player.id,
            name: player.display_name || player.name || `Player ${squadEntry.jersey_number}`,
            slug: this.generateSlug(player.display_name || player.name || `player-${player.id}`),
            firstName: player.firstname || '',
            lastName: player.lastname || '',
            displayName: player.display_name || player.name || '',
            position: positionInfo.name,
            detailedPosition: detailedPosition,
            jerseyNumber: squadEntry.jersey_number || null,
            nationality: player.nationality || '',
            age: player.age || null,
            dateOfBirth: player.date_of_birth || null,
            height: player.height || null,
            weight: player.weight || null,
            image: player.image_path || null,
            isGoalkeeper: squadEntry.position_id === 24,
            isCaptain: squadEntry.captain || false,
            contractStart: squadEntry.start || null,
            contractEnd: squadEntry.end || null,
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
            id: `${player.id}_${team.id}`,
            lastUpdated: new Date().toISOString(),
            fetchTimestamp: Date.now()
        };

        return playerData;
    }

    trackDuplicates(playerData) {
        const playerId = playerData.sportmonksId;
        if (!this.duplicatePlayers.has(playerId)) {
            this.duplicatePlayers.set(playerId, []);
        }
        this.duplicatePlayers.get(playerId).push(playerData);
    }

    resolveDuplicates() {
        const finalPlayers = [];
        const duplicatesFound = [];

        for (const [playerId, playerInstances] of this.duplicatePlayers) {
            if (playerInstances.length > 1) {
                // Sort by fetch timestamp to keep the most recent
                playerInstances.sort((a, b) => b.fetchTimestamp - a.fetchTimestamp);

                const kept = playerInstances[0];
                const removed = playerInstances.slice(1);

                duplicatesFound.push({
                    playerName: kept.name,
                    playerId: playerId,
                    keptIn: kept.team.name,
                    removedFrom: removed.map(p => p.team.name)
                });

                finalPlayers.push(kept);
                this.report.summary.duplicatesResolved++;
            } else {
                finalPlayers.push(playerInstances[0]);
            }
        }

        if (duplicatesFound.length > 0) {
            this.report.duplicatesFound = duplicatesFound;
            console.log(`\n🔄 Resolved ${duplicatesFound.length} duplicate players`);
        }

        return finalPlayers;
    }

    async syncLeague(league) {
        console.log(`\n🔄 Processing ${league.name} (${league.teams.length} teams)...`);

        this.report.leagues[league.slug] = {
            name: league.name,
            teamsProcessed: 0,
            totalPlayers: 0,
            loanedPlayersExcluded: [],
            errors: []
        };

        let processedTeams = 0;

        for (const team of league.teams) {
            processedTeams++;
            process.stdout.write(`\r   📌 Processing: ${team.name} (${processedTeams}/${league.teams.length})`);

            try {
                const squad = await this.fetchTeamSquad(team.id, league.seasonId, team.name);

                if (squad.length === 0) {
                    console.log(`\n      ⚠️  No squad data for ${team.name}`);
                    continue;
                }

                // Process each player
                let teamPlayerCount = 0;
                let excludedCount = 0;

                for (const squadEntry of squad) {
                    const playerData = await this.processPlayer(squadEntry, team, league);
                    if (playerData) {
                        this.allFetchedPlayers.push(playerData);
                        this.trackDuplicates(playerData);
                        teamPlayerCount++;
                    } else {
                        excludedCount++;
                    }
                }

                if (excludedCount > 0) {
                    console.log(`\n      🚫 Excluded ${excludedCount} loaned players from ${team.name}`);
                }

                // Small delay to avoid rate limiting
                await new Promise(resolve => setTimeout(resolve, 300));

            } catch (error) {
                console.log(`\n      ❌ Error with ${team.name}: ${error.message}`);
                this.report.leagues[league.slug].errors.push({
                    team: team.name,
                    error: error.message
                });
            }
        }

        console.log(`\n   ✅ Processed ${league.name}`);
        this.report.leagues[league.slug].teamsProcessed = processedTeams;
    }

    async syncAll() {
        console.log('🚀 Starting SMART roster synchronization...');
        console.log(`📅 Date: ${new Date().toLocaleDateString()}`);
        console.log('=' . repeat(50));
        console.log('📋 Features:');
        console.log('   ✓ Auto-detect loaned players by current club');
        console.log('   ✓ Remove duplicates (keep latest)');
        console.log('   ✓ Smart player validation\n');

        await this.initialize();

        // Pre-fetch current teams for known players (optional optimization)
        console.log('🔍 Analyzing player current teams...\n');

        // Process each league
        for (const league of LEAGUES) {
            await this.syncLeague(league);

            if (LEAGUES.indexOf(league) < LEAGUES.length - 1) {
                console.log('⏳ Waiting before next league...');
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
        }

        // Resolve duplicates
        console.log('\n📊 Resolving duplicates...');
        const finalPlayers = this.resolveDuplicates();

        // Keep players from other leagues
        const leagueSlugs = LEAGUES.map(l => l.slug);
        const otherPlayers = this.existingPlayers.filter(p => !leagueSlugs.includes(p.league));
        const allPlayers = [...otherPlayers, ...finalPlayers];

        // Update summary
        this.report.summary.totalPlayers = allPlayers.length;

        // Sort players
        allPlayers.sort((a, b) => {
            if (a.league !== b.league) return a.league.localeCompare(b.league);
            if (a.team.name !== b.team.name) return a.team.name.localeCompare(b.team.name);
            return (a.jerseyNumber || 999) - (b.jerseyNumber || 999);
        });

        // Save data
        fs.writeFileSync(this.playersPath, JSON.stringify(allPlayers, null, 2));
        fs.writeFileSync(this.reportPath, JSON.stringify(this.report, null, 2));

        this.printSummary(allPlayers);
    }

    printSummary(allPlayers) {
        console.log('\n' + '='.repeat(60));
        console.log('📊 SMART SYNCHRONIZATION COMPLETE');
        console.log('='.repeat(60));

        console.log('\n📈 Overall Summary:');
        console.log(`   ✅ Total players: ${this.report.summary.totalPlayers}`);
        console.log(`   🚫 Loaned players auto-excluded: ${this.report.summary.loanedPlayersExcluded}`);
        console.log(`   🔄 Duplicates resolved: ${this.report.summary.duplicatesResolved}`);

        console.log('\n📋 League Breakdown:');
        for (const league of LEAGUES) {
            const count = allPlayers.filter(p => p.league === league.slug).length;
            console.log(`   ${league.name}: ${count} players`);
        }

        if (this.report.loanedPlayers.length > 0) {
            console.log('\n🚫 Loaned Players Auto-Detected (first 10):');
            this.report.loanedPlayers.slice(0, 10).forEach((p, i) => {
                console.log(`   ${i + 1}. ${p.name} (listed in ${p.squadTeam} but plays elsewhere)`);
            });
            if (this.report.loanedPlayers.length > 10) {
                console.log(`   ... and ${this.report.loanedPlayers.length - 10} more`);
            }
        }

        if (this.report.duplicatesFound.length > 0) {
            console.log('\n🔄 Duplicates Resolved:');
            this.report.duplicatesFound.slice(0, 5).forEach((dup, i) => {
                console.log(`   ${i + 1}. ${dup.playerName}: kept in ${dup.keptIn}`);
            });
        }

        console.log('\n📄 Files:');
        console.log(`   Players database: ${this.playersPath}`);
        console.log(`   Backup: ${this.backupPath}`);
        console.log(`   Report: ${this.reportPath}`);

        // Verification
        console.log('\n🔍 Verification:');
        const cornelius = allPlayers.find(p => p.name.toLowerCase().includes('cornelius'));
        if (cornelius) {
            console.log(`   ⚠️  Cornelius still in ${cornelius.team.name} (check if API data is correct)`);
        } else {
            console.log(`   ✅ Cornelius removed from database`);
        }
    }
}

// Main execution
async function main() {
    const syncer = new SmartRosterSync();

    try {
        await syncer.syncAll();
        console.log('\n✅ Smart roster synchronization completed!');
    } catch (error) {
        console.error('\n❌ Fatal error:', error.message);
        console.error(error.stack);
        process.exit(1);
    }
}

// Run if executed directly
if (require.main === module) {
    main();
}

module.exports = SmartRosterSync;