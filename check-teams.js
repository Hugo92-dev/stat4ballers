const fs = require('fs');

const players = JSON.parse(fs.readFileSync('data/db/players.json'));

const problemTeams = ['Leeds United', 'Atletico Madrid', 'Borussia Mönchengladbach'];

console.log('Checking problematic teams:');
console.log('==========================\n');

for (const league of Object.values(players)) {
    for (const team of problemTeams) {
        const teamPlayers = league.filter(p => p.team === team);
        if (teamPlayers.length > 0) {
            console.log(`${team}: ${teamPlayers.length} players`);
        }
    }
}

console.log('\nAll teams summary:');
console.log('==================');

const teamCounts = {};
for (const league of Object.values(players)) {
    for (const player of league) {
        if (!teamCounts[player.team]) {
            teamCounts[player.team] = 0;
        }
        teamCounts[player.team]++;
    }
}

const emptyTeams = [];
for (const [team, count] of Object.entries(teamCounts)) {
    if (count < 15) {
        emptyTeams.push(`${team}: ${count} players`);
    }
}

if (emptyTeams.length > 0) {
    console.log('Teams with less than 15 players:');
    emptyTeams.forEach(t => console.log(`  - ${t}`));
} else {
    console.log('✅ All teams have at least 15 players!');
}

console.log(`\nTotal teams: ${Object.keys(teamCounts).length}`);
console.log(`Total players: ${Object.values(teamCounts).reduce((a,b) => a+b, 0)}`);
