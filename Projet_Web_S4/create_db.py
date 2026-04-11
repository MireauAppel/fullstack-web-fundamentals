import sqlite3

DBFILENAME = 'lupec_v1.db'

def init_db(db_name=DBFILENAME):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        
        # Réinitialisation du schéma
        cur.execute('DROP TABLE IF EXISTS booking')
        cur.execute('DROP TABLE IF EXISTS accommodation')
        cur.execute('DROP TABLE IF EXISTS user')
        
        cur.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                email TEXT UNIQUE NOT NULL, 
                password TEXT NOT NULL, 
                is_admin INTEGER DEFAULT 0
            )
        ''')
        
        cur.execute('''
            CREATE TABLE accommodation (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                description TEXT, 
                image_url TEXT, 
                gallery_image TEXT,
                capacity INTEGER, 
                price INTEGER
            )
        ''')
        
        cur.execute('''
            CREATE TABLE booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER NOT NULL, 
                accommodation_id INTEGER NOT NULL, 
                start_date TEXT NOT NULL, 
                end_date TEXT NOT NULL, 
                status TEXT DEFAULT 'pending',
                FOREIGN KEY(user_id) REFERENCES user(id),
                FOREIGN KEY(accommodation_id) REFERENCES accommodation(id)
            )
        ''')

        # --- JEU DE DONNÉES INITIAL ---
        
        cur.execute(
            'INSERT INTO user (email, password, is_admin) VALUES (?, ?, ?)',
            ('admin@domaine.fr', 'admin', 1)
        )

        accommodations = [
            ('Jasse', 'Maison familiale avec terrasse.', 'jasse.jpg', 'jasse.jpg, jasse1.jpg, jasse2.jpg', 8, 150),
            ('Avalon', 'Maison familiale avec vue montagne.', 'avalon.jpg', 'avalon.jpg, avalon1.jpg', 6, 125),
            ('Studio Frodo', 'Studio avec entrée caractéristique.', 'frodo.jpg', 'frodo.jpg, frodo1.jpg', 2, 60),
            ('Studio Gandalf', 'Studio rénové pour deux personnes.', 'gandalf.jpg', 'gandalf.jpg, gandalf1.jpg', 2, 80),
            ('Apartus', 'Appartement moderne avec terrasse.', 'app.jpg', 'app.jpg, app1.jpg', 4, 90)
        ]
        
        cur.executemany(
            'INSERT INTO accommodation (name, description, image_url, gallery_image, capacity, price) VALUES (?, ?, ?, ?, ?, ?)',
            accommodations
        )
            
        conn.commit()

if __name__ == '__main__':
    init_db()