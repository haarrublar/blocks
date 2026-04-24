import { getChatMessages } from "../../../utils/api/apiGET.js";

export async function refreshChat(dateStr) {
  const messages = await getChatMessages({ date: dateStr });
  const chatHistory = document.querySelector('.chat-history');
  if (messages && messages.length > 0) {
    renderMessages(messages);
  } else {
    chatHistory.innerHTML = '<p style="text-align:center; padding:20px;">No history for this day.</p>';
  }
}

function renderMessages(messages) {
  const chatHistory = document.querySelector('.chat-history');
  chatHistory.innerHTML = '';
  messages.forEach(msg => {
    const p = document.createElement('p');
    p.textContent = msg.content;
    p.style.margin = "4px 0";
    p.style.padding = "10px";
    p.style.border = "1px solid black";
    p.style.maxWidth = "70%";
    p.style.wordWrap = "break-word";
    if (msg.sender === 'haarrublar') {
      p.style.alignSelf = 'flex-end';
      p.style.backgroundColor = '#55a084';
      p.style.color = 'white';
      p.style.textAlign = 'right';
    } else {
      p.style.alignSelf = 'flex-start';
      p.style.backgroundColor = '#ffffff';
      p.style.color = 'black';
      p.style.textAlign = 'left';
    }
    chatHistory.appendChild(p);
  });
}