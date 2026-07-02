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
const hash = window.location.hash.replace(/^#/, '');
if (!hash) return;
const params = new URLSearchParams(hash);
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
const url = qs ? window.location.pathname + '#' + qs : window.location.pathname;
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
