from db import get_connection, hash_password, generate_token
from config import config
import datetime

# Admins

def create_admin(username: str, password: str) -> int:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO admins (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password)))
    conn.commit(); aid = cur.lastrowid; conn.close(); return aid


def create_admin_with_master_password(username: str, password: str, email: str, master_password: str) -> bool:
    """Create admin account with master password verification"""
    if master_password != config.get_master_password():
        raise ValueError("Nieprawidłowe hasło główne")
    
    if not email or "@" not in email:
        raise ValueError("Podaj prawidłowy email")
    
    conn = get_connection(); cur = conn.cursor()
    # Check if username already exists
    cur.execute("SELECT id FROM admins WHERE username=?", (username,))
    if cur.fetchone():
        conn.close()
        raise ValueError("Użytkownik już istnieje")
    
    cur.execute("INSERT INTO admins (username, password_hash, email) VALUES (?, ?, ?)",
                (username, hash_password(password), email))
    conn.commit(); aid = cur.lastrowid; conn.close()
    return aid > 0


def authenticate_admin(username: str, password: str) -> bool:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT password_hash FROM admins WHERE username=?", (username,))
    row = cur.fetchone(); conn.close()
    return bool(row and row['password_hash'] == hash_password(password))


def get_admin_emails() -> list:
    """Get all admin emails for notifications"""
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT email FROM admins WHERE email IS NOT NULL AND email != ''")
    emails = [row['email'] for row in cur.fetchall()]
    conn.close()
    
    # If no admin emails found, use config recipient
    if not emails:
        recipient_email = config.get('email', 'recipient_email')
        if recipient_email:
            emails = [recipient_email]
    
    return emails

# Rooms

def seed_rooms(names: list):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) c FROM rooms"); count = cur.fetchone()['c']
    
    if count == 0:
        # First time - insert new rooms
        for n in names: 
            cur.execute("INSERT INTO rooms(name) VALUES(?)", (n,))
    else:
        # Clear existing rooms and insert new ones to avoid conflicts
        cur.execute("DELETE FROM rooms")
        for n in names: 
            cur.execute("INSERT INTO rooms(name) VALUES(?)", (n,))
    
    conn.commit()
    conn.close()

def get_rooms() -> list:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, name FROM rooms ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]; conn.close(); return rows

# Reservations

def _overlaps(s1, e1, s2, e2) -> bool:
    fmt = "%H:%M"
    t1s = datetime.datetime.strptime(s1, fmt)
    t1e = datetime.datetime.strptime(e1, fmt)
    t2s = datetime.datetime.strptime(s2, fmt)
    t2e = datetime.datetime.strptime(e2, fmt)
    return t1s < t2e and t2s < t1e


def is_available(room_id: int, date: str, start: str, end: str) -> bool:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT start_time, end_time FROM reservations WHERE room_id=? AND date=?",
                (room_id, date))
    rows = cur.fetchall(); conn.close()
    for r in rows:
        if _overlaps(start, end, r['start_time'], r['end_time']):
            return False
    return True


def create_reservation(room_id: int, date: str, start_time: str, end_time: str,
                       user_name: str, password: str, user_email: str, description=None) -> str:
    if not user_email or "@" not in user_email:
        raise ValueError("Email jest wymagany")
    
    if not is_available(room_id, date, start_time, end_time):
        # Send collision notification
        try:
            from email_service import send_collision_notification
            # Get room name
            conn = get_connection(); cur = conn.cursor()
            cur.execute("SELECT name FROM rooms WHERE id=?", (room_id,))
            room_name = cur.fetchone()['name']
            conn.close()
            send_collision_notification(user_email, user_name, room_name, date, start_time, end_time)
        except:
            pass  # Don't fail if email sending fails
        raise ValueError("Termin zajęty")
    
    token = generate_token()
    conn = get_connection(); cur = conn.cursor()
    from db import hash_password
    password_hash = hash_password(password)
    cur.execute("INSERT INTO reservations(room_id, date, start_time, end_time, user_name, user_email, token, password_hash, description)"
                " VALUES(?,?,?,?,?,?,?,?,?)",
                (room_id, date, start_time, end_time, user_name, user_email, token, password_hash, description))
    
    # Get room name for email
    cur.execute("SELECT name FROM rooms WHERE id=?", (room_id,))
    room_name = cur.fetchone()['name']
    conn.commit(); conn.close()
    
    # Send confirmation email to user
    try:
        from email_service import send_reservation_confirmation, send_admin_notification
        send_reservation_confirmation(user_email, user_name, room_name, date, start_time, end_time, token)
        
        # Send notification to all admins
        admin_emails = get_admin_emails()
        for admin_email in admin_emails:
            send_admin_notification(admin_email, user_name, user_email, room_name, date, start_time, end_time)
    except Exception as e:
        print(f"Email sending failed: {e}")
        # Don't fail the reservation if email fails
    
    return token


