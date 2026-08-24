/* AudioFramework VST Course — light interactivity */
(function () {
  const KEY = "afw-vst-course-progress";

  function load() {
    try {
      return JSON.parse(localStorage.getItem(KEY) || "{}");
    } catch {
      return {};
    }
  }

  function save(data) {
    localStorage.setItem(KEY, JSON.stringify(data));
  }

  // Mark current page as visited
  const page = document.body.dataset.page;
  if (page) {
    const data = load();
    data[page] = true;
    save(data);
  }

  // Highlight active nav link
  document.querySelectorAll(".sidebar nav a[href]").forEach((a) => {
    const href = a.getAttribute("href");
    if (href && location.pathname.endsWith(href.replace("./", ""))) {
      a.classList.add("active");
    }
  });

  // Progress bar if present
  const bar = document.querySelector(".progress-bar");
  if (bar) {
    const pages = [
      "index",
      "01-repository",
      "02-fundamentals",
      "03-first-vst",
      "04-test-debug-quiz",
      "05-part2-projects",
    ];
    const data = load();
    const done = pages.filter((p) => data[p]).length;
    bar.style.setProperty("--pct", `${Math.round((done / pages.length) * 100)}%`);
    const label = bar.querySelector(".pct-label");
    if (label) label.textContent = `${done}/${pages.length} pages visited`;
  }

  // Reveal answer buttons
  document.querySelectorAll("[data-reveal]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-reveal");
      const el = document.getElementById(id);
      if (el) el.hidden = !el.hidden;
      btn.textContent = el && !el.hidden ? "Hide answer" : "Show answer";
    });
  });
})();
