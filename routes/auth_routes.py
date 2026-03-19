from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from models.user import create_user, get_user_by_email

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']

            existing_user = get_user_by_email(email)
            if existing_user:
                flash("Email already registered.")
                return redirect(url_for('auth.register'))

            # Directly create the user without OTP
            create_user(name, email, phone, password, is_verified=True)

            flash("Registration successful! Please login.")
            return redirect(url_for('auth.login'))

        except Exception as e:
            flash(f"Error: {e}")

    return render_template("register.html")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            user = get_user_by_email(email)
            if user:
                # user[4] or user['password'] depending on cursor
                is_valid = False
                if isinstance(user, tuple):
                    is_valid = (user[4] == password)
                else:
                    is_valid = (user.get('password') == password)

                if is_valid:
                    # check is_verified
                    verified = user[5] if isinstance(user, tuple) else user.get('is_verified')
                    if verified:
                        session['user_email'] = email
                        return redirect(url_for('dashboard.dashboard_view'))
                    else:
                        flash("Account not verified.")
                else:
                    flash("Invalid email or password")
            else:
                 flash("Invalid email or password")

        except Exception as e:
            flash(f"Error: {e}")

    return render_template("login.html")

@auth.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('auth.login'))
