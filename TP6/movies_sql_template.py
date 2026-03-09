import sqlite3
import json

DBFILENAME = 'movies.sqlite'


def db_fetch(query, args=(), all=False, db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    # to allow access to columns by name in res
    conn.row_factory = sqlite3.Row 
    cur = conn.execute(query, args)
    # convert to a python dictionary for convenience
    if all:
      res = cur.fetchall()
      if res:
        res = [dict(e) for e in res]
    else:
      res = cur.fetchone()
      if res:
        res = dict(res)
  return res

def db_insert(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.lastrowid


def db_run(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()


def db_update(query, args=(), db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.execute(query, args)
    conn.commit()
    return cur.rowcount


class MoviesDB:

  def __init__(self, db_path=None):
    # TODO: create movies table here
    if not(db_path is None):
      self.load(db_path)


  def load(self, db_path):
    with open(db_path, 'r') as fh:
      movies = json.load(fh)
    insert_stmt = 'INSERT INTO movies VALUES ' +\
                    '(:id, :title, :year,' +\
                    ' :actors, :plot, :poster)'
    for key in movies:
      db_insert(insert_stmt, movies[key])
    return True


  def save(self, db_path):
    movie_list = db_fetch('SELECT * FROM movies ORDER BY id',
                          all=True)
    movies = {}
    for movie in movie_list:
      movies[movie['id']] = movie
    with open(db_path, 'w', encoding='utf-8') as fh:
      json.dump(movies, fh, ensure_ascii=False, indent=4)
    return True


  def list(self):
    pass  #TODO


  def create(self, title, year, actors, plot, poster):
    pass  #TODO


  def read(self, id):
    pass  #TODO


  def update(self, id, title, year, actors, plot, poster):
    pass  #TODO


  def delete(self, id):
    pass  #TODO
