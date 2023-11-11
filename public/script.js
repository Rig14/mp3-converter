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
        login_user(formData.get('email'), formData.get('password'));
    } else if (form_type === 'sign-up') {
        create_user(
            formData.get('email'),
            formData.get('password'),
            formData.get('password-confirm')
        );
    }
}

function displayFormError(message) {
    // display error message
    const error = document.getElementById('error-message');
    error.innerText = message;
}

async function create_user(email, password, password_confirm) {
    const url = BACKEND_URL + '/api/signup';

    // send request to backend with user data
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            email,
            password,
            password_confirm,
        }),
        headers: { 'Content-Type': 'application/json' },
    });

    if (response.status !== 200) {
        // if response http status code is not 200, then display error message
        const data = await response.json();
        displayFormError(data.error);
    } else {
        // if response http status code is 200, then redirect to home page
        // and set token in local storage
        const data = await response.json();
        localStorage.setItem('token', data.token);
        window.location.href = '/';
    }
}

async function login_user(email, password) {
    const url = BACKEND_URL + '/api/login';

    // send request to backend with user data
    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            email,
            password,
        }),
        headers: { 'Content-Type': 'application/json' },
    });

    if (response.status !== 200) {
        // if response http status code is not 200, then display error message
        const data = await response.json();
        displayFormError(data.error);
    } else {
        // if response http status code is 200, then redirect to home page
        // and set token in local storage
        const data = await response.json();
        localStorage.setItem('token', data.token);
        window.location.href = '/';
    }
}
