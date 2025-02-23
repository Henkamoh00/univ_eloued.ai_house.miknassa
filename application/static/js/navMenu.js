window.addEventListener('resize', function () {
    var menu = document.getElementById('menu');
    var menuIcon = document.getElementById('menuIcon');
    
    
    if (window.innerWidth <= 1100) {
        menu.style.visibility = 'hidden';
        menuIcon.style.display = 'block';
    } else {
        menuIcon.style.display = 'none';
        menu.style.visibility = 'visible';
    }
});

window.dispatchEvent(new Event('resize'));



function toggleMenu() {
    var menu = document.getElementById('menu');

    if (menu.style.visibility === 'visible') {
        menu.style.visibility = 'hidden';
    } else {
        menu.style.visibility = 'visible';
    }
}