from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from configs.config import get_db
from components.validator import validator

# User model, connects with users database collection
class User:

    # initialize db collection and regex expressions for login and registration validation
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['users']
        self.email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        self.password_regex = r'(?=^.{8,}$)((?=.*\d)(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$'
        self.whitespace_regex = r'(.|\s)*\S(.|\s)*'

    # validate the input from the user login form.
    def validate_user_input(self, request_input, page):
        data = {'email': request_input[0], 'password': request_input[1]}
        # validate the email using the validator function.
        validate_email = validator(data['email'], self.email_regex)
        # if the user input is coming from the register page then validate password requirements
        if page == 'register':
            validate_password = validator(data['password'], self.password_regex)
        # if the user input is coming from the login page then validate if password input is empty
        else:
            validate_password = validator(data['password'], self.whitespace_regex)

        return {'email_validated': validate_email, 'password_validated': validate_password,
                'email': data['email'], 'password': data['password']}

    # This function handles the user registration functionality
    def register_user(self, validation_data):
        # Check that user already exists before registering.
        user_exists = self.check_user(validation_data['email'])
        if user_exists:
            validation_data['user_exists'] = user_exists
            return validation_data
        try:
            # generate user id for inserting new user record into database
            event_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            # encrypt the password
            hashed_password = generate_password_hash(validation_data['password'])
            data = {"id": event_id, "email": validation_data['email'], "password": hashed_password,
                    "date_registered": datetime.now()}
            # insert the data
            res = self.collection.insert_one(data)
            # check if data was inserted successfully
            if res.inserted_id:
                validation_data['success'] = True
            # If insert was unsuccessful then return error response message
            else:
                validation_data['success'] = False
                validation_data['error_message'] = 'An error has occurred. Please contact IT services.'
        except:
            # if server error occurred then return response error message
            validation_data['error_message'] = 'An error has occurred. Please contact IT services.'
            return validation_data
        # if user already exists return True
        validation_data['user_exists'] = user_exists
        return validation_data

    # Handles the user login functionality
    def login_user(self, validation_data):
        # Check if user exists
        user_exists = self.check_user(validation_data['email'])
        # If user exists then check if password matches in database
        if user_exists:
            try:
                record = self.collection.find_one({'email': validation_data['email']})
                # check the hashed password matches with the user input password
                if check_password_hash(record['password'], validation_data['password']):
                    validation_data['success'] = True
                else:
                    # If password is incorrect then return error message
                    validation_data['success'] = False
                    validation_data['error_message'] = 'Invalid credentials.'
            except:
                # if server or database error occurred, return error message
                validation_data['error_message'] = 'An error has occurred. Please contact IT services.'
                return validation_data
        else:
            # if email does not exist in database then return error message
            validation_data['success'] = False
            validation_data['error_message'] = 'Email does not exist. Please create an account'
        return validation_data

    # Checks if email exists in the database
    def check_user(self, email):
        fetch = {'email': email}
        response = self.collection.find_one(fetch)
        if response == None:
            return False
        else:
            return True