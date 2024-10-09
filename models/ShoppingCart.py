import os
from configs.config import get_db
from werkzeug.utils import secure_filename
from components.validator import validator
from datetime import datetime
from uuid import uuid4

# Model for shopping cart collection in database
class ShoppingCart:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['shopping_cart_items']

    # add to cart functionality
    def add_to_cart(self, email, card_id):
        response = {}
        try:
            # Generate id for shopping cart item
            event_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            data = {"id": event_id, "email": email, "card_id": card_id, "date_added": datetime.now()}
            # insert document into collection
            res = self.collection.insert_one(data)
            if res.inserted_id:
                response['insert_success'] = True
            else:
            # if database error occurred then return error message
                response['insert_success'] = False
                response['database_error_message'] = 'An error has occurred. Please contact IT services.'
            return response
        except:
            # if server error occurred then return error message
            response['insert_success'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

    # Shopping cart functionality
    def get_shopping_cart(self, email):
        response = {}
        data = []
        # query for fetching the data
        fetch = {"email": email}
        try:
            # get number of items in shopping cart
            number_of_documents = self.collection.count_documents(fetch)
            # if there are no items in shopping cart then return no items message
            if number_of_documents == 0:
                response['has_shopping_cart'] = False
                response['shopping_cart_items_total_amount'] = number_of_documents
                response['database_error_message'] = 'No shopping cart found.'
                return response
            # Begin gathering data
            shopping_cart = self.collection.find(fetch)
            # populate array with shopping cart information to query trading cards collection
            # so that we can get the additional attributes from cards such as price, description, and image
            for item in shopping_cart:
                data.append({"id": item['id'], "email": item['email'], "card_id": item['card_id']})
            response['has_shopping_cart'] = True
            response['shopping_cart_items'] = data
            response['shopping_cart_items_total_amount'] = number_of_documents
            return response
        except:
            # if error occurred then respond with error message
            response['has_shopping_cart'] = False
            response['shopping_cart_items_total_amount'] = 0
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

    # get total items from shopping cart.
    # this is for displaying the shopping cart icon on top right of screen.
    def get_total_items_for_user(self, email):
        get_shopping_cart = self.get_shopping_cart(email)
        shopping_cart_items_total = get_shopping_cart['shopping_cart_items_total_amount']
        return shopping_cart_items_total

    # Remove item from shopping cart
    def remove_from_cart(self, card_id, response):
        try:
            query = {"card_id": card_id}
            self.collection.delete_one(query)
            response['delete_success'] = True
            return response
        except:
            response['delete_success'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

