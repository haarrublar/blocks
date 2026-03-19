const { trackingFlag } = require('./utils')
const SPAWN_RADIUS = 19;


function spawningPlayers(bot) {
    bot.on('entitySpawn', (entity) => {
        handleEntitySpawn(bot, entity);
    });
}


function handleEntitySpawn(bot, entity) {
    setTimeout(() => {
        const players = Object.keys(bot.players);

        if (!entity) return;

        if (entity.type === 'player' && entity.username !== bot.username && players.length === 2) {
            trackingFlag.active = true;
            startRadarLoop(bot, entity, players[0], players[1]);
        }
    }, 500);
}

function startRadarLoop(bot, entity, name1, name2) {
    const interval = setInterval(() => {
        if (!trackingFlag.active) return clearInterval(interval);
        
        const p1 = bot.players[name1]?.entity?.position;
        const p2 = bot.players[name2]?.entity?.position;

        if (p1 && p2) {
            const distance = p1.distanceTo(p2);
            if (distance <= SPAWN_RADIUS) {
                bot.lookAt(entity.position.offset(0, entity.height, 0));
                if (!trackingFlag.inSpawnAlert) {
                    console.log(`${entity.username} entered zone`);
                    trackingFlag.inSpawnAlert = true;
                }
            } else {
                if (trackingFlag.inSpawnAlert) {
                    console.log(`${entity.username} exited zone`);
                    trackingFlag.inSpawnAlert = false;
                }
                trackingFlag.inSpawnAlert = false;
            }
        }
    }, 200);
}

module.exports = { spawningPlayers };