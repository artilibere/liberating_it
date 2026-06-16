(function () {
  const MOBILE_MQ = '(max-width: 899px)';

  function els() {
    return {
      toggle: document.querySelector('.ls-filters-toggle'),
      panel: document.querySelector('.ls-filters'),
    };
  }

  function isMobile() {
    return window.matchMedia(MOBILE_MQ).matches;
  }

  function syncInert() {
    const { panel } = els();
    if (!panel) return;
    panel.inert = isMobile() && !panel.classList.contains('is-open');
  }

  function open(focusFirst) {
    const { toggle, panel } = els();
    if (!toggle || !panel) return;
    panel.classList.add('is-open');
    toggle.setAttribute('aria-expanded', 'true');
    syncInert();
    if (focusFirst) {
      const first = panel.querySelector('.ls-chip--filter, .ls-filters__clear');
      first?.focus();
    }
  }

  function close() {
    const { toggle, panel } = els();
    if (!toggle || !panel) return;
    panel.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
    syncInert();
  }

  function togglePanel() {
    const { panel } = els();
    if (!panel) return;
    if (panel.classList.contains('is-open')) close();
    else open(true);
  }

  function init() {
    const { toggle } = els();
    if (!toggle) return;

    toggle.addEventListener('click', togglePanel);

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') return;
      const { panel, toggle: btn } = els();
      if (!panel || !btn || !panel.classList.contains('is-open')) return;
      if (!isMobile()) return;
      e.preventDefault();
      close();
      btn.focus();
    });

    window.addEventListener('resize', syncInert);
    syncInert();
  }

  window.lsFiltersPanel = { open, close, toggle: togglePanel, syncInert, isMobile };
  init();
})();
