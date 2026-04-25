import { getUsers } from "../../../utils/api/apiGET.js";

export async function getConnection() {
	const playerData = await getUsers({ username: "haarrublar" });
	const botData = await getUsers({ player_type: "B" });

	if (playerData && playerData.length > 0) {
		const isConnected = playerData[0].is_connected;
		const playerName = playerData[0].username;

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

	if (botData && botData.length > 0) {
		const listWrapper = document.getElementById("bots-list-wrapper");

		if (listWrapper) {
			listWrapper.innerHTML = "";

			botData.forEach((bot) => {
				const botItem = document.createElement("div");
				botItem.classList.add("lobby-item");

				const bgColor = bot.is_connected ? "#59A88F" : "#F0D1DF";
				const statusText = bot.is_connected ? "connected" : "disconnected";

				botItem.style.background = bgColor;
				botItem.innerHTML = `
                <p class="bot-name-label" style="font-weight: bold;">${bot.username.toUpperCase()}</p>
                <p class="bot-status-label" style="margin-left: 10px;">
                    ${statusText}
                </p>
            `;

				listWrapper.appendChild(botItem);
			});
		}
	}
}
