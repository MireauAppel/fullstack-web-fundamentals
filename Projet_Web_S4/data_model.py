import sqlite3


DBFILENAME = 'lupec_v1.db'

def get_db():
    """Fonction utilitaire pour se connecter à la base"""
    conn = sqlite3.connect(DBFILENAME)
    conn.row_factory = sqlite3.Row 
    return conn

# ==========================================
# REQUÊTES POUR LES LOGEMENTS (ACCOMMODATION)
# ==========================================

def get_all_accommodations():
    """Récupère tous les logements pour la page d'accueil"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accommodation")
        return cur.fetchall()

def get_accommodation_by_id(acc_id):
    """Récupère un logement spécifique pour sa page de détails"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accommodation WHERE id = ?", (acc_id,))
        return cur.fetchone()

# ==========================================
# REQUÊTES POUR LES UTILISATEURS (USER)
# ==========================================

def create_user(email, password):
    """Crée un nouveau compte client"""
    with get_db() as conn:
        cur = conn.cursor()
        try:
            # On utilise les '?' pour éviter les failles de sécurité (injections SQL)
            cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # L'email existe déjà dans la base de données (car email est UNIQUE)
            return False 

def get_user_by_email(email):
    """Récupère un utilisateur via son email (utile pour la connexion)"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE email = ?", (email,))
        return cur.fetchone()

# ==========================================
# REQUÊTES POUR LES RÉSERVATIONS (BOOKING)
# ==========================================

def create_booking(user_id, accommodation_id, start_date, end_date):
    """Enregistre une nouvelle demande de réservation"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO booking (user_id, accommodation_id, start_date, end_date) 
            VALUES (?, ?, ?, ?)
        """, (user_id, accommodation_id, start_date, end_date))
        conn.commit()

def get_user_bookings(user_id):
    """Récupère l'historique des réservations pour le tableau de bord d'un client"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT booking.*, accommodation.name AS accommodation_name 
            FROM booking 
            JOIN accommodation ON booking.accommodation_id = accommodation.id 
            WHERE booking.user_id = ?
        """, (user_id,))
        return cur.fetchall()

def get_all_bookings():
    """Récupère TOUTES les réservations pour le tableau de bord de l'Administrateur"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT booking.*, user.email, accommodation.name AS accommodation_name 
            FROM booking 
            JOIN user ON booking.user_id = user.id
            JOIN accommodation ON booking.accommodation_id = accommodation.id
        """)
        return cur.fetchall()

def update_booking_status(booking_id, new_status):
    """Permet à l'Administrateur d'accepter ou de refuser une réservation"""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE booking SET status = ? WHERE id = ?", (new_status, booking_id))
        conn.commit()