import sqlite3

DBFILENAME = 'lupec_v1.db'

def get_db():
    """Établit la connexion à la base de données avec accès par nom de colonne."""
    conn = sqlite3.connect(DBFILENAME)
    conn.row_factory = sqlite3.Row 
    return conn

# --- GESTION DES LOGEMENTS ---

def get_all_accommodations():
    """Récupère l'intégralité des logements enregistrés."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accommodation")
        return cur.fetchall()

def get_accommodation_by_id(acc_id):
    """Récupère les détails d'un logement par son identifiant unique."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM accommodation WHERE id = ?", (acc_id,))
        return cur.fetchone()

# --- GESTION DES UTILISATEURS ---

def create_user(email, password):
    """Insère un nouvel utilisateur. Retourne False si l'email existe déjà."""
    with get_db() as conn:
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False 

def get_user_by_email(email):
    """Récupère un profil utilisateur pour l'authentification."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE email = ?", (email,))
        return cur.fetchone()

# --- GESTION DES RÉSERVATIONS ---

def create_booking(user_id, accommodation_id, start_date, end_date):
    """Crée une nouvelle demande de réservation au statut 'pending' par défaut."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO booking (user_id, accommodation_id, start_date, end_date) 
            VALUES (?, ?, ?, ?)
        """, (user_id, accommodation_id, start_date, end_date))
        conn.commit()

def get_user_bookings(user_id):
    """Récupère l'historique des réservations d'un client spécifique."""
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
    """Récupère l'ensemble des réservations pour l'administration."""
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
    """Met à jour le statut d'une réservation (confirmed/refused)."""
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute("UPDATE booking SET status = ? WHERE id = ?", (new_status, booking_id))
        conn.commit()