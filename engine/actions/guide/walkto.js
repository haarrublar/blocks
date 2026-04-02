import pkg from "mineflayer-pathfinder";
const { Movements, goals } = pkg;
import { map } from "./map.js";

let areaIndex = 0;
let stepIndex = 0;
let isTourActive = false;

function guideLogic(bot) {
  bot.on("messagestr", (message) => {
      handleGuideLogic(bot, message);
  })
}

async function handleGuideLogic(bot, message) {

  const command = message.split(' ');
  const player = command[0].replace(/[<>]/g, '');
  const instruction = command.slice(1).join(' ');


  if (!instruction || typeof message !== "string") return;


  if (command[0] != `<${bot.username}>`) {
    if (instruction.includes("start")) {
      isTourActive = true;
      areaIndex = 0;
      stepIndex = 0;
      bot.chat("Starting the complete tour! Follow me.");
      executeMove(bot);
    } else if (instruction.includes("continue") && isTourActive) {
      const areas = Object.keys(map);
      const currentAreaKey = areas[areaIndex];
      const steps = Object.keys(map[currentAreaKey]).filter(
        (k) => k !== "detail",
      );

      if (stepIndex < steps.length - 1) {
        stepIndex++;
      } else if (areaIndex < areas.length - 1) {
        areaIndex++;
        stepIndex = 0;
        bot.chat(`Entering: ${map[areas[areaIndex]].detail}`);
      } else {
        bot.chat("We have finished the entire tour! Type 'start' to go again.");
        isTourActive = false;
        return;
      }
      executeMove(bot);
    }
  }
}

function executeMove(bot) {
  const areas = Object.keys(map);
  const currentArea = areas[areaIndex];
  const steps = Object.keys(map[currentArea]).filter((k) => k !== "detail");
  const currentStepKey = steps[stepIndex];
  const coords = map[currentArea][currentStepKey];

  bot.chat(`Heading to ${currentStepKey.replace(/_/g, " ")}...`);

  const defaultMove = new Movements(bot);
  defaultMove.canDig = false;

  bot.pathfinder.setMovements(defaultMove);
  const goal = new goals.GoalNear(coords.x, coords.y, coords.z, 1);
  bot.pathfinder.setGoal(goal);
}

export { guideLogic };