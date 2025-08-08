import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
from config import config

def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send email using SMTP"""
    
    # Get email config
    email_config = config.get_email_config()
    
    if not config.is_email_enabled():
        print("Email wyłączony w konfiguracji")
        return True
    
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = f"{email_config.get('sender_name', 'System')} <{email_config.get('sender_email')}>"
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add body to email
        message.attach(MIMEText(body, "plain", "utf-8"))
        
        # Create SMTP session
        server = smtplib.SMTP(email_config.get('smtp_server'), email_config.get('smtp_port', 587))
        if email_config.get('use_tls', True):
            server.starttls()  # Enable TLS encryption
        server.login(email_config.get('sender_email'), email_config.get('sender_password'))
        
        # Send email
        text = message.as_string()
        server.sendmail(email_config.get('sender_email'), to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email to {to_email}: {str(e)}")
        return False

def send_reservation_confirmation(user_email: str, user_name: str, room_name: str, 
                                date: str, start_time: str, end_time: str, token: str, password: str):
    """Send confirmation email to user"""
    subject = "Potwierdzenie rezerwacji sali"
    body = f"""Witaj {user_name}!

Twoja rezerwacja została pomyślnie utworzona:

🏢 Sala: {room_name}
📅 Data: {date}
⏰ Czas: {start_time} - {end_time}
🎫 Token: {token}
🔑 Hasło do anulowania: {password}

WAŻNE: Zapisz swoje hasło - będzie potrzebne do usunięcia rezerwacji!

Pozdrawiamy,
System Rezerwacji Sal
"""
    return send_email(user_email, subject, body)

def send_admin_notification(admin_email: str, user_name: str, user_email: str, 
                          room_name: str, date: str, start_time: str, end_time: str):
    """Send notification to admin about new reservation"""
    subject = "Nowa rezerwacja sali"
    body = f"""Informujemy o nowej rezerwacji:

👤 Użytkownik: {user_name} ({user_email})
🏢 Sala: {room_name}
📅 Data: {date}
⏰ Czas: {start_time} - {end_time}

System Rezerwacji Sal
"""
    return send_email(admin_email, subject, body)

def send_collision_notification(user_email: str, user_name: str, room_name: str, 
                               date: str, start_time: str, end_time: str):
    """Send collision notification to user"""
    subject = "Błąd rezerwacji - kolizja terminów"
    body = f"""Witaj {user_name}!

Niestety, Twoja próba rezerwacji nie powiodła się z powodu kolizji terminów:

🏢 Sala: {room_name}
📅 Data: {date}
⏰ Czas: {start_time} - {end_time}

Wybierz inny termin lub salę.

Pozdrawiamy,
System Rezerwacji Sal
"""
    return send_email(user_email, subject, body)

def send_edit_notification(user_email: str, user_name: str, room_name: str, 
                         old_date: str, old_start: str, old_end: str,
                         new_date: str, new_start: str, new_end: str, new_room: str):
    """Send notification about reservation edit"""
    subject = "Twoja rezerwacja została zmodyfikowana"
    body = f"""Witaj {user_name}!

Twoja rezerwacja została zmodyfikowana przez administratora:

POPRZEDNIE DANE:
🏢 Sala: {room_name}
📅 Data: {old_date}
⏰ Czas: {old_start} - {old_end}

NOWE DANE:
🏢 Sala: {new_room}
📅 Data: {new_date}
⏰ Czas: {new_start} - {new_end}

Pozdrawiamy,
System Rezerwacji Sal
"""
    return send_email(user_email, subject, body)

def send_deletion_notification(user_email: str, user_name: str, room_name: str, 
                              date: str, start_time: str, end_time: str):
    """Send notification about reservation deletion"""
    subject = "Twoja rezerwacja została usunięta"
    body = f"""Witaj {user_name}!

Twoja rezerwacja została usunięta przez administratora:

🏢 Sala: {room_name}
📅 Data: {date}
⏰ Czas: {start_time} - {end_time}

Jeśli to pomyłka, skontaktuj się z administratorem.

Pozdrawiamy,
System Rezerwacji Sal
"""
    return send_email(user_email, subject, body)

def send_admin_deletion_notification(user_name: str, room_name: str, 
                                   date: str, start_time: str, end_time: str):
    """Send notification to admins about user self-deletion"""
    print(f"Sending admin deletion notification for user: {user_name}")
    
    subject = "Użytkownik usunął swoją rezerwację"
    body = f"""Powiadomienie dla administratorów!

Użytkownik {user_name} usunął swoją rezerwację:

🏢 Sala: {room_name}
📅 Data: {date}
⏰ Czas: {start_time} - {end_time}
👤 Użytkownik: {user_name}

Rezerwacja została pomyślnie usunięta z systemu.

--
System Rezerwacji Sal - DACPOL
"""
    
    # Send to configured admin email
    admin_email = config.get_email_config().get('recipient_email')
    print(f"Admin email configured as: {admin_email}")
    
    if admin_email:
        result = send_email(admin_email, subject, body)
        print(f"Email send result: {result}")
        return result
    else:
        print("No admin email configured!")
        return False
