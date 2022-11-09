// Get the modal
var addAccModal = document.getElementById('add-acc-btn-modal');

// Get the <span> element that closes the modal
var addAccSpan = document.getElementsByClassName("tr-close")[0];

// When the user clicks the button, open the modal 
function addAccBtnClick() {
    addAccModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
addAccSpan.onclick = function() {
    addAccModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    if (event.target == addAccModal) {
        addAccModal.style.display = "none";
    }
});