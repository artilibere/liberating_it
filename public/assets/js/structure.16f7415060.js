(function () {
const mininav = document.querySelector('.ls-mininav');
if (!mininav) return;
const links = mininav.querySelectorAll('.ls-mininav__link');
const sections = [];
links.forEach(function (link) {
const id = link.getAttribute('href')?.slice(1);
if (id) {
const el = document.getElementById(id);
if (el) sections.push({ link, el });
}
});
if (!sections.length) return;
function setActive(id) {
links.forEach(function (link) {
const match = link.getAttribute('href') === '#' + id;
link.classList.toggle('ls-mininav__link--active', match);
if (match) {
link.setAttribute('aria-current', 'location');
} else {
link.removeAttribute('aria-current');
}
});
}
const observer = new IntersectionObserver(
function (entries) {
entries.forEach(function (entry) {
if (entry.isIntersecting) setActive(entry.target.id);
});
},
{
rootMargin: '-40% 0px -50% 0px',
threshold: 0,
}
);
sections.forEach(function (s) {
observer.observe(s.el);
});
})();
(function () {
function copyLink(button) {
var url = button.getAttribute("data-url");
if (!url) return;
var label = button.textContent;
var status = document.getElementById("ls-share-status");
function done() {
button.textContent = "Link copiato";
if (status) {
status.textContent = "Link copiato negli appunti";
}
window.setTimeout(function () {
button.textContent = label;
if (status) {
status.textContent = "";
}
}, 2000);
}
if (navigator.clipboard && navigator.clipboard.writeText) {
navigator.clipboard.writeText(url).then(done).catch(function () {
window.prompt("Copia il link:", url);
});
return;
}
window.prompt("Copia il link:", url);
}
document.querySelectorAll(".ls-share__copy").forEach(function (button) {
button.addEventListener("click", function () {
copyLink(button);
});
});
})();
