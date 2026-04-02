from flask import Blueprint, render_template, request, redirect, session, flash, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask_mail import Message
from extensions import mail
from models.user import create_user, get_user_by_email, update_user_password, verify_user

auth = Blueprint('auth', __name__)

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm')

def confirm_verification_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm', max_age=expiration)
    except:
        return False
    return email

def send_verification_email(to_email):
    try:
        token = generate_verification_token(to_email)
        confirm_url = url_for('auth.verify_email', token=token, _external=True)
        msg = Message('Verify Your AgroLedger Account',
                      recipients=[to_email])
        msg.body = f'''Welcome to AgroLedger!
        Please click the link below to verify your email address and activate your account:
        {confirm_url}
        
        This link will expire in 1 hour.
        If you did not create an account, please ignore this email.
        '''
        mail.send(msg)
        return True, None
    except Exception as e:
        error_msg = str(e)
        print(f"Mail send error: {error_msg}")
        return False, error_msg

def is_valid_email(email):
    # More robust email regex
    return re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email)

def is_strong_password(password):
    return (len(password) >= 8 and
            re.search(r"[A-Z]", password) and
            re.search(r"[a-z]", password) and
            re.search(r"[0-9]", password))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form['name'].strip()
            email = request.form['email'].strip().lower()
            phone = request.form['phone'].strip()
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
            
            success, error = send_verification_email(email)
            if success:
                flash("Registration successful! A verification email has been sent to your inbox. Please verify before logging in.")
            else:
                if "535" in error or "BadCredentials" in error:
                    flash("Registration successful, but we failed to send a verification email due to SMTP configuration issues (Bad Credentials). If you use Gmail, ensure you've set an 'App Password'.")
                else:
                    flash(f"Registration successful, but we failed to send a verification email ({error}). Please contact support.")
                
            return redirect(url_for('auth.login'))

        except Exception as e:
            flash(f"Error: {e}")

    return render_template("register.html")

# OTP endpoints removed

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form['email'].strip().lower()
            password = request.form['password']

            user = get_user_by_email(email)
            if user:
                # Handle both tuple (default cursor) and dict (DictCursor) if ever used
                if isinstance(user, (tuple, list)):
                    user_id = user[0]
                    db_password = user[4]
                    is_verified = user[5]
                else:
                    user_id = user.get('id')
                    db_password = user.get('password')
                    is_verified = user.get('is_verified')

                is_valid = False
                # Try modern hash verification first
                try:
                    if db_password and (':' in db_password or '$' in db_password):
                        is_valid = check_password_hash(db_password, password)
                except Exception as e:
                    print(f"Hash verification error: {e}")
                
                # Fallback to plain text comparison (for older accounts)
                if not is_valid and db_password == password:
                    is_valid = True
                    # Auto-migrate to secure hash
                    update_user_password(user_id, generate_password_hash(password))
                    print(f"Migrated user {email} to secure hash.")

                if not is_valid:
                    print(f"Login failed: Invalid password for {email}")
                    flash("Invalid Password")
                    return render_template("login.html")
                
                if not is_verified:
                    print(f"Login failed: {email} not verified.")
                    flash("Please verify your email address before logging in. If you didn't receive the email, click the link below to resend it.")
                    return render_template("login.html", show_resend=True)

                session.permanent = True
                session['user_email'] = email
                print(f"Successful login for: {email}")
                return redirect(url_for('dashboard.dashboard_view'))
            else:
                 print(f"Login failed: Email {email} not found.")
                 flash("Invalid Email")
                 return render_template("login.html")

        except Exception as e:
            flash(f"Error: {e}")
            return render_template("login.html")

    return render_template("login.html")

@auth.route('/verify-email/<token>')
def verify_email(token):
    email = confirm_verification_token(token)
    if not email:
        flash("The verification link is invalid or has expired.")
        return redirect(url_for('auth.login'))
    
    user = get_user_by_email(email)
    if not user:
        flash("User not found.")
        return redirect(url_for('auth.login'))
    
    if (isinstance(user, tuple) and user[5]) or (isinstance(user, dict) and user.get('is_verified')):
        flash("Account already verified. Please login.")
    else:
        verify_user(email)
        flash("Your email has been verified! You can now log in.")
        
    return redirect(url_for('auth.login'))

@auth.route('/resend-verification', methods=['GET', 'POST'])
def resend_verification():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        user = get_user_by_email(email)
        
        if not user:
            flash("If that email is in our system, we've sent a new verification link.")
            return redirect(url_for('auth.login'))
            
        # Check if already verified
        is_already_verified = False
        if isinstance(user, (tuple, list)):
            is_already_verified = user[5]
        else:
            is_already_verified = user.get('is_verified')
            
        if is_already_verified:
            flash("Account already verified. Please login.")
            return redirect(url_for('auth.login'))
            
        success, error = send_verification_email(email)
        if success:
            flash("A new verification email has been sent. Please check your inbox.")
        else:
             flash(f"Failed to send email: {error}. Please contact support.")
             
        return redirect(url_for('auth.login'))
        
    return render_template("resend_verification.html")

@auth.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('auth.login'))
