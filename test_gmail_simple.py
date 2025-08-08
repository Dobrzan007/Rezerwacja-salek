#!/usr/bin/env python3
"""
PROSTY TEST GMAIL SMTP
"""

import smtplib
from email.mime.text import MIMEText

def test_gmail_connection():
    print("🧪 Test połączenia z Gmail SMTP...")
    
    try:
        # Parametry Gmail SMTP
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        email = "dobrzanski.mateusz05@gmail.com"
        password = "uccb qatu vekh gppu"
        
        print(f"📧 Łączenie z {smtp_server}:{smtp_port}...")
        
        # Próba połączenia
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("✅ TLS włączone")
        
        server.login(email, password)
        print("✅ Logowanie pomyślne")
        
        # Wysłanie testowego emaila
        msg = MIMEText("Test email z systemu DACPOL")
        msg['Subject'] = 'Test SMTP DACPOL'
        msg['From'] = email
        msg['To'] = email
        
        server.send_message(msg)
        print("✅ Email wysłany pomyślnie")
        
        server.quit()
        print("🎉 Test zakończony pomyślnie!")
        
        return True
        
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False

if __name__ == "__main__":
    test_gmail_connection()
