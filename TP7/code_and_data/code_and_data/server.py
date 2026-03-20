from flask import Flask, session, Response, request, redirect, url_for, render_template, abort
from functools import wraps
import data_model as model

app = Flask(__name__)
app.secret_key = 'super_secret_key'

def login_required(f):
  @wraps(f)
  def decorated_function(*args, **kwargs):
    if 'user_id' not in session:
      abort(401)
    return f(*args, **kwargs)
  return decorated_function

########################################
# Routes des pages principales du site #
########################################

# Retourne une page principale avec le nombre de recettes
@app.get('/')
def home():
  return render_template('index.html')


# Retourne les résultats de la recherche à partir de la requête "query"
@app.get('/search')
def search():
  if 'page' in request.args:
    page = int(request.args["page"])
  else:
    page = 1
  if 'query' in request.args:
    query = request.args["query"]
  else:
    query = ""
  found = model.search(query, page)
  return render_template('search.html', found=found)

# Retourne le contenu d'une recette d'identifiant "id"
@app.get('/read/<id>')
def read(id):
  recipe = model.read(int(id))
  return render_template('read.html', recipe=recipe)


@app.get('/create')
@login_required
def create_form():
  return render_template('create.html')

@app.get('/update/<id>')
@login_required
def update_form(id):
  recipe = model.read(int(id))
  return render_template('update.html', recipe=recipe)


@app.get('/delete/<id>')
@login_required
def delete_form(id):
  entry = model.read(int(id))
  return render_template('delete.html', id=id, title=entry['title'])


############################################
# Routes pour modifier les données du site #
############################################


def parse_user_list(user_list):
  l = user_list.strip().split("-")
  l = [e.strip() for e in l]
  l = [e for e in l if len(e)> 0]
  return l

# Fonction qui facilite la création d'une recette
def post_data_to_recipe(form_data):
  ingredients = parse_user_list(form_data['ingredients'])
  stages = parse_user_list(form_data['stages'])
  return {
    'title': form_data['title'], 
    'description': form_data['description'],
    'img': form_data['img'],
    'duration': form_data['duration'],
    'ingredients': ingredients,
    'stages': stages
  }

@app.post('/create')
@login_required
def create_post():
  id = model.create(post_data_to_recipe(request.form))
  return redirect(url_for('read', id=str(id)))


@app.post('/update/<id>')
@login_required
def update_post(id):
  id = int(id)
  model.update(id, post_data_to_recipe(request.form))
  return redirect(url_for('read', id=str(id)))


@app.post('/delete/<id>')
@login_required
def delete_post(id):
  model.delete(int(id))
  return redirect(url_for('home'))

@app.get('/login')
def login_get():
  return render_template('login.html')

@app.post('/login')
def login_post():
  name = request.form['name']
  password = request.form['password']
  user_id = model.login(name, password)
  if user_id != -1:
    session['user_id'] = user_id
    session['name'] = name
    return redirect(url_for('home'))
  else:
    return redirect(url_for('login_get'))

@app.post('/logout')
def logout():
  session.clear()
  return redirect(url_for('home'))

@app.get('/new_user')
def new_user_get():
  return render_template('new_user.html')

@app.post('/new_user')
def new_user_post():
  name = request.form['name']
  password = request.form['password']
  user_id = model.new_user(name, password)
  session['user_id'] = user_id
  session['name'] = name
  return redirect(url_for('home'))