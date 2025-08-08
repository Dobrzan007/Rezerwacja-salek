# 🏢 System Rezerwacji Sal - DACPOL

> **Profesjonalny system zarządzania rezerwacjami sal konferencyjnych z automatycznymi powiadomieniami email**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3.0+-lightgrey.svg)](https://sqlite.org)
[![Gmail SMTP](https://img.shields.io/badge/Gmail-SMTP-red.svg)](https://mail.google.com)

## 📋 Spis treści
- [🎯 Opis systemu](#-opis-systemu)
- [✨ Funkcjonalności](#-funkcjonalności)
- [🛠️ Instalacja i uruchomienie](#️-instalacja-i-uruchomienie)
- [📧 Konfiguracja email](#-konfiguracja-email)
- [🏗️ Architektura systemu](#️-architektura-systemu)
- [📁 Struktura projektu](#-struktura-projektu)
- [🌐 Deployment na Railway](#-deployment-na-railway)
- [🔧 Konfiguracja](#-konfiguracja)
- [🧪 Testowanie](#-testowanie)
- [📖 API Dokumentacja](#-api-dokumentacja)
- [🔒 Bezpieczeństwo](#-bezpieczeństwo)
- [🐛 Rozwiązywanie problemów](#-rozwiązywanie-problemów)

---

## 🎯 Opis systemu

**System Rezerwacji Sal - DACPOL** to nowoczesna aplikacja webowa stworzona specjalnie dla firmy DACPOL do zarządzania rezerwacjami sal konferencyjnych. System oferuje intuicyjny interfejs kalendarza, automatyczne powiadomienia email oraz zaawansowane funkcje administracyjne.

### 🎯 **Główne cele systemu:**
- **Centralizacja rezerwacji** - wszystkie rezerwacje w jednym miejscu
- **Automatyzacja powiadomień** - email notifications dla użytkowników i adminów
- **Łatwość użytkowania** - intuicyjny kalendarz z drag&drop
- **Responsywność** - działa na wszystkich urządzeniach (desktop, tablet, mobile)
- **Bezpieczeństwo** - system uprawnień i walidacji

---

## ✨ Funkcjonalności

### 👥 **Dla użytkowników:**
- 📅 **Kalendarz rezerwacji** - wizualizacja dostępności sal
- ➕ **Łatwe rezerwowanie** - formularz z walidacją konfliktów
- 📧 **Powiadomienia email** - automatyczne potwierdzenia
- ✏️ **Edycja rezerwacji** - możliwość modyfikacji (tylko własnych)
- 🗑️ **Anulowanie rezerwacji** - z hasłem bezpieczeństwa
- 📱 **Responsywny design** - działa na wszystkich urządzeniach

### 👨‍💼 **Dla administratorów:**
- 🔐 **Panel administratora** - zaawansowane zarządzanie
- 👀 **Podgląd wszystkich rezerwacji** - pełny przegląd systemu
- ✏️ **Edycja dowolnych rezerwacji** - bez ograniczeń
- 🗑️ **Usuwanie rezerwacji** - z prawami administratora
- 📧 **Powiadomienia o wszystkich aktywnościach** - email alerts
- 👥 **Zarządzanie kontami** - tworzenie nowych adminów

### 📧 **System email (5 typów powiadomień):**
1. **Potwierdzenie rezerwacji** - dla użytkownika
2. **Powiadomienie administratora** - o nowej rezerwacji
3. **Powiadomienie o edycji** - dla użytkownika i admina
4. **Powiadomienie o usunięciu** - dla użytkownika i admina
5. **Alert o konflikcie** - ostrzeżenie przed dublowaniem

---

## 🛠️ Instalacja i uruchomienie

### 📋 **Wymagania systemowe:**
- **Python 3.7+** 
- **pip** (menedżer pakietów Python)
- **Konto Gmail** z hasłem aplikacji (dla email)
- **Dostęp do internetu** (dla SMTP Gmail)

### 🚀 **Szybki start:**

```bash
# 1. Sklonuj repozytorium
git clone https://github.com/Dobrzan007/Rezerwacja-salek.git
cd "Rezerwacja salek"

# 2. Utwórz środowisko wirtualne
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Zainstaluj zależności
pip install -r requirements.txt

# 4. Uruchom aplikację
python app.py
```

### 📂 **Alternatywnie - użyj skryptu Windows:**
```bash
# Kliknij dwukrotnie plik:
start_server.bat
```

### 🌐 **Dostęp do aplikacji:**
- **Lokalnie**: http://localhost:5000
- **W sieci LAN**: http://[IP-KOMPUTERA]:5000
- **Generator linku**: Uruchom `generuj_link.bat`

---

## 📧 Konfiguracja email

### 🔧 **Konfiguracja Gmail SMTP:**

1. **Włącz 2FA w Gmail** (dwuetapowa weryfikacja)
2. **Wygeneruj hasło aplikacji:**
   - Idź do: https://myaccount.google.com/apppasswords
   - Wybierz "Mail" i "Windows Computer"
   - Skopiuj wygenerowane hasło (16 znaków)

3. **Skonfiguruj pliki config:**

```json
{
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "use_tls": true,
        "sender_email": "twoj-email@gmail.com",
        "sender_password": "haslo-aplikacji-16-znakow",
        "recipient_email": "admin@twoja-firma.com",
        "sender_name": "System Rezerwacji Sal - DACPOL"
    }
}
```

### 🧪 **Test konfiguracji email:**
```bash
python test_email.py          # Pełny test systemu
python test_gmail_simple.py   # Prosty test SMTP
```

---

## 🏗️ Architektura systemu

### 📊 **Stack technologiczny:**
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Email**: Gmail SMTP
- **Deployment**: Railway (Production) + Local Development

### 🏗️ **Wzorzec architektury:**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│     Flask       │───▶│    SQLite       │
│   (Templates)   │    │   (Backend)     │    │   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                       ┌─────────────────┐
                       │   Gmail SMTP    │
                       │   (Email)       │
                       └─────────────────┘
```

### 🔄 **Flow aplikacji:**
1. **Użytkownik** otwiera kalendarz ➜ `templates/calendar.html`
2. **JavaScript** wysyła AJAX request ➜ `app.py` routes
3. **Flask** przetwarza dane ➜ `models.py` business logic
4. **Models** operują na bazie ➜ `db.py` SQLite operations
5. **Email service** wysyła powiadomienia ➜ `email_service.py`
6. **Response** wraca do użytkownika ➜ JSON/HTML

---

## 📁 Struktura projektu

```
Rezerwacja salek/
├── 📱 Frontend & Templates
│   ├── templates/
│   │   ├── calendar.html          # Główny interfejs kalendarza
│   │   ├── login.html             # Formularz logowania
│   │   └── create_admin.html      # Tworzenie konta admin
│   └── static/ (zawarte w templates)
│
├── 🐍 Backend Core
│   ├── app.py                     # Główny plik aplikacji (development)
│   ├── app_railway.py             # Wersja dla Railway (production)
│   ├── models.py                  # Business logic i operacje DB
│   ├── db.py                      # Operacje bazodanowe SQLite
│   ├── email_service.py           # Serwis obsługi email
│   └── config.py                  # Zarządzanie konfiguracją
│
├── ⚙️ Konfiguracja
│   ├── config.json                # Konfiguracja development
│   ├── config_production.json     # Konfiguracja production
│   ├── requirements.txt           # Zależności Python
│   └── Procfile                   # Konfiguracja Railway
│
├── 🗄️ Dane
│   └── data/
│       └── booking.db             # Baza danych SQLite
│
├── 🧪 Testy
│   ├── test_email.py              # Test systemu email
│   └── test_gmail_simple.py       # Prosty test SMTP
│
├── 🛠️ Narzędzia
│   ├── start_server.bat           # Uruchomienie serwera (Windows)
│   ├── generuj_link.bat           # Generator linku LAN
│   └── System_Rezerwacji_Salek.url # Skrót do aplikacji
│
└── 📄 Dokumentacja
    └── README.md                  # Ten plik
```

---

## 🌐 Deployment na Railway

### 🚂 **Automatyczny deployment:**

1. **Połącz z GitHub:**
   - Zaloguj się na [Railway.app](https://railway.app)
   - Połącz z repozytorium GitHub
   - Railway automatycznie wykryje Python i Flask

2. **Konfiguracja środowiska:**
   ```bash
   # Railway automatycznie ustawia:
   PORT=5000
   RAILWAY_ENVIRONMENT=production
   ```

3. **Pliki produkcyjne:**
   - `Procfile` - definiuje command startowy
   - `app_railway.py` - wersja production
   - `config_production.json` - konfiguracja production

### 🔧 **Zarządzanie środowiskami:**
```python
# Automatyczne wykrywanie środowiska:
is_production = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT')
if is_production:
    config_file = 'config_production.json'
else:
    config_file = 'config.json'
```

---

## 🔧 Konfiguracja

### 📝 **Plik config.json (Development):**
```json
{
    "company": {
        "name": "DACPOL",
        "system_title": "System Rezerwacji Sal - DACPOL"
    },
    "rooms": [
        "Sala wideo parter",
        "Sala obiadowa parter", 
        "Sala wideo 1-piętro",
        "Sala wideo 2-piętro",
        "2 piętro produktowa",
        "2 piętro MAŁA",
        "2 piętro STARY GABINET"
    ],
    "admin": {
        "master_password": "TWORZENIEKONTA",
        "default_admin": {
            "username": "administrator",
            "password": "AdminDacpol2025",
            "email": "admin@dacpol.eu"
        }
    },
    "email": {
        "enabled": true,
        "smtp_server": "smtp.gmail.com",
        "smtp_port": 587,
        "use_tls": true,
        "sender_email": "daspolrezerwacjesalek@gmail.com",
        "sender_password": "wenu zrdg lktq duqf",
        "recipient_email": "dacpoledi@dacpol.eu",
        "sender_name": "System Rezerwacji Sal - DACPOL"
    },
    "server": {
        "host": "0.0.0.0",
        "port": 5000,
        "debug": true
    },
    "security": {
        "session_secret": "super-secret-key-change-me-in-production",
        "password_min_length": 4
    }
}
```

### 🏭 **Różnice Production vs Development:**
| Ustawienie | Development | Production |
|------------|-------------|------------|
| Debug mode | `true` | `false` |
| Email logging | Verbose | Essential only |
| Error handling | Full stack trace | User-friendly messages |
| Session secret | Simple | Strong random key |

---

## 🧪 Testowanie

### 📧 **Test systemu email:**
```bash
# Pełny test systemu email
python test_email.py

# Prosty test połączenia SMTP
python test_gmail_simple.py
```

### 🔧 **Test funkcjonalności:**
1. **Test rezerwacji:**
   - Utwórz nową rezerwację
   - Sprawdź czy email został wysłany
   - Zweryfikuj zapis w bazie danych

2. **Test konfliktów:**
   - Spróbuj zarezerwować tę samą salę w tym samym czasie
   - System powinien ostrzec o konflikcie

3. **Test responsywności:**
   - Otwórz na różnych urządzeniach
   - Sprawdź modals na małych ekranach

### 🐛 **Debug mode:**
```python
# Włącz debug w config.json
"debug": true

# Lub przez environment
export FLASK_DEBUG=1
```

---

## 📖 API Dokumentacja

### 🌍 **Endpoints główne:**

#### 📅 **GET /** - Strona główna
```http
GET /
Returns: calendar.html template
```

#### 🏢 **GET /api/rooms** - Lista sal
```http
GET /api/rooms
Returns: [
    {"id": 1, "name": "Sala wideo parter"},
    {"id": 2, "name": "Sala obiadowa parter"}
]
```

#### 📋 **GET /api/reservations** - Rezerwacje
```http
GET /api/reservations?start_date=2024-01-01&end_date=2024-01-31
Returns: [
    {
        "id": 1,
        "room_name": "Sala wideo parter",
        "start_time": "2024-01-15 14:00",
        "end_time": "2024-01-15 16:00",
        "title": "Meeting zespołu",
        "description": "Planowanie sprintu",
        "created_by": "Jan Kowalski",
        "token": "abc123def456"
    }
]
```

#### ➕ **POST /api/reservations** - Nowa rezerwacja
```http
POST /api/reservations
Content-Type: application/x-www-form-urlencoded

room_id=1&start_time=2024-01-15 14:00&end_time=2024-01-15 16:00&title=Meeting&description=Opis&created_by=Jan Kowalski&password=haslo123

Returns: {"success": true, "token": "abc123def456"}
```

#### ❌ **DELETE /api/reservations** - Usuń rezerwację
```http
DELETE /api/reservations
Content-Type: application/x-www-form-urlencoded

token=abc123def456&password=haslo123

Returns: {"success": true}
```

### 🔐 **Endpoints administratora:**

#### 🔑 **POST /api/admin/login** - Logowanie admin
```http
POST /api/admin/login
Content-Type: application/x-www-form-urlencoded

username=administrator&password=AdminDacpol2025

Returns: {"success": true}
```

#### 👥 **POST /api/admin/create** - Utwórz konto admin
```http
POST /api/admin/create
Content-Type: application/x-www-form-urlencoded

master_password=TWORZENIEKONTA&username=nowy_admin&password=NoweHaslo123

Returns: {"success": true}
```

---

## 🔒 Bezpieczeństwo

### 🛡️ **Zabezpieczenia wdrożone:**

1. **Hashowanie haseł** - bcrypt dla haseł administratorów
2. **Session management** - Flask sessions z secret key
3. **CSRF protection** - tokeny dla krytycznych operacji
4. **Input validation** - walidacja wszystkich danych wejściowych
5. **SQL Injection protection** - parametryzowane zapytania
6. **Password complexity** - minimalna długość haseł
7. **Rate limiting** - ograniczenia zapytań (na poziomie infrastruktury)

### 🔐 **Hasła w systemie:**
- **Master password**: `TWORZENIEKONTA` (tworzenie adminów)
- **Default admin**: `administrator` / `AdminDacpol2025`
- **User passwords**: Dowolne (min. 4 znaki) dla rezerwacji

### 📧 **Email security:**
- **Gmail App Password** - bezpieczne hasło aplikacji
- **TLS encryption** - szyfrowane połączenie SMTP
- **No credential storage** - hasła w config (nie w kodzie)

---

## 🐛 Rozwiązywanie problemów

### ❗ **Częste problemy i rozwiązania:**

#### 📧 **Problem: Email nie wysyła się**
```bash
# 1. Sprawdź konfigurację
python test_email.py

# 2. Sprawdź hasło aplikacji Gmail
# Idź do: https://myaccount.google.com/apppasswords
# Wygeneruj nowe hasło

# 3. Sprawdź czy 2FA jest włączone w Gmail
```

#### 🗄️ **Problem: Baza danych nie działa**
```bash
# 1. Sprawdź czy katalog data/ istnieje
mkdir data

# 2. Usuń bazę i pozwól systemowi odtworzyć
rm data/booking.db
python app.py
```

#### 🌐 **Problem: Aplikacja niedostępna w sieci**
```bash
# 1. Sprawdź firewall Windows
# Dodaj wyjątek dla Python/Flask na port 5000

# 2. Sprawdź IP komputera
ipconfig
# Użyj http://[IP]:5000

# 3. Użyj generator linku
generuj_link.bat
```

#### 📱 **Problem: Modal nie działa na mobile**
- Sprawdź czy masz najnowszą wersję z responsywnym CSS
- Wyczyść cache przeglądarki
- Przetestuj na różnych urządzeniach

### 🔧 **Debug i logi:**

#### Włącz tryb debug:
```json
// config.json
"server": {
    "debug": true
}
```

#### Sprawdź logi email:
```python
# W models.py znajdziesz szczegółowe logi email
print(f"Email sending failed: {e}")
```

#### Sprawdź statusy HTTP:
- `200` - OK
- `400` - Błąd walidacji danych
- `401` - Brak autoryzacji
- `403` - Brak uprawnień
- `500` - Błąd serwera

---

## 📞 Wsparcie

### 🛠️ **Pomoc techniczna:**
- **GitHub Issues**: [Rezerwacja-salek/issues](https://github.com/Dobrzan007/Rezerwacja-salek/issues)
- **Email**: daspolrezerwacjesalek@gmail.com
- **Dokumentacja kodu**: Komentarze w języku polskim

### 📋 **Lista zadań / TODO:**
- [ ] Dodanie notyfikacji push
- [ ] Eksport do kalendarza (iCal)
- [ ] API dla aplikacji mobilnej
- [ ] Integracja z Outlook Calendar
- [ ] System raportowania statystyk

---

## 📄 Licencja

**System Rezerwacji Sal - DACPOL** jest własnością firmy DACPOL i przeznaczony do użytku wewnętrznego.

---

## 🎉 Autorzy

- **Główny Developer**: Mateusz Dobrzański
- **Firma**: DACPOL
- **Rok**: 2024-2025

---

*📅 System Rezerwacji Sal - DACPOL | Wersja 2.0 | Ostatnia aktualizacja: Styczeń 2025*
