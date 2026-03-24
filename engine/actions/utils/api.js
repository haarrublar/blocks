const axios = require('axios');

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
};

async function saveBuildTask(playerUsername, ppCoordinanates, commandType, message) {
    const payload = {
        player: playerUsername,
        coordinates: ppCoordinanates,
        task_type: commandType,
        raw_prompt: message,
    };
    try {
        const response = await axios.post(
            'http://127.0.0.1:8000/bot/agent/', 
            payload, 
            { timeout: 2000 }
        );
        const taskId = response.data.id;
        if (taskId) {
            console.log(`[Database Success] Task #${taskId} created for ${playerUsername}`);
            return taskId;
        } else {
            console.log(`[Database Warning] Record saved, but no ID returned. Check Serializer fields.`);
            return null;
        }
        return taskId;
    } catch (error) {
        console.log(`[Django Error]:`, error.response?.data || error.message);
        return null;
    }
};

async function triggerAIRequest(taskId, ppCoordinanates, instruction) {
    const payload = {
        task_id: taskId,
        player_coordinates: ppCoordinanates,
        task_description: instruction,
    };
    try {
        const response = await axios.post(
            'http://127.0.0.1:8000/bot/process-ai/',
            payload,
            { timeout: 2000 }
        );
        return response.data;
    } catch (error) {
        const data = error.response?.data;

        if (typeof data === "string" && data.trim().startsWith("<")) {
            // Django error page — save and open in browser
            const errorPath = `/tmp/django_error_${taskId}.html`;
            require("fs").writeFileSync(errorPath, data);
            require("child_process").exec(`open ${errorPath}`);
            console.error(`[AI Error] Task #${taskId}: Django error opened in browser`);
        } else {
            console.error(`[AI Error] Task #${taskId}:`, data || error.message);
        }

        return null;
    }
}



module.exports = { 
    updateDjangoPlayer,
    saveBuildTask,
    triggerAIRequest
};