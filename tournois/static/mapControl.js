/*
This file is the control for superuser on the editMatch page
must be place after an include MapModule
*/

var longitudeField = document.getElementById('id_Longitude')
var lattitudeField = document.getElementById('id_Lattitude')

function onMapClick(e) {
    longitudeField.value = e.latlng["lng"]
    lattitudeField.value = e.latlng["lat"]
    if (marker == null){
        marker= L.marker(e.latlng).addTo(map);
    }
    else {
        marker.setLatLng(e.latlng)
    }
}

function LongitudeChange(e) {
    if (marker == null) {
        marker = L.marker(map.getCenter()).addTo(map)
    }
    latlng = marker.getLatLng()
    latlng["lng"] = parseFloat(longitudeField.value.replace(",", "."))
    marker.setLatLng(latlng)
    if (!map.getBounds().contains(latlng)) {
        map.panTo(latlng)
    }
    console.log(latlng)
}
longitudeField.addEventListener("change", LongitudeChange)

function LattitudeChange(e) {
    if (marker == null) {
        marker = L.marker(map.getCenter()).addTo(map)
    }
    latlng = marker.getLatLng()
    latlng["lat"] = parseFloat(lattitudeField.value.replace(",", "."))
    marker.setLatLng(latlng)
    if (!map.getBounds().contains(latlng)) {
        map.panTo(latlng)
    }
    console.log(latlng)
}
lattitudeField.addEventListener("change", LattitudeChange);

map.on('click', onMapClick);