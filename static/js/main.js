function updateView() {
    fetch('/me')
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(user => {
        document.getElementById('authForms').style.display = 'none';
        document.getElementById('loggedInView').style.display = 'block';
        document.getElementById('welcomeText').textContent = 'Welcome, ' + user.username + '!';
        // Only update tokenDisplay if empty (to preserve token set on login)
        const tokenDisplay = document.getElementById('tokenDisplay');
        if (!tokenDisplay.textContent || tokenDisplay.textContent === 'Logged in as ' + user.type) {
            tokenDisplay.textContent = 'Logged in as ' + user.type;
        }
        document.getElementById('adminPageLink').style.display = user.type === 'admin' ? 'inline-block' : 'none';
    })
    .catch(() => {
        document.getElementById('authForms').style.display = 'block';
        document.getElementById('loggedInView').style.display = 'none';
        document.getElementById('welcomeText').textContent = 'Hello, Guest!';
        document.getElementById('tokenDisplay').textContent = '';
    });
}

document.getElementById('loginForm').addEventListener('submit', e => {
    e.preventDefault();
    const form = e.target;
    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: form.username.value,
            password: form.password.value
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.msg);
        if (data.access_token) {
            document.getElementById('tokenDisplay').textContent = data.access_token;
        }
        updateView();
    });
});

document.getElementById('registerForm').addEventListener('submit', e => {
    e.preventDefault();
    const form = e.target;
    const isAdmin = form.type.value === 'admin';
    fetch(isAdmin ? '/users/admin' : '/users/new', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            username: form.username.value,
            email: form.email.value,
            password: form.password.value
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.msg);
        form.reset();
    });
});

document.getElementById('logoutBtn').addEventListener('click', () => {
    fetch('/logout', { method: 'POST' })
    .then(() => updateView());
});

updateView();
