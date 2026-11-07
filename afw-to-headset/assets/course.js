/* AFW to headset — progress + reveal. Storage key is unique to this course. */
(function () {
  const KEY = "afw-to-headset-progress-v1";
  const pages = [
    "index",
    "01-five-compiles",
    "02-change-a-block",
    "03-vst-and-bidule",
    "04-library-map",
    "05-compile-the-archive",
    "06-copy-and-gate",
    "07-dsp-arm-boot",
    "08-qcc-flash-test",
    "09-failures-and-check",
  ];

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

  const page = document.body.dataset.page;
  if (page) {
    const data = load();
    data[page] = true;
    save(data);
  }

  document.querySelectorAll(".sidebar nav a[href]").forEach((a) => {
    const href = a.getAttribute("href");
    if (href && location.pathname.endsWith(href.replace("./", ""))) {
      a.classList.add("active");
    }
  });

  const bar = document.querySelector(".progress-bar");
  if (bar) {
    const data = load();
    const done = pages.filter((p) => data[p]).length;
    bar.style.setProperty("--pct", `${Math.round((done / pages.length) * 100)}%`);
    const label = document.querySelector(".pct-label");
    if (label) label.textContent = `${done}/${pages.length} pages visited`;
  }

  document.querySelectorAll("[data-reveal]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-reveal");
      const el = document.getElementById(id);
      if (!el) return;
      el.hidden = !el.hidden;
      btn.textContent = el.hidden ? "Show answer" : "Hide answer";
    });
  });
})();
