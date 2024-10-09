from models.ShoppingCart import ShoppingCart
from models.TradingCard import TradingCard
from flask import render_template, redirect, url_for, jsonify, session

class ShoppingCartsController:
    def __init__(self):
        pass

    def update_cart(self, email, card_id, remove_or_add):
        response = {}
        remove = False
        if 'email' in session and email == session['email']:
            shoppingCart = ShoppingCart()
            if remove_or_add:
                response = shoppingCart.add_to_cart(email, card_id)
            else:
                response = shoppingCart.remove_from_cart(card_id, response)
                remove = True

                # update shopping cart status of card
            tradingCard = TradingCard()
            response = tradingCard.update_shopping_cart_status(response, card_id, remove)
            return jsonify(response)
        return jsonify(response)


    def get_shopping_cart(self, request):
        if 'email' in session and request.args.get('email') == session['email']:
            email = session['email']
            shoppingCart = ShoppingCart()
            shopping_cart_items_total = shoppingCart.get_total_items_for_user(email)
            data = shoppingCart.get_shopping_cart(email)
            if False in data.values():
                return render_template('home/card_listings.html', email=email, shopping_cart_items_total = shopping_cart_items_total, data=data)

            tradingCard = TradingCard()
            data = tradingCard.get_cards(email, True, data['shopping_cart_items'])
            if False in data.values():
                return render_template('home/card_listings.html', email=email, shopping_cart_items_total = shopping_cart_items_total, data=data)
            return render_template('home/card_listings.html', email=email, shopping_cart_items_total = shopping_cart_items_total, data=data)

