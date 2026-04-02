import { trackingFlag, botOptions } from "../utils/utils.js";
import { updateDjangoPlayer } from "./../utils/api.js";


function setupCoreBehaviors(bot) {

    bot.once('spawn', () => {
        updateDjangoPlayer(bot.username, true, 'B');
    });
    // checking the bot connection
    bot.on('login', () => {
        console.log("Bot connected");
    });

    // bot announcing its connection into the server
    bot.on('spawn', () => {
        bot.chat("I got connected!");
    });

    // checking player online status and updating the API
    bot.on('playerLeft', async (player) => {
        if (player.username != bot.username) {
            trackingFlag.active = false
        };
        const playerType = (player.username == bot.username) ? "B" : "H";
        await updateDjangoPlayer(player.username, false, playerType)
    })

    // checking player and bot online status and updating the API
    bot.on('playerJoined', async (player) => {
        const playerType = (player.username == bot.username) ? "B" : "H";
        await updateDjangoPlayer(player.username, true, playerType)
    })

    // update bot status when exit
    bot.on('end', (reason) => {
        const botName = botOptions.username;
        updateDjangoPlayer(botName, false, 'B');
        trackingFlag.active = false;
    })
}

export { setupCoreBehaviors };