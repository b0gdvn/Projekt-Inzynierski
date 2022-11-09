// Get the modal
var addgModal = document.getElementById('add-goal-btn-modal');

// Get the <span> element that closes the modal
var addgSpan = document.getElementsByClassName("tr-close")[0];

// When the user clicks the button, open the modal 
function addGoalBtnClick() {
    addgModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
addgSpan.onclick = function() {
    addgModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    if (event.target == addgModal) {
        addgModal.style.display = "none";
    }
});