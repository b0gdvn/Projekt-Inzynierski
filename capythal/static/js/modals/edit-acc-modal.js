// Get the modal
var edAccModal = document.getElementsByClassName('modal')[1];

// Get the <span> element that closes the modal
var edAccSpan = document.getElementsByClassName("tr-close");

// When the user clicks the button, open the modal
function editAccBtnClick(i) {
    document.getElementsByClassName('modal')[i].style.display = "block";
}

// When the user clicks on <span> (x), close the modal
edAccSpan.onclick = function() {
    edAccModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    if (event.target == edAccModal) {
        edAccModal.style.display = "none";
    }
});