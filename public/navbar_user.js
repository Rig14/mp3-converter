function update_navbar() {
    const user_info_container = document.getElementById('user-info');

    if (localStorage.getItem('user_data')) {
        // if user data is in local storage, then display user info in navbar
        const user_data = JSON.parse(localStorage.getItem('user_data'));
        user_info_container.innerHTML = `
            <div class="user-info">
                <a href=${'/user-profile?id=' + user_data.id}>
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
