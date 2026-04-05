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

if __name__ == '__main__':
    app.run(debug=True)