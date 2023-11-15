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
    } else if (form_type === 'youtube-convert') {
        const url = formData.get('youtube-link');
        const media_type = formData.get('dropdown-content');
        youtube_convert(url, media_type);
    }
}

async function youtube_convert(url, format_type) {
    request_url = BACKEND_URL + '/api/download';

    const result = await fetch(request_url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            url,
            platform: 'youtube',
            format: format_type,
        }),
    });

    if (result.status !== 200) {
        // if response http status code is not 200, then display error message
        const data = await result.json();
        displayFormError(data.error);
    } else {
        const data = await result.json();

        window.location.href =
            BACKEND_URL +
            '/api/file?identifier=' +
            data.identifier +
            '&platform=youtube';
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
        await locally_save_user_data();
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
        await locally_save_user_data();
        window.location.href = '/';
    }
}

async function locally_save_user_data() {
    // fetch user data from backend and save it in local storage
    const url = BACKEND_URL + '/api/user_data';
    const token = localStorage.getItem('token');

    // send request to backend with user data
    const response = await fetch(url, {
        method: 'GET',
        headers: { Authorization: token },
    });

    if (response.status === 200) {
        // if response http status code is 200, then save user data in local storage
        const data = await response.json();
        localStorage.setItem('user_data', JSON.stringify(data));
    }
}

function logout() {
    // delete token from local storage and user data
    localStorage.removeItem('token');
    localStorage.removeItem('user_data');

    // redirect to home page
    window.location.href = '/';
}
