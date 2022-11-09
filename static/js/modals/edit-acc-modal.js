// Get the modal
var edAccModal = document.getElementById('edit-acc-btn-modal');

// Get the <span> element that closes the modal
var edAccSpan = document.getElementsByClassName("tr-close")[1];

// When the user clicks the button, open the modal 
function editAccBtnClick() {
    edAccModal.style.display = "block";
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

document.getElementById("radio-income").addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById("tr-income").style.display = "block";
        document.getElementById("tr-expense").style.display = "none";
        document.getElementById("tr-transfer").style.display = "none";
    }
})

document.getElementById("radio-expense").addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById("tr-income").style.display = "none";
        document.getElementById("tr-expense").style.display = "block";
        document.getElementById("tr-transfer").style.display = "none";
    }
})

document.getElementById("radio-transfer").addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById("tr-income").style.display = "none";
        document.getElementById("tr-expense").style.display = "none";
        document.getElementById("tr-transfer").style.display = "block";
    }
})