import { trackingFlag, botOptions } from "../utils/utils.js";
import { updateDjangoPlayer, chat } from "../utils/api.js";
import { activeSessions } from "../utils/utils.js";

function setupCoreBehaviors(bot) {

    bot.once('spawn', () => {
        updateDjangoPlayer(bot.username, true, 'B');

        const originalChat = bot.chat.bind(bot);
        
        bot.chat = (message, silent = false, sessionId = null) => {
            const activeId = sessionId || bot.currentSessionId;

            if (!silent) {
                if (activeId) {
                    chat(activeId, bot.username, message);
                } else {
                    console.warn(`[Sync Skip] No session ID for: "${message}"`);
                }
                originalChat(message);
            }
        };
    });

    bot.on('login', () => {
        console.log("Bot connected");
    });

    bot.on('playerLeft', async (player) => {
        if (player.username !== bot.username) {
            trackingFlag.active = false;
        }
        const playerType = (player.username === bot.username) ? "B" : "H";
        await updateDjangoPlayer(player.username, false, playerType);
        if (activeSessions[player.username]) {
            delete activeSessions[player.username];
            console.log(`[Session] Closed for ${player.username} (Left Game)`);
        }
    });

    bot.on('playerJoined', async (player) => {
        if (player.username === bot.username) return; 
        await updateDjangoPlayer(player.username, true, 'H');
    });

    bot.on('end', () => {
        updateDjangoPlayer(botOptions.username, false, 'B');
        trackingFlag.active = false;
    });
}

export { setupCoreBehaviors };