import { saveBuildTask, triggerAIRequest } from '../intelligence/api.js';

function generateBuildPlan(bot) {
    bot.on('messagestr', (message, messagePosition, jsonMsg, sender, verified) => {
        parseBuildPlanningRequest(bot,message, messagePosition, jsonMsg)
    })
};

async function parseBuildPlanningRequest(bot,message, messagePosition, jsonMsg, sender) {
    const command = message.split(' ');
    const player = command[0].replace(/[<>]/g, '');
    const commandType = command[1];
    const instruction = command.slice(2).join(' ');

    if (command[0] != `<${bot.username}>` && command[1] == 'build-plan') {
        const playerPosition = bot.players[player]?.entity?.position;
        const ppCoordinanates = {
            x: Math.round(playerPosition.x),
            y: Math.round(playerPosition.y),
            z: Math.round(playerPosition.z)
        }
            
        // const taskId = await saveBuildTask(player, ppCoordinanates, commandType,instruction)
        // if (taskId) {
        //     console.log(`[Pipeline] Task #${taskId} initialized. Sending to Claude`)

        //     await triggerAIRequest(taskId, ppCoordinanates, instruction);

        //     console.log(`[Pipeline] Task #${taskId} complete`)
        // }
    };

};

export { generateBuildPlan };