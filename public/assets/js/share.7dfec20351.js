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
