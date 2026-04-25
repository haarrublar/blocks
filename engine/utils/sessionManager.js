import { postCreateSession } from "./api/apiPOST.js";

const sessions = {};

export async function getOrCreateSession(playerUsername, botUsername) {
  const key = [playerUsername, botUsername].sort().join('_');

  if (sessions[key]) {
    return sessions[key];
  }

  const sessionId = await postCreateSession([playerUsername, botUsername]);
  if (sessionId) {
    sessions[key] = sessionId;
  }
  return sessionId;
}

export function clearSession(playerUsername, botUsername) {
  const key = [playerUsername, botUsername].sort().join('_');
  delete sessions[key];
}
