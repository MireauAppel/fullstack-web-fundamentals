import sqlite3

# Nom du fichier de la base de données
DBFILENAME = 'lupec_v1.db'

def init_db(db_name=DBFILENAME):
    with sqlite3.connect(db_name) as conn:
        cur = conn.cursor()
        
        # 1. Suppression des tables existantes pour éviter les conflits lors de la création
        cur.execute('DROP TABLE IF EXISTS booking')
        cur.execute('DROP TABLE IF EXISTS accommodation')
        cur.execute('DROP TABLE IF EXISTS user')
        
        # 2. Création de la table 'user' (Les utilisateurs du système)
        cur.execute('''
            CREATE TABLE user (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                email TEXT UNIQUE NOT NULL, 
                password TEXT NOT NULL, 
                is_admin INTEGER DEFAULT 0
            )
        ''')
        
        # 3. Création de la table 'accommodation' (Les logements disponibles)
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
        
        # 4. Création de la table 'booking' (Les réservations effectuées par les utilisateurs)
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

        # --- INSERTION DE DONNÉES DE TEST ---
        
        # Création du compte propriétaire (Admin)
        cur.execute(
            'INSERT INTO user (email, password, is_admin) VALUES (:email, :password, :is_admin)',
            {'email': 'admin@domaine.fr', 'password': 'admin', 'is_admin': 1}
        )

        # Création de quelques logements pour le domaine
        accommodations = [
            {
                'name': 'Jasse', 
                'description': 'Maison familiale spacieuse idéale pour les groupes de moyenne taille. Accès direct au jardin.', 
                'image_url': 'jasse.jpg', 
                'gallery_image': 'jasse.jpg, jasse1.jpg, jasse2.jpg, jasse3.jpg, jasse4.jpg, jasse5.jpg, jasse6.jpg, jasse7.jpg, jasse8.jpg',
                'capacity': 8, 
                'price': 150
            },
            {
                'name': "Avalon", 
                'description': 'Maison familiale spacieuse idéale pour les petits groupes ou familles. Accès direct au jardin.', 
                'image_url': 'avalon.jpg', 
                'gallery_image': 'avalon.jpg, avalon1.jpg, avalon2.jpg, avalon3.jpg, avalon4.jpg, avalon5.jpg, avalon6.jpg',
                'capacity': 6, 
                'price': 125
            },
            {
                'name': 'Studio Gandalf', 
                'description': 'Petit studio cosy et rénové, parfait pour un couple en quête de tranquillité.', 
                'image_url': 'gandalf.jpg', 
                'gallery_image': 'gandalf.jpg, gandalf1.jpg, gandalf2.jpg',
                'capacity': 2, 
                'price': 80
            },
            {
                'name': 'Studio Frodo', 
                'description': "Petit studio cosy et rénové, parfait pour un couple en quête de tranquillité. Petite et charmante porte d'entrée lui donnant son nom caractéristique.", 
                'image_url': 'frodo.jpg', 
                'gallery_image': 'frodo.jpg, frodo1.jpg, frodo2.jpg',
                'capacity': 2, 
                'price': 60
            },
            {
                'name': 'Apartus', 
                'description': 'Logement de taille moyenne avec poutres apparentes et terrasse privée.', 
                'image_url': 'app.jpg', 
                'gallery_image': 'app.jpg, app1.jpg, app2.jpg, app3.jpg, app4.jpg, app5.jpg, app6.jpg, app7.jpg',
                'capacity': 4, 
                'price': 90
            }
        ]
        
        insert_acc = 'INSERT INTO accommodation (name, description, image_url, gallery_image, capacity, price) VALUES (:name, :description, :image_url, :gallery_image, :capacity, :price)'
        
        for acc in accommodations:
            cur.execute(insert_acc, acc)
            
        conn.commit()
        print("La base de données 'lupec_v1.db' a été créée et pré-remplie avec succès !")

if __name__ == '__main__':
    init_db()