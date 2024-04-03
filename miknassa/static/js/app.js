

var map = L.map('map').setView([33.358905313975995, 6.838954175207063], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: ''
}).addTo(map);

L.marker([33.358905313975995, 6.838954175207063]).addTo(map);
    // .bindPopup('A pretty CSS popup.<br> Easily customizable.')
    // .openPopup();

// setInterval(function () {
//     var newLat = L.marker.getLatLng().lat + 0.01;
//     var newLng = L.marker.getLatLng().lng + 0.01;
//     L.marker.setLatLng([newLat, newLng]);
// }, 1000);