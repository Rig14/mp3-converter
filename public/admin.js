async function get_blackist() {
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
    }
}

get_blackist();
