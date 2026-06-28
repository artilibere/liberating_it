(function () {
  function initFilters() {
  const grid = document.getElementById('structure-grid');
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll('.ls-card'));
  const countEl = document.querySelector('.ls-catalog__count');
  const emptyEl = document.querySelector('.ls-catalog__empty');
  const clearBtn = document.querySelector('.ls-filters__clear');
  const filterBtns = document.querySelectorAll('.ls-chip--filter');
  const statusEl = document.querySelector('.ls-filters__status');
  const filtersToggle = document.querySelector('.ls-filters-toggle');

  const active = { difficolta: null, complessita: null, durata: null, fase: null };
  const allowed = {};

  filterBtns.forEach(function (btn) {
    const filter = btn.dataset.filter;
    const value = btn.dataset.value;
    if (!allowed[filter]) allowed[filter] = new Set();
    allowed[filter].add(value);
  });

  function parseUrl() {
    const params = new URLSearchParams(window.location.search);
    for (const key of Object.keys(active)) {
      const val = params.get(key);
      if (val && allowed[key] && allowed[key].has(val)) {
        active[key] = val;
      }
    }
  }

  function syncUrl() {
    const params = new URLSearchParams();
    for (const [key, val] of Object.entries(active)) {
      if (val) params.set(key, val);
    }
    const qs = params.toString();
    const url = qs ? '?' + qs : window.location.pathname;
    history.replaceState(null, '', url);
  }

  function syncButtons() {
    filterBtns.forEach(function (btn) {
      const filter = btn.dataset.filter;
      const value = btn.dataset.value;
      const pressed = active[filter] === value;
      btn.setAttribute('aria-pressed', String(pressed));
    });
  }

  function activeCount() {
    return Object.values(active).filter(Boolean).length;
  }

  function syncFilterToggle() {
    if (!filtersToggle) return;
    const n = activeCount();
    filtersToggle.textContent = n ? 'Filtra (' + n + ')' : 'Filtra';
  }

  function syncFilterStatus(visible) {
    if (!statusEl) return;
    const n = activeCount();
    if (n === 0) {
      statusEl.hidden = true;
      statusEl.textContent = '';
      return;
    }
    statusEl.hidden = false;
    let msg = n === 1 ? '1 filtro attivo' : n + ' filtri attivi';
    if (typeof visible === 'number') {
      msg += '. ' + visible + (visible === 1 ? ' struttura visibile' : ' strutture visibili');
      if (visible === 0) {
        msg += '. Nessuna struttura corrisponde ai filtri selezionati';
      }
    }
    statusEl.textContent = msg;
  }

  function applyFilters() {
    let visible = 0;
    cards.forEach(function (card) {
      let show = true;
      for (const [key, val] of Object.entries(active)) {
        if (val && card.dataset[key] !== val) show = false;
      }
      card.hidden = !show;
      if (show) visible++;
    });
    if (countEl) {
      countEl.textContent = visible + (visible === 1 ? ' struttura' : ' strutture');
    }
    if (emptyEl) {
      emptyEl.hidden = visible > 0;
    }
    syncFilterToggle();
    syncFilterStatus(visible);
  }

  filterBtns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      const filter = btn.dataset.filter;
      const value = btn.dataset.value;
      active[filter] = active[filter] === value ? null : value;
      syncButtons();
      syncUrl();
      applyFilters();
    });
  });

  if (clearBtn) {
    clearBtn.addEventListener('click', function () {
      for (const key of Object.keys(active)) active[key] = null;
      syncButtons();
      syncUrl();
      applyFilters();
      clearBtn.focus();
    });
  }

  parseUrl();
  syncButtons();
  applyFilters();

  if (activeCount() > 0 && window.lsFiltersPanel) {
    if (window.lsFiltersPanel.isMobile()) {
      window.lsFiltersPanel.open(false);
    }
  }
  }

  const gridEl = document.getElementById('structure-grid');
  if (gridEl && gridEl.getAttribute('data-src') && !gridEl.dataset.hydrated) {
    document.addEventListener('ls-catalog-ready', initFilters, { once: true });
    return;
  }
  initFilters();
})();
