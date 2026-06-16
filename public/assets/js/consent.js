(function () {
  var STORAGE_KEY = "ls_cookie_consent";
  var banner = document.getElementById("ls-cookie-consent");
  if (!banner) return;

  var primaryBtn = banner.querySelector('[data-consent="granted"]');

  function readChoice() {
    try {
      return localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      return null;
    }
  }

  function storeChoice(value) {
    try {
      localStorage.setItem(STORAGE_KEY, value);
    } catch (e) {}
  }

  function pushConsentUpdate(granted) {
    window.dataLayer = window.dataLayer || [];
    function gtag() {
      dataLayer.push(arguments);
    }
    if (granted) {
      gtag("consent", "update", {
        ad_storage: "granted",
        ad_user_data: "granted",
        ad_personalization: "granted",
        analytics_storage: "granted",
        functionality_storage: "granted",
        personalization_storage: "granted",
      });
      if (typeof window.lsLoadGTM === "function") {
        window.lsLoadGTM();
      }
    }
  }

  function syncLayout() {
    var visible = !banner.hidden;
    document.body.classList.toggle("ls-cookie-visible", visible);
    if (visible) {
      document.body.style.setProperty("--ls-cookie-consent-height", banner.offsetHeight + "px");
    } else {
      document.body.style.removeProperty("--ls-cookie-consent-height");
    }
  }

  function hideBanner() {
    banner.hidden = true;
    banner.setAttribute("aria-hidden", "true");
    syncLayout();
  }

  function showBanner(focusPrimary) {
    banner.hidden = false;
    banner.removeAttribute("aria-hidden");
    syncLayout();
    if (focusPrimary !== false && primaryBtn) {
      primaryBtn.focus({ preventScroll: true });
    }
  }

  function applyChoice(value) {
    storeChoice(value);
    if (value === "granted") {
      pushConsentUpdate(true);
    }
    hideBanner();
  }

  function openPreferences() {
    showBanner(true);
  }

  if (typeof ResizeObserver !== "undefined") {
    var observer = new ResizeObserver(function () {
      if (!banner.hidden) {
        syncLayout();
      }
    });
    observer.observe(banner);
  } else {
    window.addEventListener("resize", function () {
      if (!banner.hidden) {
        syncLayout();
      }
    });
  }

  document.querySelectorAll('[data-action="cookie-preferences"]').forEach(function (button) {
    button.addEventListener("click", openPreferences);
  });

  var existing = readChoice();
  if (existing) {
    hideBanner();
  } else {
    showBanner(true);
  }

  banner.querySelectorAll("[data-consent]").forEach(function (button) {
    button.addEventListener("click", function () {
      applyChoice(button.getAttribute("data-consent") || "denied");
    });
  });
})();
