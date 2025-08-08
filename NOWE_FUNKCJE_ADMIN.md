# Nowe Funkcje Zarządzania Kontami Adminów

## ✅ Co zostało dodane:

### 1. **Backend - Nowe funkcje w models.py:**
- `get_all_admins()` - pobiera listę wszystkich kont adminów
- `delete_admin_account(username, password)` - usuwa konto po weryfikacji hasła

### 2. **API Endpoints:**
- `GET /api/admins` - zwraca listę kont adminów
- `DELETE /api/admins/<username>` - usuwa konto po weryfikacji hasła

### 3. **Frontend - Zaktualizowana strona create_admin.html:**
- **Zakładka "Utwórz konto"** - poprzednia funkcjonalność
- **Zakładka "Usuń konto"** - nowa funkcjonalność z:
  - Listą wszystkich kont adminów
  - Wyborem konta do usunięcia
  - Formularzem weryfikacji hasła

## 🎯 Jak używać:

### Usuwanie konta admina:

1. **Przejdź na stronę:** `/create_admin`
2. **Kliknij zakładkę:** "🗑️ Usuń konto"
3. **Wybierz konto** z listy (kliknij na nie)
4. **Wpisz hasło** do wybranego konta
5. **Kliknij "Usuń konto"**

### Bezpieczeństwo:
- ✅ Wymagane jest hasło do usuwanego konta
- ✅ Usunięcie jest nieodwracalne
- ✅ System wyświetla ostrzeżenia

## 🔧 Test funkcjonalności:

**Aktualna lista adminów:**
```
Liczba: 1
- admin (dsw@dacpol.eu)
```

**Hasło do konta "admin":** `admin123`

## 📝 Pliki zmodyfikowane:

1. `models.py` - dodano funkcje `get_all_admins()` i `delete_admin_account()`
2. `app.py` - dodano endpoint'y `/api/admins` i `/api/admins/<username>`
3. `app_railway.py` - dodano te same endpoint'y dla Railway
4. `templates/create_admin.html` - kompletnie przeprojektowano z zakładkami

## 🚀 Gotowe do użycia!

Uruchom aplikację i przejdź na `/create_admin` żeby przetestować nową funkcjonalność.
