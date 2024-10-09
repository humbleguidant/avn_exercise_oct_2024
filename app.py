from controllers.UserAuthController import UserAuthController
from controllers.TradingCardsController import TradingCardsController
from controllers.ShoppingCartsController import ShoppingCartsController
from flask import Flask, jsonify, render_template, redirect, request
from configs.config import get_secret_key

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)
app.config.update(SECRET_KEY=get_secret_key())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

userAuth = UserAuthController()
tradingCards = TradingCardsController()
shoppingCarts = ShoppingCartsController()
@app.route('/', methods=['GET', 'POST'])
def login():
    return userAuth.login(request)

@app.route('/logout')
def logout():
    return userAuth.logout()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return userAuth.register(request)

@app.route('/home', methods=['GET', 'POST'])
def home():
    return userAuth.is_logged_in(request)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return tradingCards.upload(request, app)

@app.route('/shop')
def shop():
    return tradingCards.get_cards_from_shop(request)

@app.route('/shopping_cart')
def shopping_cart():
    return shoppingCarts.get_shopping_cart(request)

@app.route('/add_to_cart/<email>/<card_id>', methods=['POST'])
def add_to_cart(email, card_id):
    return shoppingCarts.update_cart(email, card_id, True)

@app.route('/remove_item_from_cart/<email>/<card_id>', methods=['POST'])
def remove_item_from_cart(email, card_id):
    return shoppingCarts.update_cart(email, card_id, False)

@app.route('/remove_card_from_shop/<email>/<card_id>', methods=['POST'])
def remove_card_from_shop(email, card_id):
    return tradingCards.remove_card_from_shop(email, card_id)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)