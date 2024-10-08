from models.User import User
from models.TradingCard import TradingCard
from flask import render_template, redirect, url_for, jsonify, session


class UserAuthController:
    def __init__(self):
        pass

    def register(self, request):
        if request.method == "POST":
            user = User()

            validation_status = user.validate_user_input(request.form.getlist('registerInput[]'), 'register')
            if False in validation_status.values() or None in validation_status.values():
                return render_template('register/register_index.html', validation_status = validation_status)

            validation_status = user.register_user(validation_status)
            if 'success' in validation_status and validation_status['success']:
                return redirect(url_for('login', register_success = validation_status['success']))

            return render_template('register/register_index.html', validation_status = validation_status)
        return render_template('register/register_index.html', validation_status = {})

    def login(self, request):
        if request.method == "POST":
            user = User()

            validation_status = user.validate_user_input(request.form.getlist('loginInput[]'), 'login')
            if False in validation_status.values() or None in validation_status.values():
                return render_template('login/login_index.html', validation_status = validation_status)

            validation_status = user.login_user(validation_status)
            if 'success' in validation_status and validation_status['success']:
                if 'email' in session:
                    session.pop('email')
                session['email'] = validation_status['email']
                return redirect(url_for('home', email = session['email']))
            else:
                return render_template('login/login_index.html', validation_status = validation_status)

        register_success = request.args.get('register_success')
        return render_template('login/login_index.html', register_success = register_success)

    def is_logged_in(self, request):
        if 'email' in session and request.args.get('email') == session['email']:
            email = session['email']
            trading_card = TradingCard()
            data = trading_card.get_cards(email)
            return render_template('home/home_index.html', email = session['email'], data = data)
        return redirect(url_for('login'))

    def logout(self):
        session.pop('email')
        return redirect(url_for('login'))
