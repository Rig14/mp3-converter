function update_navbar() {
    const user_info_container = document.getElementById('user-info');

    if (localStorage.getItem('user_data')) {
        locally_save_user_data();
        // if user data is in local storage, then display user info in navbar
        const user_data = JSON.parse(localStorage.getItem('user_data'));
        user_info_container.innerHTML = `
            <div class="user-info">
                <a href='/user-profile'>
                    <img src=
                    ${BACKEND_URL + '/static/' + user_data.profile_picture}>
                </a>
                <div>
                    <h2>${user_data.name}</h2>
                    <p>${user_data.motd}</p>
                </div>
                <button onclick="logout()"><img src="./resources/logout.png"></button>
            </div>
        `;
    }
}

update_navbar();

// will run if user is admin
if (
    localStorage.getItem('user_data') &&
    JSON.parse(localStorage.getItem('user_data')).admin === 1
) {
    console.log('create');
    // a floating box in the right bottom corner of the screen
    const floater = document.createElement('div');
    floater.style.position = 'fixed';
    floater.style.display = 'flex';
    floater.style.flexDirection = 'column';
    floater.style.bottom = '0';
    floater.style.right = '0';
    floater.style.border = '2px dashed orange';

    floater.innerHTML = `
            <a class="admin-link" href="./admin-blacklist.html">Blacklist</a>
            <a class="admin-link" href="./admin-users-overview.html">Users</a>
        `;

    document.body.appendChild(floater);
}
