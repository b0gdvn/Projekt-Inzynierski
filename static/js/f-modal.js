// Get the modal
var fModal = document.getElementById('filter-btn-modal');

// Get the <span> element that closes the modal
var fSpan = document.getElementsByClassName("tr-close")[1];

// When the user clicks the button, open the modal 
function filterBtnClick() {
    fModal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
fSpan.onclick = function() {
    fModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
    if (event.target == fModal) {
        fModal.style.display = "none";
    }
});

function validateFilterForm() {
    var minAmount = parseFloat(document.forms["filter"]["tr_amount_min"].value);
    var maxAmount = parseFloat(document.forms["filter"]["tr_amount_max"].value);

    if (minAmount >= maxAmount && minAmount!=0 && maxAmount!=0) {
        alert("Minimalna wartość transakcji powinna być mniejsza niż maksymalna");
        return false;
    }
  }