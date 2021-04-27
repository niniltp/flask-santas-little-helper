
document.getElementById("nav-toggle").addEventListener("click", toggleNav);
function toggleNav() {
    
    var nav = document.getElementById("nav-menu");
    var className = nav.getAttribute("class");

    if(className == "navbar-menu is-active") {
        nav.className = "navbar-menu";
    } else {
        nav.className = "navbar-menu is-active"
    }
}

