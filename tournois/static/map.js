var mapElem = document.getElementById('map')
var coords = [parseFloat(mapElem.getAttribute("start-lattitude").replace(",", ".")), parseFloat(mapElem.getAttribute("start-longitude").replace(",", "."))]
var zoom = parseFloat(mapElem.getAttribute("zoom").replace(",", "."))

var map = L.map('map').setView(coords, zoom);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

if (mapElem.getAttribute("start-point")) {
    var marker = L.marker(coords).addTo(map);
}
else {
    var marker = null
}