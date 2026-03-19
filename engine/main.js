const mineflayer = require('mineflayer');
const express = require('express');
const app = express();
app.use(express.json());

const { setupCoreBehaviors } = require('./actions/behavior/core')
const { spawningPlayers } = require('./actions/behavior/spawn')

let bot;


app.get('/status', (req, res) => {
    const isOnline = !!bot && !!bot.entity;
    res.json({ bot_online: isOnline });
});

app.post('/start', (req, res) => {
    const options = req.body;
    bot = mineflayer.createBot(options);
    
    setupCoreBehaviors(bot)
    spawningPlayers(bot)

    res.json({ status: "Bot starting..." });
});


app.post('/execute', async (req, res) => {
    const { code } = req.body;
    try {
        // This runs the JS code sent from Python
        const result = await eval(`(async () => { ${code} })()`);
        res.json({ success: true, result });
    } catch (err) {
        res.json({ success: false, error: err.message });
    }
});

app.listen(3000, () => console.log('JS Executor ready on port 3000'));