async function render_blacklist() {
    const url = BACKEND_URL + '/api/blacklist';
    const token = localStorage.getItem('token');

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: token,
        },
    });

    if (response.status !== 200) {
        window.location.href = 'index.html';
    } else {
        const data = await response.json();
        const blacklist_container = document.getElementById(
            'blacklist-container'
        );
        // clear blacklist container
        blacklist_container.innerHTML = '';

        // add data to blacklist container
        data.items.forEach((item) => {
            const blacklist_item = document.createElement('li');
            blacklist_item.className = 'blacklist-item';
            blacklist_item.innerHTML = `
                <div class="blacklist-item-data">
                    <p class="blacklist-item-content-url">Content URL: ${item[1]}</p>
                    <p class="blacklist-item-date">Date added: ${item[2]}</p>
                </div>
                <button class="blacklist-item-delete" onclick="delete_from_blacklist(${item[0]})">Remove</button>
            `;
            blacklist_container.appendChild(blacklist_item);
        });
    }
}

async function add_to_blacklist() {
    const url = BACKEND_URL + '/api/blacklist';
    const token = localStorage.getItem('token');
    const blacklisted_url = document.getElementById('blacklisted-url').value;

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            Authorization: token,
        },
        body: JSON.stringify({ content_url: blacklisted_url }),
    });

    if (response.status !== 200) {
        render_message('Error adding item to blacklist.');
    } else {
        render_blacklist();
        render_message('Successfully added item to blacklist.');
    }
}

async function delete_from_blacklist(id) {
    const url = BACKEND_URL + '/api/blacklist';
    const token = localStorage.getItem('token');

    const response = await fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            Authorization: token,
        },
        body: JSON.stringify({ content_id: id }),
    });

    if (response.status !== 200) {
        render_message('Error deleting item from blacklist.');
    } else {
        render_blacklist();
        render_message('Successfully deleted item from blacklist.');
    }
}

function render_message(message) {
    const message_container = document.getElementById('message-container');
    message_container.innerHTML = message;
}

let USERS = [];

async function get_users() {
    const url = BACKEND_URL + '/api/users';

    const response = await fetch(url, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            Authorization: localStorage.getItem('token'),
        },
    });

    if (response.status !== 200) {
        window.location.href = 'index.html';
    } else {
        // render users on screen
        const data = await response.json();
        const users = data.users;
        USERS = users;
        render_users();
    }
}

function render_users() {
    const list = document.getElementById('user-list');

    list.innerHTML = '';
    USERS.forEach((user) => {
        // check if search input matches user
        const search_input = document.getElementById('user-name-search').value;
        if (search_input) {
            if (!user[1].includes(search_input)) {
                return;
            }
        }

        const user_container = document.createElement('li');
        user_container.style.display = 'flex';
        user_container.style.flexDirection = 'row';
        user_container.style.borderBottom = '1px solid black';
        user_container.className = 'user-container';
        user_container.innerHTML = `
            <div class="user-info user-info-admin-field">
                <a>
                    <img src="${BACKEND_URL + '/static/' + user[2]}">
                </a>
                <div class="user-data-field">
                    <h2>${user[1]}</h2>
                    <p>ID: ${user[0]}</p>
                </div>
            </div>
            <div class="user-managment-buttons">
                <button onclick="delete_history(${
                    user[0]
                })">Delete history</button>
                <button onclick="delete_account(${
                    user[0]
                })">Delete account</button>
            </div>
        `;
        list.appendChild(user_container);
    });
}

async function delete_history(id) {
    const url = BACKEND_URL + '/api/delete_history';
    const token = localStorage.getItem('token');

    const response = await fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            Authorization: token,
        },
        body: JSON.stringify({ user_id: id }),
    });

    if (response.status !== 200) {
        render_message('Error deleting history.');
    } else {
        render_message('Successfully deleted history for user with id ' + id);
    }
}

async function delete_account(id) {
    const url = BACKEND_URL + '/api/delete_account_id';
    const token = localStorage.getItem('token');

    const response = await fetch(url, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            Authorization: token,
        },
        body: JSON.stringify({ user_id: id }),
    });

    if (response.status !== 200) {
        render_message('Error deleting account.');
    } else {
        render_message('Successfully deleted account with id ' + id);
        get_users();
    }
}
