from flask import Flask, render_template, request, jsonify
import string
import random
import re
from collections import Counter

app = Flask(__name__)

# Sample data to simulate articles


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_password_strength', methods=['POST'])
def check_password_strength_route():
    data = request.json
    password = data['password']
    username = data['username']
    birthdate = data['birthdate']
    email = data['email']


    missing_criteria, score = check_password_strength(password, username, birthdate, email)
    total_criteria = 10  # Adding the additional format check


    if missing_criteria:
        suggested_password = suggest_strong_password(username, birthdate, email)
        return jsonify({'weak': True, 'missingCriteria': missing_criteria, 'suggestedPassword': suggested_password, 'score': score})
    else:
        return jsonify({'weak': False, 'missingCriteria': [], 'suggestedPassword': '', 'score': score})


def suggest_strong_password(username, birthdate, email):
    SPECIAL_CHARS = set(string.punctuation)
   
    while True:
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=8))
       
        if (
            any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in SPECIAL_CHARS for char in password) and
            not any(pattern in password.lower() for pattern in {"123", "abc", "password", "qwerty"}) and
            not any(part.lower() in password.lower() for part in username.split()) and
            not any(part.lower() in password.lower() for part in re.split(r"[\W_]+", email)) and
            not any(part in password for part in re.findall(r"\d+", birthdate))
        ):
            return password


def check_password_strength(password, username, birthdate, email):
    MIN_LENGTH = 8
    SPECIAL_CHARS = set(string.punctuation)
   
    with open('common.txt', 'r') as f:
        common = f.read().splitlines()
   
    if password in common:
        print("Password was found in a common list. Score: 0 / 7")
        exit()
   
    missing_criteria = []
    score = 0
   
    # Check length
    if len(password) < MIN_LENGTH:
        missing_criteria.append("length (min 8 characters)")
    else:
        score += 1
   
    # Check for at least 1 special character
    if not any(char in SPECIAL_CHARS for char in password):
        missing_criteria.append("at least 1 special character")
    else:
        score += 1
   
    # Check for at least 1 uppercase letter
    if not any(char.isupper() for char in password):
        missing_criteria.append("at least 1 uppercase letter")
    else:
        score += 1
   
    # Check for at least 1 lowercase letter
    if not any(char.islower() for char in password):
        missing_criteria.append("at least 1 lowercase letter")
    else:
        score += 1
   
    # Check for at least 1 digit
    if not any(char.isdigit() for char in password):
        missing_criteria.append("at least 1 digit")
    else:
        score += 1
   
    # Check if password contains username, birthdate, or email
    if (
        username and any(part.lower() in password.lower() for part in username.split()) or
        email and any(part.lower() in password.lower() for part in re.split(r"[\W_]+", email)) or
        birthdate and any(part in password for part in re.findall(r"\d+", birthdate))
    ):
        missing_criteria.append("avoid using parts of your username, birthdate, or email in the password")
   
    # Check for repeated characters
    repeated_chars = [char for char, count in Counter(password).items() if count >= 2]
    if repeated_chars:
        missing_criteria.append(f"avoid repeated characters: {''.join(repeated_chars)}")
   
    score += 1  # Checking password format adds one to the score
   
    return missing_criteria, score








if __name__ == '__main__':
    app.run(debug=True)
