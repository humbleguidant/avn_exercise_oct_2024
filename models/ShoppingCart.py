import os
from configs.config import get_db
from werkzeug.utils import secure_filename
from components.validator import validator
from datetime import datetime
from uuid import uuid4

class ShoppingCart:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db['shopping_cart_items']

    def add_to_cart(self, email, card_id):
        response = {}
        try:
            event_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
            data = {"id": event_id, "email": email, "card_id": card_id, "date_added": datetime.now()}
            res = self.collection.insert_one(data)
            if res.inserted_id:
                response['insert_success'] = True
            else:
                response['insert_success'] = False
                response['database_error_message'] = 'An error has occurred. Please contact IT services.'
            return response
        except:
            response['insert_success'] = False
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response


    def get_shopping_cart(self, email):
        response = {}
        data = []
        fetch = {"email": email}
        try:
            number_of_documents = self.collection.count_documents(fetch)
            if number_of_documents == 0:
                response['has_shopping_cart'] = False
                response['shopping_cart_items_total_amount'] = number_of_documents
                response['database_error_message'] = 'No shopping cart found.'
                return response
            # Begin gathering data
            shopping_cart = self.collection.find(fetch)
            for item in shopping_cart:
                data.append({"id": item['id'], "email": item['email'], "card_id": item['card_id']})
            response['has_shopping_cart'] = True
            response['shopping_cart_items'] = data
            response['shopping_cart_items_total_amount'] = number_of_documents
            return response
        except:
            response['has_shopping_cart'] = False
            response['shopping_cart_items_total_amount'] = 0
            response['database_error_message'] = 'An error has occured. Please contact IT services.'
            return response

    def get_total_items_for_user(self, email):
        get_shopping_cart = self.get_shopping_cart(email)
        shopping_cart_items_total = get_shopping_cart['shopping_cart_items_total_amount']
        return shopping_cart_items_total

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

