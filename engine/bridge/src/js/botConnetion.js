import { getPlayerConnection } from "../../../utils/api/apiGET.js";

export async function getConnection() {
  const connectionData = await getPlayerConnection("haarrublar");

  console.log(connectionData);
  if (connectionData && connectionData.length > 0) {
    const isConnected = connectionData[0].is_connected;
    const playerName = connectionData[0].username;

    const allStatusBoxes = document.querySelectorAll(".status-box");
    const allBotImages = document.querySelectorAll(".bot-photo img");
    const playerNameSpan = document.querySelectorAll(".player-name");

    playerNameSpan.forEach((span) => {
      span.textContent = playerName;
    });

    allStatusBoxes.forEach((statusBox) => {
      const statusText = statusBox.nextElementSibling;
      const statusWrapper = statusBox.closest(".bot-status");

      if (statusBox && statusText) {
        statusText.style.fontWeight = "bold";

        if (isConnected) {
          statusBox.style.backgroundColor = "#59A88F";
          statusText.textContent = " connected ";
          statusText.style.color = "#59A88F";
        } else {
          statusBox.style.backgroundColor = "#F0D1DF";
          statusText.textContent = " disconnected ";
          statusText.style.color = "#F0D1DF";
        }

        if (statusWrapper) statusWrapper.classList.add("ready");
      }
    });

    allBotImages.forEach((img) => {
      const container = img.closest(".bot-photo");

      if (isConnected) {
        img.src = "./src/images/botConnected.png";
      } else {
        img.src = "./src/images/botDisconnected.png";
      }

      if (container) container.classList.add("ready");
    });
  }
}
