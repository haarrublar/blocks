import mineflayer from 'mineflayer';
import { pathfinder } from 'mineflayer-pathfinder';
import express from 'express';

const app = express();
app.use(express.json());

import { setupCoreBehaviors } from './behaviors/core.js';
import { spawningPlayers } from './behaviors/spawn.js';
import { guideLogic } from './behaviors/walkto.js';

let bot;


app.get('/status', (req, res) => {
    const isOnline = !!bot && !!bot.entity;
    res.json({ bot_online: isOnline });
});

app.post('/start', (req, res) => {
    const options = req.body;
    bot = mineflayer.createBot(options);

    bot.loadPlugin(pathfinder);
    
    setupCoreBehaviors(bot);
    spawningPlayers(bot);
    guideLogic(bot);
    

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