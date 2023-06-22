// Check if there is an error field and apply CSS class to highlight it
var errorField = "{{ error_field }}";
if (errorField) {
    var inputField = document.getElementById(errorField);
    inputField.classList.add("error-input");
}
    
function goBack() {
    window.history.back();
}