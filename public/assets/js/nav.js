(function () {
  const menuBtn = document.querySelector('.ls-header__menu-btn');
  const drawer = document.getElementById('ls-nav-drawer');
  if (!menuBtn || !drawer) return;

  const panel = drawer.querySelector('.ls-drawer__panel');
  const closeBtn = drawer.querySelector('.ls-drawer__close');
  const backdrop = drawer.querySelector('.ls-drawer__backdrop');
  let lastFocus = null;

  function openDrawer() {
    lastFocus = document.activeElement;
    drawer.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    drawer.inert = false;
    panel.setAttribute('aria-modal', 'true');
    menuBtn.setAttribute('aria-expanded', 'true');
    menuBtn.setAttribute('aria-label', 'Chiudi menu');
    document.body.style.overflow = 'hidden';
    (closeBtn || panel.querySelector('a, button'))?.focus();
  }

  function closeDrawer() {
    drawer.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
    drawer.inert = true;
    panel.removeAttribute('aria-modal');
    menuBtn.setAttribute('aria-expanded', 'false');
    menuBtn.setAttribute('aria-label', 'Apri menu');
    document.body.style.overflow = '';
    if (lastFocus) lastFocus.focus();
  }

  menuBtn.addEventListener('click', function () {
    if (drawer.classList.contains('is-open')) closeDrawer();
    else openDrawer();
  });
  closeBtn?.addEventListener('click', closeDrawer);
  backdrop?.addEventListener('click', closeDrawer);

  panel.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeDrawer);
  });

  drawer.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeDrawer();
    if (e.key !== 'Tab' || !drawer.classList.contains('is-open')) return;

    const focusable = panel.querySelectorAll('a, button, [tabindex]:not([tabindex="-1"])');
    if (!focusable.length) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });

  const submenuItems = document.querySelectorAll('.ls-header__nav-item--has-submenu');
  const submenuControllers = [];

  function closeAllSubmenus() {
    submenuControllers.forEach(function (controller) {
      controller.close();
    });
  }

  submenuItems.forEach(function (item) {
    const submenuBtn = item.querySelector(':scope > button');
    const submenu = item.querySelector(':scope > .ls-header__submenu');
    if (!submenuBtn || !submenu) return;

    const submenuLinks = submenu.querySelectorAll('a');
    const controller = {
      close: function () {
        submenuBtn.setAttribute('aria-expanded', 'false');
        submenu.hidden = true;
      },
      open: function (focusLink) {
        submenuBtn.setAttribute('aria-expanded', 'true');
        submenu.hidden = false;
        if (focusLink) submenuLinks[0]?.focus();
      },
      contains: function (target) {
        return submenu.contains(target) || submenuBtn.contains(target);
      },
    };

    submenuBtn.addEventListener('click', function () {
      const open = submenuBtn.getAttribute('aria-expanded') === 'true';
      if (open) controller.close();
      else {
        closeAllSubmenus();
        controller.open(false);
      }
    });

    submenuBtn.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !submenu.hidden) {
        e.preventDefault();
        controller.close();
        submenuBtn.focus();
        return;
      }
      if ((e.key === 'ArrowDown' || e.key === 'Enter' || e.key === ' ') && submenu.hidden) {
        e.preventDefault();
        closeAllSubmenus();
        controller.open(true);
      }
    });

    submenuLinks.forEach(function (link, index) {
      link.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
          e.preventDefault();
          controller.close();
          submenuBtn.focus();
          return;
        }
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          submenuLinks[Math.min(index + 1, submenuLinks.length - 1)]?.focus();
        }
        if (e.key === 'ArrowUp') {
          e.preventDefault();
          if (index === 0) submenuBtn.focus();
          else submenuLinks[index - 1]?.focus();
        }
      });
    });

    submenuControllers.push(controller);
  });

  if (submenuControllers.length) {
    document.addEventListener('click', function (e) {
      const inside = submenuControllers.some(function (controller) {
        return controller.contains(e.target);
      });
      if (!inside) closeAllSubmenus();
    });
  }
})();
