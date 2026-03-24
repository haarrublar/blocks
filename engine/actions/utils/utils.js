const axios = require('axios');

const trackingFlag = { 
    active: false,
    inSpawnAlert: false 
};

const botOptions = {
    host: 'localhost',
    port: 25565,
    username: 'mc-bot', 
    version: '1.21.1'
};

module.exports = { 
    trackingFlag,
    botOptions
};