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
