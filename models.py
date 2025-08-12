"""
MODELS.PY - GŁÓWNE FUNKCJE BIZNESOWE APLIKACJI
==============================================

Ten plik zawiera wszystkie funkcje odpowiedzialne za:
- Zarządzanie kontami administratorów 
- Tworzenie, edycję i usuwanie rezerwacji
- Pobieranie danych z bazy
- Wysyłanie emaili powiadomień
- Sprawdzanie dostępności sal

Importy:
- db: funkcje bazy danych (połączenie, hashowanie, tokeny)
- config: konfiguracja aplikacji
- datetime: operacje na datach
"""

from db import get_connection, hash_password, generate_token
from config import config
import datetime

# ========================================
# ZARZĄDZANIE KONTAMI ADMINISTRATORÓW
# ========================================

def create_admin(username: str, password: str) -> int:
    """
    PROSTA FUNKCJA TWORZENIA ADMINISTRATORA
    
    Ta funkcja tworzy podstawowe konto administratora bez dodatkowych sprawdzeń.
    Używana jest do tworzenia domyślnego konta przy starcie aplikacji.
    
    Parametry:
    - username: nazwa użytkownika (np. "admin")
    - password: hasło w czystym tekście (zostanie zahashowane)
    
    Zwraca: ID utworzonego administratora
    """
    # Nawiązujemy połączenie z bazą danych i tworzymy kursor
    conn = get_connection()
    cur = conn.cursor()
    
    # Wstawiamy nowego admina do tabeli (INSERT OR IGNORE = nie duplikuj jeśli już istnieje)
    cur.execute("INSERT OR IGNORE INTO admins (username, password_hash) VALUES (?, ?)",
                (username, hash_password(password)))  # hash_password() szyfruje hasło
    
    # Zatwierdzamy zmiany, pobieramy ID nowego rekordu i zamykamy połączenie
    conn.commit()
    aid = cur.lastrowid  # ID ostatnio wstawionego rekordu
    conn.close()
    return aid


def create_admin_with_master_password(username: str, password: str, email: str, master_password: str) -> bool:
    """
    BEZPIECZNA FUNKCJA TWORZENIA ADMINISTRATORA Z WERYFIKACJĄ
    
    Ta funkcja tworzy konto administratora z dodatkowymi zabezpieczeniami:
    - Wymaga podania master password (hasła głównego)
    - Sprawdza czy email jest prawidłowy
    - Sprawdza czy użytkownik już nie istnieje
    
    Parametry:
    - username: nazwa użytkownika do logowania
    - password: hasło do logowania  
    - email: adres email (na ten adres będą wysyłane powiadomienia)
    - master_password: hasło główne (z pliku config.py)
    
    Zwraca: True jeśli udało się utworzyć konto, False w przeciwnym razie
    Wyjątki: ValueError z opisem błędu jeśli coś poszło nie tak
    """
    # SPRAWDZENIE 1: Czy master password jest prawidłowy
    if master_password != config.get_master_password():
        raise ValueError("Nieprawidłowe hasło główne")
    
    # SPRAWDZENIE 2: Czy email jest prawidłowy (zawiera @)
    if not email or "@" not in email:
        raise ValueError("Podaj prawidłowy email")
    
    # Połączenie z bazą danych
    conn = get_connection()
    cur = conn.cursor()
    
    # SPRAWDZENIE 3: Czy użytkownik o tej nazwie już istnieje
    cur.execute("SELECT id FROM admins WHERE username=?", (username,))
    if cur.fetchone():  # Jeśli znaleziono rekord
        conn.close()
        raise ValueError("Użytkownik już istnieje")
    
    # Wszystko w porządku - tworzymy nowego administratora
    cur.execute("INSERT INTO admins (username, password_hash, email) VALUES (?, ?, ?)",
                (username, hash_password(password), email))
    
    # Zatwierdzamy zmiany i sprawdzamy czy się udało
    conn.commit()
    aid = cur.lastrowid  # ID nowo utworzonego administratora
    conn.close()
    return aid > 0  # Zwracamy True jeśli ID > 0 (sukces)


