window.addEventListener("load", function () {
    var map = new google.maps.Map(document.getElementById('map'), {
        // center: {lat: 33.36754764961736, lng: 6.8516909761955125},
        center: {lat: 33.358905313975995, lng: 6.838954175207063},
        zoom: 15
    });
    
    // انشاء علامة (Marker) ديناميكية
    var marker = new google.maps.Marker({
        position: {lat: 33.358905313975995, lng: 6.838954175207063},
        map: map,
        title: 'Miknassa'
    });
    
    // تحديث موقع العلامة بشكل ديناميكي
    setInterval(function() {
        var newLat = marker.getPosition().lat() + 0.0001;
        var newLng = marker.getPosition().lng() + 0.0001;
        marker.setPosition({lat: newLat, lng: newLng});
    }, 1000);
});
