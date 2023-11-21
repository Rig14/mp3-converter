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

        download_to_server(url);
    }
}

async function download_to_server(url) {
    const res = await fetch(BACKEND_URL + '/api/download', {
        method: 'POST',
        body: JSON.stringify({
            url,
        }),
        headers: { 'Content-Type': 'application/json' },
    });

    if (res.status === 200) {
        const data = await res.json();
        console.log(data);
        // got to backend / api / download ? identifier= data . identifier
        document.getElementById('form').innerHTML = `
            ${document.getElementById('form').innerHTML}
            <a href="${BACKEND_URL}/api/file?identifier=${data.identifier}">
                Download
        `;
    }
}
function displayFormError(message) {
    // display error message
    const error = document.getElementById('error-message');
    error.innerText = message;
}

async function create_user(email, password, password_confirm) {
    set_loading_animation();
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
        remove_loading_animation();
    } else {
        // if response http status code is 200, then redirect to home page
        // and set token in local storage
        const data = await response.json();
        localStorage.setItem('token', data.token);
        await locally_save_user_data();
        window.location.href = 'index.html';
    }
}

async function login_user(email, password) {
    set_loading_animation();
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
        remove_loading_animation();
    } else {
        // if response http status code is 200, then redirect to home page
        // and set token in local storage
        const data = await response.json();
        localStorage.setItem('token', data.token);
        await locally_save_user_data();
        window.location.href = 'index.html';
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
    window.location.href = 'index.html';
}

function set_loading_animation() {
    const button = document.getElementById('submit-button');
    button.style.display = 'none';

    const loading = document.getElementById('loading-animation');
    loading.style.display = 'block';
}

function remove_loading_animation() {
    const button = document.getElementById('submit-button');
    button.style.display = 'block';

    const loading = document.getElementById('loading-animation');
    loading.style.display = 'none';
}
