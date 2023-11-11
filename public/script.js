const BACKEND_URL = 'http://localhost:5000';

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
        return {};
    } else if (form_type === 'sign-up') {
        url = BACKEND_URL + '/api/signup';
        fetch(url, {
            method: 'POST',
            body: JSON.stringify({
                email: formData.get('email'),
                password: formData.get('password'),
                password_confirm: formData.get('password-confirm'),
            }),
            headers: { 'Content-Type': 'application/json' },
        }).then((response) => {
            if (response.status === 200) {
                window.location.href = '/login';
            } else {
                response.json().then((data) => {
                    displayFormError(data.error);
                });
            }
        });
    }
}

function displayFormError(message) {
    // display error message
    const error = document.getElementById('error-message');
    error.innerText = message;
}
