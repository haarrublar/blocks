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
    views.chatFooterIcon.addEventListener("click", () =>
      navigateTo("calendar"),
    );
  }

  if (views.chatBackIcon) {
    views.chatBackIcon.addEventListener("click", () => navigateTo("calendar"));
  }

  if (views.back2LobbyIcon) {
    views.back2LobbyIcon.addEventListener("click", () => navigateTo("lobby"));
  }

}

export function navigateTo(target) {
  views.lobby.style.display = "none";
  views.calendar.style.display = "none";
  views.chat.style.display = "none";
  views.header.style.display = "none";
  views.footer.style.display = "none";

  if (target === "chat") {
    views.lobby.style.display = "none";
    views.calendar.style.display = "none";
    views.chat.style.display = "flex";
    views.footer.style.display = "none";
    views.header.style.display = "none";
    views.profileFooterIcon.classList.add("active");
    views.chatFooterIcon.classList.remove("active");
  } else if (target === "calendar") {
    views.lobby.style.display = "none";
    views.calendar.style.display = "flex";
    views.chat.style.display = "none";
    views.header.style.display = "flex";
    views.footer.style.display = "flex";
    views.chatFooterIcon.classList.add("active");
    views.profileFooterIcon.classList.remove("active");
  } else if (target === "lobby") {
    views.lobby.style.display = "flex";
    views.calendar.style.display = "none";
    views.chat.style.display = "none";
    views.header.style.display = "flex";
    views.footer.style.display = "flex";
    views.chatFooterIcon.classList.add("active");
    views.profileFooterIcon.classList.remove("active");
  }

  window.location.hash = target;
}
