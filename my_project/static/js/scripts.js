document.addEventListener('DOMContentLoaded', function() {
    const usernameField = document.getElementById('username');
    const birthdateField = document.getElementById('birthdate');
    const emailField = document.getElementById('email');
    const usernameError = document.getElementById('usernameError');
    const birthdateError = document.getElementById('birthdateError');
    const emailError = document.getElementById('emailError');

    const passwordForm = document.getElementById('passwordForm');

    passwordForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        const username = usernameField.value.trim();
        const birthdate = birthdateField.value.trim();
        const email = emailField.value.trim();

        fetch('/check_format', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username: username, birthdate: birthdate, email: email })
        })
        .then(response => response.json())
        .then(data => {
            if (data.username) {
                usernameError.textContent = data.username;
            } else {
                usernameError.textContent = '';
                if (!data.birthdate && !data.email) {
                    // If username format is valid and no other format errors, proceed to check password strength
                    checkPassword(username, birthdate, email);
                }
            }

            birthdateError.textContent = data.birthdate || '';
            emailError.textContent = data.email || '';
        })
        .catch(error => console.error('Error:', error));
    });
});

function checkPassword(username, birthdate, email) {
    const password = document.getElementById('password').value;

    fetch('/check_password_strength', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            birthdate: birthdate,
            email: email,
            password: password
        })
    })
    .then(response => response.json())
    .then(data => {
        var passwordStrength = document.getElementById('passwordStrength');
        if (data.weak) {
            passwordStrength.innerHTML = '<p>Password missing criteria: ' + data.missingCriteria.join(", ") + '</p>';
            passwordStrength.innerHTML += '<p>Suggested strong password: ' + data.suggestedPassword + '</p>';
            if (data.passwordFoundInCommon) {
                passwordStrength.innerHTML += '<p>Password was found in a common list</p>';
            }
        } else {
            passwordStrength.innerHTML = '<p>Password meets all criteria</p>';
        }
        passwordStrength.innerHTML += '<p>Password score: ' + data.score + '/7</p>';
        passwordStrength.innerHTML += `<p>Estimated cracking time: ${data.crackingTime}</p>`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