def get_reservations_between(start_date: str, end_date: str) -> list:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT r.*, rm.name AS room_name FROM reservations r JOIN rooms rm ON r.room_id=rm.id"
                " WHERE date(r.date) BETWEEN date(?) AND date(?) ORDER BY r.date, r.start_time",
                (start_date, end_date))
    res = [dict(r) for r in cur.fetchall()]; conn.close(); return res


def get_reservation_by_token(token: str) -> dict:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT r.*, rm.name AS room_name FROM reservations r JOIN rooms rm ON r.room_id=rm.id WHERE token=?",
                (token,))
    row = cur.fetchone(); conn.close(); return dict(row) if row else None


def delete_reservation_by_token(token: str) -> bool:
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM reservations WHERE token=?", (token,))
    ok = cur.rowcount > 0; conn.commit(); conn.close(); return ok


def delete_reservation_with_password(token: str, password: str) -> bool:
    conn = get_connection(); cur = conn.cursor()
    from db import hash_password
    password_hash = hash_password(password)
    cur.execute("DELETE FROM reservations WHERE token=? AND password_hash=?", (token, password_hash))
    ok = cur.rowcount > 0; conn.commit(); conn.close(); return ok


def delete_reservation_admin(token: str) -> bool:
    """Admin function to delete reservation without password"""
    # Get reservation data for email notification
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT r.*, rm.name as room_name 
                   FROM reservations r 
                   JOIN rooms rm ON r.room_id = rm.id 
                   WHERE r.token=?""", (token,))
    res_data = cur.fetchone()
    
    # Delete reservation
    cur.execute("DELETE FROM reservations WHERE token=?", (token,))
    ok = cur.rowcount > 0
    conn.commit(); conn.close()
    
    # Send notification email if deletion successful and user has email
    if ok and res_data and res_data['user_email']:
        try:
            from email_service import send_deletion_notification
            send_deletion_notification(
                res_data['user_email'],
                res_data['user_name'], 
                res_data['room_name'],
                res_data['date'],
                res_data['start_time'],
                res_data['end_time']
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
    
    return ok


def delete_reservation_by_user_data(user_name: str, room_id: int, date: str, start_time: str, password: str) -> bool:
    """Delete reservation by user data and password"""
    conn = get_connection(); cur = conn.cursor()
    from db import hash_password
    password_hash = hash_password(password)
    cur.execute("""DELETE FROM reservations 
                   WHERE user_name=? AND room_id=? AND date=? AND start_time=? AND password_hash=?""",
                (user_name, room_id, date, start_time, password_hash))
    ok = cur.rowcount > 0; conn.commit(); conn.close(); return ok


def find_user_reservations(user_name: str, password: str) -> list:
    """Find all reservations for a user with correct password"""
    conn = get_connection(); cur = conn.cursor()
    from db import hash_password
    password_hash = hash_password(password)
    cur.execute("""SELECT r.*, rm.name AS room_name 
                   FROM reservations r 
                   JOIN rooms rm ON r.room_id=rm.id 
                   WHERE r.user_name=? AND r.password_hash=?
                   ORDER BY r.date, r.start_time""",
                (user_name, password_hash))
    res = [dict(r) for r in cur.fetchall()]; conn.close(); return res


def update_reservation(token: str, room_id: int, date: str, start_time: str, end_time: str,
                       user_name: str = None, description=None) -> bool:
    # Get old reservation data for email notification
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT r.*, rm.name as room_name 
                   FROM reservations r 
                   JOIN rooms rm ON r.room_id = rm.id 
                   WHERE r.token=?""", (token,))
    old_res = cur.fetchone()
    
    if not old_res:
        conn.close()
        raise ValueError("Rezerwacja nie znaleziona")
    
    # Check availability excluding current reservation
    cur.execute("SELECT start_time, end_time FROM reservations WHERE room_id=? AND date=? AND token!=?",
                (room_id, date, token))
    rows = cur.fetchall()
    for r in rows:
        if _overlaps(start_time, end_time, r['start_time'], r['end_time']):
            conn.close()
            raise ValueError("Termin zajęty")
    
    # Get new room name
    cur.execute("SELECT name FROM rooms WHERE id=?", (room_id,))
    new_room_name = cur.fetchone()['name']
    
    # Update reservation
    if user_name:
        cur.execute("UPDATE reservations SET room_id=?, date=?, start_time=?, end_time=?, user_name=?, description=? WHERE token=?",
                    (room_id, date, start_time, end_time, user_name, description, token))
    else:
        cur.execute("UPDATE reservations SET room_id=?, date=?, start_time=?, end_time=?, description=? WHERE token=?",
                    (room_id, date, start_time, end_time, description, token))
    ok = cur.rowcount > 0
    conn.commit(); conn.close()
    
    # Send notification email if update successful and user has email
    if ok and old_res['user_email']:
        try:
            from email_service import send_edit_notification
            send_edit_notification(
                old_res['user_email'], 
                old_res['user_name'],
                old_res['room_name'],
                old_res['date'], 
                old_res['start_time'], 
                old_res['end_time'],
                date, 
                start_time, 
                end_time, 
                new_room_name
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
    
    return ok

def edit_reservation_admin(reservation_id, user_name, description, room_id, date, start_time, end_time):
    """Edit reservation by admin - can modify all fields including user_name"""
    from db import get_db_connection
    
    # Sprawdź czy termin nie koliduje z innymi rezerwacjami
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Sprawdź kolizje z innymi rezerwacjami (pomiń bieżącą rezerwację)
    cursor.execute('''
        SELECT id FROM reservations 
        WHERE room_id = ? AND date = ? 
        AND id != ?
        AND ((start_time < ? AND end_time > ?) OR 
             (start_time < ? AND end_time > ?) OR
             (start_time >= ? AND end_time <= ?))
    ''', (room_id, date, reservation_id, end_time, start_time, start_time, end_time, start_time, end_time))
    
    if cursor.fetchone():
        conn.close()
        return False
    
    # Pobierz dane starej rezerwacji dla emaila
    cursor.execute('''
        SELECT r.user_name, r.description, rm.name as room_name, r.date, r.start_time, r.end_time
        FROM reservations r 
        JOIN rooms rm ON r.room_id = rm.id 
        WHERE r.id = ?
    ''', (reservation_id,))
    old_reservation = cursor.fetchone()
    
    # Pobierz nazwę nowej sali
    cursor.execute('SELECT name FROM rooms WHERE id = ?', (room_id,))
    new_room = cursor.fetchone()
    
    if not old_reservation or not new_room:
        conn.close()
        return False
    
    # Zaktualizuj rezerwację
    cursor.execute('''
        UPDATE reservations 
        SET user_name = ?, description = ?, room_id = ?, date = ?, start_time = ?, end_time = ?
        WHERE id = ?
    ''', (user_name, description, room_id, date, start_time, end_time, reservation_id))
    
    ok = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    # Wyślij email o zmianie (jeśli zmieniono dane)
    if ok and (old_reservation[0] != user_name or 
               old_reservation[1] != description or 
               old_reservation[3] != date or 
               old_reservation[4] != start_time or 
               old_reservation[5] != end_time or
               old_reservation[2] != new_room[0]):
        try:
            from email_service import send_update_email
            send_update_email(
                user_name, 
                old_reservation[1], 
                description,
                old_reservation[2], 
                new_room[0],
                old_reservation[3], 
                date,
                old_reservation[4], 
                old_reservation[5],
                start_time, 
                end_time
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
    
    return ok