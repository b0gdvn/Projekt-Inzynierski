// Get the modal
var edGoalModal = document.getElementById('edit-goal-btn-modal');

// Get the <span> element that closes the modal
var edGoalSpan = document.getElementsByClassName("tr-close")[1];

// When the user clicks the button, open the modal 
function editGoalBtnClick() {
    edGoalModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
edGoalSpan.onclick = function() {
    edGoalModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    if (event.target == edGoalModal) {
        edGoalModal.style.display = "none";
    }
});