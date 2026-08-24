(() => {
  "use strict";

  const state = {
    manifest: null,
    profileFeeds: {},
    activeProfile: "master",
    activeSection: "all",
    query: "",
  };

  const $ = (selector) => document.querySelector(selector);
  const $$ = (selector) => Array.from(document.querySelectorAll(selector));
  const number = new Intl.NumberFormat("en-GB");

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function safeUrl(value) {
    try {
      const url = new URL(value, window.location.href);
      return url.protocol === "https:" ? url.href : "#";
    } catch {
      return "#";
    }
  }

  function formatDate(value) {
    if (!value) return "—";
    const date = new Date(`${value}T12:00:00`);
    if (Number.isNaN(date.getTime())) return value;
    return new Intl.DateTimeFormat("en-GB", { day: "2-digit", month: "short", year: "numeric" }).format(date);
  }

  function folderLabel(value) {
    return String(value || "").replace(/^\d+\s+—\s+/, "");
  }

  function sectionClass(value) {
    return value === "Cyber Security" ? "cyber" : "finance";
  }

  function initials(title) {
    const words = String(title || "NN").replace(/[—–·:]/g, " ").trim().split(/\s+/).filter(Boolean);
    if (words.length === 1) return words[0].slice(0, 2).toUpperCase();
    return `${words[0][0]}${words[1][0]}`.toUpperCase();
  }

  function resolveProfiles(manifest) {
    const profiles = manifest.profiles || {};
    const feeds = manifest.feeds || [];
    const cache = new Map();

    function resolve(profileKey, visiting = new Set()) {
      if (cache.has(profileKey)) return cache.get(profileKey);
      if (visiting.has(profileKey)) return [];
      visiting.add(profileKey);

      const config = profiles[profileKey] || {};
      let selected = [];
      if (profileKey === "master" || config.include_all) {
        selected = feeds.slice();
      } else {
        for (const parent of config.inherits || []) {
          selected = selected.concat(resolve(parent, new Set(visiting)));
        }
        selected = selected.concat(feeds.filter((feed) => feed.profiles?.[profileKey] === true));
      }

      const unique = Array.from(new Map(selected.map((feed) => [feed.id, feed])).values());
      cache.set(profileKey, unique);
      return unique;
    }

    return Object.fromEntries(Object.keys(profiles).map((profileKey) => [profileKey, resolve(profileKey)]));
  }

  function profileLabel(profileKey) {
    return state.manifest?.profiles?.[profileKey]?.label || profileKey;
  }

  function profileDescription(profileKey) {
    const descriptions = {
      master: "full research shelf",
      "iphone-air": "recommended daily mix",
      "iphone-lite": "lower-noise mobile read",
    };
    return descriptions[profileKey] || "curated feed set";
  }

  function updateGlobalTotals() {
    const allFeeds = state.profileFeeds.master || [];
    const finance = allFeeds.filter((feed) => feed.section === "Finance").length;
    const cyber = allFeeds.filter((feed) => feed.section === "Cyber Security").length;
    const alerts = allFeeds.filter((feed) => feed.notification === "on").length;
    const validated = allFeeds.map((feed) => feed.validated).filter(Boolean).sort().at(-1);

    $("#hero-total").textContent = number.format(allFeeds.length);
    $("#hero-finance").textContent = number.format(finance);
    $("#hero-cyber").textContent = number.format(cyber);
    $("#hero-alerts").textContent = number.format(alerts);
    $("#hero-validated").textContent = formatDate(validated);
    $("#phone-all-count").textContent = `${number.format(allFeeds.length)} feeds`;
    $("#phone-finance-count").textContent = `${number.format(finance)} feeds`;
    $("#phone-cyber-count").textContent = `${number.format(cyber)} feeds`;

    $$('[data-profile-count]').forEach((node) => {
      node.textContent = number.format((state.profileFeeds[node.dataset.profileCount] || []).length);
    });

    updateSectionCounts();
  }

  function updateSectionCounts() {
    const activeFeeds = state.profileFeeds[state.activeProfile] || [];
    $$('[data-section-count]').forEach((node) => {
      const key = node.dataset.sectionCount;
      const count = key === "all" ? activeFeeds.length : activeFeeds.filter((feed) => feed.section === key).length;
      node.textContent = number.format(count);
    });
  }

  function filteredFeeds() {
    let feeds = state.profileFeeds[state.activeProfile] || [];
    if (state.activeSection !== "all") {
      feeds = feeds.filter((feed) => feed.section === state.activeSection);
    }

    const query = state.query.trim().toLowerCase();
    if (!query) return feeds;

    return feeds.filter((feed) => [feed.title, feed.section, feed.folder, feed.url, feed.html_url, feed.purpose, feed.signal_type]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(query));
  }

  function feedTags(feed) {
    const tags = [];
    if (feed.notification === "on") tags.push('<span class="feed-tag alert">alert</span>');
    if (feed.event_driven) tags.push('<span class="feed-tag">event-driven</span>');
    if (state.activeProfile === "master") {
      if (state.profileFeeds["iphone-air"]?.some((item) => item.id === feed.id)) tags.push('<span class="feed-tag profile">air</span>');
      if (state.profileFeeds["iphone-lite"]?.some((item) => item.id === feed.id)) tags.push('<span class="feed-tag profile">lite</span>');
      if (!state.profileFeeds["iphone-air"]?.some((item) => item.id === feed.id) && !state.profileFeeds["iphone-lite"]?.some((item) => item.id === feed.id)) tags.push('<span class="feed-tag">master only</span>');
    }
    return tags.join("");
  }

  function renderFeedRow(feed) {
    const meta = [folderLabel(feed.folder), feed.signal_type || feed.cadence].filter(Boolean).join(" · ");
    return `
      <article class="feed-row">
        <span class="feed-mark ${sectionClass(feed.section)}" aria-hidden="true">${escapeHtml(initials(feed.title))}</span>
        <div class="feed-copy">
          <div class="feed-title" title="${escapeHtml(feed.title)}">${escapeHtml(feed.title)}</div>
          <div class="feed-meta" title="${escapeHtml(meta)}">${escapeHtml(meta)}</div>
          <div class="feed-tags">${feedTags(feed)}</div>
        </div>
        <div class="feed-side">
          <a class="feed-link" href="${safeUrl(feed.url)}" target="_blank" rel="noreferrer">RSS ↗</a>
          <span class="feed-validated">checked ${escapeHtml(formatDate(feed.validated))}</span>
        </div>
      </article>`;
  }

  function renderFeedLibrary() {
    const feeds = filteredFeeds();
    const grouped = new Map();

    for (const feed of feeds) {
      if (!grouped.has(feed.section)) grouped.set(feed.section, new Map());
      const folders = grouped.get(feed.section);
      if (!folders.has(feed.folder)) folders.set(feed.folder, []);
      folders.get(feed.folder).push(feed);
    }

    const sections = Array.from(grouped.entries());
    const folderCount = sections.reduce((total, [, folders]) => total + folders.size, 0);
    const queryLabel = state.query.trim() ? ` matching “${escapeHtml(state.query.trim())}”` : "";
    $("#results-label").textContent = `Showing ${number.format(feeds.length)} feeds in the ${profileLabel(state.activeProfile)} inventory${state.activeSection === "all" ? "" : ` · ${state.activeSection}`}${state.query.trim() ? ` · search${queryLabel}` : ""}`;
    $("#active-profile-kicker").textContent = `${profileLabel(state.activeProfile).toUpperCase()} · ${profileDescription(state.activeProfile).toUpperCase()}`;
    $("#active-profile-title").textContent = `${number.format(feeds.length)} feeds arranged in folders`;
    $("#toolbar-result").textContent = `${folderCount} folders · ${sections.length} sections`;

    if (!feeds.length) {
      $("#feed-list").innerHTML = `<div class="empty-state">No feeds match this view.<br />Try another profile, section or search term.</div>`;
      return;
    }

    $("#feed-list").innerHTML = sections.map(([section, folders]) => `
      <section class="feed-section" aria-labelledby="section-${escapeHtml(sectionClass(section))}">
        <div class="feed-section-heading">
          <h3 id="section-${escapeHtml(sectionClass(section))}">${escapeHtml(section)}</h3>
          <span>${number.format(Array.from(folders.values()).flat().length)} feeds in ${folders.size} folders</span>
        </div>
        ${Array.from(folders.entries()).map(([folder, folderFeeds]) => `
          <div class="feed-folder">
            <div class="feed-folder-heading"><strong>${escapeHtml(folderLabel(folder))}</strong><span>${number.format(folderFeeds.length)} sources</span></div>
            ${folderFeeds.map(renderFeedRow).join("")}
          </div>`).join("")}
      </section>`).join("");
  }

  function renderProfileCards() {
    const container = $("#profile-cards");
    const profileOrder = ["iphone-air", "iphone-lite", "master"];
    const cards = {
      "iphone-air": {
        index: "01",
        className: "profile-card-air",
        badge: "Recommended",
        kicker: "iPhone Air",
        headline: "Broad enough for the morning. Quiet enough for the day.",
      },
      "iphone-lite": {
        index: "02",
        className: "profile-card-lite",
        badge: "Lightweight",
        kicker: "iPhone Lite",
        headline: "A smaller refresh for focused reading on the move.",
      },
      master: {
        index: "03",
        className: "profile-card-master",
        badge: "Full shelf",
        kicker: "Master",
        headline: "The complete research shelf for rebuilding every profile.",
      },
    };

    container.innerHTML = profileOrder.map((profileKey) => {
      const card = cards[profileKey];
      const profile = state.manifest.profiles[profileKey];
      const file = profile?.opml_file || "#";
      return `
        <article class="profile-card ${card.className}">
          <div class="profile-card-top"><span class="profile-card-index">${card.index}</span><span class="profile-badge ${profileKey === "iphone-air" ? "" : "badge-muted"}">${card.badge}</span></div>
          <p class="profile-card-kicker">${card.kicker}</p>
          <h3>${card.headline}</h3>
          <div class="profile-card-count"><strong>${number.format((state.profileFeeds[profileKey] || []).length)}</strong><span>feeds</span></div>
          <a class="profile-card-link" href="${escapeHtml(file)}">Download OPML <span aria-hidden="true">↗</span></a>
        </article>`;
    }).join("");
  }

  function updateActiveButtons() {
    $$('[data-profile]').forEach((button) => {
      const active = button.dataset.profile === state.activeProfile;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", String(active));
    });
    $$('[data-section]').forEach((button) => {
      const active = button.dataset.section === state.activeSection;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-selected", String(active));
    });
  }

  function setProfile(profileKey) {
    if (!state.profileFeeds[profileKey]) return;
    state.activeProfile = profileKey;
    updateSectionCounts();
    updateActiveButtons();
    renderFeedLibrary();
    document.querySelector("#library")?.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function setSection(section) {
    state.activeSection = section;
    updateActiveButtons();
    renderFeedLibrary();
  }

  function setupInteractions() {
    $$('[data-profile]').forEach((button) => button.addEventListener("click", () => setProfile(button.dataset.profile)));
    $$('[data-section]').forEach((button) => button.addEventListener("click", () => setSection(button.dataset.section)));
    $("#feed-search").addEventListener("input", (event) => {
      state.query = event.target.value;
      renderFeedLibrary();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "/" && document.activeElement !== $("#feed-search")) {
        event.preventDefault();
        $("#feed-search").focus();
      }
    });
  }

  async function loadManifest() {
    try {
      const response = await fetch("./feed-manifest.json", { cache: "no-store" });
      if (!response.ok) throw new Error(`Manifest request failed with ${response.status}`);
      state.manifest = await response.json();
      state.profileFeeds = resolveProfiles(state.manifest);
      updateGlobalTotals();
      renderProfileCards();
      renderFeedLibrary();
      $("#manifest-status").innerHTML = '<span class="status-dot" aria-hidden="true"></span><span>manifest linked</span>';
    } catch (error) {
      console.error(error);
      $("#manifest-status").innerHTML = '<span class="status-dot" aria-hidden="true" style="background:#eb8158;box-shadow:none"></span><span>manifest unavailable</span>';
      $("#feed-list").innerHTML = '<div class="error-state">The feed manifest could not be loaded.<br />Serve this folder from a local web server or open the GitHub Pages URL.</div>';
    }
  }

  setupInteractions();
  loadManifest();
})();
