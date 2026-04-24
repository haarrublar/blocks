import pkg from "mineflayer-pathfinder";
const { Movements, goals } = pkg;

import { activeSessions } from "../utils/utils.js";
import { botPersona } from "../intelligence/botMind.js";
import { botVoice } from "./voiceManager.js";
import { GUIDE } from "../intelligence/prompts.js";
import { map } from "../utils/map.js";
import { postChatMessages, postCreateSession } from "../utils/api/apiPOST.js";

function guideLogic(bot) {
  bot.on("messagestr", (message) => {
    handleGuideLogic(bot, message);
  });
}

export let currentTask = {
  areaKey: null,
  stepKey: null,
  isPaused: false,
};

let areaIndex = 0;
let stepIndex = 0;
let startAreaIndex = 0;
let isTourActive = false;
let isWaitingForSelection = false;
let isWaitingForQuestion = false;

const welcomedPlayers = new Set();

async function handleGuideLogic(bot, message) {
  const command = message.split(" ");
  const player = command[0].replace(/[<>]/g, "");
  const instruction = command.slice(1).join(" ").toLowerCase().trim();

  if (!instruction || typeof message !== "string") return;

  console.log(command[0], player, instruction);

  if (command[0] !== `<${bot.username}>`) {
    
    console.log(instruction);
    
    if (!activeSessions[player]) {
      const sessionUuid = await postCreateSession(player);

      if (sessionUuid) {
        activeSessions[player] = sessionUuid; 
      } else {
        console.error("Failed to initialize session for", player);
        return;
      }
    }

    const sessionId = activeSessions[player];
    bot.currentSessionId = sessionId;
    postChatMessages(sessionId, player, instruction);

    if (!welcomedPlayers.has(player)) {
      const welcomeMsg = `Welcome to the guided tour ${player}!`;
      bot.postChatMessages(welcomeMsg, false, sessionId);
      welcomedPlayers.add(player);
    }

    const areas = Object.keys(map);

    const helpKeywords = ["tour", "help", "information"];

    if (helpKeywords.some((keyword) => instruction.includes(keyword))) {
      const commandsMsg = `Commands: 'start' (full tour), 'move to' (pick a building), or 'continue' (next stop), 'question' (ask any question to the librarian)`;
      bot.postChatMessages(commandsMsg, false, sessionId);
      return;
    }

    if (isWaitingForSelection) {
      const selectedArea = areas.find((a) => a.toLowerCase() === instruction);

      if (selectedArea) {
        isWaitingForSelection = false;
        isTourActive = true;

        areaIndex = areas.indexOf(selectedArea);
        startAreaIndex = areaIndex;
        stepIndex = 0;

        const steps = Object.keys(map[selectedArea]);
        const selectedAreMsg = `Starting tour at ${selectedArea}. We will loop through all buildings!`;
        bot.postChatMessages(selectedAreMsg, false, sessionId);
        executeMove(bot, selectedArea, steps[stepIndex], sessionId);
      }

      return;
    }

    const exitKeywords = ["stop"];

    if (
      isWaitingForQuestion &&
      exitKeywords.some((k) => instruction.includes(k))
    ) {
      isWaitingForQuestion = false;
      const byeMsg = `You're very welcome, ${player}! Let me know if you need anything else.`;
      bot.postChatMessages(byeMsg, false, sessionId);
      // botVoice("You are very welcome! Let me know if you need anything else.", "Samantha");
      return;
    }

    if (isWaitingForQuestion) {
      const introReasoningMsg = "Let me think about that...";
      bot.postChatMessages(introReasoningMsg, true, sessionId);

      const response = await botPersona(instruction, GUIDE);
      const reasoningMsg = `${introReasoningMsg} ${response.replace(/\n/g, " ")}`;
      bot.postChatMessages(reasoningMsg, false, sessionId);
      console.log("CALLING BOT.postChatMessages WITH:", reasoningMsg);
      console.log("IS OVERRIDDEN:", bot.postChatMessages.toString().includes("silent"));
      // botVoice(response, 'Samantha');
      return;
    }

    if (instruction.includes("question")) {
      isWaitingForQuestion = true;
      const questionMsg = `${player} what questions do you have?`;
      bot.postChatMessages(questionMsg, false, sessionId);
      return;
    } else if (instruction.includes("move to")) {
      isWaitingForSelection = true;
      const moveToMsg = `${player}, please select the building you would like to explore: ${areas.join(", ")}`;
      bot.postChatMessages(moveToMsg, false, sessionId);
    } else if (instruction.includes("start")) {
      isTourActive = true;
      areaIndex = 0;
      stepIndex = 0;
      const currentAreaKey = areas[areaIndex];
      const steps = Object.keys(map[currentAreaKey]);
      const startMsg = "Starting the complete tour!";
      bot.postChatMessages(startMsg, false, sessionId);
      executeMove(bot, currentAreaKey, steps[stepIndex], sessionId);
    } else if (instruction.includes("continue") && isTourActive) {
      let currentAreaKey = areas[areaIndex];
      let steps = Object.keys(map[currentAreaKey]);

      if (stepIndex < steps.length - 1) {
        stepIndex++;
      } else {
        const nextAreaIndex = (areaIndex + 1) % areas.length;

        if (nextAreaIndex === startAreaIndex) {
          const completeTourMsg = `Tour complete! Have a nice day ${player}`;
          bot.postChatMessages(completeTourMsg, false, sessionId);
          isTourActive = false;
          return;
        }

        areaIndex = nextAreaIndex;
        stepIndex = 0;
        currentAreaKey = areas[areaIndex];
        steps = Object.keys(map[currentAreaKey]);
        const MovingNextStopMsg = `Building finished. Moving to the next stop: ${map[currentAreaKey].detail}`;
        bot.postChatMessages(MovingNextStopMsg, false, sessionId);
      }

      executeMove(bot, currentAreaKey, steps[stepIndex], sessionId);
    }
  }
}

async function executeMove(bot, areaKey, stepKey, sessionId) {
  try {
    currentTask.areaKey = areaKey;
    currentTask.stepKey = stepKey;

    const coords = map[areaKey][stepKey]["coordinates"];
    const detail = map[areaKey][stepKey]["detail"];

    bot.removeAllListeners("goal_reached");
    bot.postChatMessages(`Heading to ${stepKey}...`, false, sessionId);

    const defaultMove = new Movements(bot);
    defaultMove.canDig = false;
    bot.pathfinder.setMovements(defaultMove);

    const goal = new goals.GoalNear(coords.x, coords.y, coords.z, 1);
    bot.pathfinder.setGoal(goal);

    const botResponse = await botPersona(detail, GUIDE);

    let hasSpoken = false;
    bot.once("goal_reached", async () => {
      if (hasSpoken) return;
      if (currentTask.isPaused) return;
      if (currentTask.areaKey !== areaKey || currentTask.stepKey !== stepKey)
        return;

      hasSpoken = true;
      await botVoice(botResponse, "Samantha");
    });
  } catch (err) {
    console.error("Movement/Voice error:", err);
  }
}

export { guideLogic, handleGuideLogic, executeMove };
