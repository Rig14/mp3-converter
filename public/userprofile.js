function load_user_profile() {
    const user_data = JSON.parse(localStorage.getItem('user_data'));
    const user_profile_image = document.getElementById('user-profile-image');
    user_profile_image.src =
        BACKEND_URL + '/static/' + user_data.profile_picture;
    const user_profile_name = document.getElementById('user-profile-name');
    user_profile_name.value = user_data.name;
    const user_profile_motd = document.getElementById('user-profile-message');
    user_profile_motd.value = user_data.motd;
    const user_profile_email = document.getElementById('user-profile-email');
    user_profile_email.value = user_data.email;
}
load_user_profile();

async function change_user_data() {
    set_loading_animation();
    // send image
    const image_error = await upload_image();
    if (image_error) {
        set_error(image_error);
        remove_loading_animation();
        return;
    }

    const name = document.getElementById('user-profile-name').value;
    const motd = document.getElementById('user-profile-message').value;
    const email = document.getElementById('user-profile-email').value;
    const password = document.getElementById('user-profile-password').value;
    const token = localStorage.getItem('token');

    const url = BACKEND_URL + '/api/change_user_data';

    const data = {
        name: name,
        motd: motd,
        email: email,
        password: password,
    };

    const response = await fetch(url, {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
            Authorization: token,
        },
    });

    if (response.status != 200) {
        const data = await response.json();
        set_error(data.error);
        remove_loading_animation();
    } else {
        await locally_save_user_data();
        remove_loading_animation();
        window.location.reload();
    }
}

function set_error(message) {
    const error = document.getElementById('user-profile-error');
    error.innerHTML = message;
}

function process_image() {
    const image = document.getElementById('image-upload').files[0];
    const reader = new FileReader();
    // display the image file inside the img element with id=user-profile-image
    reader.onload = function (e) {
        const img = document.getElementById('user-profile-image');
        img.src = e.target.result;
    };
    reader.readAsDataURL(image);
}

async function upload_image() {
    const image = document.getElementById('image-upload').files[0];
    if (image === undefined) return false;

    const token = localStorage.getItem('token');

    const url = BACKEND_URL + '/api/change_profile_picture';

    const data = new FormData();
    data.append('image', image);

    const response = await fetch(url, {
        method: 'POST',
        body: data,
        headers: {
            Authorization: token,
        },
    });

    if (response.status != 200) {
        const data = await response.json();
        return data.error;
    }
    return false;
}

const upload_btn = document.getElementById('image-upload');
upload_btn.addEventListener('change', process_image);

async function load_user_history() {
    // get user history from backend
    const token = localStorage.getItem('token');
    const url = BACKEND_URL + '/api/get_history';
    const response = await fetch(url, {
        method: 'GET',
        headers: {
            Authorization: token,
        },
    });

    if (response.status != 200) {
        return;
    }

    const data = await response.json();
    const user_history = data.history;

    if (user_history.length === 0) {
        const user_history_container = document.getElementById('user-history');
        user_history_container.innerHTML = `
                <p>No history</p>
        `;
        return;
    }

    // content_title, content_url, content_format
    const history_elements = user_history.map((history) => {
        return `
            <div class="history-element">
                <div class="history-video-text">
                    <h2>${history.content_title}</h2>
                    <p>(Downloaded in "${history.content_format}" format)</p>
                </div>
                <p>
                    Content link:
                    <a href=${history.content_url}>
                        ${history.content_url}
                    </a>
                </p>
            </div>
        `;
    });

    // display the history elements in the user-history container
    const user_history_container = document.getElementById('user-history');
    user_history_container.innerHTML = history_elements.join('');
}
load_user_history();
