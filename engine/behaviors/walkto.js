import pkg from "mineflayer-pathfinder";
const { Movements, goals } = pkg;

import { botPersona } from "../intelligence/botMind.js";
import { botVoice } from "./voiceManager.js";
import { GUIDE } from "../intelligence/prompts.js";
import { map } from "../utils/map.js";

function guideLogic(bot) {
  bot.on("messagestr", (message) => {
    handleGuideLogic(bot, message);
  });
}

let areaIndex = 0;
let stepIndex = 0;
let startAreaIndex = 0;
let isTourActive = false;
let isWaitingForSelection = false;

async function handleGuideLogic(bot, message) {
  const command = message.split(" ");
  const player = command[0].replace(/[<>]/g, "");
  const instruction = command.slice(1).join(" ").toLowerCase().trim();

  if (!instruction || typeof message !== "string") return;

  if (command[0] !== `<${bot.username}>`) {
    const areas = Object.keys(map);

    const helpKeywords = ["tour", "help", "info"];
    if (helpKeywords.some((keyword) => instruction === keyword)) {
      bot.chat(`Welcome to the guided tour ${player}!`);
      bot.chat(
        "Commands: 'start' (full tour), 'move to' (pick a building), or 'continue' (next stop).",
      );
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
        bot.chat(
          `Starting tour at ${selectedArea}. We will loop through all buildings!`,
        );
        executeMove(bot, selectedArea, steps[stepIndex]);
      }
      return;
    }

    if (instruction === "move to") {
      isWaitingForSelection = true;
      bot.chat(
        `${player}, please select the building you would like to explore: ${areas.join(", ")}`,
      );
    } else if (instruction === "start") {
      isTourActive = true;
      areaIndex = 0;
      stepIndex = 0;
      const currentAreaKey = areas[areaIndex];
      const steps = Object.keys(map[currentAreaKey]);
      bot.chat("Starting the complete tour!");
      executeMove(bot, currentAreaKey, steps[stepIndex]);
    } else if (instruction === "continue" && isTourActive) {
      let currentAreaKey = areas[areaIndex];
      let steps = Object.keys(map[currentAreaKey]);

      if (stepIndex < steps.length - 1) {
        stepIndex++;
      } else {
        const nextAreaIndex = (areaIndex + 1) % areas.length;

        if (nextAreaIndex === startAreaIndex) {
          bot.chat(`Tour complete! Have a nice day ${player}`);
          isTourActive = false;
          return;
        }

        areaIndex = nextAreaIndex;
        stepIndex = 0;
        currentAreaKey = areas[areaIndex];
        steps = Object.keys(map[currentAreaKey]);
        bot.chat(
          `Building finished. Moving to the next stop: ${map[currentAreaKey].detail}`,
        );
      }

      executeMove(bot, currentAreaKey, steps[stepIndex]);
    }
  }
}

async function executeMove(bot, areaKey, stepKey) {
  try {
    const coords = map[areaKey][stepKey]["coordinates"];
    const detail = map[areaKey][stepKey]["detail"];
    bot.removeAllListeners("goal_reached");

    bot.chat(`Heading to ${stepKey}...`);
    const defaultMove = new Movements(bot);
    defaultMove.canDig = false;
    bot.pathfinder.setMovements(defaultMove);

    const goal = new goals.GoalNear(coords.x, coords.y, coords.z, 1);
    bot.pathfinder.setGoal(goal);

    const botResponse = await botPersona(detail, GUIDE);

    let hasSpoken = false;
    bot.once("goal_reached", async () => {
      if (hasSpoken) return; 
      hasSpoken = true;

      await botVoice(botResponse, 'Samantha'); 
    });
  } catch (err) {
    console.error("Movement/Voice error:", err);
  }
}

export { guideLogic };
