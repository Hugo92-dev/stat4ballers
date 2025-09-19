const axios = require('axios');

async function test() {
    const apiToken = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';
    
    // Test get teams for a season 
    const url = 'https://api.sportmonks.com/v3/football/teams/seasons/23490';
    
    try {
        const response = await axios.get(url, {
            params: { 
                api_token: apiToken,
                include: 'squad.player'
            }
        });
        
        console.log('API Response status:', response.status);
        console.log('Teams received:', response.data?.data ? response.data.data.length : 'No data');
        
        if (response.data?.data && response.data.data.length > 0) {
            const marseille = response.data.data.find(t => t.id === 44);
            if (marseille) {
                console.log('Marseille found!');
                console.log('Squad size:', marseille.squad?.length || 0);
                if (marseille.squad && marseille.squad.length > 0) {
                    console.log('First player:', marseille.squad[0].player?.name);
                }
            }
        }
    } catch (error) {
        console.log('Error:', error.response?.status || error.message);
    }
}

test();
