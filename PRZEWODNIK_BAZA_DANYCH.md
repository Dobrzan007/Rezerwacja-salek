# Przewodnik Zarządzania Bazą Danych

## Aktualna Konfiguracja

✅ **Baza danych została wyczyszczona:**
- Usunięto wszystkie stare rezerwacje (14 pozycji)
- Usunięto wszystkie stare konta adminów (3 konta)

✅ **Utworzono nowe konto administratora:**
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `dsw@dacpol.eu`
- **Powiadomienia:** Wszystkie powiadomienia email będą wysyłane na dsw@dacpol.eu

## Jak Zarządzać Bazą Danych w Przyszłości

### 1. Usuwanie Wszystkich Rezerwacji

```python
# Skrypt do uruchomienia w terminalu:
./venv/Scripts/python.exe -c "
import sqlite3
conn = sqlite3.connect('data/booking.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM reservations')
print(f'Usunięto {cursor.rowcount} rezerwacji')
conn.commit()
conn.close()
"
```

### 2. Usuwanie Wszystkich Kont Adminów

```python
# Skrypt do uruchomienia w terminalu:
./venv/Scripts/python.exe -c "
import sqlite3
conn = sqlite3.connect('data/booking.db')
cursor = conn.cursor()
cursor.execute('DELETE FROM admins')
print(f'Usunięto {cursor.rowcount} kont adminów')
conn.commit()
conn.close()
"
```

### 3. Sprawdzanie Zawartości Bazy Danych

```python
# Skrypt do sprawdzenia co jest w bazie:
./venv/Scripts/python.exe -c "
import sqlite3
conn = sqlite3.connect('data/booking.db')
cursor = conn.cursor()

# Rezerwacje
cursor.execute('SELECT COUNT(*) FROM reservations')
print(f'Rezerwacje: {cursor.fetchone()[0]}')

# Konta adminów
cursor.execute('SELECT username, email FROM admins')
admins = cursor.fetchall()
print('Admini:')
for admin in admins:
    print(f'  {admin[0]} - {admin[1]}')

conn.close()
"
```

### 4. Tworzenie Nowego Konta Administratora

```python
# Skrypt do tworzenia nowego admina:
./venv/Scripts/python.exe -c "
from models import create_admin_with_master_password

success = create_admin_with_master_password(
    username='NAZWA_UZYTKOWNIKA',
    password='HASLO',
    email='EMAIL@dacpol.eu',
    master_password='TWORZENIEKONTA'
)

if success:
    print('✅ Utworzono konto administratora')
else:
    print('❌ Błąd podczas tworzenia konta')
"
```

### 5. Usuwanie Rezerwacji Dla Konkretnej Sali

```python
# Skrypt do usunięcia rezerwacji dla konkretnej sali (np. sala ID=99):
./venv/Scripts/python.exe -c "
import sqlite3
conn = sqlite3.connect('data/booking.db')
cursor = conn.cursor()
room_id = 99  # Zmień na ID sali którą chcesz wyczyścić
cursor.execute('DELETE FROM reservations WHERE room_id = ?', (room_id,))
print(f'Usunięto {cursor.rowcount} rezerwacji dla sali {room_id}')
conn.commit()
conn.close()
"
```

### 6. Backup Bazy Danych

```bash
# Skopiuj plik bazy danych:
copy "data\\booking.db" "data\\booking_backup_$(date +%Y%m%d).db"
```

## Ważne Informacje

🔑 **Master Password:** `TWORZENIEKONTA` (potrzebne do tworzenia nowych kont adminów)

📧 **Email Powiadomień:** `dsw@dacpol.eu` (na ten adres będą wysyłane powiadomienia o usuwaniu rezerwacji przez użytkowników)

🏢 **Sale:** System ma obecnie 7 sal, jeśli dodasz/usuniesz sale w config.json, pamiętaj o restart aplikacji

⚠️ **Uwaga:** Przed usuwaniem danych zawsze sprawdź co jest w bazie danych za pomocą skryptu sprawdzającego zawartość!
