/* ============================================================
   TechSpecsHub - Main JavaScript
   Search modal, mobile menu, Lucide icon initialization
   ============================================================ */

(function() {
  'use strict';

  // ----- Search index (matches pages in sitemap.xml) -----
  var SEARCH_INDEX = [
    { title: 'Home', desc: 'Technical specifications, error codes & repair data', url: '/' },
    { title: 'Outdoor Power Station Specs', desc: 'Portable power station comparison and specifications', url: '/pages/specs/outdoor-power.html' },
    { title: 'EcoFlow Delta Pro 3 Specs', desc: 'Complete specs, error codes and troubleshooting for Delta Pro 3', url: '/pages/specs/ecoflow-delta-pro-3.html' },
    { title: 'Bluetti AC200MAX Specs', desc: 'Portable power station specifications and error codes', url: '/pages/specs/bluetti-ac200max.html' },
    { title: 'Jackery Explorer 2000 Plus Specs', desc: 'Technical specifications for Jackery Explorer 2000 Plus', url: '/pages/specs/jackery-explorer-2000-plus.html' },
    { title: 'Budget Power Station Comparison', desc: 'Mid-range 500W-1500W power station buying guide', url: '/pages/specs/budget-500w-power-station-comparison.html' },
    { title: 'Off-Grid Solar Sizing Guide', desc: 'How to calculate your solar panel and battery needs', url: '/pages/specs/off-grid-solar-system-sizing-guide.html' },
    { title: 'Portable Power Station FAQ', desc: 'Common questions about batteries, inverters and charging', url: '/pages/specs/portable-power-station-faq.html' },
    { title: 'Hybrid & EV Battery Specs', desc: 'Toyota Prius, Tesla and other hybrid battery specifications', url: '/pages/specs/hybrid-cars.html' },
    { title: 'Toyota Prius Battery Specs', desc: 'Prius hybrid battery module specifications and replacement data', url: '/pages/specs/toyota-prius-2022-battery.html' },
    { title: 'Drone & UAV Specs', desc: 'DJI Mavic, Air and other drone technical specifications', url: '/pages/specs/drones.html' },
    { title: 'DJI Mavic 3 Pro Specs', desc: 'Complete Mavic 3 Pro camera, battery and performance data', url: '/pages/specs/dji-mavic-3-pro.html' },
    { title: 'DJI Air 3 Specs', desc: 'DJI Air 3 camera, flight time and technical specifications', url: '/pages/specs/dji-air-3.html' },
    { title: 'Smart Home Device Specs', desc: 'Smart home devices and connected appliance specifications', url: '/pages/specs/smart-home.html' },
    { title: 'Navigation & Marine Specs', desc: 'GPS, marine electronics and navigation device specifications', url: '/pages/specs/navigation.html' },
    { title: 'E-Bike & Micro-Mobility Specs', desc: 'Electric bicycles, scooters and micro-mobility specifications', url: '/pages/specs/ebike-micromobility.html' },
    { title: '3D Printer Specs', desc: 'FDM and resin 3D printer technical specifications', url: '/pages/specs/3d-printers.html' },
    { title: 'Error Code Database', desc: '200+ fault codes for hybrids, drones, power stations and more', url: '/pages/error-code-db.html' },
    { title: 'P0A80 - Replace Hybrid Battery', desc: 'Step-by-step guide for Toyota P0A80 fault code diagnosis and repair', url: '/pages/troubleshooting/p0a80-replace-hybrid-battery.html' },
    { title: 'P0A7F - HV Battery Deterioration', desc: 'Toyota hybrid battery module balance fault troubleshooting', url: '/pages/troubleshooting/p0a7f-hybrid-battery-deterioration.html' },
    { title: 'Power Station Won\'t Turn On', desc: 'Troubleshooting guide for portable power stations that fail to power on', url: '/pages/troubleshooting/power-station-wont-turn-on.html' },
    { title: 'DJI Gimbal Error Codes', desc: 'DJI drone gimbal motor stuck, overload and calibration errors', url: '/pages/troubleshooting/dji-gimbal-error-codes.html' },
    { title: 'Master Specs Comparison', desc: 'Side-by-side comparison of all device specifications', url: '/pages/master-specs.html' },
    { title: 'Brand Index A-Z', desc: 'All brands covered on TechSpecsHub', url: '/pages/brand-index.html' },
    { title: 'Best Multimeters 2026', desc: 'Buyer\'s guide for CAT-rated digital multimeters', url: '/pages/tools/best-multimeters-2026.html' },
    { title: 'About TechSpecsHub', desc: 'Our mission, data sources and editorial standards', url: '/pages/about.html' },
    { title: 'Contact', desc: 'Get in touch with the TechSpecsHub team', url: '/pages/contact.html' }
  ];

  // ----- Lucide icon initialization -----
  function initLucide() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      try {
        window.lucide.createIcons();
      } catch (e) {
        // Fallback: ignore
      }
    } else {
      // Retry after short delay
      setTimeout(initLucide, 200);
    }
  }

  // ----- Search modal -----
  function initSearch() {
    var searchBtn = document.getElementById('search-btn');
    var searchModal = document.getElementById('search-modal');
    var searchCloseBtn = document.getElementById('search-close-btn');
    var searchInput = document.getElementById('search-input-field');
    var searchResults = document.getElementById('search-results-list');
    var heroSearch = document.getElementById('hero-search');

    if (!searchBtn || !searchModal) return;

    function openSearch() {
      searchModal.classList.add('is-open');
      if (searchInput) {
        searchInput.focus();
        searchInput.select();
      }
      document.body.style.overflow = 'hidden';
    }

    function closeSearch() {
      searchModal.classList.remove('is-open');
      if (searchInput) searchInput.value = '';
      if (searchResults) searchResults.innerHTML = '';
      document.body.style.overflow = '';
    }

    searchBtn.addEventListener('click', function(e) {
      e.preventDefault();
      openSearch();
    });

    if (heroSearch) {
      heroSearch.addEventListener('focus', openSearch);
    }

    if (searchCloseBtn) {
      searchCloseBtn.addEventListener('click', closeSearch);
    }

    // Close on backdrop click
    var backdrop = document.getElementById('search-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', closeSearch);
    }

    // Keyboard: Esc to close, Ctrl/Cmd+K to open
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && searchModal.classList.contains('is-open')) {
        closeSearch();
      }
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        openSearch();
      }
    });

    // Search functionality
    if (searchInput && searchResults) {
      searchInput.addEventListener('input', function() {
        var query = searchInput.value.trim().toLowerCase();

        if (!query) {
          searchResults.innerHTML = '';
          return;
        }

        var matches = SEARCH_INDEX.filter(function(item) {
          return (item.title.toLowerCase().indexOf(query) !== -1) ||
                 (item.desc.toLowerCase().indexOf(query) !== -1);
        }).slice(0, 10);

        if (matches.length === 0) {
          searchResults.innerHTML = '<div class="search-result-empty">No results found for "' + escapeHtml(query) + '"</div>';
          return;
        }

        var html = matches.map(function(item) {
          return '<a href="' + item.url + '" class="search-result-item">' +
                   '<div class="search-result-title">' + item.title + '</div>' +
                   '<div class="search-result-desc">' + item.desc + '</div>' +
                 '</a>';
        }).join('');

        searchResults.innerHTML = html;
      });
    }
  }

  // ----- Mobile menu toggle -----
  function initMobileMenu() {
    var mobileBtn = document.getElementById('mobile-menu-btn');
    var mobileMenu = document.getElementById('mobile-menu');

    if (!mobileBtn || !mobileMenu) return;

    mobileBtn.addEventListener('click', function() {
      mobileMenu.classList.toggle('is-open');
    });
  }

  // ----- HTML escape helper -----
  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function(c) {
      return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c];
    });
  }

  // ----- Current year for footer -----
  function initFooterYear() {
    var yearEl = document.getElementById('current-year');
    if (yearEl) {
      yearEl.textContent = new Date().getFullYear();
    }
  }

  // ----- Initialize everything when DOM is ready -----
  function init() {
    initLucide();
    initSearch();
    initMobileMenu();
    initFooterYear();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
