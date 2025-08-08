# 📧 SYSTEM POWIADOMIEŃ EMAIL - DACPOL

## ✅ **SYSTEM JEST AKTYWNY!**

System powiadomień email został pomyślnie skonfigurowany i jest gotowy do użycia w produkcji.

---

## 🔧 **KONFIGURACJA GMAIL SMTP**

### **Aktywne ustawienia:**
```json
{
  "email": {
    "enabled": true,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "use_tls": true,
    "sender_email": "dobrzanski.mateusz05@gmail.com",
    "sender_password": "uccb qatu vekh gppu",
    "recipient_email": "dacpoledi@dacpol.eu",
    "sender_name": "System Rezerwacji Sal - DACPOL"
  }
}
```

### **Bezpieczeństwo:**
- ✅ Używa App Password zamiast głównego hasła Gmail
- ✅ Połączenie szyfrowane TLS
- ✅ Sprawdzone i przetestowane

---

## 📬 **RODZAJE POWIADOMIEŃ EMAIL**

### **1. 🎉 POTWIERDZENIE NOWEJ REZERWACJI**

**Kto otrzymuje:** Osoba, która utworzyła rezerwację  
**Kiedy:** Natychmiast po utworzeniu rezerwacji  

**Przykład treści:**
```
TEMAT: Potwierdzenie rezerwacji sali

Witaj Jan Kowalski!

Twoja rezerwacja została pomyślnie utworzona:

🏢 Sala: Sala wideo parter
📅 Data: 2025-08-08
⏰ Czas: 09:00 - 10:00
📋 Opis: Spotkanie z klientem ABC
🔑 Token: ABC123XYZ

WAŻNE: Zapisz token - będzie potrzebny do edycji/usunięcia rezerwacji!

Pozdrawiamy,
System Rezerwacji Sal - DACPOL
```

### **2. 🔔 POWIADOMIENIE DLA ADMINISTRATORÓW**

**Kto otrzymuje:** Wszyscy administratorzy systemu  
**Kiedy:** Natychmiast po utworzeniu każdej rezerwacji  

**Przykład treści:**
```
TEMAT: Nowa rezerwacja w systemie DACPOL

Nowa rezerwacja została utworzona:

👤 Użytkownik: Jan Kowalski
📧 Email: jan.kowalski@dacpol.eu
🏢 Sala: Sala wideo parter
📅 Data: 2025-08-08
⏰ Czas: 09:00 - 10:00
📋 Opis: Spotkanie z klientem ABC

System Rezerwacji Sal - DACPOL
```

### **3. ✏️ POWIADOMIENIE O EDYCJI REZERWACJI**

**Kto otrzymuje:** Osoba, której rezerwacja została zmodyfikowana  
**Kiedy:** Po edycji rezerwacji przez administratora  

**Przykład treści:**
```
TEMAT: Twoja rezerwacja została zmodyfikowana

Witaj Jan Kowalski!

Twoja rezerwacja została zmodyfikowana przez administratora:

POPRZEDNIE DANE:
🏢 Sala: Sala wideo parter
📅 Data: 2025-08-08
⏰ Czas: 09:00 - 10:00

NOWE DANE:
🏢 Sala: Sala wideo 1-piętro
📅 Data: 2025-08-08
⏰ Czas: 10:00 - 11:00
📋 Opis: Spotkanie z klientem ABC - przeniesione

Pozdrawiamy,
System Rezerwacji Sal - DACPOL
```

### **4. 🗑️ POWIADOMIENIE O USUNIĘCIU REZERWACJI**

**Kto otrzymuje:** Osoba, której rezerwacja została usunięta przez admina  
**Kiedy:** Po usunięciu rezerwacji przez administratora  

**Przykład treści:**
```
TEMAT: Twoja rezerwacja została usunięta

Witaj Jan Kowalski!

Twoja rezerwacja została usunięta przez administratora:

🏢 Sala: Sala wideo parter
📅 Data: 2025-08-08
⏰ Czas: 09:00 - 10:00

Jeśli to pomyłka, skontaktuj się z administratorem.

Pozdrawiamy,
System Rezerwacji Sal - DACPOL
```

### **5. ⚠️ POWIADOMIENIE O KONFLIKCIE TERMINU**

**Kto otrzymuje:** Osoba próbująca zarezerwować zajęty termin  
**Kiedy:** Gdy próbuje zarezerwować już zajętą salę  

