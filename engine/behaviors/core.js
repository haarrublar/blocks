import { trackingFlag, botOptions } from "../utils/utils.js";
import { getOrCreateSession } from "../utils/sessionManager.js";
import { updatePlayerStatus, chat } from "../utils/api/apiPOST.js";
import { activeSessions } from "../utils/utils.js";

function setupCoreBehaviors(bot) {

    bot.once('spawn', () => {
        updatePlayerStatus(bot.username, true, 'B');
        const originalMessage = bot.chat.bind(bot);
        
        bot.chat = (message, silent = false, sessionId = null) => {
            const activeId = sessionId || bot.currentSessionId;

            if (!silent) {
                if (activeId) {
                    chat(activeId, bot.username, message);
                } else {
                    console.warn(`[Sync Skip] No session ID for: "${message}"`);
                }
                originalMessage(message);
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
        await updatePlayerStatus(player.username, false, playerType);
        if (activeSessions[player.username]) {
            delete activeSessions[player.username];
            console.log(`[Session] Closed for ${player.username} (Left Game)`);
        }
    });

    bot.on('playerJoined', async (player) => {
        if (player.username === bot.username) return; 
        await new Promise(resolve => setTimeout(resolve, 3000));
        await getOrCreateSession(player.username, bot.username);
        console.log(`[Session ready for ${player.username}]`);
        await updatePlayerStatus(player.username, true, 'H');
    });

    bot.on('end', () => {
        updatePlayerStatus(botOptions.username, false, 'B');
        trackingFlag.active = false;
    });
}

export { setupCoreBehaviors };