def authenticate_admin(username: str, password: str) -> bool:
    """
    FUNKCJA LOGOWANIA ADMINISTRATORA
    
    Sprawdza czy podane dane logowania (username + password) są prawidłowe.
    Używana przy logowaniu do panelu administratora.
    
    Parametry:
    - username: nazwa użytkownika
    - password: hasło w czystym tekście
    
    Zwraca: True jeśli dane są prawidłowe, False w przeciwnym razie
    
    Jak to działa:
    1. Pobiera zahashowane hasło z bazy dla danego username
    2. Porównuje hash z bazy z hashem wprowadzonego hasła
    3. Jeśli się zgadzają - logowanie udane
    """
    # Pobieramy zahashowane hasło z bazy danych
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM admins WHERE username=?", (username,))
    row = cur.fetchone()  # Pobieramy pierwszy (i jedyny) wynik
    conn.close()
    # Sprawdzamy czy znaleźliśmy użytkownika i czy hasło się zgadza
    return bool(row and row['password_hash'] == hash_password(password))


def get_admin_emails() -> list:
    """
    POBIERANIE ADRESÓW EMAIL ADMINISTRATORÓW
    
    Ta funkcja pobiera wszystkie adresy email administratorów z bazy danych.
    Używana do wysyłania powiadomień o rezerwacjach, edycjach, usunięciach.
    
    Zwraca: Lista adresów email administratorów
    
    Logika:
    1. Pobiera wszystkie niepuste adresy email z tabeli admins
    2. Jeśli nie ma żadnych adresów w bazie, używa domyślnego z config.py
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Pobieramy wszystkie niepuste adresy email administratorów
    cur.execute("SELECT email FROM admins WHERE email IS NOT NULL AND email != ''")
    emails = [row['email'] for row in cur.fetchall()]  # Lista comprehension - tworzy listę emaili
    conn.close()
    
    # Jeśli nie ma żadnych adresów email w bazie, użyj domyślnego z konfiguracji
    if not emails:
        recipient_email = config.get('email', 'recipient_email')  # Pobierz z config.py
        if recipient_email:
            emails = [recipient_email]
    
    return emails


# ========================================
# ZARZĄDZANIE SALAMI KONFERENCYJNYMI
# ========================================

def seed_rooms(names: list):
    """
    INICJALIZACJA SAL KONFERENCYJNYCH W BAZIE DANYCH
    
    Ta funkcja jest wywoływana przy starcie aplikacji i zapewnia,
    że w bazie danych są wszystkie sale zdefiniowane w config.py
    
    Parametry:
    - names: lista nazw sal z pliku konfiguracyjnego
    
    Logika:
    1. Sprawdza czy w bazie są jakieś sale
    2. Jeśli nie ma - dodaje wszystkie z konfiguracji
    3. Jeśli są - aktualizuje listę (dodaje nowe, usuwa nieistniejące)
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Sprawdzamy ile sal jest obecnie w bazie danych
    cur.execute("SELECT COUNT(*) c FROM rooms")
    count = cur.fetchone()['c']
    
    if count == 0:
        # PIERWSZY RAZ - baza jest pusta, dodajemy wszystkie sale
        print("Inicjalizacja sal konferencyjnych...")
        for n in names: 
            cur.execute("INSERT INTO rooms(name) VALUES(?)", (n,))
    else:
        # AKTUALIZACJA - czyścimy stare sale i dodajemy nowe aby uniknąć konfliktów
        print("Aktualizacja listy sal konferencyjnych...")
        cur.execute("DELETE FROM rooms")  # Usuń wszystkie stare sale
        for n in names: 
            cur.execute("INSERT INTO rooms(name) VALUES(?)", (n,))  # Dodaj nowe
    
    # Zatwierdzamy zmiany w bazie danych
    conn.commit()
    conn.close()


