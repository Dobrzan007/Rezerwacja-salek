# 🏢 System Rezerwacji Sal - DACPOL

Zaawansowany system rezerwacji sal konferencyjnych z panelem administracyjnym, automatycznymi powiadomieniami email i responsywnym interfejsem użytkownika.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap-purple.svg)

## 📋 Spis treści
- [✨ Funkcje systemu](#-funkcje-systemu)
- [🚀 Szybki start](#-szybki-start)
- [💻 Uruchomienie lokalne](#-uruchomienie-lokalne)
- [☁️ Deployment na Railway](#️-deployment-na-railway)
- [📁 Struktura projektu](#-struktura-projektu)
- [⚙️ Konfiguracja systemu](#️-konfiguracja-systemu)
- [👤 Zarządzanie administratorami](#-zarządzanie-administratorami)
- [📧 Konfiguracja email](#-konfiguracja-email)
- [🛡️ Bezpieczeństwo](#️-bezpieczeństwo)
- [🔧 API Endpoints](#-api-endpoints)
- [❓ FAQ](#-faq)

---

## ✨ Funkcje systemu

### 👥 **Dla użytkowników:**
- 📅 **Kalendarz rezerwacji** - przejrzyste wyświetlanie wszystkich rezerwacji
- ➕ **Tworzenie rezerwacji** - intuicyjny formularz z walidacją konfliktów
- 📧 **Powiadomienia email** - automatyczne potwierdzenia rezerwacji
- 🗑️ **Usuwanie rezerwacji** - możliwość anulowania własnych rezerwacji
- 📱 **Responsive design** - działa na wszystkich urządzeniach

### 🔐 **Dla administratorów:**
- 👑 **Panel administracyjny** - zaawansowane zarządzanie po zalogowaniu
- ✏️ **Edycja rezerwacji** - możliwość modyfikacji wszystkich parametrów
- 🗑️ **Usuwanie dowolnych rezerwacji** - kontrola nad wszystkimi rezerwacjami
- 📊 **Dropdown aktywnych rezerwacji** - szybki dostęp do edycji
- 👤 **Zarządzanie kontami** - tworzenie i usuwanie innych administratorów
- 📧 **Powiadomienia o aktywności** - informacje o wszystkich akcjach użytkowników

### 🔧 **Techniczne:**
- ⚡ **Sprawdzanie konfliktów** - zapobiega nakładaniu się rezerwacji
- 🔒 **Bezpieczne hasła** - hashowanie SHA-256
- 🎫 **Unikalne tokeny** - każda rezerwacja ma swój identyfikator
- 📧 **Gmail SMTP** - profesjonalne powiadomienia email
- 🗄️ **SQLite** - lokalna baza danych z automatyczną inicjalizacją

---

## 🚀 Szybki start

### Wymagania:
- **Python 3.8+**
- **pip** (menedżer pakietów Python)

### ⬇️ Klonowanie repozytorium:
```bash
git clone https://github.com/Dobrzan007/Rezerwacja-salek.git
cd Rezerwacja-salek
```

---

## 💻 Uruchomienie lokalne

### 1️⃣ **Środowisko wirtualne:**
```bash
# Windows (PowerShell)
python -m venv venv
venv\\Scripts\\Activate.ps1

# Windows (CMD)
python -m venv venv
venv\\Scripts\\activate.bat

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ **Instalacja zależności:**
```bash
pip install -r requirements.txt
```

### 3️⃣ **Konfiguracja (opcjonalna):**
Sprawdź i dostosuj `config.json`:
- Sale konferencyjne
- Ustawienia email SMTP
- Dane administratora

### 4️⃣ **Uruchomienie:**
```bash
python app.py
```

### 5️⃣ **Dostęp:**
- 🌐 **Aplikacja:** http://localhost:5000
- 👤 **Login administratora:** `administrator` / `AdminDacpol2025`

### 6️⃣ **Gotowe skrypty (Windows):**
```bash
start_server.bat      # Uruchomienie serwera
generuj_link.bat      # Generowanie linku do aplikacji
```

---

## ☁️ Deployment na Railway

### 📋 **Przygotowanie:**
1. Utwórz konto na [Railway.app](https://railway.app)
2. Połącz z GitHub
3. Fork tego repozytorium

### 🚀 **Deployment:**
1. **New Project** → Deploy from GitHub repo
2. **Wybierz** `Rezerwacja-salek`
3. **Auto-deploy** - Railway automatycznie wykryje Python i użyje `Procfile`

### ⚙️ **Zmienne środowiskowe Railway:**
```
FLASK_ENV=production
PYTHONUNBUFFERED=1
```

### 🔄 **Różnice produkcyjne:**
- Automatyczne wykrywanie środowiska Railway
- Użycie `config_production.json` w chmurze
- Debug wyłączony w produkcji
- Automatyczne HTTPS i skalowanie

---

## 📁 Struktura projektu

```
📁 Rezerwacja-salek/
├── 🧠 models.py                 # Logika biznesowa i operacje CRUD
├── 🌐 app.py                    # Aplikacja Flask z API endpoints
├── 🌐 app_railway.py            # Wersja dla Railway (identyczna)
├── 🗄️ db.py                     # Operacje bazy danych i narzędzia
├── 📧 email_service.py          # System powiadomień SMTP
├── ⚙️ config.py                 # Klasa zarządzania konfiguracją
├── ⚙️ config.json               # Konfiguracja lokalna (development)
├── ⚙️ config_production.json    # Konfiguracja produkcyjna (Railway)
├── 📦 requirements.txt          # Zależności Python
├── 🚀 Procfile                  # Konfiguracja Railway deployment
├── 🎨 templates/               # Szablony HTML
│   ├── calendar.html            # Główny interfejs kalendarza
│   ├── login.html              # Strona logowania administratora
│   └── create_admin.html       # Panel zarządzania kontami
├── 📊 data/                    # Folder bazy danych
│   └── booking.db              # SQLite database
├── 🔧 start_server.bat         # Skrypt uruchomienia Windows
├── 🔗 generuj_link.bat         # Generator linku aplikacji
└── 📚 README.md                # Ta dokumentacja
```

### 🔍 **Opis kluczowych plików:**

#### **🧠 models.py** - Centrum logiki biznesowej
- **Rezerwacje:** `create_reservation()`, `update_reservation()`, `delete_reservation_with_password()`
- **Administratorzy:** `authenticate_admin()`, `create_admin_with_master_password()`
- **Sale:** `seed_rooms()`, `get_rooms()`, `is_available()`
- **Walidacja:** sprawdzanie konfliktów, walidacja email, hashowanie haseł

#### **🌐 app.py** - Serwer Flask
- **Routes:** `/`, `/api/reservations`, `/login`, `/admin`
- **API:** RESTful endpoints dla operacji CRUD
- **Sesje:** zarządzanie loginami administratorów
- **Templates:** renderowanie interfejsu HTML

#### **⚙️ config.py** - Inteligentna konfiguracja
- **Automatyczne wykrywanie środowiska** (local vs Railway)
- **Ładowanie konfiguracji** z odpowiedniego pliku JSON
- **Tworzenie domyślnej konfiguracji** przy pierwszym uruchomieniu
- **Metody pomocnicze** do dostępu do ustawień

---

## ⚙️ Konfiguracja systemu

### 📊 **Dwa pliki konfiguracyjne - DLACZEGO?**

System automatycznie wybiera odpowiedni plik konfiguracji:

#### **🔧 config.json** - Środowisko lokalne (development)
```json
{
    "server": {
        "debug": true,           # Debug włączony lokalnie
        "port": 5000
    }
}
```

#### **🚀 config_production.json** - Środowisko produkcyjne (Railway)
```json
{
    "server": {
        "debug": false,          # Debug wyłączony w produkcji
        "port": 5000
    }
}
```

**Automatyczne wykrywanie środowiska:**
```python
# W config.py - automatycznie wybiera plik
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT'):
    config_file = 'config_production.json'  # Produkcja
else:
    config_file = 'config.json'             # Lokalne
```

### 🏢 **Konfiguracja sal konferencyjnych:**

```json
{
    "rooms": [
        "Sala wideo parter",
        "Sala obiadowa parter", 
        "Sala wideo 1-piętro",
        "Sala wideo 2-piętro",
        "2 piętro produktowa",
        "2 piętro MAŁA",
        "2 piętro STARY GABINET"
    ]
}
```

**Jak dodać nowe sale:**
1. Edytuj `config.json` (lokalnie) lub `config_production.json` (produkcja)
2. Dodaj nazwy do listy `"rooms"`
3. Restart aplikacji - nowe sale zostaną automatycznie dodane do bazy

### 🏷️ **Branding firmy:**

```json
{
    "company": {
        "name": "DACPOL",
        "system_title": "System Rezerwacji Sal - DACPOL"
    }
}
```

### 📧 **Konfiguracja email:**

```json
{
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "use_tls": true,
        "sender_email": "daspolrezerwacjesalek@gmail.com",
        "sender_password": "wenu zrdg lktq duqf",
        "recipient_email": "dacpoledi@dacpol.eu",
        "sender_name": "System Rezerwacji Sal - DACPOL"
    }
}
```

---

## 👤 Zarządzanie administratorami

### 🔑 **Hasło główne: `TWORZENIEKONTA`**

To specjalne hasło zabezpiecza tworzenie nowych kont administratorów:

```json
{
    "admin": {
        "master_password": "TWORZENIEKONTA",
        "default_admin": {
            "username": "administrator",
            "password": "AdminDacpol2025",
            "email": "admin@dacpol.eu"
        }
    }
}
```

### 📋 **Domyślne konto administratora:**
- **Login:** `administrator`
- **Hasło:** `AdminDacpol2025`
- **Email:** `admin@dacpol.eu`

### ➕ **Tworzenie nowych administratorów:**

1. **Zaloguj się** jako administrator
2. **Przejdź** do "Zarządzaj kontami administratorów"
3. **Wypełnij formularz:**
   - Nazwa użytkownika (unikalna)
   - Hasło (min. 4 znaki)
   - Email (do powiadomień)
   - **Hasło główne:** `TWORZENIEKONTA` ⚠️ **WYMAGANE!**
4. **Kliknij** "Utwórz konto"

### 🔄 **Funkcje w kodzie:**

```python
# W models.py
def create_admin_with_master_password(username, password, email, master_password):
    """Tworzy nowego administratora z walidacją hasła głównego"""
    if master_password != config.get_master_password():
        return None, "Nieprawidłowe hasło główne"
    # ... reszta logiki
```

### 🗑️ **Usuwanie administratorów:**
- Panel administratorów → "Usuń" przy wybranym koncie
- ⚠️ **Zabezpieczenie:** Nie można usunąć ostatniego administratora

---

## 📧 Konfiguracja email

### 🔧 **Gmail SMTP - przewodnik krok po kroku:**

#### 1️⃣ **Włącz weryfikację dwuetapową:**
- Przejdź do [Google Account Security](https://myaccount.google.com/security)
- Włącz "2-Step Verification"

#### 2️⃣ **Wygeneruj App Password:**
- W ustawieniach Google → Security → 2-Step Verification
- Scroll down → App passwords
- Select app: "Mail", Device: "Other" → wpisz "System Rezerwacji"
- **Skopiuj 16-znakowy kod** (np: `wenu zrdg lktq duqf`)

#### 3️⃣ **Skonfiguruj w aplikacji:**
```json
{
    "email": {
        "sender_email": "twoj-email@gmail.com",
        "sender_password": "wenu zrdg lktq duqf",  # App Password!
        "recipient_email": "admin@firma.com"
    }
}
```

### 📬 **Typy powiadomień email:**

| Typ powiadomienia | Odbiorca | Trigger |
|-------------------|----------|---------|
| 🎉 **Potwierdzenie rezerwacji** | Użytkownik | Po utworzeniu rezerwacji |
| 🔔 **Powiadomienie administratora** | Wszyscy adminowie | Nowa rezerwacja |
| ⚠️ **Kolizja terminów** | Użytkownik | Sala zajęta |
| ✏️ **Edycja rezerwacji** | Użytkownik | Po zmianie przez admina |
| 🗑️ **Usunięcie przez użytkownika** | Administratorzy | Anulowanie rezerwacji |
| 🗑️ **Usunięcie przez admina** | Użytkownik | Admin anulował |

### 📧 **Przykład emaila potwierdzenia:**

```
Temat: Potwierdzenie rezerwacji sali

Witaj Jan Kowalski!

Twoja rezerwacja została pomyślnie utworzona:

🏢 Sala: Sala wideo parter
📅 Data: 15.08.2025
⏰ Godzina: 10:00 - 12:00
🎫 Token: A7X9M2
🔑 Hasło do usunięcia: ****** (ukryte)

Aby anulować rezerwację, użyj tokena: A7X9M2

Pozdrawiam,
System Rezerwacji Sal - DACPOL
```

---

## 🛡️ Bezpieczeństwo

### 🔐 **Hashowanie haseł:**
```python
# W db.py
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
```
- **SHA-256** - silne hashowanie jednostronne
- **Hasła nigdy nie są przechowywane w czystym tekście**
- **Sól systemowa** - dodatkowa ochrona

### 🎫 **System tokenów:**
```python
# W db.py
def generate_token():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
```
- **6-znakowe alfanumeryczne ID** (np: "A7X9M2")
- **Unikalne dla każdej rezerwacji**
- **Używane do usuwania przez użytkowników**

### 👑 **Kontrola dostępu administratorów:**
```python
# W app.py
@app.route('/admin')
def admin_panel():
    if not session.get('is_admin'):
        return redirect(url_for('login'))
    # ... reszta kodu
```

### 🔑 **Master password:**
- **Hasło główne** (`TWORZENIEKONTA`) chroni tworzenie administratorów
- **Dodatkowa warstwa bezpieczeństwa** nawet po włamaniu do konta admin
- **Konfigurowalne** w pliku konfiguracji

### 📧 **Bezpieczeństwo email:**
- **App Passwords** zamiast zwykłych haseł Gmail
- **TLS encryption** dla połączeń SMTP
- **Walidacja formatów email**

---

## 🔧 API Endpoints

### 🏠 **Główne strony:**
```http
GET  /                          # Strona główna z kalendarzem
GET  /login                     # Strona logowania administratora
GET  /admin                     # Panel zarządzania kontami (admin only)
```

### 📅 **API Rezerwacji:**
```http
GET    /api/rooms               # Lista wszystkich sal
GET    /api/reservations        # Wszystkie rezerwacje
POST   /api/reservations        # Tworzenie nowej rezerwacji
PUT    /api/reservations/<token> # Edycja rezerwacji (admin only)
DELETE /api/reservations/<token> # Usuwanie rezerwacji
GET    /api/reservations/active # Aktywne rezerwacje (dropdown admin)
```

### 👤 **API Autoryzacji:**
```http
POST   /login                   # Logowanie administratora
GET    /logout                  # Wylogowanie
POST   /admin/create            # Tworzenie nowego administratora
DELETE /admin/delete/<username> # Usuwanie konta administratora
```

### 📝 **Przykład API - Tworzenie rezerwacji:**

**Request:**
```bash
curl -X POST http://localhost:5000/api/reservations \\
  -H "Content-Type: application/json" \\
  -d '{
    "room_id": 1,
    "date": "2025-08-15",
    "start_time": "10:00",
    "end_time": "12:00",
    "user_name": "Jan Kowalski",
    "password": "mojhaslo123",
    "email": "jan@email.com"
  }'
```

**Response (sukces):**
```json
{
  "success": true,
  "message": "Rezerwacja utworzona pomyślnie",
  "token": "A7X9M2"
}
```

**Response (błąd - sala zajęta):**
```json
{
  "success": false,
  "message": "Sala jest już zarezerwowana w tym terminie"
}
```

---

## ❓ FAQ

### ❔ **Nie mogę się zalogować jako administrator**
- **Sprawdź dane:** `administrator` / `AdminDacpol2025`
- **Upewnij się** że baza danych została zainicjalizowana (uruchom aplikację raz)
- **Sprawdź** czy plik `config.json` zawiera prawidłowe dane administratora

### ❔ **Nie przychodzą emaile**
1. **Gmail App Password** - sprawdź czy używasz 16-znakowego kodu, nie zwykłego hasła
2. **2FA** - upewnij się że weryfikacja dwuetapowa jest włączona
3. **Folder SPAM** - sprawdź skrzynkę odbiorczą
4. **Logi aplikacji** - sprawdź terminal czy są błędy SMTP
5. **Email enabled** - upewnij się że `"enabled": true` w konfiguracji

### ❔ **Jak dodać nowe sale konferencyjne?**
1. **Edytuj konfigurację:**
   - Lokalnie: `config.json` → sekcja `"rooms"`
   - Produkcja: `config_production.json` → sekcja `"rooms"`
2. **Dodaj nazwy** do listy (np: `"Nowa sala"`)
3. **Restart aplikacji** - nowe sale zostaną automatycznie dodane do bazy
4. **Sprawdź** w formularzu rezerwacji czy pojawiły się nowe opcje

### ❔ **Zapomniałem hasła głównego**
- **Sprawdź konfigurację:** `config.json` → `"admin"` → `"master_password"`
- **Domyślnie:** `TWORZENIEKONTA`
- **Aby zmienić:** edytuj plik konfiguracji i restart aplikacji

### ❔ **Jak zmienić port aplikacji?**
1. **Edytuj konfigurację:** `"server"` → `"port": 8080`
2. **Restart aplikacji**
3. **Nowy adres:** `http://localhost:8080`

### ❔ **Konflikt portów na Railway**
Railway automatycznie przydziela port z zmiennej środowiskowej `PORT` - nie trzeba nic zmieniać.

### ❔ **Jak zrobić backup bazy danych?**
```bash
# Kopia pliku bazy
cp data/booking.db data/backup_$(date +%Y%m%d_%H%M%S).db

# Windows
copy "data\\booking.db" "data\\backup_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db"
```

### ❔ **Jak wyczyścić wszystkie rezerwacje?**
⚠️ **UWAGA: To usunie wszystkie dane!**
```bash
# Usuń bazę danych
rm data/booking.db

# Windows
del "data\\booking.db"

# Restart aplikacji - baza zostanie utworzona na nowo
python app.py
```

### ❔ **Różnica między config.json a config_production.json**
- **config.json** - używany lokalnie (development)
  - `debug: true` - szczegółowe logi błędów
  - Różne ustawienia testowe
- **config_production.json** - używany na Railway (produkcja)
  - `debug: false` - bezpieczniejsze logi
  - Optymalizacja dla produkcji
- **Automatyczne wykrywanie** przez `config.py` na podstawie zmiennych środowiskowych

### ❔ **Aplikacja nie startuje**
1. **Sprawdź Python:** `python --version` (min. 3.8)
2. **Zainstaluj zależności:** `pip install -r requirements.txt`
3. **Sprawdź porty:** czy port 5000 nie jest zajęty
4. **Sprawdź logi:** uruchom `python app.py` i sprawdź błędy
5. **Sprawdź konfigurację:** czy pliki JSON są prawidłowe

---



## 📄 Licencja

Projekt open-source. Możesz swobodnie używać, modyfikować i dystrybuować zgodnie z potrzebami.

---

**🎉 Dziękujemy za korzystanie z Systemu Rezerwacji Sal DACPOL!**

*System utworzony dla firmy DACPOL - sierpień 2025*
