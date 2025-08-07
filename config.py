import json
import os

class Config:
    """Klasa do zarządzania konfiguracją aplikacji"""
    
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Ładuje konfigurację z pliku JSON"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku konfiguracji {self.config_file}")
            self._create_default_config()
            return self._load_config()
        except json.JSONDecodeError as e:
            print(f"Błąd w pliku konfiguracji: {e}")
            raise
    
    def _create_default_config(self):
        """Tworzy domyślny plik konfiguracji"""
        default_config = {
            "company": {
                "name": "DACPOL",
                "system_title": "System Rezerwacji Sal - DACPOL"
            },
            "rooms": [
                "Sala wideo parter",
                "2 piętro MAŁA", 
                "2 piętro DUŻA",
                "3 piętro LEWY",
                "3 piętro PRAWY",
                "1 piętro MAIN",
                "Sala konferencyjna A"
            ],
            "admin": {
                "master_password": "TWORZENIEKONTA",
                "default_admin": {
                    "username": "sekretarka",
                    "password": "TajneHaslo123"
                }
            },
            "email": {
                "enabled": True,
                "smtp_server": "poczta.dacpol.eu",
                "smtp_port": 587,
                "use_tls": True,
                "sender_email": "system@dacpol.eu",
                "sender_password": "TUTAJ_WPISZ_HASLO_DO_EMAILA",
                "recipient_email": "dacpoledi@dacpol.eu",
                "sender_name": "System Rezerwacji Sal"
            },
            "server": {
                "host": "0.0.0.0",
                "port": 5000,
                "debug": False
            },
            "security": {
                "session_secret": "super-secret-key-change-me-in-production",
                "password_min_length": 4
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        print(f"Utworzono domyślny plik konfiguracji: {self.config_file}")
    
    def get(self, *keys):
        """Pobiera wartość z konfiguracji używając ścieżki kluczy"""
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    
    def get_rooms(self):
        """Zwraca listę sal"""
        return self.get('rooms') or []
    
    def get_master_password(self):
        """Zwraca hasło główne do tworzenia adminów"""
        return self.get('admin', 'master_password') or 'TWORZENIEKONTA'
    
    def get_default_admin(self):
        """Zwraca dane domyślnego admina"""
        return self.get('admin', 'default_admin') or {}
    
    def get_email_config(self):
        """Zwraca konfigurację email"""
        return self.get('email') or {}
    
    def get_server_config(self):
        """Zwraca konfigurację serwera"""
        return self.get('server') or {}
    
    def get_company_name(self):
        """Zwraca nazwę firmy"""
        return self.get('company', 'name') or 'Firma'
    
    def get_system_title(self):
        """Zwraca tytuł systemu"""
        return self.get('company', 'system_title') or 'System Rezerwacji Sal'
    
    def get_session_secret(self):
        """Zwraca klucz sesji"""
        return self.get('security', 'session_secret') or 'default-secret-key'
    
    def is_email_enabled(self):
        """Sprawdza czy email jest włączony"""
        return self.get('email', 'enabled') is True
    
    def reload(self):
        """Przeładowuje konfigurację z pliku"""
        self.config = self._load_config()
        print("Konfiguracja została przeładowana")

# Globalna instancja konfiguracji
config = Config()
