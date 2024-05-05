import string
import random
from collections import Counter
import re
from datetime import datetime

def generate_strong_password(min_length=8):
    SPECIAL_CHARS = set(string.punctuation)
    
    while True:
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=min_length))
        
        if (
            any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            any(char in SPECIAL_CHARS for char in password) and
            not any(pattern in password.lower() for pattern in {"123", "abc", "password", "qwerty"})
        ):
            return password

def suggest_strong_password(username, birthdate, email):
    strong_password = generate_strong_password()
    print(f"Suggested strong password : {strong_password}")

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

def main():
    username = input("Enter your username: ")
    birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
    email = input("Enter your email: ")
    
    format_errors = check_format(username, birthdate, email)
    if format_errors:
        print("Format errors:")
        for error in format_errors:
            print(error)
        return
   
    password = input("Enter your password: ")
   
    missing_criteria, score = check_password_strength(password, username, birthdate, email)
    total_criteria = 10  # Adding the additional format check
   
    if missing_criteria:
        print(f"Password missing criteria: {', '.join(missing_criteria)}")
        suggest_strong_password(username, birthdate, email)
    else:
        print("Password meets all criteria")
   
    password_score = round((score / total_criteria) * 5, 2)
    print(f"Password score: {password_score}/5")

if __name__ == "__main__":
    main()

