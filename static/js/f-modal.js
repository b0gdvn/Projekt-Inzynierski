// Get the modal
var fModal = document.getElementById('filter-btn-modal');

// Get the <span> element that closes the modal
var fSpan = document.getElementsByClassName("f-close")[0];

// When the user clicks the button, open the modal 
function filterBtnClick() {
    fModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
fSpan.onclick = function() {
    fModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == fModal) {
        fModal.style.display = "none";
    }
}