#!/usr/bin/env python3
"""
Simplified version for Railway deployment
System Rezerwacji Sal - DACPOL
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
    import datetime
    import json
    
    # Try to import local modules with error handling
    try:
        from db import init_db, get_connection, hash_password
        from config import config
        from models import (
            seed_rooms, get_rooms, create_reservation, get_reservations_between,
            delete_reservation_with_password, is_available, authenticate_admin,
            create_admin_with_master_password, delete_reservation_admin,
            update_reservation, get_admin_emails
        )
        LOCAL_MODULES_OK = True
    except ImportError as e:
        print(f"Warning: Could not import local modules: {e}")
        LOCAL_MODULES_OK = False
        
    app = Flask(__name__)
    
    # Set secret key from environment or default
    app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    if LOCAL_MODULES_OK:
        # Initialize database and rooms on startup
        def initialize_app():
            try:
                init_db()
                # Load room names from config
                room_names = config.get_rooms()
                seed_rooms(room_names)
                
                # Wyłącz email w środowisku Railway (brak dostępu do SMTP)
                is_production = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT')
                if is_production:
                    print("🌐 Production mode - email notifications disabled")
                
                # Create default admin from config
                default_admin = config.get_default_admin()
                if default_admin:
                    create_admin_with_master_password(
                        default_admin['username'],
                        default_admin['password'],
                        default_admin.get('email', ''),
                        config.get_master_password()
                    )
                print("✅ Aplikacja zainicjalizowana pomyślnie")
            except Exception as e:
                print(f"❌ Błąd inicjalizacji: {e}")
                
        # Import all routes from the main app module
        try:
            # We'll include the route definitions here directly
            
            @app.route('/')
            def index():
                return render_template('calendar.html', 
                                       is_admin=session.get('is_admin', False),
                                       app_title=config.get_system_title() if LOCAL_MODULES_OK else "System Rezerwacji")
            
            @app.route('/admin')
            def admin():
                return render_template('login.html')
            
            @app.route('/login', methods=['GET', 'POST'])
            def login():
                """Admin login"""
                if request.method == 'POST':
                    try:
                        data = request.json
                        username = data.get('username', '')
                        password = data.get('password', '')
                        
                        if authenticate_admin(username, password):
                            session['is_admin'] = True
                            session['admin_username'] = username
                            return jsonify({'success': True})
                        else:
                            return jsonify({'error': 'Nieprawidłowe dane logowania'}), 401
                    except Exception as e:
                        print(f"Login error: {e}")
                        return jsonify({'error': 'Błąd logowania'}), 500
                
                return render_template('login.html')
            
            @app.route('/create_admin', methods=['GET', 'POST'])
            def create_admin():
                """Create new admin account"""
                if request.method == 'POST':
                    try:
                        data = request.json
                        
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
                        print(f"Create admin error: {e}")
                        return jsonify({'error': str(e)}), 500
                
                return render_template('create_admin.html')
            
            @app.route('/logout')
            def logout():
                session.clear()
                return redirect(url_for('index'))
            
            @app.route('/api/rooms')
            def api_rooms():
                if not LOCAL_MODULES_OK:
                    return jsonify([])
                    
                try:
                    # Upewnij się że baza jest zainicjalizowana
                    rooms = get_rooms()
                    if not rooms:
                        # Jeśli brak sal, zainicjalizuj je ponownie
                        print("No rooms found, reinitializing...")
                        room_names = config.get_rooms()
                        seed_rooms(room_names)
                        rooms = get_rooms()
                    
                    # Bezpieczne przetwarzanie danych
                    room_list = []
                    for r in rooms:
                        if isinstance(r, dict):
                            # Format słownikowy: {'id': 99, 'name': 'Sala wideo parter'}
                            room_list.append({'id': r['id'], 'name': r['name']})
                        elif isinstance(r, (list, tuple)) and len(r) >= 2:
                            # Format tuple/list: (id, name)
                            room_list.append({'id': r[0], 'name': r[1]})
                        elif hasattr(r, 'id') and hasattr(r, 'name'):
                            # Format obiektu: r.id, r.name
                            room_list.append({'id': r.id, 'name': r.name})
                        else:
                            print(f"Unexpected room format: {r}")
                            # Próbuj wyciągnąć dane w każdy możliwy sposób
                            if hasattr(r, '__getitem__'):
                                try:
                                    room_list.append({'id': r['id'], 'name': r['name']})
                                except (KeyError, TypeError):
                                    pass
                    
                    return jsonify(room_list)
                except Exception as e:
                    print(f"Error in api_rooms: {e}")
                    # Fallback - zwróć sale z konfiguracji
                    try:
                        room_names = config.get_rooms()
                        fallback_rooms = [{'id': i+1, 'name': name} for i, name in enumerate(room_names)]
                        return jsonify(fallback_rooms)
                    except:
                        return jsonify([{'id': 1, 'name': 'Sala przykładowa'}])
            
            @app.route('/api/reservations')
            def api_reservations():
                """Get reservations for a date range"""
                if not LOCAL_MODULES_OK:
                    return jsonify([])
                
                try:
                    start_date = request.args.get('start_date')
                    end_date = request.args.get('end_date')
                    
                    if not start_date or not end_date:
                        return jsonify({'error': 'start_date and end_date required'}), 400
                    
                    reservations = get_reservations_between(start_date, end_date)
                    return jsonify(reservations)
                except Exception as e:
                    print(f"Error in api_reservations: {e}")
                    return jsonify([])

            @app.route('/api/reservations', methods=['POST'])
            def api_create_reservation():
                """Create new reservation"""
                if not LOCAL_MODULES_OK:
                    return jsonify({'error': 'System maintenance mode'}), 503
                
                try:
                    data = request.json
                    
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
                        data.get('email', ''), data.get('description', '')
                    )
                    
                    return jsonify({'success': True, 'token': token})
                    
                except Exception as e:
                    print(f"Error in api_create_reservation: {e}")
                    return jsonify({'error': str(e)}), 500

            @app.route('/api/reservations/<token>', methods=['DELETE'])
            def api_delete_reservation(token):
                """Delete reservation"""
                if not LOCAL_MODULES_OK:
                    return jsonify({'error': 'System maintenance mode'}), 503
                
                try:
                    data = request.json or {}
                    password = data.get('password', '')
                    
                    if session.get('is_admin'):
                        # Admin can delete without password
                        success = delete_reservation_admin(token)
                    else:
                        # Regular user needs password
                        success = delete_reservation_with_password(token, password)
                    
                    if success:
                        return jsonify({'success': True})
                    else:
                        return jsonify({'error': 'Nieprawidłowy token lub hasło'}), 400
                        
                except Exception as e:
                    print(f"Error in api_delete_reservation: {e}")
                    return jsonify({'error': str(e)}), 500

            @app.route('/api/reservations/<token>', methods=['PUT'])
            def api_edit_reservation(token):
                """Edit reservation (admin only)"""
                if not LOCAL_MODULES_OK:
                    return jsonify({'error': 'System maintenance mode'}), 503
                
                if not session.get('is_admin'):
                    return jsonify({'error': 'Unauthorized'}), 403
                
                try:
                    data = request.json
                    
                    success = update_reservation(
                        token,
                        data.get('room_id'),
                        data.get('date'),
                        data.get('start_time'),
                        data.get('end_time'),
                        data.get('user_name'),
                        data.get('description', '')
                    )
                    
                    if success:
                        return jsonify({'success': True})
                    else:
                        return jsonify({'error': 'Failed to update reservation'}), 400
                        
                except Exception as e:
                    print(f"Error in api_edit_reservation: {e}")
                    return jsonify({'error': str(e)}), 500
            
            # Simple health check endpoint
            @app.route('/health')
            def health():
                return jsonify({
                    'status': 'ok', 
                    'modules': LOCAL_MODULES_OK,
                    'timestamp': datetime.datetime.now().isoformat()
                })
            
            # Debug endpoint to check rooms data
            @app.route('/debug/rooms')
            def debug_rooms():
                if not LOCAL_MODULES_OK:
                    return jsonify({'error': 'Modules not loaded'})
                
                try:
                    rooms = get_rooms()
                    return jsonify({
                        'raw_rooms': rooms,
                        'rooms_count': len(rooms),
                        'rooms_type': str(type(rooms)),
                        'first_room_type': str(type(rooms[0])) if rooms else 'No rooms',
                        'processed_rooms': [{'id': r['id'], 'name': r['name']} for r in rooms if isinstance(r, dict)]
                    })
                except Exception as e:
                    return jsonify({'error': str(e)})
                
            print("✅ Routes loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading routes: {e}")
    else:
        # Fallback routes if modules fail to load
        @app.route('/')
        def index():
            return f"""
            <h1>System Rezerwacji - Maintenance Mode</h1>
            <p>System is currently in maintenance mode.</p>
            <p>Error: Could not load application modules.</p>
            <p><a href="/health">Check system status</a></p>
            """
        
        @app.route('/health')
        def health():
            return jsonify({
                'status': 'maintenance',
                'modules': False,
                'timestamp': datetime.datetime.now().isoformat(),
                'message': 'Local modules could not be loaded'
            })
    
    # Production vs Development configuration
    def run_app():
        is_production = os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('PORT')
        
        if is_production:
            # Production settings - this will be handled by gunicorn
            if LOCAL_MODULES_OK:
                initialize_app()
            print("🚀 Production mode - handled by gunicorn")
        else:
            # Development settings
            if LOCAL_MODULES_OK:
                initialize_app()
                
            print("🚀 Development mode")
            print(f"📅 Aplikacja dostępna pod adresem: http://localhost:5000")
            print("⏹️  Aby zatrzymać serwer naciśnij Ctrl+C")
            app.run(host='0.0.0.0', port=5000, debug=True)
    
    if __name__ == '__main__':
        run_app()
    else:
        # For gunicorn
        if LOCAL_MODULES_OK:
            initialize_app()
        print("🌐 WSGI mode - handled by gunicorn")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    
    # Create a minimal fallback app
    app = Flask(__name__)
    
    @app.route('/')
    def emergency():
        return f"""
        <h1>System Error</h1>
        <p>Critical error occurred: {str(e)}</p>
        <p>Please contact system administrator.</p>
        """
        
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
