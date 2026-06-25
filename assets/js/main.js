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
    { title: 'Power Station Output Not Working', desc: 'Troubleshoot AC, USB and DC port output issues', url: '/pages/specs/portable-power-station-output-not-working.html' },
    { title: 'Power Station Beeping Alarm', desc: 'Diagnose beep patterns and what they mean', url: '/pages/specs/portable-power-station-beeping.html' },
    { title: 'Power Station Won\'t Turn On', desc: '9 causes and fixes for dead power stations', url: '/pages/specs/portable-power-station-wont-turn-on.html' },
    { title: 'Power Station Not Charging', desc: 'AC, solar and DC charging troubleshooting', url: '/pages/specs/portable-power-station-not-charging.html' },
    { title: 'ECO Mode Explained', desc: 'How ECO mode works and when to use it', url: '/pages/specs/portable-power-station-eco-mode.html' },
    { title: 'Solar Charging 0W Fix', desc: '8 causes and fixes for zero watt solar charging', url: '/pages/specs/solar-charging-0w-power-station.html' },
    { title: 'Charging Stops at 80%', desc: 'Why power stations stop charging at 80% and how to change it', url: '/pages/specs/power-station-charging-stops-at-80.html' },
    { title: 'Long-Term Storage Guide', desc: 'How to store a portable power station properly', url: '/pages/specs/how-to-store-portable-power-station.html' },
    { title: 'DJI Drone Won\'t Turn On', desc: '9 causes and fixes for DJI drones that won\'t power on', url: '/pages/specs/dji-drone-wont-turn-on.html' },
    { title: 'DJI Battery Hibernation', desc: 'What is hibernation mode and how to wake up battery', url: '/pages/specs/dji-battery-hibernation-mode.html' },
    { title: 'DJI GPS Weak Signal', desc: '8 fixes to get 10+ satellites on DJI drones', url: '/pages/specs/dji-drone-gps-weak-signal.html' },
    { title: 'Controller Disconnecting', desc: 'Why DJI controller disconnects mid-flight and fixes', url: '/pages/specs/dji-controller-disconnecting-mid-flight.html' },
    { title: 'Drone Not Connecting to Controller', desc: 'Complete DJI pairing and linking guide', url: '/pages/specs/dji-drone-not-connecting-to-controller.html' },
    { title: 'IMU & Compass Calibration', desc: 'Step-by-step DJI drone calibration guide', url: '/pages/specs/how-to-calibrate-dji-drone-imu-compass.html' },
    { title: 'DJI Gimbal Not Working', desc: '8 fixes for stuck or broken gimbal', url: '/pages/specs/dji-gimbal-not-working-stuck.html' },
    { title: 'Hybrid & EV Battery Specs', desc: 'Toyota Prius, Tesla and other hybrid battery specifications', url: '/pages/specs/hybrid-cars.html' },
    { title: 'Drone & UAV Specs', desc: 'DJI Mavic, Air and other drone technical specifications', url: '/pages/specs/drones.html' },
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
    { title: 'Power Station Runtime Calculator', desc: 'Calculate how long your portable power station will run devices.', url: '/pages/tools/power-station-runtime-calculator.html' },
    { title: 'Solar Panel Needs Calculator', desc: 'Calculate how many solar panels you need to charge your power station.', url: '/pages/tools/solar-panel-needs-calculator.html' },
    { title: 'Appliance Wattage Calculator', desc: 'Calculate total power consumption of your devices and appliances.', url: '/pages/tools/appliance-wattage-calculator.html' },
    { title: 'Camping Power Calculator', desc: 'Calculate what size power station you need for camping.', url: '/pages/tools/camping-power-calculator.html' },
    { title: 'CPAP Battery Calculator', desc: 'Calculate CPAP runtime on portable power stations.', url: '/pages/tools/cpap-battery-calculator.html' },
    { title: 'Drone Flight Time Calculator', desc: 'Calculate drone flight time based on battery and weight.', url: '/pages/tools/drone-flight-time-calculator.html' },
    { title: 'Drone Battery Life Calculator', desc: 'Calculate remaining drone battery life and cycles.', url: '/pages/tools/drone-battery-life-calculator.html' },
    { title: 'Drone Photo Settings Calculator', desc: 'Find optimal drone camera settings for any condition.', url: '/pages/tools/drone-photo-settings-calculator.html' },
    { title: 'Power Station Fan Noise Loud?', desc: 'Causes and fixes for loud fan noise on portable power stations.', url: '/pages/specs/portable-power-station-fan-noise-loud.html' },
    { title: 'Can Power Station Run Refrigerator?', desc: 'Can a portable power station run a refrigerator? Wattage and runtime.', url: '/pages/specs/can-portable-power-station-run-refrigerator.html' },
    { title: 'Power Station vs Generator', desc: 'Portable power station vs generator - which is better?', url: '/pages/specs/portable-power-station-vs-generator.html' },
    { title: 'LiFePO4 vs Lithium Ion', desc: 'LiFePO4 vs lithium ion power stations comparison.', url: '/pages/specs/lifepo4-vs-lithium-ion-power-station.html' },
    { title: 'Pass-Through Charging Explained', desc: 'Can a power station charge while in use? Pass-through charging.', url: '/pages/specs/can-portable-power-station-charge-while-in-use.html' },
    { title: 'DJI Mini 4 Pro vs Mini 5 Pro Specs', desc: 'Full specs comparison of DJI Mini 4 Pro vs Mini 5 Pro.', url: '/pages/specs/dji-mini-4-pro-vs-mini-5-pro-specs.html' },
    { title: 'Best DJI Drone for Beginners 2026', desc: 'Top picks and buying guide for beginner DJI drones.', url: '/pages/specs/best-dji-drone-for-beginners-2026.html' },
    { title: 'DJI RTH Not Working', desc: 'DJI drone return to home not working - causes and fixes.', url: '/pages/specs/dji-drone-return-to-home-not-working.html' },
    { title: 'DJI Fly App Not Connecting', desc: 'DJI Fly app not connecting to drone - troubleshooting guide.', url: '/pages/specs/dji-fly-app-not-connecting-to-drone.html' },
    { title: 'DJI Drone Firmware Update Guide', desc: 'Step-by-step guide to update DJI drone firmware.', url: '/pages/specs/how-to-update-dji-drone-firmware.html' },
    { title: 'Charge Power Station Without Electricity', desc: 'How to charge a portable power station without electricity - solar, car, generator, and more.', url: '/pages/specs/how-to-charge-power-station-without-electricity.html' },
    { title: 'Power Station Battery Replacement Cost', desc: 'Portable power station battery replacement cost and options by brand.', url: '/pages/specs/portable-power-station-battery-replacement-cost.html' },
    { title: 'Best Power Station for RV & Boondocking', desc: 'Best portable power station for RV and boondocking off-grid.', url: '/pages/specs/best-portable-power-station-for-rv.html' },
    { title: 'Dispose of Power Station & Battery Recycling', desc: 'How to dispose of a portable power station and battery recycling.', url: '/pages/specs/how-to-dispose-of-portable-power-station.html' },
    { title: 'Best Power Station for Tailgating', desc: 'Best portable power station for tailgating and outdoor events.', url: '/pages/specs/portable-power-station-for-tailgating.html' },
    { title: 'Why Is My Power Station Charging Slow?', desc: 'Why is my power station charging so slow? Causes and fixes.', url: '/pages/specs/why-is-my-power-station-charging-so-slow.html' },
    { title: 'Power Station Overheating & Hot', desc: 'Portable power station overheating and getting hot - causes and fixes.', url: '/pages/specs/portable-power-station-overheating-hot.html' },
    { title: 'Extension Cord With Power Station', desc: 'Can I use an extension cord with a portable power station?', url: '/pages/specs/can-i-use-extension-cord-with-power-station.html' },
    { title: 'Best Power Station Under $500', desc: 'Best portable power station under $500 budget guide.', url: '/pages/specs/best-portable-power-station-under-500.html' },
    { title: 'Power Station UPS Mode Explained', desc: 'Portable power station UPS mode explained - how it works.', url: '/pages/specs/portable-power-station-ups-mode-explained.html' },
    { title: 'How to Find a Lost DJI Drone', desc: 'How to find a lost DJI drone - step-by-step guide.', url: '/pages/specs/how-to-find-lost-dji-drone.html' },
    { title: 'Best Memory Card for DJI Mini 5 Pro', desc: 'Best memory card for DJI Mini 5 Pro SD card guide.', url: '/pages/specs/best-memory-card-for-dji-mini-5-pro.html' },
    { title: 'How Long Do DJI Drone Batteries Last?', desc: 'How long do DJI drone batteries last - cycles and lifespan.', url: '/pages/specs/how-long-do-dji-drone-batteries-last.html' },
    { title: 'Fly DJI Drone in Rain? Water Resistance', desc: 'Can you fly a DJI drone in the rain? Water resistance guide.', url: '/pages/specs/can-you-fly-dji-drone-in-rain.html' },
    { title: 'Transfer DJI Drone Photos to Phone', desc: 'How to transfer DJI drone photos and videos to phone.', url: '/pages/specs/how-to-transfer-dji-drone-photos-to-phone.html' },
    { title: 'DJI Mini Under 250g License Requirements', desc: 'DJI Mini drone under 250g - do I need a license? FAA rules.', url: '/pages/specs/dji-mini-drone-under-250g-license-requirements.html' },
    { title: 'DJI Drone Battery Swelling & Safety', desc: 'DJI drone battery swelling - what to do and is it safe?', url: '/pages/specs/dji-drone-battery-swelling-what-to-do.html' },
    { title: 'Calibrate DJI Remote Controller', desc: 'How to calibrate DJI remote controller stick calibration.', url: '/pages/specs/how-to-calibrate-dji-remote-controller.html' },
    { title: 'DJI Drone ATTI Mode Explained', desc: 'DJI drone ATTI mode - what it is and how to get out.', url: '/pages/specs/dji-drone-atti-mode-how-to-get-out.html' },
    { title: 'Best DJI Drone for Photography', desc: 'Best DJI drone for photography aerial photography guide.', url: '/pages/specs/best-dji-drone-for-photography-2026.html' },
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
