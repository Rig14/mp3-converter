// const BACKEND_URL = 'http://193.40.156.222';

const BACKEND_URL = 'http://127.0.0.1:5000';

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
        const new_filename = formData.get('youtube-filename');
        const params = new URLSearchParams(window.location.search);
        const identifier = params.get('identifier');
        // localStorage.removeItem(identifier)

        window.location.href =
            BACKEND_URL +
            '/api/file?identifier=' +
            identifier +
            '&selected=0' +
            '&new_filename=' +
            new_filename;
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
        const new_filename = formData.get('soundcloud-filename');
        const params = new URLSearchParams(window.location.search);
        const identifier = params.get('identifier');
        // localStorage.removeItem(identifier)

        window.location.href =
            BACKEND_URL +
            '/api/file?identifier=' +
            identifier +
            '&selected=0' +
            '&new_filename=' +
            new_filename;
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
        const new_filename = formData.get('tiktok-filename');
        const params = new URLSearchParams(window.location.search);
        const identifier = params.get('identifier');
        // localStorage.removeItem(identifier)

        window.location.href =
            BACKEND_URL +
            '/api/file?identifier=' +
            identifier +
            '&selected=0' +
            '&new_filename=' +
            new_filename;
    } else if (form_type === 'playlist-convert') {
        const url = formData.get('playlist-link');
        //const regex = url.search(
        // Accepts playlist links from yt/sc only, some regular video or song links might get through
        //    String.raw`^((?:https?:)?\/\/)?((?:www|m)\.)?(?:youtube\.com\/playlist\?)([\w\-]+)(\S+)?$|^((?:https?:)?\/\/)?((?:www|m|on)\.)?soundcloud\.com\/([\w\-\.]+)\/sets\/(?!.*?(-|_){2})([\w\-]+)(\S+)?$|^((?:https?:)?\/\/)?((?:m|on)\.)soundcloud\.com\/(?!.*?(-|_){2})([\w\-]+)(\S+)?$`
        //);

        // New regex that searches for youtube single-video links
        const regex = url.search(
            String.raw`^((?:https?:)?\/\/)?((?:www|m)\.)?(?:youtube\.com\/watch\?v=?)([\w\-]+)(\S+)?$`
        );

        if (regex != 0 && url != '') {
            const media_type = formData.get('dropdown-content');
            window.location.href = `./loading.html?url=${url}&media_type=${media_type}&converted_from=${converted_from}`;
        } else {
            displayFormError(
                //'Youtube playlist url must contain: youtube.com/playlist?\nSoundcloud playlist url must contain: /sets/'
                'A valid playlist url must contain:  "youtube.com/playlist?" OR "/sets/" OR "on.soundcloud"'
            );
        }
    } else if (form_type === 'playlist-download') {
        const new_filename = formData.get('playlist-filename');
        const params = new URLSearchParams(window.location.search);
        const identifier = params.get('identifier');

        // get data from playlist selection form
        const selectionForm = document.getElementById('playlist-form');
        const selectionData = new FormData(selectionForm);
        selected_indexes = [];
        i = 0;
        // must be replaced by a for loop, currently selected items amount max 50
        while (i < 150) {
            content = selectionData.get('media' + i);
            if (typeof content === typeof 'a') {
                selected_indexes.push(content);
            }
            i += 1;
        }
        // selected media files indexes
        if (selected_indexes.length > 0) {
            const selected = selected_indexes.join('.');
            // edge case only 1 media selected
            if (selected_indexes.length == 1) {
                data = JSON.parse(localStorage.getItem(identifier));
                console.log(data);
                // replace playlist title with selected file name
                index = parseInt(selected_indexes[0]);
                const new_filename = data['files_data'][index]['file_name'];
                console.log(new_filename);

                window.location.href =
                    BACKEND_URL +
                    '/api/file?identifier=' +
                    identifier +
                    '&selected=' +
                    selected +
                    '&new_filename=' +
                    new_filename;
            } else {
                window.location.href =
                    BACKEND_URL +
                    '/api/file?identifier=' +
                    identifier +
                    '&selected=' +
                    selected +
                    '&new_filename=' +
                    new_filename;
            }
        }
    } else if (form_type === 'experimental-convert') {
        const url = formData.get('experimental-link');
        // Hardcoded to mp4, soundcloud etc might not work.
        const media_type = 'random';
        window.location.href = `./loading.html?url=${url}&media_type=${media_type}&converted_from=${converted_from}`;
    } else if (form_type === 'experimental-download') {
        const new_filename = formData.get('experimental-filename');
        const params = new URLSearchParams(window.location.search);
        const identifier = params.get('identifier');
        // localStorage.removeItem(identifier)

        window.location.href =
            BACKEND_URL +
            '/api/file?identifier=' +
            identifier +
            '&selected=0' +
            '&new_filename=' +
            new_filename;
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
    } else {
        localStorage.removeItem('user_data');
        localStorage.removeItem('token');
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
        // Display error message if the video/song doesn't exist.
        // Replace loading animation and converting text with error message.
        const loading_animation = document.getElementById(
            'loading-page-animation'
        );
        loading_animation.style.display = 'none';
        const converting_text = document.getElementById('converting-text');
        converting_text.style.display = 'none';
        const error = document.getElementById('converting-error-message');
        error.style.display = 'block';
        const data = await response.json();
        error.innerHTML = 'Error: ' + data.error;
    } else {
        const data = await response.json();
        const identifier = data.identifier;
        window.location.href =
            './' +
            converted_from +
            '-download.html?identifier=' +
            identifier +
            '&url=' +
            url +
            '&media_type=' +
            media_type;
    }
}