**Przykład treści:**
```
TEMAT: Nie można utworzyć rezerwacji - termin zajęty

Witaj Jan Kowalski!

Nie udało się utworzyć rezerwacji:

🏢 Sala: Sala wideo parter
📅 Data: 2025-08-08
⏰ Czas: 09:00 - 10:00

PRZYCZYNA: Sala jest już zarezerwowana w tym czasie.

Spróbuj wybrać inny termin lub salę.

Pozdrawiamy,
System Rezerwacji Sal - DACPOL
```

---

## 🎯 **ADRESY EMAIL**

### **Nadawca:**
- **Email:** dobrzanski.mateusz05@gmail.com
- **Nazwa:** System Rezerwacji Sal - DACPOL

### **Administratorzy otrzymujący powiadomienia:**
- **Główny:** dacpoledi@dacpol.eu
- **Dodatkowi:** Wszyscy adminowie z kont w systemie

---

## 🔄 **AUTOMATYZACJA PROCESU**

### **Tworzenie rezerwacji:**
```
1. Użytkownik wypełnia formularz
2. System sprawdza dostępność
3. Tworzy rezerwację w bazie danych
4. Wysyła email potwierdzenia do użytkownika
5. Wysyła powiadomienie do wszystkich adminów
6. Odświeża kalendarz
```

### **Edycja rezerwacji (admin):**
```
1. Admin modyfikuje rezerwację
2. System sprawdza nową dostępność
3. Zapisuje zmiany w bazie danych
4. Wysyła email o zmianie do pierwotnego użytkownika
5. Odświeża kalendarz
```

### **Usunięcie rezerwacji:**
```
- PRZEZ UŻYTKOWNIKA: Brak emaila (usuwa swoje)
- PRZEZ ADMINA: Email o usunięciu do pierwotnego użytkownika
```

---

## 🛠️ **ZARZĄDZANIE SYSTEMEM EMAIL**

### **Włączanie/Wyłączanie:**
W pliku `config.json` lub `config_production.json`:
```json
"email": {
  "enabled": true    // true = włączone, false = wyłączone
}
```

### **Zmiana ustawień Gmail:**
```json
"email": {
  "smtp_server": "smtp.gmail.com",
  "smtp_port": 587,
  "sender_email": "twój-email@gmail.com",
  "sender_password": "twoje-app-password"
}
```

### **Dodanie nowych administratorów:**
Administratorzy mogą się zalogować i utworzyć nowe konta. Email nowych adminów automatycznie zostanie dodany do listy powiadomień.

---

## 📊 **MONITORING I LOGI**

### **Sprawdzanie działania:**
- Logi w konsoli Railway pokazują status wysyłania emaili
- `✅ Email sent successfully to user@email.com`
- `❌ Error sending email: [opis błędu]`

### **Test systemu:**
Można uruchomić `test_gmail_simple.py` do sprawdzenia połączenia SMTP.

---

## ⚡ **WYDAJNOŚĆ**

- **Czas wysyłania:** ~2-3 sekundy na email
- **Limit Gmail:** 500 emaili dziennie (wystarczy dla firmy)
- **Awarie:** System działa nawet jeśli email nie działa
- **Retry:** Jeśli email nie pójdzie, rezerwacja się tworzy normalnie

---

## 🚨 **ROZWIĄZYWANIE PROBLEMÓW**

### **"Email nie działa":**
1. Sprawdź czy `enabled: true` w config
2. Sprawdź App Password Gmail
3. Sprawdź logi w Railway
4. Uruchom test: `python test_gmail_simple.py`

### **"Adminowie nie dostają powiadomień":**
1. Sprawdź czy mają emaile w swoich kontach
2. Sprawdź `recipient_email` w config
3. Sprawdź folder SPAM

### **"Gmail blokuje wysyłanie":**
1. Włącz 2FA na Gmail
2. Wygeneruj nowe App Password
3. Sprawdź limity Gmail (500/dzień)

---

## 🎉 **SYSTEM GOTOWY!**

✅ **Gmail SMTP skonfigurowany i przetestowany**  
✅ **Wszystkie rodzaje powiadomień działają**  
✅ **Automatyczne powiadomienia dla adminów**  
✅ **Wdrożony na Railway z pełną funkcjonalnością**  

**System jest już aktywny na:** `web-production-ee2fb.up.railway.app`

Wszystkie emaile będą wysyłane automatycznie przy każdej rezerwacji! 📧✨
