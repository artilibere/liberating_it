(function () {
  var grid = document.getElementById("structure-grid");
  if (!grid || !grid.getAttribute("data-src")) return;

  function escapeHtml(text) {
    return String(text)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/"/g, "&quot;");
  }

  function assetPath(path) {
    if (!path) return "";
    return path.charAt(0) === "/" ? path : "/" + path;
  }

  function structureUrl(slug) {
    return "/structures/" + slug + "/";
  }

  function renderCard(item, defaultIcon) {
    var icon = assetPath(item.icon || defaultIcon);
    var url = assetPath(item.url || structureUrl(item.slug));
    var diffUrl = "/difficolta/" + item.difficolta_slug + "/";
    var durUrl = "/durata/" + item.durata_slug + "/";
    return (
      '<article class="ls-card ls-card--interactive" aria-labelledby="card-' +
      escapeHtml(item.slug) +
      '" data-slug="' +
      escapeHtml(item.slug) +
      '" data-difficolta="' +
      escapeHtml(item.difficolta_slug) +
      '" data-complessita="' +
      escapeHtml(item.complessita_slug) +
      '" data-durata="' +
      escapeHtml(item.durata_slug) +
      '" data-fase="' +
      escapeHtml(item.fase_slug) +
      '">' +
      '<div class="ls-card__header">' +
      '<img class="ls-card__icon" src="' +
      escapeHtml(icon) +
      '" alt="" width="48" height="72" loading="lazy" decoding="async" fetchpriority="low" aria-hidden="true">' +
      '<h3 class="ls-card__title" id="card-' +
      escapeHtml(item.slug) +
      '"><a href="' +
      escapeHtml(url) +
      '">' +
      escapeHtml(item.title) +
      "</a></h3>" +
      "</div>" +
      '<p class="ls-card__brief">' +
      escapeHtml(item.brief) +
      "</p>" +
      '<div class="ls-chips ls-card__chips">' +
      '<a href="' +
      escapeHtml(assetPath(diffUrl)) +
      '" class="ls-chip">' +
      escapeHtml(item.difficolta) +
      "</a>" +
      '<a href="' +
      escapeHtml(assetPath(durUrl)) +
      '" class="ls-chip">' +
      escapeHtml(item.durata) +
      "</a>" +
      "</div>" +
      "</article>"
    );
  }

  fetch(grid.getAttribute("data-src"))
    .then(function (response) {
      if (!response.ok) throw new Error("catalog fetch failed");
      return response.json();
    })
    .then(function (data) {
      var items = data.structures || [];
      grid.innerHTML = items
        .map(function (item) {
          return renderCard(item, data.default_icon);
        })
        .join("");
      grid.dataset.hydrated = "true";
      document.dispatchEvent(new CustomEvent("ls-catalog-ready"));
    })
    .catch(function () {
      grid.innerHTML =
        '<p class="ls-catalog__error" role="alert">Impossibile caricare il catalogo. <a href="/structures/">Ricarica la pagina</a>.</p>';
    });
})();
