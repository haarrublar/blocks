async function getChatMessages(filters = {}) {
    try {
        const response = await axios.get(`http://127.0.0.1:8000/bot/chat/`, {
            params: filters,
            timeout: 10000
        });
        return response.data;
    } catch (error) {
        console.log(`[Error]:`, error.response?.data || error.message);
        return null;
    }
}

async function getPlayerConnection(botName) {
    try {
        const response = await axios.get('http://127.0.0.1:8000/bot/players/', {
            params: { username: botName },
            timeout: 2000
        });
        return response.data;
    } catch (error) {
        console.log(`[Connection Error]:`, error.message);
        return null;
    }
}

async function getActiveDates() {
    const response = await axios.get('http://127.0.0.1:8000/bot/chat/sessions/active/');
    return response.data; 
}

export {
    getChatMessages,
    getPlayerConnection,
    getActiveDates
}