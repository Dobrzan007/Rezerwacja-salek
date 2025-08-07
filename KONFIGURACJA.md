# 🔧 PRZEWODNIK KONFIGURACJI SYSTEMU

## 📄 Plik `config.json` - Centralna konfiguracja

Cały system można skonfigurować edytując jeden plik: **`config.json`**

### 🏢 **Sekcja: company** - Dane firmy
```json
"company": {
    "name": "DACPOL",
    "system_title": "System Rezerwacji Sal - DACPOL"
}
```
- `name` - Nazwa firmy wyświetlana w aplikacji
- `system_title` - Tytuł systemu w przeglądarce

### 🏛️ **Sekcja: rooms** - Konfiguracja sal
```json
"rooms": [
    "Sala wideo parter",
    "2 piętro MAŁA", 
    "2 piętro DUŻA",
    "3 piętro LEWY",
    "3 piętro PRAWY",
    "1 piętro MAIN",
    "Sala konferencyjna A"
]
```
**Jak zmienić sale:**
1. Edytuj listę w `config.json`
2. Uruchom ponownie aplikację
3. Sale zostaną automatycznie zaktualizowane

### 👤 **Sekcja: admin** - Administratorzy
```json
"admin": {
    "master_password": "TWORZENIEKONTA",
    "default_admin": {
        "username": "sekretarka",
        "password": "TajneHaslo123"
    }
}
```
- `master_password` - Hasło do tworzenia nowych adminów
- `default_admin` - Domyślne konto administratora

### 📧 **Sekcja: email** - Konfiguracja powiadomień
```json
"email": {
    "enabled": true,
    "smtp_server": "poczta.dacpol.eu",
    "smtp_port": 587,
    "use_tls": true,
    "sender_email": "system@dacpol.eu",
    "sender_password": "TUTAJ_WPISZ_HASLO_DO_EMAILA",
    "recipient_email": "dacpoledi@dacpol.eu",
    "sender_name": "System Rezerwacji Sal"
}
```

**Wymagane zmiany:**
- `sender_password` - **MUSISZ WPISAĆ** prawdziwe hasło do konta email
- `sender_email` - Email z którego będą wysyłane powiadomienia
- `recipient_email` - Email na który będą przychodzić powiadomienia

**Wyłączenie emaili:**
- Ustaw `"enabled": false` żeby wyłączyć powiadomienia

### 🌐 **Sekcja: server** - Ustawienia serwera
```json
"server": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false
}
```
- `port` - Zmień jeśli port 5000 jest zajęty (np. na 5555)
- `debug` - Ustaw `true` dla trybu debugowania

### 🔒 **Sekcja: security** - Bezpieczeństwo
```json
"security": {
    "session_secret": "super-secret-key-change-me-in-production",
    "password_min_length": 4
}
```
- `session_secret` - **ZMIEŃ** na losowy ciąg znaków w środowisku produkcyjnym

## 🚀 **Jak zastosować zmiany:**

1. **Edytuj `config.json`**
2. **Zatrzymaj aplikację** (Ctrl+C)
3. **Uruchom ponownie** aplikację
4. **Gotowe!** Zmiany zostały zastosowane

## ⚠️ **WAŻNE UWAGI:**

### 📧 **Konfiguracja email - OBOWIĄZKOWA:**
Żeby powiadomienia email działały:
```json
"sender_password": "PRAWDZIWE_HASLO_DO_EMAILA"
```
**Jeśli nie masz hasła do emaila:**
- Ustaw `"enabled": false` żeby wyłączyć email
- Lub skontaktuj się z administratorem IT

### 🏛️ **Nazwy sal:**
- Możesz dodać dowolną liczbę sal
- Usuń sale których nie używasz
- Nazwy mogą zawierać polskie znaki
- Istniejące rezerwacje dostosują się automatycznie

### 🔐 **Hasła:**
- `master_password` - hasło do tworzenia adminów przez stronę
- `default_admin.password` - hasło domyślnego administratora
- `sender_password` - hasło do emaila (NIE ZOSTAWIAJ PUSTEGO!)

## 📝 **Przykłady zmian:**

### Zmiana nazw sal na angielskie:
```json
"rooms": [
    "Conference Room A",
    "Meeting Room B", 
    "Video Room Ground Floor",
    "Training Room"
]
```

### Zmiana portu serwera:
```json
"server": {
    "port": 8080
}
```

### Wyłączenie emaili:
```json
"email": {
    "enabled": false
}
```

---
**Po każdej zmianie w `config.json` pamiętaj o ponownym uruchomieniu aplikacji!**
