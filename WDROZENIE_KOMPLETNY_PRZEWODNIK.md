# 🚀 Kompletny przewodnik wdrożenia systemu

## ✅ Zmiany dotyczące słowa "sekretarka"

Wszystkie wystąpienia słowa "sekretarka" zostały zastąpione słowem "admin" w następujących miejscach:
- ✅ `templates/calendar.html` - przyciski "Login Admin" i "Utwórz konto admina"
- ✅ `templates/login.html` - nagłówek "Login Admin"
- ✅ `templates/create_admin.html` - nagłówek "Utwórz konto admina"
- ✅ `email_service.py` - powiadomienia mówią o "administratorze"
- ✅ `app.py` - email domyślny admin@dacpol.eu

## 🖥️ Ikona na pulpicie Windows

### Metoda 1: Skrót do przeglądarki (Zalecane)
1. **Kliknij prawym przyciskiem na pulpit** → "Nowy" → "Skrót"
2. **Wpisz ścieżkę**:
   ```
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=https://web-production-ee2fb.up.railway.app
   ```
   (lub Edge: `"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app=...`)
3. **Nazwa**: "System Rezerwacji Sal - DACPOL"
4. **Zmień ikonę**: Kliknij prawym → "Właściwości" → "Zmień ikonę" → wybierz ikonę kalendarza

### Metoda 2: Plik .url
Utwórz plik `System_Rezerwacji_DACPOL.url` na pulpicie:
```ini
[InternetShortcut]
URL=https://web-production-ee2fb.up.railway.app
IconFile=C:\Windows\System32\shell32.dll
IconIndex=13
```

### Metoda 3: Aplikacja PWA (Progressive Web App)
1. Otwórz stronę w Chrome/Edge
2. Kliknij menu (⋮) → "Zainstaluj aplikację System Rezerwacji..."
3. Automatycznie pojawi się ikona na pulpicie i w menu Start

## 👥 Wielodostęp - Co się dzieje gdy kilka osób korzysta jednocześnie?

### ✅ **System jest w pełni przystosowany do wielodostępu:**

**Zwykli użytkownicy (nie-admini):**
- ✅ Mogą jednocześnie przeglądać kalendarz
- ✅ Mogą tworzyć rezerwacje bez konfliktów
- ✅ Każda rezerwacja ma unikalny ID
- ✅ Baza danych SQLite obsługuje współbieżność

**Administratorzy:**
- ✅ Mogą jednocześnie edytować różne rezerwacje
- ⚠️ Jeśli dwóch adminów edytuje tę samą rezerwację - zostanie zapisana ostatnia zmiana
- ✅ System automatycznie odświeża kalendarz po każdej zmianie

### 🔐 **Logowanie administratorów:**

**Jak działa sesja admin:**
- 🔒 Każda sesja jest **niezależna** dla każdego komputera/przeglądarki
- 🔒 Admin na komputerze A **NIE** loguje automatycznie komputera B
- 🔒 Sesje są przechowywane lokalnie w cookies przeglądarki
- 🔒 Każdy admin musi się zalogować osobno na swoim komputerze

**Przykład:**
- Komputer A: Admin loguje się → tylko komputer A ma uprawnienia
- Komputer B: Ktoś otwiera stronę → widzi interfejs zwykłego użytkownika
- Komputer C: Admin loguje się → tylko komputer C ma uprawnienia

### 🛡️ **Bezpieczeństwo:**
- ✅ Sesje wygasają automatycznie
- ✅ Hasła są zahashowane w bazie danych
- ✅ Każda sesja ma unikalny identyfikator
- ✅ Logout usuwa sesję tylko na danym komputerze

## 📊 **Monitoring wykorzystania:**

```bash
# W przyszłości można dodać logi dostępu w app_railway.py:
import logging
logging.basicConfig(filename='access.log', level=logging.INFO)

@app.before_request
def log_request():
    logging.info(f"{request.remote_addr} - {request.method} {request.path}")
```

## 🚀 **Deployment zmiany na Railway:**

Aby wdrożyć aktualne zmiany:
```bash
git add .
git commit -m "Remove all references to 'sekretarka', replace with 'admin'"
git push origin main
```

Railway automatycznie wykona redeploy w ciągu 1-2 minut.

## 📧 **Status powiadomień email:**
- 🔧 Lokalnie: Skonfigurowane dla poczta.dacpol.eu
- ⚠️ Produkcja: Wyłączone (można włączyć Gmail SMTP)
- 📝 Instrukcje Gmail SMTP w pliku `GMAIL_SMTP_SETUP.md`

## 🎯 **System gotowy do pracy!**
- ✅ Wszystkie referencje do "sekretarka" zostały usunięte
- ✅ Wielodostęp działa prawidłowo
- ✅ Sesje admina są bezpieczne i niezależne
- ✅ Można utworzyć ikonę na pulpicie
- ✅ System działa 24/7 na Railway
