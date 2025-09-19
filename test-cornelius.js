const axios = require('axios');

async function test() {
    const res = await axios.get('https://api.sportmonks.com/v3/football/players/586846', {
        params: {
            api_token: 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ',
            include: 'teams'
        }
    });

    const teams = res.data.data.teams;
    console.log('All teams for Cornelius:');
    teams.forEach(t => {
        console.log(`- Team ID: ${t.team_id}, End: ${t.end || 'Active'}`);
    });

    const currentTeams = teams.filter(t => {
        if (!t.end || t.end === null) return true;
        const endDate = new Date(t.end);
        return endDate > new Date();
    }).map(t => t.team_id);

    console.log('\nCurrent teams:', currentTeams);
    console.log('Is in Marseille (44)?', currentTeams.includes(44));
}

test();