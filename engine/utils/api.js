import axios from 'axios';
import fs from 'fs';
import { exec } from 'child_process';

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

async function createSession(username) {
    const payload = {
        player:username,
    };
    try {
        const response = await axios.post('http://127.0.0.1:8000/bot/chat/sessions/', payload, { timeout: 10000 });
        console.log(`[Session Created] ${response.data.id}`);
        return response.data.id;
    } catch (error) {
        const html = error.response?.data;
        fs.writeFileSync('/tmp/django_error.html', typeof html === 'string' ? html : JSON.stringify(html, null, 2));
        exec('open /tmp/django_error.html');
    }
};

async function chat(sessionId, username, message) {
    const payload = {
        session:sessionId,
        sender: username,
        content: message,
    };
    try {
        await axios.post('http://127.0.0.1:8000/bot/chat/', payload, { timeout: 10000 });
        console.log(`[Django Update]`);
    } catch (error) {
        const html = error.response?.data;
        fs.writeFileSync('/tmp/django_error.html', typeof html === 'string' ? html : JSON.stringify(html, null, 2));
        exec('open /tmp/django_error.html');
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
        coordinates: ppCoordinanates,
        task_description: instruction,
    };
    try {
        const response = await axios.post(
            'http://127.0.0.1:8000/bot/process-ai/',
            payload,
            { timeout:2000 }
        );
    } catch (error) {
        console.log(`[AI Error] Task #${taskId}:`, error.response?.data || error.message);
        return null;
    }
}



export { 
    updateDjangoPlayer,
    createSession,
    chat,
    saveBuildTask,
    triggerAIRequest
};