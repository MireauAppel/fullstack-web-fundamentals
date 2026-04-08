from flask import Flask, render_template, request, session, redirect, url_for
import data_model

app = Flask(__name__)
app.secret_key = 'cle_secrete_domaine_lupec'

# ==========================================
# ROUTE PRINCIPALE (ACCUEIL)
# ==========================================
@app.route('/')
def index():
    accommodations = data_model.get_all_accommodations()
    return render_template('index.html', accommodations=accommodations)

# ==========================================
# ROUTE NOTRE HISTOIRE
# ==========================================
@app.route('/histoire')
def history():
    return render_template('history.html')

# ==========================================
# ROUTES D'AUTHENTIFICATION
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if data_model.create_user(email, password):
            # Succès : on l'envoie vers la page de connexion
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error="Cet email est déjà utilisé.")
            
    # Si c'est un simple GET, on affiche juste la page
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # On vérifie dans la base de données
        user = data_model.get_user_by_email(email)
        
        # Si l'utilisateur existe et que le mot de passe correspond
        if user and user['password'] == password:
            # On sauvegarde son ID et son rôle dans sa "session"
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            session['email'] = user['email']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Email ou mot de passe incorrect.")
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    # On vide la session pour déconnecter l'utilisateur
    session.clear()
    return redirect(url_for('index'))

# ==========================================
# ROUTES DES LOGEMENTS ET RÉSERVATIONS
# ==========================================

@app.route('/accommodation/<int:acc_id>')
def accommodation(acc_id):
    """Affiche les détails d'un logement spécifique"""
    acc = data_model.get_accommodation_by_id(acc_id)
    if not acc:
        return "Logement introuvable", 404
    return render_template('accommodation.html', acc=acc)

@app.route('/book', methods=['POST'])
def book():
    """Traite le formulaire de réservation"""
    # Si l'utilisateur n'est pas connecté, on le renvoie au login
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    acc_id = request.form['accommodation_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    
    # On enregistre la réservation dans la base de données
    data_model.create_booking(user_id, acc_id, start_date, end_date)
    
    # On redirige vers le tableau de bord client
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    """Affiche l'historique des réservations du client"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    # On récupère toutes les réservations de cet utilisateur
    bookings = data_model.get_user_bookings(session['user_id'])
    return render_template('dashboard.html', bookings=bookings)

# ==========================================
# ROUTES ADMINISTRATEUR
# ==========================================

@app.route('/admin')
def admin_dashboard():
    """Affiche le tableau de bord du propriétaire"""
    # On vérifie que la personne est connectée ET qu'elle est admin (is_admin == 1)
    if session.get('is_admin') != 1:
        return "Accès refusé. Cette page est réservée au propriétaire.", 403
        
    # On utilise la fonction de data_model pour récupérer TOUTES les réservations
    bookings = data_model.get_all_bookings()
    return render_template('admin_dashboard.html', bookings=bookings)

@app.route('/admin/update_booking', methods=['POST'])
def update_booking():
    """Permet au propriétaire d'accepter ou refuser une demande"""
    if session.get('is_admin') != 1:
        return "Accès refusé.", 403
        
    booking_id = request.form['booking_id']
    new_status = request.form['status'] # 'confirmed' ou 'refused'
    
    # On met à jour le statut dans la base de données
    data_model.update_booking_status(booking_id, new_status)
    
    # On recharge la page admin
    return redirect(url_for('admin_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)