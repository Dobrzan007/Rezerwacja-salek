#!/usr/bin/env python3
"""
TEST SYSTEMU EMAIL - DACPOL
============================

Ten skrypt testuje czy system email działa prawidłowo z Gmail SMTP.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from config import config
    from email_service import send_email, send_reservation_confirmation, send_admin_notification
    
    print("🧪 TEST SYSTEMU EMAIL")
    print("=" * 50)
    
    # Test 1: Konfiguracja
    print("\n1. SPRAWDZANIE KONFIGURACJI:")
    email_config = config.get_email_config()
    print(f"   ✅ Email włączony: {config.is_email_enabled()}")
    print(f"   ✅ Serwer SMTP: {email_config.get('smtp_server')}")
    print(f"   ✅ Port: {email_config.get('smtp_port')}")
    print(f"   ✅ Email nadawcy: {email_config.get('sender_email')}")
    print(f"   ✅ Hasło ustawione: {'Tak' if email_config.get('sender_password') else 'Nie'}")
    
    if not config.is_email_enabled():
        print("❌ Email jest wyłączony w konfiguracji!")
        exit(1)
    
    # Test 2: Prosty email
    print("\n2. TEST WYSYŁANIA PROSTEGO EMAILA:")
    test_email = "dobrzanski.mateusz05@gmail.com"  # Wysyłamy do siebie
    success = send_email(
        test_email, 
        "🧪 Test systemu DACPOL", 
        "To jest testowy email z systemu rezerwacji sal DACPOL.\n\nJeśli otrzymujesz tę wiadomość, system email działa poprawnie! ✅"
    )
    
    if success:
        print(f"   ✅ Email testowy wysłany pomyślnie do {test_email}")
    else:
        print(f"   ❌ Błąd wysyłania emaila do {test_email}")
        exit(1)
    
    # Test 3: Email potwierdzenia rezerwacji
    print("\n3. TEST EMAILA POTWIERDZENIA REZERWACJI:")
    success = send_reservation_confirmation(
        test_email,
        "Jan Testowy",
        "Sala wideo parter", 
        "2025-08-08",
        "10:00",
        "11:00",
        "TEST123ABC"
    )
    
    if success:
        print("   ✅ Email potwierdzenia rezerwacji wysłany pomyślnie")
    else:
        print("   ❌ Błąd wysyłania emaila potwierdzenia")
        exit(1)
    
    # Test 4: Email dla administratora
    print("\n4. TEST EMAILA DLA ADMINISTRATORA:")
    success = send_admin_notification(
        test_email,
        "Jan Testowy",
        "jan.testowy@dacpol.eu",
        "Sala wideo parter",
        "2025-08-08", 
        "10:00",
        "11:00"
    )
    
    if success:
        print("   ✅ Email dla administratora wysłany pomyślnie")
    else:
        print("   ❌ Błąd wysyłania emaila dla administratora")
        exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")
    print("📧 System email jest gotowy do użycia")
    print("🚀 Można wdrażać na Railway")
    
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
    print("🔧 Sprawdź czy wszystkie pliki są na miejscu")
except Exception as e:
    print(f"❌ Błąd testu: {e}")
    print("🔧 Sprawdź konfigurację email w config.json")
