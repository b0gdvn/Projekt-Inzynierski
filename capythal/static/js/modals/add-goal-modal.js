// Get the modal
var addGoalModal = document.getElementById('add-goal-btn-modal');

// Get the <span> element that closes the modal
var addGoalSpan = document.getElementsByClassName("tr-close")[0];

// When the user clicks the button, open the modal 
function addGoalBtnClick() {
    addGoalModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
addGoalSpan.onclick = function() {
    addGoalModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    if (event.target == addGoalModal) {
        addGoalModal.style.display = "none";
    }
});