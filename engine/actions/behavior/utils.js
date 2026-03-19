const axios = require('axios');

const trackingFlag = { 
    active: false,
    inSpawnAlert: false 
};

const botOptions = {
    host: 'localhost',
    port: 25565,
    username: 'mc-bot', // <--- This is our "Safety Name"
    version: '1.21.1'
};

async function updateDjangoPlayer(username, isConnected, type) {
    const payload = {
        username: username,
        is_connected: isConnected,
        player_type: type
    };
    try {
        await axios.post('http://127.0.0.1:8000/bot/players/', payload, { timeout: 2000 });
        console.log(`[Django Update] ${username}: ${isConnected ? 'Online' : 'Offline'}`);
    } catch (error) {
        console.log(`[Django Error] ${username}: ${error.message}`);
    }
}

module.exports = { 
    trackingFlag,
    botOptions,
    updateDjangoPlayer
};