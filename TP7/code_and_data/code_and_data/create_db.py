import sqlite3
import json

JSONFILENAME = 'recipes.json'
DBFILENAME = 'recipes.sqlite'

def load(fname=JSONFILENAME, db_name=DBFILENAME):
  with sqlite3.connect(db_name) as conn:
    cur = conn.cursor()
    
    cur.execute('DROP TABLE IF EXISTS recipe')
    cur.execute('DROP TABLE IF EXISTS ingredient')
    cur.execute('DROP TABLE IF EXISTS stage')
    cur.execute('DROP TABLE IF EXISTS user')
    
    cur.execute('CREATE TABLE recipe (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, img TEXT, description TEXT, duration TEXT)')
    cur.execute('CREATE TABLE ingredient (recipe INT, rank INT, name TEXT)')
    cur.execute('CREATE TABLE stage (recipe INT, rank INT, description TEXT)')
    cur.execute('CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password_hash TEXT)')

    insert1 = 'INSERT INTO recipe VALUES (:id, :title, :img, :description, :duration)'
    insert2 = 'INSERT INTO ingredient VALUES (:recipe, :rank, :name)'
    insert3 = 'INSERT INTO stage VALUES (:recipe, :rank, :description)'
    
    with open(fname, 'r', encoding='utf-8') as fh:
      recipes = json.load(fh)
      
    for id, recipe in enumerate(recipes):
      recipe['id'] = id
      cur.execute(insert1, recipe)
      for r, ingredient in enumerate(recipe['ingredients']):
        cur.execute(insert2, {'recipe': id, 'rank': r, 'name': ingredient['name']})
      for r, stage in enumerate(recipe['stages']):
        cur.execute(insert3, {'recipe': id, 'rank': r, 'description': stage['description']})
        
    conn.commit()

# load recipe data
load()