from models.ShoppingCart import ShoppingCart
from models.TradingCard import TradingCard
from flask import render_template, redirect, url_for, jsonify, session

class ShoppingCartsController:
    def __init__(self):
        pass

    # Functionality for adding and removing a card from the shopping cart
    def update_cart(self, email, card_id, remove_or_add):
        response = {}
        remove = False
        if 'email' in session and email == session['email']:
            shoppingCart = ShoppingCart()
            # If the remove_or_add variable is passed as True then the action is to add item to shopping cart
            if remove_or_add:
                response = shoppingCart.add_to_cart(email, card_id)
            else:
                # remove card from the shopping cart.
                response = shoppingCart.remove_from_cart(card_id, response)
                remove = True

            # update shopping cart status of card
            tradingCard = TradingCard()
            response = tradingCard.update_shopping_cart_status(response, card_id, remove)
            return jsonify(response)
        return jsonify(response)

    # Get shopping cart items
    def get_shopping_cart(self, request):
        # if user is logged in then get shopping cart items otherwise redirect to the login
        if 'email' in session and request.args.get('email') == session['email']:
            # get the card ids from the shopping cart collection
            email = session['email']
            shoppingCart = ShoppingCart()
            shopping_cart_items_total = shoppingCart.get_total_items_for_user(email)
            data = shoppingCart.get_shopping_cart(email)
            # if no shopping carts are available or server error occured, then load the listings page with error message.
            if False in data.values():
                return render_template('home/card_listings.html', email=email, shopping_cart_items_total = shopping_cart_items_total, data=data)

            # if shopping cart items are available then get the cards attributes such as price, description, and image.
            tradingCard = TradingCard()
            data = tradingCard.get_cards(email, True, data['shopping_cart_items'])
            # if server error occurred then load page with error messages.
            if False in data.values():
                return render_template('home/card_listings.html', email=email, shopping_cart_items_total = shopping_cart_items_total, data=data)
            return render_template('home/card_listings.html', email=email, shopping_cart_items_total = shopping_cart_items_total, data=data)
        return redirect(url_for('login'))
