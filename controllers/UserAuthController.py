from models.User import User
from models.TradingCard import TradingCard
from models.ShoppingCart import ShoppingCart
from flask import render_template, redirect, url_for, jsonify, session


class UserAuthController:
    def __init__(self):
        pass

    def register(self, request):
        # if user submitted registration form then validate fields and insert new user to database
        if request.method == "POST":
            user = User()

            # if input fields have any validation error then reload register page with error messages
            validation_status = user.validate_user_input(request.form.getlist('registerInput[]'), 'register')
            if False in validation_status.values() or None in validation_status.values():
                return render_template('register/register_index.html', validation_status = validation_status)

            # if user successfully registered then redirect to login page
            validation_status = user.register_user(validation_status)
            if 'success' in validation_status and validation_status['success']:
                return redirect(url_for('login', register_success = validation_status['success']))

            return render_template('register/register_index.html', validation_status = validation_status)
        # if user is accessing register page then load page
        return render_template('register/register_index.html', validation_status = {})

    def login(self, request):
        # if user is logging in then get the user from the database
        if request.method == "POST":
            user = User()

            # if user login failed then reload login page with error messages
            validation_status = user.validate_user_input(request.form.getlist('loginInput[]'), 'login')
            if False in validation_status.values() or None in validation_status.values():
                return render_template('login/login_index.html', validation_status = validation_status)

            # if user is successfully logged in then delete any old sessions and begin new session
            # to avoid user logging into more than one user simultaneously.
            # redirect to home page.
            validation_status = user.login_user(validation_status)
            if 'success' in validation_status and validation_status['success']:
                if 'email' in session:
                    session.pop('email')
                session['email'] = validation_status['email']
                shoppingCart = ShoppingCart()
                shopping_cart_items_total = shoppingCart.get_total_items_for_user(session['email'])
                return redirect(url_for('home', email = session['email'], shopping_cart_items_total = shopping_cart_items_total))
            else:
                # if user does not exist or password is incorrect reload page with error message.
                return render_template('login/login_index.html', validation_status = validation_status)

        register_success = request.args.get('register_success')
        return render_template('login/login_index.html', register_success = register_success)

    #check if user is logged in
    def is_logged_in(self, request):
        # if user is logged in then get the trading cards associated with the logged in user
        if 'email' in session and request.args.get('email') == session['email']:
            email = session['email']
            shoppingCart = ShoppingCart()
            shopping_cart_items_total = shoppingCart.get_total_items_for_user(email)
            trading_card = TradingCard()
            data = trading_card.get_cards(email)
            return render_template('home/card_listings.html', email = email, shopping_cart_items_total = shopping_cart_items_total, data = data)
        # if user is not logged in then redirect to the login page
        return redirect(url_for('login'))

    # log out the user by deleting the session and redirecting to the login page
    def logout(self):
        session.pop('email')
        return redirect(url_for('login'))
