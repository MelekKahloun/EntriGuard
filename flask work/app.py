from flask import Flask, request, jsonify
import string
import random
import re
from datetime import datetime
from collections import Counter
from utils import generate_strong_password, suggest_strong_password,check_format,check_password_strength
    


app = Flask(__name__)

@app.route('/check_password_strength', methods=['POST'])
def check_password_strength():
    data = request.json
    password = data['password']
    username = data['username']
    birthdate = data['birthdate']
    email = data['email']

    # Implement the check_password_strength function here
    # (Copy the function from your backend code)
    
    
    
    
    
    


    missing_criteria, score = check_password_strength(password, username, birthdate, email)
    total_criteria = 10  # Adding the additional format check

    if missing_criteria:
        suggested_password = suggest_strong_password()
        return jsonify({'weak': True, 'missingCriteria': missing_criteria, 'suggestedPassword': suggested_password, 'score': score})
    else:
        return jsonify({'weak': False, 'score': score})

@app.route('/')
def index():
    return '''
    <html>
    <body>
        <h1>Password Strength Checker</h1>
        <form id="passwordForm">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br>
            <label for="birthdate">Birthdate (YYYY-MM-DD):</label>
            <input type="text" id="birthdate" name="birthdate" pattern="\d{4}-\d{2}-\d{2}" required><br>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br>
            <button type="button" onclick="checkPassword()">Check Password</button>
        </form>
        <div id="passwordStrength"></div>
        <script>
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
                    } else {
                        passwordStrength.innerHTML = '<p>Password meets all criteria</p>';
                    }
                    passwordStrength.innerHTML += '<p>Password score: ' + data.score + '/5</p>';
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            }
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)

