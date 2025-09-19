const axios = require('axios');

async function test() {
    const apiToken = 'KCKLQvVx687XrO9EBMLbZYEf8lQ7frEfZ9dvSqHt9PSIYMplUiVI3s3g34qZ';
    
    // Test Marseille (Ligue 1)
    const url = 'https://api.sportmonks.com/v3/football/squads/seasons/23490/teams/44';
    
    try {
        const response = await axios.get(url, {
            params: { api_token: apiToken }
        });
        
        console.log('API Response status:', response.status);
        console.log('Data received:', response.data?.data ? `${response.data.data.length} players` : 'No data');
        
        if (response.data?.data && response.data.data.length > 0) {
            console.log('First player:', response.data.data[0].player?.name);
        }
    } catch (error) {
        console.log('Error:', error.response?.status || error.message);
        if (error.response?.data) {
            console.log('Error data:', JSON.stringify(error.response.data, null, 2));
        }
    }
}

test();
