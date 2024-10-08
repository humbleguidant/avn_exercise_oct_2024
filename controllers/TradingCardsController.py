from models.User import User
from models.TradingCard import TradingCard
from flask import render_template, redirect, url_for, jsonify, session

class TradingCardController:
    def __init__(self):
        pass

    def upload(self, request):
        if request.method == "POST":
            pass
        return render_template('upload/upload_index.html')
