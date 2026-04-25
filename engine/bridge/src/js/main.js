import { initCalendar } from "./calendar.js";
import { refreshChat } from "./chat.js";
import { getConnection } from "./userConnetion.js";
import { getActiveDates } from "../../../utils/api/apiGET.js";
import { navigateTo, initNavigation } from "./router.js";

async function loadComponent(id, url) {
  const response = await fetch(url);
  const html = await response.text();
  document.getElementById(id).innerHTML = html;
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await loadComponent("header-view", "./src/components/header.html");
    await loadComponent("lobby-view", "./src/components/lobby.html");
    await loadComponent("calendar-view", "./src/components/calendar.html");
    await loadComponent("chat-view", "./src/components/chat.html");
    await loadComponent("footer-view", "./src/components/footer.html");
    
    initNavigation();

    const backBtn = document.getElementById("back-to-calendar");
    if (backBtn)
      backBtn.addEventListener("click", () => navigateTo("calendar"));

    await getConnection();
    const activeDates = await getActiveDates();
    const todayStr = new Date().toISOString().split("T")[0];
    await refreshChat(todayStr);

    initCalendar(async (dateStr) => {
      await refreshChat(dateStr);
      await getConnection();
      navigateTo("chat");
    }, activeDates);

    navigateTo("calendar");
  } catch (err) {
    console.error("Init error:", err);
  }
});
