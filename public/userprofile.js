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
