export function initCalendar(onSelect, activeDates) {
  const selectBtn = document.getElementById("cal-select-btn");
  selectBtn.disabled = true;

  const MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  const today = new Date();
  let view = { year: today.getFullYear(), month: today.getMonth() };

  let selected = null;
  let selectedInactive = null;

  function render() {
    document.getElementById("cal-month-label").textContent =
      MONTHS[view.month] + " " + view.year;

    const grid = document.getElementById("cal-days");
    grid.innerHTML = "";

    const firstDay = new Date(view.year, view.month, 1);
    let startDay = firstDay.getDay();
    startDay = startDay === 0 ? 6 : startDay - 1;
    const daysInMonth = new Date(view.year, view.month + 1, 0).getDate();
    const prevMonthDays = new Date(view.year, view.month, 0).getDate();

    // Previous month filler days
    for (let i = 0; i < startDay; i++) {
      const d = document.createElement("div");
      d.className = "cal-day other-month";
      d.textContent = prevMonthDays - startDay + 1 + i;
      grid.appendChild(d);
    }

    for (let i = 1; i <= daysInMonth; i++) {
      const dateStr = `${view.year}-${String(view.month + 1).padStart(2, "0")}-${String(i).padStart(2, "0")}`;
      const hasHistory = activeDates.includes(dateStr);

      const d = document.createElement("div");
      d.textContent = i;
      d.className = "cal-day";

      const isSel =
        selected &&
        i === selected.day &&
        view.month === selected.month &&
        view.year === selected.year;

      const isInactiveSel =
        selectedInactive &&
        i === selectedInactive.day &&
        view.month === selectedInactive.month &&
        view.year === selectedInactive.year;

      if (hasHistory) {
        if (isSel) {
          d.classList.add("selected");
        } else {
          d.style.background = "#fff";
          d.style.outline = "2px solid #1D9E75";
          d.style.outlineOffset = "-2px";
          d.style.color = "#000";
        }
      } else {
        d.style.color = "white";
        if (isInactiveSel) {
          d.style.background = "black";
        } else {
          d.style.background = "#ccc";
        }
      }

      d.addEventListener("click", () => {
        if (!hasHistory) {
          selectedInactive = { day: i, month: view.month, year: view.year };
          selected = null;

          selectBtn.disabled = true;
          selectBtn.style.opacity = "0.5";
          selectBtn.style.cursor = "default";
        } else {
          selected = { day: i, month: view.month, year: view.year };
          selectedInactive = null;

          selectBtn.disabled = false;
          selectBtn.style.opacity = "1";
          selectBtn.style.cursor = "pointer";
        }

        document.getElementById("cal-selected-label").textContent =
          MONTHS[view.month] + " " + i + ", " + view.year;
        render();
      });

      grid.appendChild(d);
    }
  }

  document.getElementById("cal-prev").addEventListener("click", () => {
    view.month--;
    if (view.month < 0) {
      view.month = 11;
      view.year--;
    }
    render();
  });

  document.getElementById("cal-next").addEventListener("click", () => {
    view.month++;
    if (view.month > 11) {
      view.month = 0;
      view.year++;
    }
    render();
  });

  document.getElementById("cal-select-btn").addEventListener("click", () => {
    if (!selected) return;
    const dateStr =
      selected.year +
      "-" +
      String(selected.month + 1).padStart(2, "0") +
      "-" +
      String(selected.day).padStart(2, "0");
    onSelect(dateStr);
  });

  render();
}
