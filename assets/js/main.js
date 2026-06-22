/* ============================================================
   TechSpecsHub | Enhanced main.js
   Features: Search, Comparison, FAQ Accordion, TOC, Performance
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
        background: '#0a1628',
        primaryColor: '#0f1d32',
        primaryTextColor: '#e5e7eb',
        primaryBorderColor: '#00d4ff',
        lineColor: '#00b8e6',
        secondaryColor: '#162544',
        tertiaryColor: '#0a1628',
        edgeLabelBackground: '#0f1d32',
        fontFamily: 'Space Grotesk, system-ui, sans-serif',
        fontSize: '14px',
      },
    });
  }

  /* ═══════════════════════════════════════════════════════
     1. ENHANCED SEARCH WITH KEYBOARD NAVIGATION
     ═══════════════════════════════════════════════════════ */
  const searchModal = document.getElementById('search-modal');
  const searchBackdrop = document.getElementById('search-backdrop');
  const searchCloseBtn = document.getElementById('search-close-btn');
  const searchOpenBtn = document.getElementById('search-btn');
  const searchInput = document.getElementById('search-input-field');
  const searchResultsList = document.getElementById('search-results-list');

  let selectedIndex = -1;
  let currentResults = [];

  function openSearch() {
    if (!searchModal) return;
    searchModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    setTimeout(() => searchInput && searchInput.focus(), 60);
    selectedIndex = -1;
    renderSearchResults('');
  }

  function closeSearch() {
    if (!searchModal) return;
    searchModal.classList.add('hidden');
    document.body.style.overflow = '';
    if (searchInput) searchInput.value = '';
    selectedIndex = -1;
  }

  if (searchOpenBtn) searchOpenBtn.addEventListener('click', openSearch);
  if (searchCloseBtn) searchCloseBtn.addEventListener('click', closeSearch);
  if (searchBackdrop) searchBackdrop.addEventListener('click', closeSearch);

  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape') closeSearch();
  });

  // Keyboard navigation for search results
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      const results = searchResultsList?.querySelectorAll('.search-result-item');
      if (!results || results.length === 0) return;

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = Math.min(selectedIndex + 1, results.length - 1);
        updateSelection(results);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = Math.max(selectedIndex - 1, -1);
        updateSelection(results);
      } else if (e.key === 'Enter') {
        e.preventDefault();
        if (selectedIndex >= 0 && results[selectedIndex]) {
          window.location.href = results[selectedIndex].href;
        } else if (searchInput.value.trim()) {
          window.location.href = getSearchUrl(searchInput.value.trim());
        }
      }
    });

    searchInput.addEventListener('input', () => {
      selectedIndex = -1;
      renderSearchResults(searchInput.value);
    });
  }

  function updateSelection(results) {
    results.forEach((r, i) => {
      r.classList.toggle('selected', i === selectedIndex);
      if (i === selectedIndex) r.scrollIntoView({ block: 'nearest' });
    });
  }

  function getSearchUrl(query) {
    const depth = getPageDepth();
    const prefix = depth > 0 ? '../'.repeat(depth) : '';
    return prefix + 'pages/error-code-db.html?q=' + encodeURIComponent(query);
  }

  function renderSearchResults(query) {
    if (!searchResultsList) return;

    const q = query.trim();
    if (!q) {
      searchResultsList.innerHTML = getQuickLinks();
      return;
    }

    const results = searchIndex(q);

    if (results.length === 0) {
      searchResultsList.innerHTML = '<div class="p-6 text-center text-gray-500">No results found for "' + escHtml(q) + '"</div>';
      return;
    }

    currentResults = results.slice(0, 10);
    const depth = getPageDepth();
    const prefix = depth > 0 ? '../'.repeat(depth) : '';

    let html = '<div class="p-2 text-xs text-gray-500 border-b border-white/10">' + results.length + ' result' + (results.length !== 1 ? 's' : '') + '</div>';

    currentResults.forEach((r, idx) => {
      const iconMap = { 'spec': 'file-text', 'error': 'alert-circle', 'tool': 'wrench', 'guide': 'book-open' };
      const icon = iconMap[r.type] || 'file';

      html += '<a href="' + prefix + r.url + '" class="search-result-item" data-index="' + idx + '">' +
        '<i data-lucide="' + icon + '" style="width:1rem;height:1rem;flex-shrink:0;color:#00b8e6"></i>' +
        '<div class="flex-1 min-w-0">' +
        '<div class="truncate text-sm">' + highlightMatch(r.title, q) + '</div>' +
        '<div class="text-xs text-gray-500 truncate mt-0.5">' + highlightMatch(r.description, q) + '</div>' +
        '</div>' +
        '<span class="search-result-tag tag-' + r.type + '">' + r.type + '</span>' +
        '</a>';
    });

    searchResultsList.innerHTML = html;
    if (typeof lucide !== 'undefined') lucide.createIcons();
  }

  /* ── Search Index ─────────────────────────────────────── */
  var SEARCH_INDEX = [
    // Outdoor Power - EcoFlow
    { title: 'EcoFlow Delta Pro 3 | Full Specs', description: '4096 Wh LFP 4000 cycles Split-Phase New', type: 'spec', url: 'pages/specs/ecoflow-delta-pro-3.html', keywords: ['ecoflow', 'delta pro 3', '4096wh', '4000w', 'solar'] },
    { title: 'EcoFlow Delta Pro | Full Specs', description: '3600 Wh LFP 6500+ cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow', keywords: ['ecoflow', 'delta pro', '3600wh'] },
    { title: 'EcoFlow Delta 2 | Specs & Cycle Life', description: '1024 Wh LFP 3000 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow', keywords: ['ecoflow', 'delta 2', '1024wh'] },
    { title: 'EcoFlow Delta 2 Max | Specs', description: '2048 Wh LFP 3000 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow', keywords: ['ecoflow', 'delta 2 max'] },
    { title: 'EcoFlow River 2 Pro | Specs', description: '768 Wh LFP 3000 cycles portable', type: 'spec', url: 'pages/specs/outdoor-power.html#ecoflow', keywords: ['ecoflow', 'river 2 pro'] },
    // Outdoor Power - Jackery
    { title: 'Jackery Explorer 2000 Plus | Specs', description: '2042 Wh LFP 4000 cycles Top Rated', type: 'spec', url: 'pages/specs/outdoor-power.html#jackery', keywords: ['jackery', 'explorer 2000 plus'] },
    { title: 'Jackery Explorer 3000 Pro | Specs', description: '3024 Wh LFP 2000 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#jackery', keywords: ['jackery', 'explorer 3000 pro'] },
    { title: 'Jackery Explorer 1000 v2 | Specs', description: '1070 Wh LFP 1000 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#jackery', keywords: ['jackery', 'explorer 1000'] },
    // Outdoor Power - Bluetti
    { title: 'Bluetti EP500 Pro | Home Backup', description: '5100 Wh LFP 6000 cycles UPS', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti', keywords: ['bluetti', 'ep500 pro', '5100wh'] },
    { title: 'Bluetti AC300 | Modular System', description: 'Expandable modular power 12.3 kWh', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti', keywords: ['bluetti', 'ac300', 'modular'] },
    { title: 'Bluetti AC200L | Portable Power', description: '2048 Wh LFP 3500 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#bluetti', keywords: ['bluetti', 'ac200l'] },
    // Outdoor Power - Anker
    { title: 'Anker SOLIX F3800 | Specs', description: '3840 Wh LFP 3000 cycles Home Backup', type: 'spec', url: 'pages/specs/outdoor-power.html#anker', keywords: ['anker', 'solix', 'f3800'] },
    { title: 'Anker SOLIX F2000 | Specs', description: '2048 Wh LFP 3000 cycles', type: 'spec', url: 'pages/specs/outdoor-power.html#anker', keywords: ['anker', 'solix', 'f2000'] },
    // Hybrid Cars
    { title: 'Toyota Prius 2022 Battery Specs', description: '201.6 V NiMH Li hybrid battery', type: 'spec', url: 'pages/specs/toyota-prius-2022-battery.html', keywords: ['toyota', 'prius', 'hybrid battery'] },
    { title: 'Hybrid & EV Battery Specs Index', description: 'Toyota Tesla Honda Ford hybrid electric vehicle battery', type: 'spec', url: 'pages/specs/hybrid-cars.html', keywords: ['hybrid', 'ev', 'toyota', 'tesla', 'battery'] },
    // Drones
    { title: 'DJI Mavic 3 Pro | Battery Specs', description: '5000 mAh 77 Wh LiPo drone battery', type: 'spec', url: 'pages/specs/drones.html#dji', keywords: ['dji', 'mavic 3 pro', 'drone', 'battery'] },
    { title: 'DJI Air 2S | Battery Specs', description: '3500 mAh 40.42 Wh LiPo', type: 'spec', url: 'pages/specs/drones.html#dji', keywords: ['dji', 'air 2s'] },
    { title: 'DJI Mini 4 Pro | Battery Specs', description: '2597 mAh 35.71 Wh LiPo', type: 'spec', url: 'pages/specs/drones.html#dji', keywords: ['dji', 'mini 4 pro'] },
    // Error Codes - Hybrid
    { title: 'P0A80 Hybrid Battery Replacement Guide', description: 'Toyota Prius hybrid battery module replacement', type: 'guide', url: 'pages/troubleshooting/p0a80-replace-hybrid-battery.html', keywords: ['p0a80', 'hybrid battery', 'prius', 'replacement'] },
    { title: 'P0A7F Battery Deterioration Fix', description: 'Toyota Honda Lexus hybrid battery degradation', type: 'guide', url: 'pages/troubleshooting/p0a7f-hybrid-battery-deterioration.html', keywords: ['p0a7f', 'hybrid battery', 'deterioration'] },
    { title: 'P3000 Battery Control Malfunction', description: 'Battery management system fault code', type: 'guide', url: 'pages/troubleshooting/p3000-battery-control-malfunction.html', keywords: ['p3000', 'battery control', 'malfunction'] },
    { title: 'P3004 HV Battery Module Fault', description: 'High voltage battery module failure', type: 'guide', url: 'pages/troubleshooting/p3004-hv-battery-module-fault.html', keywords: ['p3004', 'hv battery', 'module fault'] },
    { title: 'P3009 Battery Cooling Fault', description: 'Hybrid battery cooling system fault', type: 'guide', url: 'pages/troubleshooting/p3009-battery-cooling-fault.html', keywords: ['p3009', 'cooling', 'battery fault'] },
    { title: 'C1259 HV System Disable', description: 'High voltage system disabled fault', type: 'guide', url: 'pages/troubleshooting/c1259-hv-system-disable.html', keywords: ['c1259', 'hv system', 'disable'] },
    // Error Codes - Power Station
    { title: 'E1 Overload Error Fix', description: 'EcoFlow Jackery Bluetti Anker power station overload', type: 'guide', url: 'pages/troubleshooting/e1-overload-ecoflow-jackery-blutti-anker.html', keywords: ['e1', 'overload', 'power station', 'ecoflow', 'jackery'] },
    { title: 'E2 High Temperature Error', description: 'Power station overheat protection', type: 'guide', url: 'pages/troubleshooting/e2-high-temperature-power-station.html', keywords: ['e2', 'temperature', 'overheat', 'power station'] },
    { title: 'E3 AC Overload Error', description: 'AC output overload fault', type: 'guide', url: 'pages/troubleshooting/e3-ac-overload-power-station.html', keywords: ['e3', 'ac overload', 'inverter'] },
    { title: 'E6 Battery Fault Fix', description: 'BMS battery cell anomaly', type: 'guide', url: 'pages/troubleshooting/e6-battery-fault-power-station.html', keywords: ['e6', 'battery fault', 'bms'] },
    { title: 'E7 Fan Blocked Error', description: 'Cooling fan obstruction error', type: 'guide', url: 'pages/troubleshooting/e7-fan-blocked-power-station.html', keywords: ['e7', 'fan', 'blocked', 'cooling'] },
    { title: 'Solar Input Not Working', description: 'Power station solar charging troubleshooting', type: 'guide', url: 'pages/troubleshooting/power-station-solar-input-not-working.html', keywords: ['solar', 'input', 'not working', 'mppt'] },
    // Error Codes - Drone
    { title: 'Gimbal Motor Overload Fix', description: 'DJI drone gimbal motor error', type: 'guide', url: 'pages/troubleshooting/gimbal-motor-overload-dji.html', keywords: ['gimbal', 'motor', 'overload', 'dji', 'drone'] },
    { title: 'Gimbal IMU Calibration Error', description: 'DJI IMU calibration required', type: 'guide', url: 'pages/troubleshooting/gimbal-imu-calibration-dji.html', keywords: ['imu', 'calibration', 'gimbal', 'dji'] },
    { title: 'Vision System Error Fix', description: 'DJI vision sensor fault', type: 'guide', url: 'pages/troubleshooting/vision-system-error-dji.html', keywords: ['vision', 'sensor', 'obstacle avoidance', 'dji'] },
    { title: 'Compass Error Fix', description: 'Drone compass calibration required', type: 'guide', url: 'pages/troubleshooting/compass-error-drone.html', keywords: ['compass', 'calibration', 'magnetic', 'dji'] },
    { title: 'Battery Temperature Error', description: 'Drone battery temperature fault', type: 'guide', url: 'pages/troubleshooting/battery-temperature-error-drone.html', keywords: ['battery', 'temperature', 'cold', 'heat', 'drone'] },
    { title: 'Drone Wont Connect Controller', description: 'Drone pairing and connection issues', type: 'guide', url: 'pages/troubleshooting/drone-wont-connect-controller.html', keywords: ['connection', 'controller', 'pairing', 'wifi', 'drone'] },
    // General Troubleshooting
    { title: 'Cooling Fan Noise Fix', description: 'Hybrid battery cooling fan loud grinding', type: 'guide', url: 'pages/troubleshooting/hybrid-battery-cooling-fan-noise.html', keywords: ['cooling fan', 'noise', 'hybrid', 'prius'] },
    { title: 'Smart Home Device Offline', description: 'Smart plug wifi connection issues', type: 'guide', url: 'pages/troubleshooting/smart-home-device-offline.html', keywords: ['smart home', 'offline', 'wifi', 'connection'] },
    { title: '3D Printer Thermal Runaway', description: 'Hotend bed temperature control fault', type: 'guide', url: 'pages/troubleshooting/3d-printer-thermal-runaway.html', keywords: ['3d printer', 'thermal runaway', 'hotend', 'thermistor'] },
    // Smart Home
    { title: 'Smart Home Device Specs', description: 'Roborock Yale Ecobee smart home specs', type: 'spec', url: 'pages/specs/smart-home.html', keywords: ['smart home', 'roborock', 'yale', 'ecobee'] },
    // Tools
    { title: 'Best Multimeters 2026', description: 'Fluke Klein multimeter review', type: 'tool', url: 'pages/tools/best-multimeters-2026.html', keywords: ['multimeter', 'fluke', 'tool', 'voltage'] },
    { title: 'Runtime Calculator', description: 'Calculate power station runtime', type: 'tool', url: 'pages/tools/runtime-calculator.html', keywords: ['runtime', 'calculator', 'wh', 'wattage'] },
    { title: 'Unit Converter', description: 'Wh mAh km miles conversion', type: 'tool', url: 'pages/tools/unit-converter.html', keywords: ['converter', 'unit', 'conversion'] },
    // Database & Index
    { title: 'Error Code Database', description: 'All fault codes and troubleshooting guides', type: 'error', url: 'pages/error-code-db.html', keywords: ['error code', 'database', 'fault', 'troubleshooting'] },
    { title: 'Master Specs Comparison', description: 'Cross-brand spec comparison tables', type: 'spec', url: 'pages/master-specs.html', keywords: ['comparison', 'specs', 'compare', 'master'] },
    { title: 'Brand Index A-Z', description: 'All supported brands directory', type: 'spec', url: 'pages/brand-index.html', keywords: ['brand', 'index', 'directory'] },
  ];

  function searchIndex(query) {
    var q = query.toLowerCase().trim();
    if (!q) return [];

    var results = SEARCH_INDEX.filter(function (item) {
      var title = item.title.toLowerCase();
      var desc = (item.description || '').toLowerCase();
      var keywords = (item.keywords || []).join(' ').toLowerCase();
      return title.indexOf(q) !== -1 || desc.indexOf(q) !== -1 || keywords.indexOf(q) !== -1;
    });

    // Sort by priority
    results.sort(function (a, b) {
      var titleA = a.title.toLowerCase();
      var titleB = b.title.toLowerCase();
      var aExact = titleA.indexOf(q) !== -1;
      var bExact = titleB.indexOf(q) !== -1;
      if (aExact && bExact) return titleA.localeCompare(titleB);
      if (aExact) return -1;
      if (bExact) return 1;
      return titleA.localeCompare(titleB);
    });

    return results;
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

  /* ═══════════════════════════════════════════════════════
     2. SPEC COMPARISON TOOL (localStorage)
     ═══════════════════════════════════════════════════════ */
  const COMPARE_STORAGE_KEY = 'tsh_compare_items';
  const MAX_COMPARE_ITEMS = 4;
  let compareItems = JSON.parse(localStorage.getItem(COMPARE_STORAGE_KEY) || '[]');

  function updateCompareUI() {
    const btn = document.getElementById('compare-btn');
    const count = document.getElementById('compare-count');
    if (btn) {
      btn.style.display = compareItems.length >= 2 ? 'inline-flex' : 'none';
    }
    if (count) {
      count.textContent = compareItems.length;
    }
  }

  function toggleCompareItem(modelName, brand, capacity, output, cycles, weight, url) {
    const existingIndex = compareItems.findIndex(item => item.model === modelName);
    if (existingIndex >= 0) {
      compareItems.splice(existingIndex, 1);
    } else {
      if (compareItems.length >= MAX_COMPARE_ITEMS) {
        alert('Maximum ' + MAX_COMPARE_ITEMS + ' items can be compared. Remove one to add another.');
        return;
      }
      compareItems.push({ model: modelName, brand, capacity, output, cycles, weight, url });
    }
    localStorage.setItem(COMPARE_STORAGE_KEY, JSON.stringify(compareItems));
    updateCompareUI();
    updateCompareCheckboxes();
  }

  function updateCompareCheckboxes() {
    document.querySelectorAll('[data-compare-item]').forEach(btn => {
      const model = btn.getAttribute('data-compare-item');
      const isSelected = compareItems.some(item => item.model === model);
      btn.classList.toggle('compare-selected', isSelected);
      btn.innerHTML = isSelected
        ? '<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg> Selected'
        : '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path></svg> Compare';
    });
  }

  function openCompareModal() {
    if (compareItems.length < 2) return;
    const modal = document.getElementById('compare-modal');
    if (!modal) return;

    const container = document.getElementById('compare-items');
    if (!container) return;

    let html = '';
    compareItems.forEach(item => {
      html += '<div class="compare-item">' +
        '<button class="compare-remove" data-model="' + item.model + '">&times;</button>' +
        '<h4 class="font-semibold">' + item.model + '</h4>' +
        '<p class="text-sm text-gray-500">' + item.brand + '</p>' +
        '<a href="' + item.url + '" class="text-electric-400 text-sm hover:underline">View Specs</a>' +
        '</div>';
    });
    container.innerHTML = html;

    // Render comparison table
    const tableContainer = document.getElementById('compare-table');
    if (tableContainer) {
      renderComparisonTable(tableContainer);
    }

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';

    // Remove buttons
    modal.querySelectorAll('.compare-remove').forEach(btn => {
      btn.addEventListener('click', () => {
        const model = btn.getAttribute('data-model');
        compareItems = compareItems.filter(item => item.model !== model);
        localStorage.setItem(COMPARE_STORAGE_KEY, JSON.stringify(compareItems));
        openCompareModal();
        updateCompareUI();
      });
    });
  }

  function renderComparisonTable(container) {
    if (compareItems.length < 2) return;

    const specs = [
      { label: 'Capacity (Wh)', key: 'capacity' },
      { label: 'AC Output (W)', key: 'output' },
      { label: 'Battery Cycles', key: 'cycles' },
      { label: 'Weight (kg)', key: 'weight' },
    ];

    let html = '<table class="compare-table"><thead><tr><th>Spec</th>';
    compareItems.forEach(item => {
      html += '<th>' + item.model + '</th>';
    });
    html += '</tr></thead><tbody>';

    specs.forEach(spec => {
      html += '<tr><td class="spec-label">' + spec.label + '</td>';
      const values = compareItems.map(item => item[spec.key] || '-');
      const numericValues = values.map(v => parseFloat(String(v).replace(/[^0-9.]/g, '')) || 0);
      const maxVal = Math.max(...numericValues);
      const minVal = Math.min(...numericValues.filter(v => v > 0));

      compareItems.forEach((item, idx) => {
        const val = values[idx];
        const num = numericValues[idx];
        let cellClass = '';
        if (spec.key === 'weight' && num > 0 && num === minVal) cellClass = 'best-value';
        if (spec.key !== 'weight' && num > 0 && num === maxVal) cellClass = 'best-value';
        html += '<td class="' + cellClass + '">' + val + '</td>';
      });
      html += '</tr>';
    });

    html += '</tbody></table>';
    container.innerHTML = html;
  }

  function closeCompareModal() {
    const modal = document.getElementById('compare-modal');
    if (modal) {
      modal.classList.add('hidden');
      document.body.style.overflow = '';
    }
  }

  // Initialize compare functionality
  document.addEventListener('DOMContentLoaded', () => {
    updateCompareUI();
    updateCompareCheckboxes();

    // Add click handlers for compare buttons
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-compare-item]');
      if (btn) {
        const modelName = btn.getAttribute('data-compare-item');
        const brand = btn.getAttribute('data-brand');
        const capacity = btn.getAttribute('data-capacity');
        const output = btn.getAttribute('data-output');
        const cycles = btn.getAttribute('data-cycles');
        const weight = btn.getAttribute('data-weight');
        const url = btn.getAttribute('data-url');
        toggleCompareItem(modelName, brand, capacity, output, cycles, weight, url);
      }
    });

    const compareBtn = document.getElementById('compare-btn');
    const closeCompareBtn = document.getElementById('close-compare-btn');
    const compareModal = document.getElementById('compare-modal');

    if (compareBtn) compareBtn.addEventListener('click', openCompareModal);
    if (closeCompareBtn) closeCompareBtn.addEventListener('click', closeCompareModal);
    if (compareModal) {
      compareModal.addEventListener('click', (e) => {
        if (e.target === compareModal) closeCompareModal();
      });
    }
  });

  /* ═══════════════════════════════════════════════════════
     3. FAQ ACCORDION COMPONENT
     ═══════════════════════════════════════════════════════ */
  function initFAQAccordion() {
    document.querySelectorAll('.faq-accordion').forEach(accordion => {
      const items = accordion.querySelectorAll('.faq-item');
      items.forEach((item, index) => {
        const header = item.querySelector('.faq-header');
        const content = item.querySelector('.faq-content');
        if (!header || !content) return;

        header.addEventListener('click', () => {
          const isOpen = item.classList.contains('open');
          // Close all
          items.forEach(i => {
            i.classList.remove('open');
            const c = i.querySelector('.faq-content');
            if (c) c.style.maxHeight = '0';
          });
          // Open clicked if was closed
          if (!isOpen) {
            item.classList.add('open');
            content.style.maxHeight = content.scrollHeight + 'px';
          }
        });
      });
    });
  }
  initFAQAccordion();

  /* ═══════════════════════════════════════════════════════
     4. TABLE OF CONTENTS (TOC)
     ═══════════════════════════════════════════════════════ */
  function initTOC() {
    const toc = document.querySelector('.toc-nav');
    if (!toc) return;

    const headings = document.querySelectorAll('main h2[id], main h3[id]');
    if (headings.length < 3) {
      toc.style.display = 'none';
      return;
    }

    const list = toc.querySelector('.toc-list');
    if (!list) return;

    headings.forEach(heading => {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.href = '#' + heading.id;
      a.textContent = heading.textContent;
      a.className = heading.tagName === 'H3' ? 'toc-link toc-link-h3' : 'toc-link';
      li.appendChild(a);
      list.appendChild(li);
    });

    // Active state on scroll
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.getAttribute('id');
        const link = toc.querySelector('a[href="#' + id + '"]');
        if (link) {
          link.classList.toggle('active', entry.isIntersecting);
        }
      });
    }, { rootMargin: '-20% 0px -70% 0px' });

    headings.forEach(h => observer.observe(h));

    // Smooth scroll
    list.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const id = link.getAttribute('href').slice(1);
        const el = document.getElementById(id);
        if (el) {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          history.pushState(null, '', '#' + id);
        }
      });
    });
  }
  initTOC();

  /* ═══════════════════════════════════════════════════════
     5. PDF DOWNLOAD PLACEHOLDER
     ═══════════════════════════════════════════════════════ */
  function initPDFButtons() {
    document.querySelectorAll('[data-pdf-download]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const pdfUrl = btn.getAttribute('data-pdf-download');
        const title = btn.getAttribute('data-pdf-title') || 'Guide';

        // Show email subscription modal
        const modal = document.getElementById('pdf-modal');
        if (modal) {
          modal.classList.remove('hidden');
          document.body.style.overflow = 'hidden';
          const titleEl = modal.querySelector('#pdf-modal-title');
          if (titleEl) titleEl.textContent = 'Download ' + title;
          const form = modal.querySelector('#pdf-email-form');
          if (form) {
            form.onsubmit = (e) => {
              e.preventDefault();
              const email = form.querySelector('input[type="email"]').value;
              if (email) {
                // Placeholder - would send to email service
                alert('Thank you! In a production environment, the PDF would be sent to ' + email);
                modal.classList.add('hidden');
                document.body.style.overflow = '';
              }
            };
          }
        }
      });
    });

    // Close modal handlers
    const closePdfModal = document.getElementById('close-pdf-modal');
    const pdfModal = document.getElementById('pdf-modal');
    if (closePdfModal && pdfModal) {
      closePdfModal.addEventListener('click', () => {
        pdfModal.classList.add('hidden');
        document.body.style.overflow = '';
      });
      pdfModal.addEventListener('click', (e) => {
        if (e.target === pdfModal) {
          pdfModal.classList.add('hidden');
          document.body.style.overflow = '';
        }
      });
    }
  }
  initPDFButtons();

  /* ═══════════════════════════════════════════════════════
     6. IMAGE LAZY LOADING & OPTIMIZATION
     ═══════════════════════════════════════════════════════ */
  function initLazyImages() {
    if ('loading' in HTMLImageElement.prototype) {
      // Native lazy loading supported
      document.querySelectorAll('img[data-src]').forEach(img => {
        img.src = img.getAttribute('data-src');
      });
    } else {
      // Fallback for older browsers
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.getAttribute('data-src') || img.src;
            observer.unobserve(img);
          }
        });
      });
      document.querySelectorAll('img[data-src]').forEach(img => observer.observe(img));
    }
  }
  initLazyImages();

  /* ═══════════════════════════════════════════════════════
     7. RELATED ARTICLES
     ═══════════════════════════════════════════════════════ */
  function initRelatedArticles() {
    document.querySelectorAll('[data-related-articles]').forEach(container => {
      const currentPage = container.getAttribute('data-related-articles');
      const category = container.getAttribute('data-category') || '';
      const related = getRelatedArticles(currentPage, category);
      renderRelatedArticles(container, related);
    });
  }

  function getRelatedArticles(currentPage, category) {
    const allArticles = SEARCH_INDEX.filter(item => item.type === 'guide' && item.url !== currentPage);
    // Prioritize same category
    const sameCategory = allArticles.filter(item =>
      item.keywords?.some(k => category && k.includes(category))
    );
    const others = allArticles.filter(item => !sameCategory.includes(item));
    return [...sameCategory, ...others].slice(0, 3);
  }

  function renderRelatedArticles(container, articles) {
    if (articles.length === 0) return;

    const depth = getPageDepth();
    const prefix = depth > 0 ? '../'.repeat(depth) : '';

    let html = '<div class="related-articles-grid">';
    articles.forEach(article => {
      html += '<a href="' + prefix + article.url + '" class="related-article-card">' +
        '<h4 class="font-semibold text-sm">' + article.title + '</h4>' +
        '<p class="text-xs text-gray-500 mt-1">' + article.description + '</p>' +
        '<span class="text-electric-400 text-xs mt-2 inline-block">Read more &rarr;</span>' +
        '</a>';
    });
    html += '</div>';
    container.innerHTML = html;
  }
  initRelatedArticles();

  /* ═══════════════════════════════════════════════════════
     8. MOBILE MENU
     ═══════════════════════════════════════════════════════ */
  const mobileBtn = document.getElementById('mobile-menu-btn');
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

  /* ── Table Filter ──────────────────────────────────────── */
  var filterInputs = document.querySelectorAll('[data-filter-input]');
  for (var i = 0; i < filterInputs.length; i++) {
    var input = filterInputs[i];
    var targetId = input.getAttribute('data-filter-input');
    var table = document.getElementById(targetId);
    if (!table) continue;
    var rows = table.querySelectorAll('tbody tr');
    input.addEventListener('input', (function (allRows) {
      return function () {
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
      tab.addEventListener('click', (function (t, ps, w) {
        return function () {
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
    copyBtns[ci].addEventListener('click', function () {
      var text = this.getAttribute('data-copy');
      navigator.clipboard.writeText(text).then((function (btn) {
        return function () {
          var orig = btn.textContent;
          btn.textContent = 'Copied!';
          setTimeout(function () { btn.textContent = orig; }, 1500);
        };
      })(this));
    });
  }

  /* ── Smooth Scroll for anchor links ───────────────────── */
  var anchorLinks = document.querySelectorAll('a[href^="#"]');
  for (var ai = 0; ai < anchorLinks.length; ai++) {
    anchorLinks[ai].addEventListener('click', function (e) {
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
    return s.replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
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
