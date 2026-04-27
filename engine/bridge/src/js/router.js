import { getSessions } from "../../../utils/api/apiGET.js";
import { initCalendar } from "./calendar.js";
import { refreshChat } from "./chat.js";
import { state } from "./state.js";

let views = {};

export function initNavigation() {
  views = {
    lobby: document.getElementById("lobby-view"),
    calendar: document.getElementById("calendar-view"),
    chat: document.getElementById("chat-view"),
    header: document.getElementById("header-view"),
    footer: document.getElementById("footer-view"),
    profileFooterIcon: document.querySelector(".icon:nth-child(1)"),
    chatFooterIcon: document.querySelector(".icon:nth-child(2)"),
    chatBackIcon: document.getElementById("back-to-search-session"),
    back2LobbyIcon: document.getElementById("back-to-lobby"),
  };

  if (views.chatFooterIcon) {
    views.chatFooterIcon.addEventListener("click", () => navigateTo("calendar"));
  }
  if (views.chatBackIcon) {
    views.chatBackIcon.addEventListener("click", () => navigateTo("calendar"));
  }
  if (views.back2LobbyIcon) {
    views.back2LobbyIcon.addEventListener("click", () => navigateTo("lobby"));
  }
}

export async function navigateTo(target) {
  // hide everything first
  views.lobby.style.display = "none";
  views.calendar.style.display = "none";
  views.chat.style.display = "none";
  views.header.style.display = "none";
  views.footer.style.display = "none";

  if (target === "chat") {
    views.chat.style.display = "flex";
    views.profileFooterIcon.classList.add("active");
    views.chatFooterIcon.classList.remove("active");

  } else if (target === "calendar") {
    views.calendar.style.display = "flex";
    views.header.style.display = "flex";
    views.footer.style.display = "flex";
    views.chatFooterIcon.classList.add("active");
    views.profileFooterIcon.classList.remove("active");

    // fetch sessions for this bot/user pair
    if (state.selectedBot) {
      const sessions = await getSessions([state.currentUser, state.selectedBot]);
      const activeDates = sessions.map(s => s.date);
      const sessionMap = {};
      sessions.forEach(s => sessionMap[s.date] = s.id);

      initCalendar(async (dateStr) => {
        const sessionId = sessionMap[dateStr];
        await refreshChat(sessionId);
        navigateTo("chat");
      }, activeDates);
    }

  } else if (target === "lobby") {
    views.lobby.style.display = "flex";
    views.header.style.display = "flex";
    views.footer.style.display = "flex";
    views.chatFooterIcon.classList.add("active");
    views.profileFooterIcon.classList.remove("active");
  }

  window.location.hash = target;
}