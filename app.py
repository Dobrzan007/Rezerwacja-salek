from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import datetime
import json
from db import init_db, get_connection, hash_password
from config import config
from models import (
    seed_rooms, get_rooms, create_reservation, get_reservations_between,
    delete_reservation_with_password, is_available, authenticate_admin,
    create_admin_with_master_password, delete_reservation_admin,
    update_reservation, get_admin_emails
)

app = Flask(__name__)
app.secret_key = config.get_session_secret()

# Initialize database and rooms on startup
def initialize_app():
    init_db()
    # Load room names from config
    room_names = config.get_rooms()
    seed_rooms(room_names)
    
    # Create default admin from config
    default_admin = config.get_default_admin()
    if default_admin:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT OR IGNORE INTO admins (username, password_hash, email) VALUES (?, ?, ?)",
                    (default_admin.get('username'), 
                     hash_password(default_admin.get('password')), 
                     'sekretarka@dacpol.eu'))
        conn.commit()
        conn.close()

@app.route('/')
def index():
    """Main calendar view"""
    is_admin = session.get('is_admin', False)
    admin_username = session.get('admin_username', '')
    return render_template('calendar.html', 
                         is_admin=is_admin, 
                         admin_username=admin_username,
                         system_title=config.get_system_title(),
                         company_name=config.get_company_name())

@app.route('/api/rooms')
def api_rooms():
    """Get all rooms"""
    rooms = get_rooms()
    return jsonify(rooms)

@app.route('/api/reservations')
def api_reservations():
    """Get reservations for a date range"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'error': 'start_date and end_date required'}), 400
    
    reservations = get_reservations_between(start_date, end_date)
    return jsonify(reservations)

@app.route('/api/reservations', methods=['POST'])
def api_create_reservation():
    """Create new reservation"""
    data = request.json
    
    try:
        # Validate required fields
        required_fields = ['room_id', 'date', 'start_time', 'end_time', 'user_name', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Check availability
        if not is_available(data['room_id'], data['date'], data['start_time'], data['end_time']):
            return jsonify({'error': 'Sala jest już zarezerwowana w tym czasie'}), 400
        
        # Create reservation
        token = create_reservation(
            data['room_id'], data['date'], data['start_time'], 
            data['end_time'], data['user_name'], data['password'],
            data.get('email', '')
        )
        
        return jsonify({'success': True, 'token': token})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservations/<token>', methods=['DELETE'])
def api_delete_reservation(token):
    """Delete reservation"""
    data = request.json
    password = data.get('password', '')
    
    try:
        if session.get('is_admin'):
            # Admin can delete without password
            print(f"Admin deleting reservation: {token}")
            success = delete_reservation_admin(token)
        else:
            # Regular user needs password
            print(f"User deleting reservation: {token} with password: {bool(password)}")
            success = delete_reservation_with_password(token, password)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Nieprawidłowy token lub hasło'}), 400
            
    except Exception as e:
        print(f"Delete reservation error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservations/<token>', methods=['PUT'])
def api_edit_reservation(token):
    """Edit reservation (admin only)"""
    if not session.get('is_admin'):
        return jsonify({'error': 'Brak uprawnień administratora'}), 403
    
    data = request.json
    
    try:
        success = update_reservation(
            token, data['room_id'], data['date'], 
            data['start_time'], data['end_time'], 
            data['user_name'], data.get('description', '')
        )
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Nie udało się edytować rezerwacji'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        data = request.json
        username = data.get('username', '')
        password = data.get('password', '')
        
        if authenticate_admin(username, password):
            session['is_admin'] = True
            session['admin_username'] = username
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Nieprawidłowe dane logowania'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Admin logout"""
    session.pop('is_admin', None)
    session.pop('admin_username', None)
    flash('Wylogowano pomyślnie')
    return redirect(url_for('index'))

@app.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    """Create new admin account"""
    if request.method == 'POST':
        data = request.json
        
        try:
            success = create_admin_with_master_password(
                data['username'], data['password'], 
                data['email'], data['master_password']
            )
            
            if success:
                return jsonify({'success': True})
            else:
                return jsonify({'error': 'Nie udało się utworzyć konta'}), 400
                
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return render_template('create_admin.html')

if __name__ == '__main__':
    initialize_app()
    print("🚀 Uruchamianie System Rezerwacji Salek - DACPOL")
    
    # Production vs Development configuration
    import os
    is_production = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('HEROKU_APP_NAME')
    
    if is_production:
        # Production settings
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    else:
        # Development settings
        server_config = config.get_server_config()
        host = server_config.get('host', '0.0.0.0')
        port = server_config.get('port', 5000)
        debug = server_config.get('debug', False)
        
        print(f"📅 Aplikacja dostępna pod adresem: http://localhost:{port}")
        print(f"🌐 W sieci lokalnej: http://[IP-KOMPUTERA]:{port}")
        print("⏹️  Aby zatrzymać serwer naciśnij Ctrl+C")
        app.run(host=host, port=port, debug=debug)
else:
    # For gunicorn
    initialize_app()
