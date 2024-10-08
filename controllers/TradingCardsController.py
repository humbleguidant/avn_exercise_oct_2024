from models.User import User
from models.ShoppingCart import ShoppingCart
from models.TradingCard import TradingCard
from flask import render_template, redirect, url_for, jsonify, session

class TradingCardsController:
    def __init__(self):
        pass

    # Get all cards that are not added to a shopping cart
    def get_cards_from_shop(self, request):
        # If user is not logged in then redirect to the login page
        if 'email' in session and request.args.get('email') == session['email']:
            # get the users shopping cart items
            email = session['email']
            shoppingCart = ShoppingCart()
            shopping_cart_items_total = shoppingCart.get_total_items_for_user(email)
            # get the cards that are in the shopping cart their attributes such as price, description, and image
            tradingCard = TradingCard()
            data = tradingCard.get_cards(None)
            return render_template('home/card_listings.html', email = email, shopping_cart_items_total = shopping_cart_items_total, data = data)
        return redirect(url_for('login'))

    # Upload input values from upload form.
    def upload(self, request, app):
        # check if user is logged in. If not, redirect to login page.
        if 'email' in session and request.args.get('email') == session['email']:
            email = session['email']
            shoppingCart = ShoppingCart()
            shopping_cart_items_total = shoppingCart.get_total_items_for_user(email)
            # if user is submitting data then go here
            if request.method == "POST":
                tradingCard = TradingCard()

                # validate the upload form input
                validation_status = tradingCard.validate_input(request)
                if False in validation_status.values() or None in validation_status.values():
                    return render_template('upload/upload_index.html', validation_status = validation_status, email = email,
                                           shopping_cart_items_total = shopping_cart_items_total)

                # upload the card to the server
                validation_status = tradingCard.upload_card(validation_status, email, app)
                if False in validation_status.values() or None in validation_status.values():
                    return render_template('upload/upload_index.html', validation_status = validation_status, email = email,
                                           shopping_cart_items_total = shopping_cart_items_total)

                # If validation and insertion were successful then redirect to home page
                return redirect(url_for('home', email = email, shopping_cart_items_total = shopping_cart_items_total))
            # load upload page if the user is logged in and is accessing the upload page
            return render_template('upload/upload_index.html', email = email, shopping_cart_items_total = shopping_cart_items_total)
        # redirect to login if user is not logged in
        return redirect(url_for('login'))

    # Delete card entirely from the application functionality
    def remove_card_from_shop(self, email, card_id, file_name, app):
        response = {'delete_success': False}
        if 'email' in session and email == session['email']:
            # Delete card
            tradingCard = TradingCard()
            response = tradingCard.delete(response, card_id, file_name, app)

            # Remove card from shopping cart
            shoppingCart = ShoppingCart()
            response = shoppingCart.remove_from_cart(card_id, response)
            return jsonify(response)
        return jsonify(response)