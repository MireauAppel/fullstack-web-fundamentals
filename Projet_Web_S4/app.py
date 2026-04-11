from flask import Flask, render_template, request, session, redirect, url_for
import data_model
import os

app = Flask(__name__)
app.secret_key = 'cle_secrete_domaine_lupec'

# --- ROUTES FRONT-OFFICE ---

@app.route('/')
def index():
    accommodations = data_model.get_all_accommodations()
    return render_template('index.html', accommodations=accommodations)

@app.route('/histoire')
def history():
    static_folder = os.path.join(app.root_path, 'static')
    misc_images = []
    
    if os.path.exists(static_folder):
        for filename in os.listdir(static_folder):
            if 'misc' in filename.lower() and os.path.isfile(os.path.join(static_folder, filename)):
                misc_images.append(filename)
                
    misc_images.sort()
    return render_template('history.html', misc_images=misc_images)

# --- AUTHENTIFICATION ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if data_model.create_user(email, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Cet email est déjà utilisé.")
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = data_model.get_user_by_email(email)
        
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            session['email'] = user['email']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Email ou mot de passe incorrect.")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# --- RÉSERVATIONS ---

@app.route('/accommodation/<int:acc_id>')
def accommodation(acc_id):
    acc = data_model.get_accommodation_by_id(acc_id)
    if not acc:
        return "Logement introuvable", 404
    return render_template('accommodation.html', acc=acc)

@app.route('/book', methods=['POST'])
def book():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    acc_id = request.form['accommodation_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    data_model.create_booking(user_id, acc_id, start_date, end_date)
    return redirect(url_for('dashboard'))

@app.route('/group_booking', methods=['GET', 'POST'])
def group_booking():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        user_id = session['user_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        acc_ids = request.form.getlist('accommodation_ids')
        for acc_id in acc_ids:
            data_model.create_booking(user_id, acc_id, start_date, end_date)
        return redirect(url_for('dashboard'))
        
    accommodations = data_model.get_all_accommodations()
    all_bookings = data_model.get_all_bookings()
    
    confirmed_list = [{
        'accommodation_id': b['accommodation_id'],
        'start_date': b['start_date'],
        'end_date': b['end_date']
    } for b in all_bookings if b['status'] == 'confirmed']
    
    return render_template('group_booking.html', accommodations=accommodations, bookings=confirmed_list)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    bookings = data_model.get_user_bookings(session['user_id'])
    return render_template('dashboard.html', bookings=bookings)

# --- BACK-OFFICE ADMIN ---

@app.route('/admin')
def admin_dashboard():
    if session.get('is_admin') != 1:
        return "Accès refusé.", 403
        
    bookings = data_model.get_all_bookings()
    return render_template('admin_dashboard.html', bookings=bookings)

@app.route('/admin/update_booking', methods=['POST'])
def update_booking():
    if session.get('is_admin') != 1:
        return "Accès refusé.", 403
        
    booking_id = request.form['booking_id']
    new_status = request.form['status']
    
    data_model.update_booking_status(booking_id, new_status)
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)