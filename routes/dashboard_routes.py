from flask import Blueprint, render_template, session, redirect, url_for, request, flash, current_app
from models.user import get_user_by_email, delete_user
from models.land import add_land, get_user_lands, delete_land
from models.crop import add_crop, get_user_crops, delete_crop
from models.labour import add_labour, get_user_labour, delete_labour
from models.expense import add_expense, get_user_expenses, delete_expense
from models.sales import add_sale, get_user_sales, delete_sale

dashboard = Blueprint('dashboard', __name__)

def get_current_user_id():
    if 'user_email' not in session:
        return None
    user = get_user_by_email(session['user_email'])
    return user[0] if user else None

@dashboard.route('/dashboard')
def dashboard_view():
    user_id = get_current_user_id()
    if not user_id:
        return redirect(url_for('auth.login'))
        
    crops = get_user_crops(user_id)
    labour_logs = get_user_labour(user_id)
    expenses = get_user_expenses(user_id)
    sales = get_user_sales(user_id)
    
    active_crops_count = len(crops)
    labour_count = len(labour_logs)
    
    user_lands = get_user_lands(user_id)
    total_land_area = sum(float(land[2]) for land in user_lands) if user_lands else 0.0
    
    total_expenses = sum(exp[3] for exp in expenses) if expenses else 0
    total_sales = sum((sale[3] * sale[4]) for sale in sales) if sales else 0
    
    net_profit = total_sales - total_expenses
    import json
    crop_data = []
    for c in crops:
        try:
            # c[2]=crop_name, c[4]=sown_date, c[5]=expected_yield
            c_year = c[4].year if c[4] else 'Unknown'
            c_yield = float(c[5]) if c[5] is not None else 0.0
            crop_data.append({
                'name': c[2],
                'year': c_year,
                'yield': c_yield
            })
        except Exception:
            pass
    crop_data_json = json.dumps(crop_data)
    
    return render_template(
        "dashboard.html", 
        active_crops_count=active_crops_count,
        labour_count=labour_count,
        net_profit=net_profit,
        total_sales=total_sales,
        total_expenses=total_expenses,
        total_land_area=total_land_area,
        crop_data_json=crop_data_json
    )

# --- LAND ROUTES ---
@dashboard.route('/land', methods=['GET', 'POST'])
def land_view():
    user_id = get_current_user_id()
    if not user_id: return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        area = request.form['area']
        location = request.form['location']
        soil_type = request.form['soil_type']
        try:
            add_land(user_id, area, location, soil_type)
            flash("Land record added successfully!")
        except Exception as e:
            flash(f"Error adding land: {e}")
        return redirect(url_for('dashboard.land_view'))
        
    lands = get_user_lands(user_id)
    return render_template("land.html", lands=lands)

@dashboard.route('/land/delete/<int:land_id>')
def land_delete(land_id):
    user_id = get_current_user_id()
    if user_id:
        delete_land(land_id, user_id)
        flash("Land record deleted.")
    return redirect(url_for('dashboard.land_view'))

# --- CROP ROUTES ---
@dashboard.route('/crops', methods=['GET', 'POST'])
def crops_view():
    user_id = get_current_user_id()
    if not user_id: return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        crop_name = request.form['crop_name']
        season = request.form['season']
        sown_date = request.form['sown_date']
        expected_yield = request.form['expected_yield']
        try:
            add_crop(user_id, crop_name, season, sown_date, expected_yield)
            flash("Crop added successfully!")
        except Exception as e:
            flash(f"Error adding crop: {e}")
        return redirect(url_for('dashboard.crops_view'))
        
    crops = get_user_crops(user_id)
    seasons_dict = {'Kharif': [], 'Rabi': [], 'Zaid': []}
    for crop in crops:
        s = crop[3]
        if s in seasons_dict:
            seasons_dict[s].append(crop)
        else:
            # If there's an arbitrary generic season, default it to Kharif or store separately. Let's force it to Kharif for simplicity if unknown, or just leave as is.
            pass  # Assuming user only creates from the UI we provide now.

    return render_template("crops.html", crops=crops, seasons=seasons_dict)

@dashboard.route('/crops/delete/<int:crop_id>')
def crop_delete(crop_id):
    user_id = get_current_user_id()
    if user_id:
        delete_crop(crop_id, user_id)
        flash("Crop deleted.")
    return redirect(url_for('dashboard.crops_view'))

# --- LABOUR ROUTES ---
@dashboard.route('/labour', methods=['GET', 'POST'])
def labour_view():
    user_id = get_current_user_id()
    if not user_id: return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        worker_name = request.form['worker_name']
        work_date = request.form['work_date']
        end_date = request.form.get('end_date') or None
        wages_paid = request.form['wages_paid']
        try:
            add_labour(user_id, worker_name, work_date, end_date, wages_paid)
            flash("Labour log added successfully!")
        except Exception as e:
            flash(f"Error adding labour log: {e}")
        return redirect(url_for('dashboard.labour_view'))
        
    labour_logs = get_user_labour(user_id)
    return render_template("labour.html", labour_logs=labour_logs)

@dashboard.route('/labour/delete/<int:labour_id>')
def labour_delete(labour_id):
    user_id = get_current_user_id()
    if user_id:
        delete_labour(labour_id, user_id)
        flash("Labour log deleted.")
    return redirect(url_for('dashboard.labour_view'))

# --- FINANCIAL ROUTES ---
@dashboard.route('/financials', methods=['GET'])
def financials_view():
    user_id = get_current_user_id()
    if not user_id: return redirect(url_for('auth.login'))
    
    expenses = get_user_expenses(user_id)
    sales = get_user_sales(user_id)
    crops = get_user_crops(user_id)  # Needed for sales dropdown
    return render_template("financials.html", expenses=expenses, sales=sales, crops=crops)

@dashboard.route('/financials/expense/add', methods=['POST'])
def expense_add():
    user_id = get_current_user_id()
    if user_id:
        try:
            category = request.form['expense_category']
            amount = request.form['amount']
            date = request.form['expense_date']
            desc = request.form['description']
            add_expense(user_id, category, amount, date, desc)
            flash("Expense added successfully!")
        except Exception as e:
            flash(f"Error adding expense: {e}")
    return redirect(url_for('dashboard.financials_view'))

@dashboard.route('/financials/expense/delete/<int:expense_id>')
def expense_delete(expense_id):
    user_id = get_current_user_id()
    if user_id:
        delete_expense(expense_id, user_id)
        flash("Expense deleted.")
    return redirect(url_for('dashboard.financials_view'))

@dashboard.route('/financials/sale/add', methods=['POST'])
def sale_add():
    user_id = get_current_user_id()
    if user_id:
        try:
            crop_id = request.form['crop_id']
            qty = request.form['quantity_sold']
            price = request.form['price_per_unit']
            date = request.form['sale_date']
            add_sale(user_id, crop_id, qty, price, date)
            flash("Sale added successfully!")
        except Exception as e:
            flash(f"Error adding sale: {e}")
    return redirect(url_for('dashboard.financials_view'))

@dashboard.route('/financials/sale/delete/<int:sale_id>')
def sale_delete(sale_id):
    user_id = get_current_user_id()
    if user_id:
        delete_sale(sale_id, user_id)
        flash("Sale deleted.")
    return redirect(url_for('dashboard.financials_view'))

# --- PROFILE ROUTES ---
@dashboard.route('/profile')
def profile_view():
    if 'user_email' not in session:
        return redirect(url_for('auth.login'))
    user = get_user_by_email(session['user_email'])
    return render_template("profile.html", user=user)

