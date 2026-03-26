from flask import Blueprint, render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import random
import re
from datetime import datetime, timedelta
from models.user import create_user, get_user_by_email, update_user_password

auth = Blueprint('auth', __name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_strong_password(password):
    return (len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            password = request.form['password']

            if not is_valid_email(email):
                flash("Invalid email format.")
                return render_template("register.html")
            
            if not is_strong_password(password):
                flash("Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, and a number.")
                return render_template("register.html")

            existing_user = get_user_by_email(email)
            hashed_pw = generate_password_hash(password)

            if existing_user:
                flash("Email already registered. Please login.")
                return redirect(url_for('auth.register'))

            create_user(name, email, phone, hashed_pw)

            flash("Registration successful! You can now log in.")
            return redirect(url_for('auth.login'))

        except Exception as e:
            flash(f"Error: {e}")

    return render_template("register.html")

# OTP endpoints removed

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']

            user = get_user_by_email(email)
            if user:
                user_id = user[0]
                db_password = user[4] if isinstance(user, tuple) else user.get('password')
                is_valid = False
                if db_password.startswith('scrypt:') or db_password.startswith('pbkdf2:'):
                    is_valid = check_password_hash(db_password, password)
                else: 
                    # Backwards compatibility for plain text
                    if db_password == password:
                        is_valid = True
                        update_user_password(user_id, generate_password_hash(password))

                if is_valid:
                    session['user_email'] = email
                    return redirect(url_for('dashboard.dashboard_view'))
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
