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
            return "Erreur : Cet email est déjà utilisé."
            
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
            return "Erreur : Email ou mot de passe incorrect."
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    # On vide la session pour déconnecter l'utilisateur
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)