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
