import { trackingFlag } from "../utils/utils.js";
import { startVoiceTranscription } from "./playerVoiceManager.js";
import { botVoice } from "./voiceManager.js";
import { handleGuideLogic, executeMove, currentTask } from "./walkto.js";

const SPAWN_RADIUS = 20;
const WAIT_THRESHOLD = 12;
const RESUME_THRESHOLD = 8;

let voiceProcess = null;

async function handlePlayerVoice(text, bot, entity) {
  console.log(`[BOT HEARD]: ${text}`);
  if (!text) return;
  const formattedMessage = `<${entity.username}> ${text}`;
  await handleGuideLogic(bot, formattedMessage);
}

function stopVoice() {
  if (voiceProcess) {
    voiceProcess.kill('SIGKILL');
    voiceProcess = null;
    console.log(`voice process shutdown`);
  }
}

function startRadarLoop(bot, entity, name1, name2) {
  const interval = setInterval(async () => {
    if (!trackingFlag.active) {
      stopVoice();
      return clearInterval(interval);
    }

    const p1 = bot.players[name1]?.entity?.position;
    const p2 = bot.players[name2]?.entity?.position;

    if (p1 && p2) {
      const distance = p1.distanceTo(p2);

      if (trackingFlag.inSpawnAlert && currentTask.areaKey) {

        if (distance > WAIT_THRESHOLD && !currentTask.isPaused) {
          bot.pathfinder.setGoal(null);
          currentTask.isPaused = true;
          bot.lookAt(p1);
          bot.chat("Waiting for you to catch up...");
          console.log("Tour paused: Player out of range.");
        }

        else if (distance < RESUME_THRESHOLD && currentTask.isPaused) {
          currentTask.isPaused = false;
          bot.chat("Great, let's continue.");
          executeMove(bot, currentTask.areaKey, currentTask.stepKey);
          console.log("Tour resumed.");
        }
      }

      if (distance <= SPAWN_RADIUS) {
        bot.lookAt(entity.position.offset(0, entity.height, 0));

        if (!trackingFlag.inSpawnAlert) {
          // Set flag FIRST before any async calls to prevent re-triggering
          trackingFlag.inSpawnAlert = true;
          botVoice(`Hello ${entity.username}! Welcome to the Library. Say "information" for a tour.`);

          if (!voiceProcess) {
            voiceProcess = startVoiceTranscription((text) => handlePlayerVoice(text, bot, entity));
          }
        }
      } else {
        if (trackingFlag.inSpawnAlert) {
          // Set flag FIRST before any async calls
          trackingFlag.inSpawnAlert = false;
          currentTask.areaKey = null;
          currentTask.stepKey = null;
          currentTask.isPaused = false;
          botVoice(`Bye bye ${entity.username}!`);
          stopVoice();
        }
      }
    }
  }, 200);
}

export function spawningPlayers(bot) {
  bot.on("entitySpawn", (entity) => {
    handleEntitySpawn(bot, entity);
  });
}

function handleEntitySpawn(bot, entity) {
  setTimeout(() => {
    const players = Object.keys(bot.players);
    if (!entity || entity.type !== "player" || entity.username === bot.username) return;

    if (players.length === 2) {
      trackingFlag.active = true;
      startRadarLoop(bot, entity, players[0], players[1]);
    }
  }, 500);
}