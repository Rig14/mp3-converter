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

async function get_users() {}
