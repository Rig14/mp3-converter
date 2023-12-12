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
        blacklist_container.innerHTML = data;
    }
}

render_blacklist();

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
        window.location.href = 'index.html';
    } else {
        const data = await response.json();
        render_blacklist();
        render_message('Successfully added item to blacklist.');
    }
}

function render_message(message) {
    const message_container = document.getElementById('message-container');
    message_container.innerHTML = message;
}
