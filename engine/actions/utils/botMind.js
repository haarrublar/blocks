import ollama from 'ollama'; 
import { CLASSIFIER_PROMPT } from './prompts.js';

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