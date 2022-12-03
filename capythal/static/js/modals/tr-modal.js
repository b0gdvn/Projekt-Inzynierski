document.getElementById("radio-income").addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById("exp-form").reset();
        document.getElementById("transf-form").reset();
        document.getElementById("tr-income").style.display = "block";
        document.getElementById("tr-expense").style.display = "none";
        document.getElementById("tr-transfer").style.display = "none";
    }
})

document.getElementById("radio-expense").addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById("inc-form").reset();
        document.getElementById("transf-form").reset();
        document.getElementById("tr-income").style.display = "none";
        document.getElementById("tr-expense").style.display = "block";
        document.getElementById("tr-transfer").style.display = "none";
    }
})

document.getElementById("radio-transfer").addEventListener('change', (event) => {
    if (event.currentTarget.checked) {
        document.getElementById("inc-form").reset();
        document.getElementById("exp-form").reset();
        document.getElementById("tr-income").style.display = "none";
        document.getElementById("tr-expense").style.display = "none";
        document.getElementById("tr-transfer").style.display = "block";
    }
})