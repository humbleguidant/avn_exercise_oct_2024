import os
from configs.config import get_db
from werkzeug.utils import secure_filename
from components.validator import validator
from datetime import datetime
from uuid import uuid4
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class TradingCard:

    def __init__(self):
        self.db = get_db()
        self.collection = self.db['trading_cards']
        self.money_regex = r'[0-9]+\.[0-9][0-9](?:[^0-9]|$)'
        self.whitespace_regex = r'(.|\s)*\S(.|\s)*'

    def check_file_extension(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def validate_input(self, request):
        validate_data = {}

        validate_data = self.validate_file(request, validate_data)

        price_validated = validator(request.form['priceInput'], self.money_regex)
        if not price_validated:
            validate_data['price_success'] = False
            validate_data['price_error_message'] = 'Invalid price amount. Please do not add \'$\''
        else:
            validate_data['price_success'] = True
        validate_data['price'] = request.form['priceInput']

        description_validated = validator(request.form['descriptionInput'], self.whitespace_regex)
        if not description_validated:
            validate_data['description_success'] = False
            validate_data['description_error_message'] = 'Description cannot be empty.'
        else:
            validate_data['description_success'] = True
        validate_data['description'] = request.form['descriptionInput']

        return validate_data

    def validate_file(self, request, validate_data):
        if 'fileUpload' not in request.files:
            validate_data['file_success'] = False
            validate_data['file_error_message'] = 'No file attached.'
            return validate_data

        image = request.files['fileUpload']
        if image.filename == '':
            validate_data['file_success'] = False
            validate_data['file_error_message'] = 'No file selected.'
            return validate_data

        if image and self.check_file_extension(image.filename):
            validate_data['file_success'] = True
            validate_data['file_name'] = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(image.filename)
            validate_data['file'] = image
            return validate_data
        else:
            validate_data['file_success'] = False
            validate_data['file_error_message'] = 'Incorrect file type. Must be png, jpg, or jpeg'
            return validate_data

    def get_cards(self, email, for_shopping_cart = False, shopping_cart_items = {}):
        response = {'for_shop': True}
        data = []
        fetch = {}
        if for_shopping_cart:
            response['for_shop'] = False
            response['for_shopping_cart'] = for_shopping_cart
            card_ids = []
            for item in shopping_cart_items:
                card_ids.append(item['card_id'])
            fetch = {"id": {"$in": card_ids}, "is_added_to_shopping_cart": True}
        else:
            response['for_shopping_cart'] = False
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
            # Html table index. If index is on the 3rd then that means end the html table row
            table_index = 0
            # loop index for checking the last iteration of loop. If index is on the last iteration then close the html table
            loop_index = 0
            # loop through data
            for card in cards:
                if table_index > 2:
                    table_index = 0
                if loop_index == number_of_documents - 1:
                    data.append({"id": card['id'], "email": card['email'], "file_name": 'images/' + card["file_name"],
                                 "price": card['price'], "description": card['description'],
                                 "date_uploaded": card['date_uploaded'], "table_index": table_index,
                                 "is_added_to_shopping_cart": card['is_added_to_shopping_cart'], "last_iteration": True})
                else:
                    data.append({"id": card['id'], "email": card['email'], "file_name": 'images/' + card["file_name"],
                                "price": card['price'], "description": card['description'],
                                "date_uploaded": card['date_uploaded'], "table_index": table_index,
                                 "is_added_to_shopping_cart": card['is_added_to_shopping_cart']})
                loop_index += 1
                table_index += 1
            response['has_cards'] = True
            response['cards'] = data
            response['number_of_cards'] = number_of_documents
            return response
        except:
            response['has_cards'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

    def upload_card(self, validation_data, email, app):
            try:
                filename = secure_filename(validation_data['file_name'])
                image = validation_data['file']
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try:
                    event_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
                    data = {"id": event_id, "email": email, "file_name": validation_data['file_name'], "price": validation_data['price'],
                            "description": validation_data['description'], "is_added_to_shopping_cart": False, "date_uploaded": datetime.now()}
                    res = self.collection.insert_one(data)
                    # check if data was inserted successfully
                    if res.inserted_id:
                        validation_data['success'] = True
                    else:
                        validation_data['success'] = False
                        validation_data['database_error_message'] = 'An error has occurred. Please contact IT services.'
                    return validation_data
                except:
                    validation_data['database_error_message'] = 'An error has occured. Please contact IT services.'
                    return validation_data
            except:
                validation_data['file_success'] = False
                validation_data['file_error_message'] = 'File upload failed. Please contact IT services.'
                return validation_data

    def update_shopping_cart_status(self, response, card_id, remove_from_shopping_cart = False):
        try:
            query = {"id": card_id}
            if remove_from_shopping_cart:
                values = {"$set": {"is_added_to_shopping_cart": False}}
            else:
                values = {"$set" : {"is_added_to_shopping_cart": True}}
            self.collection.update_one(query, values)
            response['update_success'] = True
            return response
        except:
            response['update_success'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

    def delete(self, response, card_id):
        try:
            query = {"id": card_id}
            self.collection.delete_one(query)
            response['delete_success'] = True
            return response
        except:
            response['delete_success'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response