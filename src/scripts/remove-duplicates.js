const fs = require('fs');
const path = require('path');

async function removeDuplicates() {
    try {
        console.log('🔧 Removing duplicate players and keeping most recent data...\n');

        // Read current players
        const playersPath = path.join(__dirname, '../../data/db/players.json');
        const playersData = fs.readFileSync(playersPath, 'utf8');
        const players = JSON.parse(playersData);

        console.log(`📊 Starting with ${players.length} players`);

        // Group by sportmonksId
        const playerGroups = {};

        players.forEach(player => {
            const id = player.sportmonksId;
            if (!playerGroups[id]) {
                playerGroups[id] = [];
            }
            playerGroups[id].push(player);
        });

        // For each group, keep only the most recently updated player
        const uniquePlayers = [];
        let duplicatesRemoved = 0;

        Object.entries(playerGroups).forEach(([id, group]) => {
            if (group.length === 1) {
                // No duplicate, keep as is
                uniquePlayers.push(group[0]);
            } else {
                // Multiple players with same ID - keep the most recent
                const mostRecent = group.reduce((latest, current) => {
                    const latestDate = new Date(latest.lastUpdated || '1970-01-01');
                    const currentDate = new Date(current.lastUpdated || '1970-01-01');

                    // If dates are equal, prefer based on league priority (Serie A > Ligue 1 > Premier League > La Liga > Bundesliga)
                    // This handles cases where API updates happened at the same time
                    if (latestDate.getTime() === currentDate.getTime()) {
                        const leaguePriority = {
                            'seriea': 5,
                            'ligue1': 4,
                            'premierleague': 3,
                            'laliga': 2,
                            'bundesliga': 1
                        };

                        const latestPriority = leaguePriority[latest.league] || 0;
                        const currentPriority = leaguePriority[current.league] || 0;

                        return currentPriority > latestPriority ? current : latest;
                    }

                    return currentDate > latestDate ? current : latest;
                });

                uniquePlayers.push(mostRecent);
                duplicatesRemoved += (group.length - 1);

                // Log which player we kept for important cases
                if (group[0].name.toLowerCase().includes('rabiot') ||
                    group[0].name.toLowerCase().includes('rowe')) {
                    console.log(`🔧 ${group[0].name}: Kept at ${mostRecent.team.name} (${mostRecent.league})`);
                    group.forEach(player => {
                        if (player !== mostRecent) {
                            console.log(`   ❌ Removed from ${player.team.name} (${player.league})`);
                        }
                    });
                }
            }
        });

        // Sort by sportmonksId
        uniquePlayers.sort((a, b) => a.sportmonksId - b.sportmonksId);

        // Create backup
        const backupPath = playersPath.replace('.json', '.backup.json');
        fs.writeFileSync(backupPath, playersData);

        // Write cleaned data
        fs.writeFileSync(playersPath, JSON.stringify(uniquePlayers, null, 2));

        console.log(`\n✅ Cleanup completed!`);
        console.log(`📊 Summary:`);
        console.log(`- Original players: ${players.length}`);
        console.log(`- Duplicates removed: ${duplicatesRemoved}`);
        console.log(`- Final players: ${uniquePlayers.length}`);
        console.log(`- Backup saved to: ${backupPath}`);

        // Verify specific players
        console.log(`\n🔍 Verification:`);
        const rabiot = uniquePlayers.find(p => p.name.toLowerCase().includes('rabiot'));
        const rowe = uniquePlayers.find(p => p.name.toLowerCase().includes('rowe') && p.name.includes('Jonathan'));

        if (rabiot) {
            console.log(`- Rabiot: ${rabiot.name} at ${rabiot.team.name} (${rabiot.league})`);
        }
        if (rowe) {
            console.log(`- Jonathan Rowe: ${rowe.name} at ${rowe.team.name} (${rowe.league})`);
        }

    } catch (error) {
        console.error('❌ Error:', error.message);
    }
}

removeDuplicates();