function checkFormat(fieldName) {
    var value = document.getElementById(fieldName).value;
    var errorElement = document.getElementById(fieldName + 'Error');
    var errorMessage = '';

    if (fieldName === 'username' && !/^[a-zA-Z0-9_]+$/.test(value)) {
        errorMessage = 'Username must be alphanumeric and underscores only';
    } else if (fieldName === 'birthdate') {
        try {
            var date = new Date(value);
            if (isNaN(date.getTime())) {
                errorMessage = 'Invalid date format';
            }
        } catch (error) {
            errorMessage = 'Invalid date format';
        }
    } else if (fieldName === 'email' && (!value.includes('@') || !value.includes('.'))) {
        errorMessage = 'Invalid email format';
    }

    errorElement.textContent = errorMessage;
}

function checkPassword() {
    var username = document.getElementById('username').value;
    var birthdate = document.getElementById('birthdate').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

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
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
