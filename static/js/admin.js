document.addEventListener('DOMContentLoaded', () => {
    fetch('/me')
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(user => {
        if (user.type !== 'admin') {
            document.body.innerHTML = '<h2>Admins only!</h2><a href="/">Back to Home</a>';
            return;
        }

        const viewUsersBtn = document.getElementById('viewUsersBtn');
        const lookupUserBtn = document.getElementById('lookupUserBtn');
        const userIdInput = document.getElementById('userIdInput');
        const lookupResult = document.getElementById('lookupResult');
        const allUsersDiv = document.getElementById('allUsers');

        viewUsersBtn.addEventListener('click', () => {
            fetch('/admin/data')
            .then(res => res.json())
            .then(data => {
                let html = '<h3>All Users:</h3><ul>';
                data.users.forEach(user => {
                    html += `<li>ID: ${user.id}, Username: ${user.username}, Email: ${user.email}, Type: ${user.type}</li>`;
                });
                html += '</ul>';
                allUsersDiv.innerHTML = html;
                lookupResult.innerHTML = '';
            });
        });

        lookupUserBtn.addEventListener('click', () => {
            const userId = userIdInput.value.trim();
            if (!userId) {
                lookupResult.innerHTML = '<p style="color:red;">Please enter a user ID.</p>';
                return;
            }
            fetch(`/users/${userId}`)
            .then(res => {
                if (!res.ok) {
                    if (res.status === 404) {
                        throw new Error("User not found");
                    }
                    throw new Error("Error fetching user");
                }
                return res.json();
            })
            .then(data => {
                lookupResult.innerHTML = `<p>ID: ${data.id}, Username: ${data.username}, Email: ${data.email}, Type: ${data.type}</p>`;
            })
            .catch(err => {
                lookupResult.innerHTML = `<p style="color:red;">${err.message}</p>`;
            });
        });

        document.getElementById('backHomeBtn').addEventListener('click', () => {
            window.location.href = '/';
        });

    })
    .catch(() => {
        document.body.innerHTML = '<h2>You must be logged in as an admin to view this page.</h2><a href="/">Back to Home</a>';
    });
});