def get_rooms() -> list:
    """
    POBIERANIE LISTY WSZYSTKICH SAL
    
    Funkcja pobiera wszystkie sale konferencyjne z bazy danych.
    Używana do wyświetlania w formularzu rezerwacji.
    
    Zwraca: Lista słowników z danymi sal [{'id': 1, 'name': 'Sala A'}, ...]
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Pobieramy ID i nazwę wszystkich sal, posortowane według ID
    cur.execute("SELECT id, name FROM rooms ORDER BY id")
    rows = [dict(r) for r in cur.fetchall()]  # Konwertujemy każdy wiersz na słownik
    
    conn.close()
    return rows


# ========================================
# ZARZĄDZANIE REZERWACJAMI
# ========================================

def _overlaps(s1, e1, s2, e2) -> bool:
    """
    FUNKCJA POMOCNICZA - SPRAWDZANIE CZY GODZINY SIĘ NAKŁADAJĄ
    
    Sprawdza czy dwa przedziały czasowe nachodzą na siebie.
    Używana do kontroli czy nowa rezerwacja nie koliduje z istniejącą.
    
    Parametry:
    - s1, e1: start i koniec pierwszego przedziału (format "HH:MM")
    - s2, e2: start i koniec drugiego przedziału (format "HH:MM")
    
    Zwraca: True jeśli przedziały się nakładają, False w przeciwnym razie
    
    Przykład:
    _overlaps("10:00", "12:00", "11:00", "13:00") -> True (nakładają się)
    _overlaps("10:00", "11:00", "12:00", "13:00") -> False (nie nakładają się)
    """
    fmt = "%H:%M"  # Format godziny
    
    # Konwertujemy stringi na obiekty datetime dla łatwiejszego porównania
    t1s = datetime.datetime.strptime(s1, fmt)  # start pierwszego przedziału
    t1e = datetime.datetime.strptime(e1, fmt)  # koniec pierwszego przedziału
    t2s = datetime.datetime.strptime(s2, fmt)  # start drugiego przedziału
    t2e = datetime.datetime.strptime(e2, fmt)  # koniec drugiego przedziału
    
    # Sprawdzamy czy przedziały się nakładają
    # Logika: przedziały się nakładają jeśli start jednego jest przed końcem drugiego
    # i start drugiego jest przed końcem pierwszego
    return t1s < t2e and t2s < t1e


def is_available(room_id: int, date: str, start: str, end: str) -> bool:
    """
    SPRAWDZANIE DOSTĘPNOŚCI SALI
    
    Sprawdza czy dana sala jest wolna w określonym terminie.
    Używana przed utworzeniem nowej rezerwacji.
    
    Parametry:
    - room_id: ID sali (z tabeli rooms)
    - date: data w formacie "YYYY-MM-DD"
    - start: godzina rozpoczęcia "HH:MM"  
    - end: godzina zakończenia "HH:MM"
    
    Zwraca: True jeśli sala jest wolna, False jeśli zajęta
    
    Logika:
    1. Pobiera wszystkie istniejące rezerwacje dla danej sali w danym dniu
    2. Sprawdza czy nowy termin nakłada się z którąkolwiek z istniejących rezerwacji
    3. Jeśli tak - sala zajęta, jeśli nie - sala wolna
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Pobieramy wszystkie rezerwacje dla tej sali w tym dniu
    cur.execute("SELECT start_time, end_time FROM reservations WHERE room_id=? AND date=?",
                (room_id, date))
    rows = cur.fetchall()
    conn.close()
    
    # Sprawdzamy czy nowy termin koliduje z którąkolwiek istniejącą rezerwacją
    for r in rows:
        if _overlaps(start, end, r['start_time'], r['end_time']):
            return False  # Kolizja znaleziona - sala zajęta
    
    return True  # Brak kolizji - sala wolna


def create_reservation(room_id: int, date: str, start_time: str, end_time: str,
                       user_name: str, password: str, user_email: str, description=None) -> str:
    """
    TWORZENIE NOWEJ REZERWACJI
    
    Główna funkcja odpowiedzialna za utworzenie nowej rezerwacji sali.
    Sprawdza dostępność, zapisuje w bazie i wysyła powiadomienia email.
    
    Parametry:
    - room_id: ID sali do zarezerwowania
    - date: data rezerwacji "YYYY-MM-DD"
    - start_time, end_time: godziny "HH:MM"
    - user_name: imię i nazwisko rezerwującego
    - password: hasło do zarządzania rezerwacją (użytkownik może potem usunąć/edytować)
    - user_email: email rezerwującego (wymagany do powiadomień)
    - description: opcjonalny opis rezerwacji
    
    Zwraca: token rezerwacji (unikalny identyfikator)
    Wyjątki: ValueError jeśli email nieprawidłowy lub sala zajęta
    """
    # WALIDACJA 1: Sprawdzenie czy email jest prawidłowy
    if not user_email or "@" not in user_email:
        raise ValueError("Email jest wymagany")
    
    # WALIDACJA 2: Sprawdzenie czy sala jest dostępna
    if not is_available(room_id, date, start_time, end_time):
        # Sala jest zajęta - wysyłamy powiadomienie o kolizji
        try:
            from email_service import send_collision_notification
            
            # Pobieramy nazwę sali do powiadomienia
            conn = get_connection()
            cur = conn.cursor()
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
        send_reservation_confirmation(user_email, user_name, room_name, date, start_time, end_time, token, password)
        
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
    # Get reservation data before deletion for email notification
    conn = get_connection(); cur = conn.cursor()
    cur.execute("""SELECT r.*, rm.name as room_name 
                   FROM reservations r 
                   JOIN rooms rm ON r.room_id = rm.id 
                   WHERE r.token=?""", (token,))
    res_data = cur.fetchone()
    
    from db import hash_password
    password_hash = hash_password(password)
    cur.execute("DELETE FROM reservations WHERE token=? AND password_hash=?", (token, password_hash))
    ok = cur.rowcount > 0
    conn.commit(); conn.close()
    
    # Send notification to admins if deletion successful
    if ok and res_data:
        print(f"User deletion successful, sending admin notification for user: {res_data['user_name']}")
        try:
            from email_service import send_admin_deletion_notification
            result = send_admin_deletion_notification(
                res_data['user_name'], 
                res_data['room_name'],
                res_data['date'],
                res_data['start_time'],
                res_data['end_time']
            )
            print(f"Admin notification email result: {result}")
        except Exception as e:
            print(f"Email sending failed: {e}")
    else:
        print(f"User deletion failed or no reservation data. ok={ok}, res_data={bool(res_data)}")
    
    return ok


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


