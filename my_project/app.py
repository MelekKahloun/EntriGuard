from flask import Flask, render_template, request, jsonify
import string
import random
import re
from collections import Counter
from datetime import datetime  




app = Flask(__name__, static_url_path='/static')




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




    format_errors = check_format(username, birthdate, email)
    if format_errors:
        return jsonify({'weak': True, 'missingCriteria': format_errors, 'suggestedPassword': suggest_strong_password(username, birthdate, email), 'score': 0})




    missing_criteria, score, password_found_in_common = check_password_strength(password, username, birthdate, email)
    cracking_time = estimate_cracking_time(password)



    total_criteria = 7  # Adding the additional format check




    if missing_criteria:
        suggested_password = suggest_strong_password(username, birthdate, email)
        return jsonify({'weak': True, 'missingCriteria': missing_criteria, 'suggestedPassword': suggested_password, 'score': score, 'passwordFoundInCommon': password_found_in_common, 'crackingTime': cracking_time})
    else:
        return jsonify({'weak': False, 'missingCriteria': [], 'suggestedPassword': '', 'score': score, 'passwordFoundInCommon': password_found_in_common, 'crackingTime': cracking_time})
















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
        password_found_in_common = True
    else:
        password_found_in_common = False
   
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
   
    if password_found_in_common:
        score -= 2  # Subtract 2 from score if password is found in common
   
    return missing_criteria, score, password_found_in_common


def estimate_cracking_time(password):
    # This is a simplified estimation. In a real application, use a more accurate method.
    complexity = len(set(password))
    length = len(password)
    possible_combinations = complexity ** length
    cracking_speed = 1e9  # assume 1 billion guesses per second
    time_to_crack_seconds = possible_combinations / cracking_speed

    if time_to_crack_seconds < 1:
        return "less than 1 second"
    elif time_to_crack_seconds < 60:
        return f"{int(time_to_crack_seconds)} seconds"
    elif time_to_crack_seconds < 3600:
        return f"{int(time_to_crack_seconds // 60)} minutes"
    elif time_to_crack_seconds < 86400:
        return f"{int(time_to_crack_seconds // 3600)} hours"
    elif time_to_crack_seconds < 31536000:
        return f"{int(time_to_crack_seconds // 86400)} days"
    else:
        return f"{int(time_to_crack_seconds // 31536000)} years"


def check_format(username, birthdate, email):
    errors = []


    # Check username format (alphanumeric and underscores)
    if not re.match(r"^[a-zA-Z0-9_]+$", username):
        errors.append("Username must be alphanumeric and underscores only")


    # Check birthdate format (YYYY-MM-DD) and validity
    try:
        datetime.strptime(birthdate, "%Y-%m-%d")
        # Additional check for valid date (e.g., not February 30th)
        datetime.fromisoformat(birthdate)  # Raises an error for invalid dates
    except ValueError:
        errors.append("Birthdate must be in YYYY-MM-DD format and a valid date")


    # Check email format (basic validation, consider a more robust library)
    if "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Invalid email format")
    return errors






if __name__ == '__main__':
    app.run(debug=True)


