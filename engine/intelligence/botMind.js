import ollama from 'ollama'; 

async function botPersona(text,role) {
  const response = await ollama.chat({
    model: 'llama3.2:1b',
    messages: [
      { role: 'system', content: role },
      { role: 'user', content: text }
    ]
  });

  return response.message.content.toLowerCase();
};

export {botPersona};