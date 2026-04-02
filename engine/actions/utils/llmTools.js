import ollama from 'ollama'; 
import { CLASSIFIER_PROMPT } from './prompts.js';

async function classifySentiment(text) {
  const response = await ollama.chat({
    model: 'llama3.2:1b',
    messages: [
      { role: 'system', content: CLASSIFIER_PROMPT },
      { role: 'user', content: text }
    ]
  });

  return response.message.content.toLowerCase();
};

export {classifySentiment};