async function set_file_data() {
    const params = new URLSearchParams(window.location.search);
    const identifier = params.get('identifier');

    const url =
        BACKEND_URL +
        '/api/file?identifier=' +
        identifier +
        '&get_data_only=true';

    const response = await fetch(url, {
        method: 'GET',
    });

    if (response.status !== 200) {
        window.location.href = 'index.html';
    } else {
        const data = await response.json();
        const files_data = data.files_data;
        localStorage.setItem(identifier, JSON.stringify(data));
        // determine if converted content was a playlist or single file
        const len = Object.keys(files_data).length;

        // set single file data
        if (len == 1) {
            const single_media = data.files_data[0];
            const file_name = single_media.file_name;
            const file_extension = single_media.file_extension;
            const file_size = single_media.file_size;

            const file_name_field = document.getElementById(
                'filename-input-element'
            );
            file_name_field.value = file_name;

            const file_format_box = document.getElementById('file-format-box');
            file_format_box.innerText = file_extension;

            const file_size_box = document.getElementById('file-size');
            file_size_box.innerText = '(' + file_size + ')';

            // set playlist data
        } else if (len > 1) {
            const playlist_data = data.playlist_data;
            const file_name = playlist_data.title;
            const file_extension = playlist_data.file_extension;
            const file_size = playlist_data.file_size;

            const file_name_field = document.getElementById(
                'filename-input-element'
            );
            file_name_field.value = file_name;

            const file_format_box = document.getElementById('file-format-box');
            file_format_box.innerText = file_extension;

            const file_size_box = document.getElementById('file-size');
            file_size_box.innerText = '(' + file_size + ')';

            const media_dict = data.files_data;

            // fill custom selection form
            const custom_selection_container = document.getElementById(
                'custom-selection-box'
            );

            let text = '';
            const media_dict_keys = Object.keys(media_dict);
            for (let i = 0; i < media_dict_keys.length; i++) {
                const id = 'media' + i;
                text += `
                <div class="media">
                    <input type="checkbox" class="media-checkbox" id=${id} name=${id} value=${i} checked>
                    <label for=${id}>${media_dict[i]['file_name']}</label>
                </div>
            `;
            }
            custom_selection_container.innerHTML = text;
        }

        // get filename for add_user_history function
        const file_name_field = document.getElementById(
            'filename-input-element'
        );
        const converted_file = file_name_field.value;

        // send history to backend if user is logged in
        if (localStorage.getItem('token')) {
            const url = params.get('url');
            const media_type = params.get('media_type');
            add_user_history(converted_file, url, media_type);
        }
    }
}

async function add_user_history(content_title, content_url, content_format) {
    const url = BACKEND_URL + '/api/add_history';
    const token = localStorage.getItem('token');

    const res = await fetch(url, {
        method: 'POST',
        body: JSON.stringify({
            content_title,
            content_url,
            content_format,
        }),
        headers: {
            'Content-Type': 'application/json',
            Authorization: token,
        },
    });
}
