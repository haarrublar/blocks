let views = {};

export function initNavigation() {
  views = {
    calendar: document.getElementById("calendar-view"),
    chat: document.getElementById("chat-view"),
    CRHeader: document.getElementById("chat-room-header"),
    footer: document.getElementById("footer"),
    profileFooterIcon: document.querySelector(".icon:nth-child(1)"),
    chatFooterIcon: document.querySelector(".icon:nth-child(2)"),
    chatBackIcon: document.getElementById("back-to-search-session"),
  };

  if (views.chatFooterIcon) {
    views.chatFooterIcon.addEventListener("click", () =>
      navigateTo("calendar"),
    );
  }

  if (views.chatBackIcon) {
    views.chatBackIcon.addEventListener("click", () => navigateTo("calendar"));
  }
}

export function navigateTo(target) {
  if (target === "chat") {
    views.calendar.style.display = "none";
    views.footer.style.display = "none";
    views.chat.style.display = "flex";
    views.CRHeader.style.display = "none";
    views.profileFooterIcon.classList.add("active");
    views.chatFooterIcon.classList.remove("active");
  } else if (target === "calendar") {
    views.chat.style.display = "none";
    views.calendar.style.display = "flex";
    views.CRHeader.style.display = "flex";
    views.footer.style.display = "flex";
    views.chatFooterIcon.classList.add("active");
    views.profileFooterIcon.classList.remove("active");
  }
  window.location.hash = target;
}
