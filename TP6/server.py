from flask import Flask, render_template, redirect, request # type: ignore
import movies
app = Flask(__name__)
db_path = './movies.json'
movies_db = movies.MoviesDB(db_path)

@app.route('/')
def movie_list():
    movies = movies_db.list()
    return render_template('movie-list.html', movies=movies)
@app.route('/movie-details/<id>')
def movie_details(id):
    movie = movies_db.read(int(id))
    return render_template('movie-details.html', movie=movie)

@app.get('/add-movie-form')
def add_movie_form():
    return render_template('add-movie-form.html')

@app.get('/add-movie')
def add_movie():
    title = request.args['title']
    year = request.args['year']
    actors = request.args['actors']
    plot = request.args['plot']
    poster = request.args['poster']
    
    movies_db.create(title, year, actors, plot, poster)
    movies_db.save(db_path)
    
    return redirect('/')

@app.route('/edit-movie-form/<id>')
def edit_movie_form(id):
    movie = movies_db.read(int(id))
    if movie == None:
        return redirect('/')
    return render_template('edit-movie-form.html', movie=movie)

@app.get('/edit-movie/<id>')
def edit_movie(id):
    title = request.args['title']
    year = request.args['year']
    actors = request.args['actors']
    plot = request.args['plot']
    poster = request.args['poster']
    
    movies_db.update(int(id), title, year, actors, plot, poster)
    movies_db.save(db_path)
    
    return redirect('/')


@app.get('/delete-movie/<id>')
def delete_movie(id):
    movies_db.delete(int(id))
    movies_db.save(db_path)
    return redirect('/')

@app.route('/delete-movie-form/<id>')
def delete_movie_form(id):
    movie = movies_db.read(int(id))
    if movie == None:
        return redirect('/')
    return render_template('delete-movie-form.html' , movie=movie)