#!/usr/bin/env python3
"""
TEST NOWYCH FUNKCJI EMAIL
=========================
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from email_service import send_admin_deletion_notification, send_reservation_confirmation
    
    print("🧪 TEST NOWYCH FUNKCJI EMAIL")
    print("=" * 50)
    
    # Test 1: Powiadomienie adminów o usunięciu przez użytkownika
    print("\n1. TEST: Powiadomienie adminów o usunięciu przez użytkownika")
    result1 = send_admin_deletion_notification(
        user_name="Jan Kowalski",
        room_name="Sala wideo parter", 
        date="2024-01-15",
        start_time="14:00",
        end_time="16:00"
    )
    print(f"   Wynik: {'✅ Wysłano' if result1 else '❌ Błąd'}")
    
    # Test 2: Potwierdzenie z hasłem
    print("\n2. TEST: Potwierdzenie rezerwacji z hasłem")
    result2 = send_reservation_confirmation(
        user_email="test@example.com",
        user_name="Anna Nowak",
        room_name="Sala obiadowa parter",
        date="2024-01-16", 
        start_time="10:00",
        end_time="12:00",
        token="test123",
        password="mojhaslo123"
    )
    print(f"   Wynik: {'✅ Wysłano' if result2 else '❌ Błąd'}")
    
    print("\n🎉 Test zakończony!")
    
except ImportError as e:
    print(f"❌ Błąd importu: {e}")
except Exception as e:
    print(f"❌ Błąd: {e}")
