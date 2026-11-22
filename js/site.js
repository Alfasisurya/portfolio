const stored = localStorage.getItem("theme");
document.documentElement.dataset.theme = stored || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
document.querySelectorAll(".nav-toggle").forEach((button) => {
  button.addEventListener("click", () => {
    const nav = button.parentElement.querySelector(".nav");
    const open = nav.classList.toggle("is-open");
    button.setAttribute("aria-expanded", open ? "true" : "false");
  });
});
document.querySelectorAll(".theme-btn").forEach((button) => {
  const label = () => { button.textContent = document.documentElement.dataset.theme === "dark" ? "Light" : "Dark"; };
  label();
  button.addEventListener("click", () => {
    const next = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("theme", next);
    label();
  });
});
document.querySelectorAll("[data-archive]").forEach((root) => {
  const search = root.querySelector("[data-filter-search]");
  const year = root.querySelector("[data-filter-year]");
  const topic = root.querySelector("[data-filter-topic]");
  const count = document.querySelector("[data-filter-count]");
  const empty = document.querySelector("[data-filter-empty]");
  const items = [...document.querySelectorAll("[data-item]")];
  const apply = () => {
    const query = (search.value || "").trim().toLowerCase();
    let visible = 0;
    for (const item of items) {
      const topics = (item.dataset.topics || "").split("|");
      const match = (!query || (item.dataset.text || "").includes(query)) && (year.value === "all" || item.dataset.year === year.value) && (topic.value === "all" || topics.includes(topic.value));
      item.hidden = !match;
      if (match) visible += 1;
    }
    if (count) count.textContent = String(visible);
    if (empty) empty.hidden = visible !== 0;
  };
  search.addEventListener("input", apply);
  year.addEventListener("change", apply);
  topic.addEventListener("change", apply);
});
