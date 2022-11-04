// Get the modal
var Modal = document.getElementById('add-tr-btn-modal');

// Get the <span> element that closes the modal
var Span = document.getElementsByClassName("tr-close")[0];

// When the user clicks the button, open the modal 
function AddTrBtnClick() {
    Modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
Span.onclick = function() {
    Modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == Modal) {
        Modal.style.display = "none";
    }
}