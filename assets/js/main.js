/* ============================================================
   TechSpecsHub — main.js
   Shared UI interactions: search modal, nav, tables, utils
   ============================================================ */

(function () {
  'use strict';

  /* ── Lucide Icons ──────────────────────────────────────── */
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }

  /* ── Mermaid ───────────────────────────────────────────── */
  if (typeof mermaid !== 'undefined') {
    mermaid.initialize({
      startOnLoad: true,
      theme: 'base',
      themeVariables: {
        background:        '#0a1628',
        primaryColor:      '#0f1d32',
        primaryTextColor:  '#e5e7eb',
        primaryBorderColor:'#00d4ff',
        lineColor:         '#00b8e6',
        secondaryColor:    '#162544',
        tertiaryColor:     '#0a1628',
        edgeLabelBackground:'#0f1d32',
        fontFamily:        'Space Grotesk, system-ui, sans-serif',
        fontSize:          '14px',
      },
    });
  }

  /* ── Mobile Menu ───────────────────────────────────────── */
  const mobileBtn  = document.getElementById('mobile-menu-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  if (mobileBtn && mobileMenu) {
    mobileBtn.addEventListener('click', () => {
      const open = mobileMenu.classList.toggle('hidden');
      const icon = mobileBtn.querySelector('[data-lucide]');
      if (icon) {
        icon.setAttribute('data-lucide', open ? 'menu' : 'x');
        if (typeof lucide !== 'undefined') lucide.createIcons();
      }
    });
  }

  /* ── Search Modal ──────────────────────────────────────── */
  const searchModal    = document.getElementById('search-modal');
  const searchBackdrop = document.getElementById('search-backdrop');
  const searchCloseBtn = document.getElementById('search-close-btn');
  const searchOpenBtn  = document.getElementById('search-btn');
  const searchInput    = document.getElementById('search-input-field');

  function openSearch() {
    if (!searchModal) return;
    searchModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    setTimeout(() => searchInput && searchInput.focus(), 60);
  }
  function closeSearch() {
    if (!searchModal) return;
    searchModal.classList.add('hidden');
    document.body.style.overflow = '';
    if (searchInput) searchInput.value = '';
    renderSearchResults('');
  }

  if (searchOpenBtn)  searchOpenBtn.addEventListener('click', openSearch);
  if (searchCloseBtn) searchCloseBtn.addEventListener('click', closeSearch);
  if (searchBackdrop) searchBackdrop.addEventListener('click', closeSearch);

  // Cmd+K / Ctrl+K shortcut
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
    if (e.key === 'Escape') closeSearch();
  });

  /* ── Search Index ────────────────────────────────────────
   * Data structure: { title, description, type, url }
   * All URLs are relative to tech-specs-hub root directory
   */
  var SEARCH_INDEX = [
    // Outdoor Power - EcoFlow
    { title: 'EcoFlow Delta Pro 3 — Full Specs', description: '4096 Wh LFP 4000 cycles Split-Phase New', type: 'spec', url: 'pages/specs/ecoflow-delta-pro-3.html' },
    { title: 'EcoFlow Delta Pro — Full Specs', description: '3600 Wh LFP 6500+ cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow' },
    { title: 'EcoFlow Delta 2 — Specs & Cycle Life', description: '1024 Wh LFP 3000 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow' },
    { title: 'EcoFlow Delta 2 Max — Specs', description: '2048 Wh LFP 3000 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow' },
    { title: 'EcoFlow River 2 Pro — Specs', description: '768 Wh LFP 3000 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow' },
    { title: 'EcoFlow River 2 Max — Specs', description: '512 Wh LFP 3000 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow' },
    { title: 'EcoFlow River 2 — Specs', description: '256 Wh LFP 3000 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow' },
    // Outdoor Power - Jackery
    { title: 'Jackery Explorer 2000 Plus — Specs', description: '2042 Wh LFP 4000 cycles Top Rated outdoor power station', type: 'spec', url: 'pages/specs/outdoor-power.html#jackery' },
    { title: 'Jackery Explorer 3000 Pro — Specs', description: '3024 Wh LFP 2000 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#jackery' },
    { title: 'Jackery Explorer 1000 v2 — Specs', description: '1070 Wh LFP 1000 cycles outdoor power', type: 'spec', url: 'pages/specs/outdoor-power.html#jackery' },
    // Outdoor Power - Bluetti
    { title: 'Bluetti EP500 Pro — Home Backup', description: '5100 Wh LFP 6000 cycles UPS home backup power station', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti' },
    { title: 'Bluetti AC300 — Modular System', description: 'Expandable modular power up to 12.3 kWh with B300 battery', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti' },
    { title: 'Bluetti B300 — Expansion Battery', description: '3072 Wh 51.2V Built-in MPPT expansion battery pack', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti' },
    { title: 'Bluetti AC200L — Portable Power', description: '2048 Wh LFP 3500 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti' },
    { title: 'Bluetti AC180 — Portable Power', description: '1152 Wh LFP 3500 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti' },
    // Outdoor Power - Anker
    { title: 'Anker SOLIX F3800 — Specs', description: '3840 Wh LFP 3000 cycles Best Value home backup', type: 'spec', url: 'pages/specs/outdoor-power.html#anker' },
    { title: 'Anker SOLIX F2000 — Specs', description: '2048 Wh LFP 3000 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#anker' },
    { title: 'Anker SOLIX C1000 — Specs', description: '1056 Wh LFP 3000 cycles portable power station', type: 'spec', url: 'pages/specs/outdoor-power.html#anker' },
    // Outdoor Power - Victron Energy
    { title: 'Victron Energy MultiPlus-II — Specs', description: 'Inverter charger 48V 3000-5000 VA off-grid RV power system', type: 'spec', url: 'pages/specs/outdoor-power.html#victron' },
    { title: 'Victron SmartSolar MPPT — Specs', description: 'Solar charge controller 98% efficiency 100-250V PV input', type: 'spec', url: 'pages/specs/outdoor-power.html#victron' },
    { title: 'Outdoor Power Station Specs Index', description: 'EcoFlow Jackery Bluetti Anker Victron portable power stations comparison', type: 'spec', url: 'pages/specs/outdoor-power.html' },
    { title: 'Portable Power Station Maintenance Guide', description: 'Battery care, storage tips, troubleshooting, and maintenance schedules for LFP and NMC batteries', type: 'spec', url: 'pages/specs/outdoor-power.html#maintenance' },
    { title: 'LFP vs NMC Battery Chemistry', description: 'Compare lithium iron phosphate vs nickel manganese cobalt battery pros, cons, and best use cases', type: 'spec', url: 'pages/specs/outdoor-power.html' },
    { title: 'EcoFlow vs Jackery vs Bluetti 2026', description: 'Side-by-side comparison of outdoor power station brands', type: 'spec', url: 'pages/master-specs.html' },
    // Hybrid Cars - Toyota
    { title: 'Toyota Prius 2022 Battery Specs', description: '201.6 V NiMH Li hybrid battery 15 mOhm', type: 'spec', url: 'pages/specs/toyota-prius-2022-battery.html' },
    { title: 'Toyota Prius Gen 5 — Battery Specs', description: '2023+ Li-ion 13.6 kWh hybrid battery', type: 'spec', url: 'pages/specs/hybrid-cars.html#toyota' },
    { title: 'Toyota RAV4 Prime — Battery Specs', description: '355.2 V 18.1 kWh CATL LFP plug-in hybrid', type: 'spec', url: 'pages/specs/hybrid-cars.html#toyota' },
    { title: 'Toyota Corolla Hybrid — Battery', description: '2019-2025 NiMH Li-ion hybrid battery', type: 'spec', url: 'pages/specs/hybrid-cars.html#toyota' },
    // Hybrid Cars - Tesla
    { title: 'Tesla Model 3 LFP — Battery Pack', description: '108S1P 60 kWh CATL lithium iron phosphate EV battery', type: 'spec', url: 'pages/specs/hybrid-cars.html#tesla' },
    { title: 'Tesla Model Y LFP — Battery Pack', description: '112S1P 62.5 kWh CATL lithium iron phosphate EV battery', type: 'spec', url: 'pages/specs/hybrid-cars.html#tesla' },
    { title: 'Tesla SOH Calculator', description: 'Calculate battery State of Health for Tesla LFP vehicles', type: 'tool', url: 'pages/specs/hybrid-cars.html#tesla' },
    { title: 'Hybrid & EV Battery Specs Index', description: 'Toyota Tesla Honda Ford hybrid electric vehicle battery specifications', type: 'spec', url: 'pages/specs/hybrid-cars.html' },
    // Drones - DJI
    { title: 'DJI Mavic 3 Pro — Battery Specs', description: '5000 mAh 77 Wh LiPo drone battery A-level expert data', type: 'spec', url: 'pages/specs/drones.html#dji' },
    { title: 'DJI Air 2S — Battery Specs', description: '3500 mAh 40.42 Wh LiPo drone battery', type: 'spec', url: 'pages/specs/drones.html#dji' },
    { title: 'DJI Mini 3 — Battery Specs', description: 'Standard vs Plus weight warning drone battery', type: 'spec', url: 'pages/specs/drones.html#dji' },
    { title: 'DJI Mini 4 Pro — Battery Specs', description: '2597 mAh 35.71 Wh LiPo drone battery', type: 'spec', url: 'pages/specs/drones.html#dji' },
    { title: 'DJI Mini 5 Pro — Specs', description: '2024 flagship 1-inch CMOS 50MP 249.9g drone', type: 'spec', url: 'pages/specs/drones.html#dji' },
    // Drones - Autel
    { title: 'Autel EVO II Pro V3 — Specs', description: '7100 mAh 79 Wh drone battery no geofencing alternative', type: 'spec', url: 'pages/specs/drones.html#autel' },
    { title: 'Autel EVO Nano+ — Specs', description: '249g sub-250g drone 28 min flight time', type: 'spec', url: 'pages/specs/drones.html#autel' },
    { title: 'Autel EVO Lite+ — Specs', description: '4300 mAh 34 Wh drone 40 min flight', type: 'spec', url: 'pages/specs/drones.html#autel' },
    // Drones - Skydio
    { title: 'Skydio X10 — Specs', description: 'American-made autonomous drone 360° AI obstacle avoidance', type: 'spec', url: 'pages/specs/drones.html#skydio' },
    { title: 'Skydio X2 — Specs', description: 'Autonomous drone 35 min flight 6 km range', type: 'spec', url: 'pages/specs/drones.html#skydio' },
    { title: 'Skydio S4+ — Specs', description: 'Autonomous drone 27 min flight IP55 rating', type: 'spec', url: 'pages/specs/drones.html#skydio' },
    { title: 'Drones & UAV Specs Index', description: 'DJI Autel Skydio drone battery specifications comparison', type: 'spec', url: 'pages/specs/drones.html' },
    // Smart Home - Dyson
    { title: 'Dyson V15 Detect — Specs', description: 'Laser dust detection cordless vacuum 230 AW', type: 'spec', url: 'pages/specs/smart-home.html#dyson' },
    { title: 'Dyson Gen5detect — Specs', description: 'Latest cordless vacuum 262 AW 70 min runtime', type: 'spec', url: 'pages/specs/smart-home.html#dyson' },
    { title: 'Dyson V12 — Specs', description: 'Slim cordless vacuum 150 AW laser dust detection', type: 'spec', url: 'pages/specs/smart-home.html#dyson' },
    // Navigation & Marine
    { title: 'Garmin Fenix 8 — Specs', description: 'Smartwatch with multiband GPS, 1.4" AMOLED display', type: 'spec', url: 'pages/specs/navigation.html#garmin' },
    { title: 'Garmin Epix (Gen 3) — Specs', description: 'Premium smartwatch with AMOLED display and GPS', type: 'spec', url: 'pages/specs/navigation.html#garmin' },
    { title: 'Garmin Forerunner 965 — Specs', description: 'Running watch with multiband GPS and AMOLED', type: 'spec', url: 'pages/specs/navigation.html#garmin' },
    { title: 'Garmin Instinct 2X — Specs', description: 'Rugged GPS watch with 850 mAh battery', type: 'spec', url: 'pages/specs/navigation.html#garmin' },
    { title: 'Navigation & Marine Specs Index', description: 'Garmin watches, marine electronics, aviation avionics', type: 'spec', url: 'pages/specs/navigation.html' },
    // Smart Home - iRobot
    { title: 'iRobot Roomba Combo j7+ — Specs', description: 'Robot vacuum & mop with Clean Base auto-empty iRobot Roomba', type: 'spec', url: 'pages/specs/smart-home.html#irobot' },
    { title: 'iRobot Roomba j7+ — Specs', description: 'Robot vacuum with AI obstacle detection Clean Base', type: 'spec', url: 'pages/specs/smart-home.html#irobot' },
    { title: 'iRobot Roomba s9+ — Specs', description: 'D-shaped robot vacuum 40x suction', type: 'spec', url: 'pages/specs/smart-home.html#irobot' },
    // Smart Home
    { title: 'Husqvarna Automower 450X — Specs', description: 'Robot mower 18V Li-ion 3200 m2 lawn care', type: 'spec', url: 'pages/specs/smart-home.html#husqvarna' },
    { title: 'Smart Home Device Teardowns', description: 'Roborock S8 MaxV Ultra Yale Ecobee Husqvarna iRobot smart home device specifications', type: 'spec', url: 'pages/specs/smart-home.html' },
    { title: 'Roborock S8 MaxV Ultra — Specs', description: '2024 CES flagship 10000Pa AI obstacle avoidance robot vacuum', type: 'spec', url: 'pages/specs/smart-home.html#roborock' },
    // E-Bike & Micromobility
    { title: 'Bosch Performance Line CX Gen 4 — Specs', description: '2024 new 125Nm 750W eMTB motor Smart System 2.0', type: 'spec', url: 'pages/specs/ebike-micromobility.html#bosch' },
    { title: 'Bosch Performance Line CX — Specs', description: '120 Nm 750W eMTB motor Smart System e-bike', type: 'spec', url: 'pages/specs/ebike-micromobility.html#bosch' },
    { title: 'Bafang M400 M620 — Specs', description: '80-160 Nm mid-drive motor DIY ebike error codes', type: 'spec', url: 'pages/specs/ebike-micromobility.html#bafang' },
    { title: 'Segway-Ninebot Max G2 — Specs', description: 'Electric scooter 70km range 551Wh battery', type: 'spec', url: 'pages/specs/ebike-micromobility.html#segway' },
    { title: 'Shimano STEPS EP801 — Specs', description: 'Shimano EP8 EP6 e-bike motor 85 Nm STEPS system', type: 'spec', url: 'pages/specs/ebike-micromobility.html#shimano' },
    { title: 'Yamaha PW-X3 — Specs', description: 'Yamaha PWseries e-bike motor 85 Nm eMTB', type: 'spec', url: 'pages/specs/ebike-micromobility.html#yamaha' },
    // 3D Printers
    { title: 'Bambu Lab X1 Carbon — Specs', description: '3D printer 500mm/s nozzle hotend AMS error codes', type: 'spec', url: 'pages/specs/3d-printers.html#bambulab' },
    { title: 'Prusa MK4 — Specs', description: 'Open source 3D printer MK4 XL specifications', type: 'spec', url: 'pages/specs/3d-printers.html#prusa' },
    { title: 'Creality K1 — Specs', description: 'Budget 3D printer Ender K1 CoreXY specifications', type: 'spec', url: 'pages/specs/3d-printers.html#creality' },
    { title: 'Anycubic Kobra 3 — Specs', description: 'Anycubic Kobra Photon resin 3D printer', type: 'spec', url: 'pages/specs/3d-printers.html#anycubic' },
    { title: 'Anycubic Photon Mono M5s — Specs', description: '14K resin printer Anycubic Photon', type: 'spec', url: 'pages/specs/3d-printers.html#anycubic' },
    { title: 'Elegoo Neptune 4 Pro — Specs', description: 'Elegoo Neptune 4 Klipper 3D printer', type: 'spec', url: 'pages/specs/3d-printers.html#elegoo' },
    { title: 'Elegoo Saturn 4 Ultra — Specs', description: '12K resin printer Elegoo Saturn', type: 'spec', url: 'pages/specs/3d-printers.html#elegoo' },
    { title: '3D Printer Specs Index', description: 'Bambu Lab Prusa Creality Anycubic Elegoo 3D printer comparison', type: 'spec', url: 'pages/specs/3d-printers.html' },
    // Error Codes
    { title: 'EcoFlow Error Codes — Troubleshooting', description: 'E01 E03 BMS_ERR CHG@80% power station fault codes', type: 'error', url: 'pages/specs/outdoor-power.html#ecoflow' },
    { title: 'Bluetti DTC Codes — Troubleshooting', description: '004 008 026 049 Bluetti power station error codes', type: 'error', url: 'pages/specs/outdoor-power.html#bluetti' },
    { title: 'DJI Drone Error Codes', description: 'ESC_ERR BATT_CELL_ERR IMU drone fault codes', type: 'error', url: 'pages/specs/drones.html#dji' },
    { title: 'Error Code Database', description: 'Troubleshooting guides and error code references', type: 'error', url: 'pages/error-code-db.html' },
    // Tools
    { title: 'Best Multimeters 2026', description: 'Fluke Klein AstroAI ranked digital multimeter review', type: 'tool', url: 'pages/tools/best-multimeters-2026.html' },
    { title: 'Power Station Runtime Calculator', description: 'Calculate how long your power station will run appliances. Enter Wh capacity and device wattage', type: 'tool', url: 'pages/tools/runtime-calculator.html' },
    { title: 'Solar Panel Compatibility Guide', description: 'Third-party solar panels compatible with EcoFlow Jackery Bluetti. MC4 XT60 adapter reference', type: 'tool', url: 'pages/specs/outdoor-power.html#solar-compatibility' },
    { title: 'Community User Experiences', description: 'Real user stories, tips, and hacks from Reddit, Amazon reviews, and forums. Camping and backup power testimonials', type: 'spec', url: 'pages/specs/outdoor-power.html#user-experiences' },
    { title: 'Unit Converter Tools', description: 'Wh to mAh, km to miles, C to F temperature conversion calculators', type: 'tool', url: 'pages/tools/unit-converter.html' },
    { title: 'Brand Index A-Z', description: 'All supported brands alphabetical index', type: 'spec', url: 'pages/brand-index.html' },
    { title: 'Master Specs Comparison', description: 'Cross-category spec tables comparison', type: 'spec', url: 'pages/master-specs.html' },
  ];

  /* ── Search Logic (Strict Priority Order) ───────────────
   * Priority 1: Title exactly contains keyword (full word match)
   * Priority 2: Title partially contains keyword
   * Priority 3: Description contains keyword
   */
  function searchIndex(query) {
    var q = query.toLowerCase().trim();
    if (!q) return [];

    var results = SEARCH_INDEX.filter(function(item) {
      var title = item.title.toLowerCase();
      var desc = item.description.toLowerCase();
      return title.indexOf(q) !== -1 || desc.indexOf(q) !== -1;
    });

    // Sort by priority: title exact > title partial > description only
    results.sort(function(a, b) {
      var titleA = a.title.toLowerCase();
      var titleB = b.title.toLowerCase();
      var descA = a.description.toLowerCase();
      var descB = b.description.toLowerCase();

      var aExact = titleA.indexOf(q) !== -1;
      var bExact = titleB.indexOf(q) !== -1;
      var aDescOnly = !aExact && descA.indexOf(q) !== -1;
      var bDescOnly = !bExact && descB.indexOf(q) !== -1;

      // Priority 1: Both exact match - sort alphabetically
      if (aExact && bExact) {
        return titleA.localeCompare(titleB);
      }
      // Priority 2: A exact, B not exact
      if (aExact) return -1;
      // Priority 2: B exact, A not exact
      if (bExact) return 1;

      // Priority 3: A in title partial, B only in description
      if (titleA.indexOf(q) !== -1 && bDescOnly) return -1;
      // Priority 3: B in title partial, A only in description
      if (titleB.indexOf(q) !== -1 && aDescOnly) return 1;

      // Both in description - sort alphabetically
      return titleA.localeCompare(titleB);
    });

    return results;
  }

  function renderSearchResults(query) {
    var container = document.getElementById('search-results-list');
    if (!container) return;

    var q = query.trim();
    if (!q) {
      container.innerHTML = getQuickLinks();
      return;
    }

    var results = searchIndex(q);

    if (results.length === 0) {
      container.innerHTML = '<div class="p-6 text-center text-gray-500">No results found for "' + escHtml(q) + '"</div>';
      return;
    }

    var depth = getPageDepth();
    var prefix = depth > 0 ? '../'.repeat(depth) : '';

    var html = '<div class="p-2 text-xs text-gray-500 border-b border-white/10">' + results.length + ' result' + (results.length !== 1 ? 's' : '') + '</div>';

    results.forEach(function(r) {
      var iconMap = {
        'spec': 'file-text',
        'error': 'alert-circle',
        'tool': 'wrench'
      };
      var icon = iconMap[r.type] || 'file';

      html += '<a href="' + prefix + r.url + '" class="search-result-item">' +
        '<i data-lucide="' + icon + '" style="width:1rem;height:1rem;flex-shrink:0;color:#00b8e6"></i>' +
        '<div class="flex-1 min-w-0">' +
        '<div class="truncate text-sm">' + highlightMatch(r.title, q) + '</div>' +
        '<div class="text-xs text-gray-500 truncate mt-0.5">' + highlightMatch(r.description, q) + '</div>' +
        '</div>' +
        '<span class="search-result-tag tag-' + r.type + '">' + r.type + '</span>' +
        '</a>';
    });

    container.innerHTML = html;
    if (typeof lucide !== 'undefined') lucide.createIcons();
  }

  function getQuickLinks() {
    var depth = getPageDepth();
    var prefix = depth > 0 ? '../'.repeat(depth) : '';
    return '<p class="nav-dropdown-section-label py-2">Quick Access</p>' +
      '<a href="' + prefix + 'pages/error-code-db.html" class="search-result-item">' +
      '<i data-lucide="alert-circle" style="width:1rem;height:1rem;flex-shrink:0;color:#f87171"></i>' +
      '<span>Error Code Database</span>' +
      '<span class="search-result-tag tag-error">error</span></a>' +
      '<a href="' + prefix + 'pages/specs/outdoor-power.html" class="search-result-item">' +
      '<i data-lucide="battery-charging" style="width:1rem;height:1rem;flex-shrink:0;color:#00b8e6"></i>' +
      '<span>Outdoor Power Station Specs</span>' +
      '<span class="search-result-tag tag-spec">spec</span></a>' +
      '<a href="' + prefix + 'pages/specs/hybrid-cars.html" class="search-result-item">' +
      '<i data-lucide="car" style="width:1rem;height:1rem;flex-shrink:0;color:#00b8e6"></i>' +
      '<span>Hybrid & EV Battery Specs</span>' +
      '<span class="search-result-tag tag-spec">spec</span></a>' +
      '<a href="' + prefix + 'pages/master-specs.html" class="search-result-item">' +
      '<i data-lucide="table" style="width:1rem;height:1rem;flex-shrink:0;color:#00b8e6"></i>' +
      '<span>Master Specs Comparison</span>' +
      '<span class="search-result-tag tag-spec">spec</span></a>' +
      '<a href="' + prefix + 'pages/tools/best-multimeters-2026.html" class="search-result-item">' +
      '<i data-lucide="wrench" style="width:1rem;height:1rem;flex-shrink:0;color:#fbbf24"></i>' +
      '<span>Best Multimeters 2026</span>' +
      '<span class="search-result-tag tag-tool">tool</span></a>';
  }

  if (searchInput) {
    searchInput.addEventListener('input', function() {
      renderSearchResults(searchInput.value);
    });
    searchInput.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' && searchInput.value.trim()) {
        var depth = getPageDepth();
        var prefix = depth > 0 ? '../'.repeat(depth) : '';
        window.location.href = prefix + 'pages/error-code-db.html?q=' + encodeURIComponent(searchInput.value.trim());
      }
    });
  }

  /* ── Table Filter ──────────────────────────────────────── */
  var filterInputs = document.querySelectorAll('[data-filter-input]');
  for (var i = 0; i < filterInputs.length; i++) {
    var input = filterInputs[i];
    var targetId = input.getAttribute('data-filter-input');
    var table = document.getElementById(targetId);
    if (!table) continue;
    var rows = table.querySelectorAll('tbody tr');
    input.addEventListener('input', (function(allRows) {
      return function() {
        var q = this.value.toLowerCase();
        for (var j = 0; j < allRows.length; j++) {
          allRows[j].style.display = allRows[j].textContent.toLowerCase().indexOf(q) !== -1 ? '' : 'none';
        }
      };
    })(rows));
  }

  /* ── Tab Switcher ──────────────────────────────────────── */
  var tabWrappers = document.querySelectorAll('[data-tabs]');
  for (var ti = 0; ti < tabWrappers.length; ti++) {
    var wrapper = tabWrappers[ti];
    var tabs = wrapper.querySelectorAll('[data-tab]');
    var panels = wrapper.querySelectorAll('[data-panel]');
    for (var tj = 0; tj < tabs.length; tj++) {
      var tab = tabs[tj];
      tab.addEventListener('click', (function(t, ps, w) {
        return function() {
          var target = t.getAttribute('data-tab');
          for (var k = 0; k < w.length; k++) {
            var active = w[k].getAttribute('data-tab') === target;
            if (active) {
              w[k].classList.add('bg-electric-500', 'text-navy-900', 'font-semibold');
              w[k].classList.remove('bg-white/5', 'text-gray-300');
            } else {
              w[k].classList.remove('bg-electric-500', 'text-navy-900', 'font-semibold');
              w[k].classList.add('bg-white/5', 'text-gray-300');
            }
          }
          for (var m = 0; m < ps.length; m++) {
            if (ps[m].getAttribute('data-panel') === target) {
              ps[m].classList.remove('hidden');
            } else {
              ps[m].classList.add('hidden');
            }
          }
        };
      })(tab, panels, tabs));
    }
  }

  /* ── Copy-to-Clipboard for error codes ────────────────── */
  var copyBtns = document.querySelectorAll('[data-copy]');
  for (var ci = 0; ci < copyBtns.length; ci++) {
    copyBtns[ci].addEventListener('click', function() {
      var text = this.getAttribute('data-copy');
      navigator.clipboard.writeText(text).then((function(btn) {
        return function() {
          var orig = btn.textContent;
          btn.textContent = 'Copied!';
          setTimeout(function() { btn.textContent = orig; }, 1500);
        };
      })(this));
    });
  }

  /* ── Smooth Scroll for anchor links ───────────────────── */
  var anchorLinks = document.querySelectorAll('a[href^="#"]');
  for (var ai = 0; ai < anchorLinks.length; ai++) {
    anchorLinks[ai].addEventListener('click', function(e) {
      var id = this.getAttribute('href').slice(1);
      var el = document.getElementById(id);
      if (el) { e.preventDefault(); el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
    });
  }

  /* ── Active Nav Link ───────────────────────────────────── */
  var currentPath = window.location.pathname.split('/').pop() || 'index.html';
  var navLinks = document.querySelectorAll('nav a[href]');
  for (var ni = 0; ni < navLinks.length; ni++) {
    if (navLinks[ni].getAttribute('href').endsWith(currentPath)) {
      navLinks[ni].classList.add('text-white', 'bg-white/8');
    }
  }

  /* ── Utilities ─────────────────────────────────────────── */
  function escHtml(s) {
    return s.replace(/[&<>"']/g, function(c) {
      return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];
    });
  }

  function highlightMatch(text, query) {
    if (!query) return escHtml(text);
    var escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    var re = new RegExp('(' + escapedQuery + ')', 'gi');
    return escHtml(text).replace(re, '<mark class="bg-yellow-500/30 text-white rounded px-0.5">$1</mark>');
  }

  function getPageDepth() {
    var path = window.location.pathname;
    var parts = path.split('/').filter(Boolean);
    var idx = parts.indexOf('pages');
    if (idx >= 0) {
      return idx;
    }
    var idx2 = parts.indexOf('specs');
    if (idx2 >= 0) {
      return idx2;
    }
    return 0;
  }

})();
