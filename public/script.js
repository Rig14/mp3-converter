function showPassword(fieldID) {
    // shows the password in plain text instead on dots
    const field = document.getElementById(fieldID);
    field.type = 'text';
}
function hidePassword(fieldID) {
    // hides the password and shows dots
    const field = document.getElementById(fieldID);
    field.type = 'password';
}

function processFormData(form_type) {
    // get form data from the fields in the form
    const form = document.getElementById('form');
    const formData = new FormData(form);

    if (form_type === 'login') {
        console.log('login form submitted. Data:');
        console.log(formData);
    } else if (form_type === 'sign-up') {
        console.log('sign-up form submitted. Data:');
        console.log(formData);
    } else if (form_type === 'youtube-convert') {
        console.log('youtube url and format submitted. Data:');
        console.log(formData);
    }
}

function displayFormError(message) {
    // display error message
    const error = document.getElementById('error-message');
    error.innerText = message;
}
