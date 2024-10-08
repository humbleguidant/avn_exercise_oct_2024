from flask import Flask, jsonify, render_template, redirect, request
from configs.config import get_db, get_secret_key
from controllers.TradingCardsController import TradingCardController
from controllers.UserAuthController import UserAuthController
app = Flask(__name__)
app.config.update(SECRET_KEY=get_secret_key())
userAuth = UserAuthController()
tradingCard = TradingCardController()
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
    return tradingCard.upload(request)

@app.route('/cards')
def get_stored_cards():
    db = get_db()
    _cards = db.trading_card_shop_tb.find()
    cards = [{"id": card["id"], "name": card["name"], "type": card["type"]} for card in _cards]
    return jsonify({"cards": cards})
    #return db

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)