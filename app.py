#import Controllers, configs, and libraries
from controllers.UserAuthController import UserAuthController
from controllers.TradingCardsController import TradingCardsController
from controllers.ShoppingCartsController import ShoppingCartsController
from flask import Flask, jsonify, render_template, redirect, request
from configs.config import get_secret_key

# set the path where images will be uploaded
UPLOAD_FOLDER = 'static/images'

# initiliaze the application
# get the secret key from .env
# and set the path for image uploads
app = Flask(__name__)
app.config.update(SECRET_KEY=get_secret_key())
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# initialize Controllers
userAuth = UserAuthController()
tradingCards = TradingCardsController()
shoppingCarts = ShoppingCartsController()

# Route to login user
@app.route('/', methods=['GET', 'POST'])
def login():
    return userAuth.login(request)

# Log user out of system
@app.route('/logout')
def logout():
    return userAuth.logout()

# Register user to application and save information to database
@app.route('/register', methods=['GET', 'POST'])
def register():
    return userAuth.register(request)

# Go to home page if user is logged in. If not then redirect to login page
@app.route('/home', methods=['GET', 'POST'])
def home():
    return userAuth.is_logged_in(request)

# Page for uploading card. If its POST request then that means user is submitting form.
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return tradingCards.upload(request, app)

# Page for viewing all submitted cards.
@app.route('/shop')
def shop():
    return tradingCards.get_cards_from_shop(request)

# Page to view users shopping cart.
@app.route('/shopping_cart')
def shopping_cart():
    return shoppingCarts.get_shopping_cart(request)

# POST request to add card to shopping cart.
@app.route('/add_to_cart/<email>/<card_id>', methods=['POST'])
def add_to_cart(email, card_id):
    return shoppingCarts.update_cart(email, card_id, True)

# POST request to remove card from shopping cart
@app.route('/remove_item_from_cart/<email>/<card_id>', methods=['POST'])
def remove_item_from_cart(email, card_id):
    return shoppingCarts.update_cart(email, card_id, False)

# Post request to delete card entirely
@app.route('/remove_card_from_shop/<email>/<card_id>', methods=['POST'])
def remove_card_from_shop(email, card_id):
    return tradingCards.remove_card_from_shop(email, card_id)

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)