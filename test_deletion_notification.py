#!/usr/bin/env python3
"""
TEST USUWANIA REZERWACJI I POWIADOMIEŃ
=====================================
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from models import create_reservation, delete_reservation_with_password
    from config import config
    
    print("🧪 TEST USUWANIA REZERWACJI")
    print("=" * 50)
    
    # Test 1: Utwórz testową rezerwację
    print("\n1. Tworzenie testowej rezerwacji...")
    try:
        token = create_reservation(
            room_id=1,
            date="2025-08-10",
            start_time="14:00",
            end_time="15:00",
            user_name="Test User",
            password="testpass123",
            user_email="test@example.com",
            description="Test rezerwacji do usunięcia"
        )
        print(f"✅ Rezerwacja utworzona z tokenem: {token}")
    except Exception as e:
        print(f"❌ Błąd tworzenia rezerwacji: {e}")
        sys.exit(1)
    
    # Test 2: Usuń rezerwację jako użytkownik
    print("\n2. Usuwanie rezerwacji przez użytkownika...")
    try:
        result = delete_reservation_with_password(token, "testpass123")
        print(f"✅ Usuwanie zakończyło się: {'Pomyślnie' if result else 'Niepowodzeniem'}")
        
        if result:
            print("📧 Sprawdź czy email do adminów został wysłany!")
        
    except Exception as e:
        print(f"❌ Błąd usuwania rezerwacji: {e}")
    
    # Test 3: Sprawdź konfigurację email
    print("\n3. Sprawdzanie konfiguracji email...")
    email_config = config.get_email_config()
    print(f"   Email włączony: {config.is_email_enabled()}")
    print(f"   Admin email: {email_config.get('recipient_email')}")
    print(f"   Sender email: {email_config.get('sender_email')}")
    
    print("\n🎉 Test zakończony!")
    
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
except Exception as e:
    print(f"❌ Błąd: {e}")
