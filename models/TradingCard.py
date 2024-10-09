import os
from configs.config import get_db
from werkzeug.utils import secure_filename
from components.validator import validator
from datetime import datetime
from uuid import uuid4
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Model for trading_cards database collection
class TradingCard:

    # initialize database collection and regex expressions for the upload form user input
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['trading_cards']
        self.money_regex = r'[0-9]+\.[0-9][0-9](?:[^0-9]|$)'
        self.whitespace_regex = r'(.|\s)*\S(.|\s)*'

    # validate the image name extension. Must be jpg, jpeg, or png
    def check_file_extension(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # Validate the user input from the upload form page. Price must be in price format and description cannot be empty.
    def validate_input(self, request):
        validate_data = {}
        # Validate the file input. Cannot be empty or incorrect file extension.
        validate_data = self.validate_file(request, validate_data)

        # # Validate the price input. Must have at least 2 decimals.
        price_validated = validator(request.form['priceInput'], self.money_regex)
        if not price_validated:
            validate_data['price_success'] = False
            validate_data['price_error_message'] = 'Invalid price amount. Please do not add \'$\''
        else:
            validate_data['price_success'] = True
        validate_data['price'] = request.form['priceInput']

        # Validate description input. Cannot be empty
        description_validated = validator(request.form['descriptionInput'], self.whitespace_regex)
        if not description_validated:
            validate_data['description_success'] = False
            validate_data['description_error_message'] = 'Description cannot be empty.'
        else:
            validate_data['description_success'] = True
        validate_data['description'] = request.form['descriptionInput']

        return validate_data

    # Functionality for validating the image.
    def validate_file(self, request, validate_data):
        # if the file input is empty then return error message
        if 'fileUpload' not in request.files:
            validate_data['file_success'] = False
            validate_data['file_error_message'] = 'No file attached.'
            return validate_data

        # if a file is uploaded but has no file name, return error message
        image = request.files['fileUpload']
        if image.filename == '':
            validate_data['file_success'] = False
            validate_data['file_error_message'] = 'No file selected.'
            return validate_data

        # if the file name extension is .jpg, .jpeg, or .png then file validation is successful
        if image and self.check_file_extension(image.filename):
            validate_data['file_success'] = True
            validate_data['file_name'] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(image.filename)
            validate_data['file'] = image
            return validate_data
        # otherwise return file extension error message
        else:
            validate_data['file_success'] = False
            validate_data['file_error_message'] = 'Incorrect file type. Must be png, jpg, or jpeg'
            return validate_data

    # Functionality for retrieving cards from database.
    # This function is executed when the home, shop, and shopping cart pages are loaded
    def get_cards(self, email, for_shopping_cart = False, shopping_cart_items = {}):
        # set response params, data from the query result, and fetch query to retrieve data
        response = {'for_shop': True}
        data = []
        fetch = {}
        # if action is to get items from shopping cart then set params
        if for_shopping_cart:
            # get items for shop is equal to False
            response['for_shop'] = False
            # get items for_shopping_cart is equal to True
            response['for_shopping_cart'] = for_shopping_cart
            card_ids = []
            # populate the card_ids array with the card ids from the shopping cart
            for item in shopping_cart_items:
                card_ids.append(item['card_id'])
            # Set the query to retrieve the data.
            fetch = {"id": {"$in": card_ids}, "is_added_to_shopping_cart": True}
        else:
            # if action is to get cards not from shopping cart then set params
            response['for_shopping_cart'] = False
            # if email is provided then get cards uploaded by the user only.
            if email is not None:
                response['for_shop'] = False
                fetch = {"email": email}
            else:
                # if the email is null then we're loading the shop page
                fetch = {"is_added_to_shopping_cart": False}
        try:
            # if email exists then we're loading the home page.
            number_of_documents = self.collection.count_documents(fetch)
            if number_of_documents == 0:
                response['has_cards'] = False
                return response
            # Begin gathering data
            cards = self.collection.find(fetch)
            # Html table index.
            # If index is on the 3rd then that means end the html table row with a closing </div> element
            table_index = 0
            # loop index for checking the last iteration of loop.
            # If index is on the last iteration then close the html table row with a closing </div> element
            loop_index = 0
            # loop through data that will be populated to home/card_listings.html page.
            for card in cards:
                # if table_index is on 3rd then this indicates html table row is closing and is set back to 0
                if table_index > 2:
                    table_index = 0
                # if the loop index is on its last iteration then pass last_iteration
                # to indicate that the html table row is closing.
                if loop_index == number_of_documents - 1:
                    # append to data array which will be populated to view
                    data.append({"id": card['id'], "email": card['email'], "file_name": 'images/' + card["file_name"],
                                 "price": card['price'], "description": card['description'],
                                 "date_uploaded": card['date_uploaded'], "table_index": table_index,
                                 "is_added_to_shopping_cart": card['is_added_to_shopping_cart'], "last_iteration": True})
                else:
                    data.append({"id": card['id'], "email": card['email'], "file_name": 'images/' + card["file_name"],
                                "price": card['price'], "description": card['description'],
                                "date_uploaded": card['date_uploaded'], "table_index": table_index,
                                 "is_added_to_shopping_cart": card['is_added_to_shopping_cart']})
                # keep looping
                loop_index += 1
                table_index += 1
            # return successful response after loop is successfully done
            response['has_cards'] = True
            response['cards'] = data
            response['number_of_cards'] = number_of_documents
            return response
        except:
            # if server error occurred then respond with error message
            response['has_cards'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

    # Functionality for uploading card from the upload page
    def upload_card(self, validation_data, email, app):
            # filename has already been validated in validate_input function,
            # therefore save the file to the static/images directory
            try:
                filename = secure_filename(validation_data['file_name'])
                image = validation_data['file']
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try:
                    # generate card id
                    event_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
                    data = {"id": event_id, "email": email, "file_name": validation_data['file_name'], "price": validation_data['price'],
                            "description": validation_data['description'], "is_added_to_shopping_cart": False, "date_uploaded": datetime.now()}
                    # insert card to database
                    res = self.collection.insert_one(data)
                    # check if data was inserted successfully
                    if res.inserted_id:
                        validation_data['success'] = True
                    else:
                        validation_data['success'] = False
                        validation_data['database_error_message'] = 'An error has occurred. Please contact IT services.'
                    return validation_data
                # if database insert failed then return error message
                except:
                    validation_data['database_error_message'] = 'An error has occured. Please contact IT services.'
                    return validation_data
            # if file upload failed then return error message
            except:
                validation_data['file_success'] = False
                validation_data['file_error_message'] = 'File upload failed. Please contact IT services.'
                return validation_data

    # Functionality for updating is_added_to_shopping_cart field to True or False.
    # This function is executed when the user adds or removes a card from the shopping cart
    def update_shopping_cart_status(self, response, card_id, remove_from_shopping_cart = False):
        try:
            # set params for removing shopping cart action
            query = {"id": card_id}
            if remove_from_shopping_cart:
                values = {"$set": {"is_added_to_shopping_cart": False}}
            else:
                values = {"$set" : {"is_added_to_shopping_cart": True}}
            # perform the database update
            self.collection.update_one(query, values)
            response['update_success'] = True
            return response
        except:
            # if database error occurred then respond with error message
            response['update_success'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

    # Functionality for deleting card in database
    def delete(self, response, card_id, file_name, app):
        # perform delete action
        try:
            query = {"id": card_id}
            # remove the card from the database
            self.collection.delete_one(query)
            # remove the image associated with the card from the folder in the application
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
            response['delete_success'] = True
            return response
        except:
            # if error occurred then return message
            response['delete_success'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response