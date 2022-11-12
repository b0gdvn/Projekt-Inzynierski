document.getElementById("nav-toggler").addEventListener("click", open_close);
document.getElementById("exit-nav").addEventListener("click", open_close);

var menuState = 0 // close
function open_close() {
if(menuState === 0){
    menuState = 1;
    document.getElementById("exit-nav").style.width = "100%";
    document.getElementById("exit-nav").style.opacity = "0.3";
    document.getElementById("navbar").style.width = "28rem";
    document.getElementById("navbar").style.opacity = "1";
}
else {
    menuState = 0;
    document.getElementById("exit-nav").style.width = "0";
    document.getElementById("exit-nav").style.opacity = "0";
    document.getElementById("navbar").style.width = "0";
    document.getElementById("navbar").style.opacity = "0";
}
}