def get_active_reservations_for_admin() -> list:
    """
    Funkcja pobiera aktywne rezerwacje (dzisiejsze i przyszłe) 
    dla administratora z formatowaniem do dropdown.
    
    Zwraca listę słowników z danymi rezerwacji przygotowanymi do wyświetlenia.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Pobierz rezerwacje od dzisiaj w przyszłość
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        
        query = """
            SELECT r.token, r.user_name, r.room_id, r.date, 
                   r.start_time, r.end_time, r.description, rm.name as room_name
            FROM reservations r
            LEFT JOIN rooms rm ON r.room_id = rm.id
            WHERE r.date >= ?
            ORDER BY r.date ASC, r.start_time ASC
        """
        
        cursor.execute(query, (today,))
        results = cursor.fetchall()
        
        reservations = []
        for result in results:
            display_text = f"{result[1]} - {result[7] or f'Sala {result[2]}'} - {result[3]} {result[4]}-{result[5]}"
            
            reservations.append({
                'token': result[0],
                'display': display_text,
                'user_name': result[1],
                'room_id': result[2],
                'room_name': result[7] or f'Sala {result[2]}',
                'date': result[3],
                'start_time': result[4],
                'end_time': result[5],
                'description': result[6] or ''
            })
        
        conn.close()
        print(f"Znaleziono {len(reservations)} aktywnych rezerwacji dla administratora")
        return reservations
        
    except Exception as e:
        print(f"Błąd pobierania aktywnych rezerwacji: {e}")
        import traceback
        traceback.print_exc()
        return []


def get_all_admins() -> list:
    """
    Funkcja pobiera listę wszystkich kont administratorów.
    
    Zwraca listę słowników z danymi administratorów (bez haseł).
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, email FROM admins ORDER BY username")
        results = cursor.fetchall()
        
        admins = []
        for result in results:
            admins.append({
                'username': result[0],
                'email': result[1] or 'Brak emaila'
            })
        
        conn.close()
        return admins
        
    except Exception as e:
        print(f"Błąd pobierania listy adminów: {e}")
        return []


def delete_admin_account(username: str, password: str) -> bool:
    """
    Funkcja usuwa konto administratora po weryfikacji hasła.
    
    Parametry:
    - username: nazwa użytkownika do usunięcia
    - password: hasło do weryfikacji
    
    Zwraca True jeśli usunięcie powiodło się, False w przeciwnym razie.
    """
    try:
        from db import hash_password
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Sprawdź czy konto istnieje i hasło jest poprawne
        password_hash = hash_password(password)
        cursor.execute("SELECT username FROM admins WHERE username = ? AND password_hash = ?", 
                      (username, password_hash))
        admin = cursor.fetchone()
        
        if not admin:
            print(f"Nieprawidłowe hasło dla użytkownika {username}")
            conn.close()
            return False
        
        # Usuń konto
        cursor.execute("DELETE FROM admins WHERE username = ?", (username,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        if success:
            print(f"Usunięto konto administratora: {username}")
        else:
            print(f"Nie udało się usunąć konta: {username}")
            
        return success
        
    except Exception as e:
        print(f"Błąd usuwania konta administratora: {e}")
        return False