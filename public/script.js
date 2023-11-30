const BACKEND_URL = 'http://193.40.156.222';

//const BACKEND_URL = 'http://127.0.0.1:5000';

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
    const converted_from = form_type.split('-')[0];
    if (form_type === 'youtube-convert') {
        const url = formData.get('youtube-link');
        // Accepts all https combinations, youtu.be and m.youtube
        // Certain invalid characters in url might cause false-positive
        const regex = url.search(
            // less strict regex: String.raw`^((?:https?:)?\/\/)?((?:www|m)\.)?(?:youtube\.com\/watch\?v=|youtu\.be)`
            String.raw`^((?:https?:)?\/\/)?((?:www|m)\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/?)([\w\-]+)(\S+)?$`
        );
        if (regex === 0) {
            const media_type = formData.get('dropdown-content');
            window.location.href = `./loading.html?url=${url}&media_type=${media_type}&converted_from=${converted_from}`;
        } else {
            displayFormError('Please enter a valid Youtube url');
        }
    } else if (form_type === 'youtube-download') {
        file_name = formData.get('youtube-filename');
        const params = new URLSearchParams(window.location.search);

        window.location.href =
            BACKEND_URL +
            '/api/file?identifier=' +
            params.get('identifier') +
            '&file_name=' +
            file_name;
    } else if (form_type === 'soundcloud-convert') {
        const url = formData.get('soundcloud-link');
        const regex = url.search(
            // Desktop browser: www.soundcloud    Mobile browser: m.soundcloud    Mobile app: on.soundcloud
            // negative lookahead contains discover|feed|you because user might forget to open the song directly and copy only the discover page url
            // less strict regex: String.raw`^((?:https?:)?\/\/)?((?:www|m|on)\.)?soundcloud\.com\/(?!discover|feed|you)`
            String.raw`^((?:https?:)?\/\/)?((?:www|m|on)\.)?soundcloud\.com\/(?!discover|feed|you)(?!.*?(-|_){2})([\w\-]+)(\S+)?$`
        );
        if (regex === 0) {
            const media_type = formData.get('dropdown-content');
            window.location.href = `./loading.html?url=${url}&media_type=${media_type}&converted_from=${converted_from}`;
        } else {
            displayFormError('Please enter a valid Soundcloud url');
        }
    } else if (form_type === 'soundcloud-download') {
        const params = new URLSearchParams(window.location.search);

        window.location.href =
            BACKEND_URL + '/api/file?identifier=' + params.get('identifier');
    } else if (form_type === 'tiktok-convert') {
        const url = formData.get('tiktok-link');
        const regex = url.search(
            // this link causes problems for some reason - in regex (fixed) and in backend: https://www.tiktok.com/@aestetic._.paper/video/7302525927177620768
            // 2 main regex parts:  url copied from mobile app containing "vm.tiktok"   |   url copied directly from a browser that must contain "/video/"
            String.raw`^((?:https?:)?\/\/)?((?:www)\.)?tiktok\.com\/([\w\-@_\.]+)/video/(?!.*?(-|_){2})([\w\-@]+)(\S+)?$|^((?:https?:)?\/\/)?((?:vm)\.)?tiktok\.com\/(?!.*?(-|_){2})([\w\-@]+)(\S+)?$`
        );
        if (regex === 0) {
            const media_type = formData.get('dropdown-content');
            const convert_from = form_type;
            window.location.href = `./loading.html?url=${url}&media_type=${media_type}&converted_from=${converted_from}`;
        } else {
            displayFormError('Please enter a valid Tiktok url');
        }
    } else if (form_type === 'tiktok-download') {
        const params = new URLSearchParams(window.location.search);

        window.location.href =
            BACKEND_URL + '/api/file?identifier=' + params.get('identifier');
    } else if (form_type === 'playlist-convert') {
        const url = formData.get('playlist-link');
        const regex = url.search(
            // Accepts playlist links from yt/sc only, some regular video or song links might get through
            String.raw`^((?:https?:)?\/\/)?((?:www|m)\.)?(?:youtube\.com\/playlist\?)([\w\-]+)(\S+)?$|^((?:https?:)?\/\/)?((?:www|m|on)\.)?soundcloud\.com\/([\w\-\.]+)\/sets\/(?!.*?(-|_){2})([\w\-]+)(\S+)?$|^((?:https?:)?\/\/)?((?:m|on)\.)soundcloud\.com\/(?!.*?(-|_){2})([\w\-]+)(\S+)?$`
        );
        if (regex === 0) {
            const media_type = formData.get('dropdown-content');
            window.location.href = `./loading.html?url=${url}&media_type=${media_type}&converted_from=${converted_from}`;
        } else {
            displayFormError(
                //'Youtube playlist url must contain: youtube.com/playlist?\nSoundcloud playlist url must contain: /sets/'
                'A valid playlist url must contain:  "youtube.com/playlist?" OR "/sets/" OR "on.soundcloud"'
            );
        }
    } else if (form_type === 'playlist-download') {
        const params = new URLSearchParams(window.location.search);

        window.location.href =
            BACKEND_URL + '/api/file?identifier=' + params.get('identifier');
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

async function on_loading_page() {
    const params = new URLSearchParams(window.location.search);
    const url = params.get('url');
    const media_type = params.get('media_type');
    const converted_from = params.get('converted_from');

    const request_url = BACKEND_URL + '/api/download';

    const response = await fetch(request_url, {
        body: JSON.stringify({
            url,
            format: media_type,
        }),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    });

    if (response.status !== 200) {
        window.location.href = 'index.html';
    } else {
        const data = await response.json();
        const identifier = data.identifier;
        if (converted_from === 'playlist') {
            window.location.href =
                './youtube-download.html?identifier=' + identifier;
        } else {
            window.location.href =
                './' +
                converted_from +
                '-download.html?identifier=' +
                identifier;
        }
    }
}

async function set_file_data() {
    const params = new URLSearchParams(window.location.search);
    const identifier = params.get('identifier');

    const url =
        BACKEND_URL +
        '/api/file?identifier=' +
        identifier +
        '&get_name_only=true';

    const response = await fetch(url, {
        method: 'GET',
    });

    if (response.status !== 200) {
        window.location.href = 'index.html';
    } else {
        const data = await response.json();
        const file_name = data.file_name;
        const file_extention = data.file_extention;
        const file_size = data.file_size;

        const file_name_field = document.getElementById(
            'filename-input-element'
        );
        file_name_field.value = file_name;

        const file_format_box = document.getElementById('file-format-box');
        file_format_box.innerText = file_extention;

        const file_size_box = document.getElementById('file-size');
        file_size_box.innerText = '(' + file_size + ')';
    }
}
