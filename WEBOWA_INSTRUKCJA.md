# 🌐 SYSTEM REZERWACJI SALEK - WERSJA WEBOWA

## 🚀 JAK URUCHOMIĆ (BARDZO PROSTE):

### 1. Dwuklik na `start_server.bat`
- Automatycznie zainstaluje Flask
- Uruchomi serwer na porcie 5000
- Wyświetli adres w konsoli

### 2. Otwórz przeglądarkę i wejdź na:
- **Lokalnie:** `http://localhost:5000`
- **W sieci:** `http://[IP-KOMPUTERA]:5000`

## 🌍 DOSTĘP DLA CAŁEJ FIRMY:

### ✅ **OPCJA A: JEDEN SERWER (POLECANA - WSPÓLNA BAZA DANYCH)**
1. Na jednym komputerze uruchom `start_server.bat`
2. Znajdź IP tego komputera: Otwórz cmd → wpisz `ipconfig`
3. Wszyscy w firmie wchodzą na `http://IP-SERWERA:5000`

**🎯 ZALETY:**
- ✅ Wszyscy widzą te same rezerwacje w czasie rzeczywistym
- ✅ Jedna centralna baza danych
- ✅ Automatyczna synchronizacja
- ✅ Łatwiejsze zarządzanie

**⚠️ UWAGA:**
- Serwer musi być zawsze włączony (Twój komputer)
- Jeśli Twój komputer się wyłączy - nikt nie ma dostępu

### ❌ **OPCJA B: DYSK SIECIOWY (NIE POLECANA)**
1. Skopiuj cały folder na dysk sieciowy
2. Każdy uruchamia `start_server.bat` z dysku sieciowego

**⚠️ PROBLEMY:**
- ❌ Każdy ma osobną bazę danych
- ❌ Brak synchronizacji między użytkownikami
- ❌ Konflikty rezerwacji

## 📱 CO DZIAŁA:

✅ **Kalendarz tygodniowy** - identyczny jak poprzednio  
✅ **7 nazwanych salek** - Sala wideo parter, 2 piętro MAŁA, etc.  
✅ **Tworzenie rezerwacji** z hasłem i obowiązkowym emailem  
✅ **Usuwanie rezerwacji** tylko hasłem (bez tokenów)  
✅ **System administracyjny** - login/logout  
✅ **Powiadomienia email** - do dacpoledi@dacpol.eu  
✅ **Responsywny design** - działa na telefonach/tabletach  
✅ **Automatyczne odświeżanie** kalendarza  

## 🔐 DANE LOGOWANIA:

**Administrator domyślny:**
- Użytkownik: `sekretarka`
- Hasło: `TajneHaslo123`

**Tworzenie nowych adminów:**
- Hasło główne: `TWORZENIEKONTA`

## 🔧 TROUBLESHOOTING:

**Problem: Nie widzą inni w sieci**
1. Sprawdź firewall Windows
2. Dodaj wyjątek dla portu 5000
3. Sprawdź czy antywirus nie blokuje

**Problem: Port 5000 zajęty**
- Edytuj `app.py`, zmień `port=5000` na `port=5555`

**Problem: Błąd przy uruchomieniu**
- Sprawdź czy Python jest zainstalowany (powinien być w folderze venv)
- Upewnij się że masz uprawnienia do folderu

**Problem: Serwer się wyłącza gdy zamykam laptopa**
- Ustaw Windows: Ustawienia → System → Zasilanie → "Gdy zamknę pokrywę: Nie rób nic"
- Lub zostaw komputer włączony 24/7

**Problem: Każdy widzi inne rezerwacje**
- To znaczy że każdy uruchamia aplikację osobno
- Rozwiązanie: Tylko JEDEN komputer ma uruchomioną aplikację

## � STRUKTURA PLIKÓW (PO CZYSZCZENIU):

```
Rezerwacja salek/
├── app.py                 # Główna aplikacja webowa
├── start_server.bat       # Skrypt uruchomieniowy
├── db.py                  # Baza danych
├── models.py              # Logika biznesowa
├── email_service.py       # System powiadomień
├── requirements.txt       # Wymagane pakiety
├── WEBOWA_INSTRUKCJA.md   # Ta instrukcja
├── templates/             # Szablony HTML
│   ├── calendar.html      # Główny kalendarz
│   ├── login.html         # Logowanie adminów
│   └── create_admin.html  # Tworzenie kont
├── data/                  # Baza danych
│   └── booking.db         # SQLite
└── venv/                  # Środowisko Python
```

## 🎉 GOTOWE!

Aplikacja jest gotowa do użycia w sieci firmowej!

**Podsumowanie zmian:**
- ❌ Usunięto wszystkie pliki Tkinter (gui/, main.py, etc.)
- ✅ Zostawiono tylko pliki potrzebne do wersji webowej
- ✅ Jedna instrukcja, jeden sposób uruchomienia
- ✅ Identyczna funkcjonalność, tylko przez przeglądarkę
- ✅ Uproszczone usuwanie - tylko hasło, bez tokenów
- ✅ Email obowiązkowy przy tworzeniu rezerwacji
- ✅ **NOWE:** Centralna konfiguracja w pliku `config.json`

## 🔧 **KONFIGURACJA SYSTEMU:**

**Wszystkie ustawienia w jednym pliku:** `config.json`

- 🏛️ **Nazwy sal** - łatwa edycja listy sal
- 🔐 **Hasła administratorów** - zmiana hasła głównego
- 📧 **Ustawienia email** - SMTP, hasła, odbiorcy
- 🌐 **Port serwera** - jeśli 5000 jest zajęty
- 🏢 **Nazwa firmy** - w tytule systemu

**📖 Szczegółowy przewodnik:** `KONFIGURACJA.md`

**⚠️ UWAGA:** Po zmianach w `config.json` uruchom aplikację ponownie!
