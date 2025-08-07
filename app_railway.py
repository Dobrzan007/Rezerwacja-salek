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
            
            @app.route('/login', methods=['POST'])
            def login():
                if not LOCAL_MODULES_OK:
                    return jsonify({'error': 'System configuration error'}), 500
                    
                username = request.form['username']
                password = request.form['password']
                
                if authenticate_admin(username, password):
                    session['is_admin'] = True
                    session['admin_username'] = username
                    return redirect(url_for('index'))
                else:
                    flash('Nieprawidłowa nazwa użytkownika lub hasło')
                    return redirect(url_for('admin'))
            
            @app.route('/logout')
            def logout():
                session.clear()
                return redirect(url_for('index'))
            
            @app.route('/api/rooms')
            def api_rooms():
                if not LOCAL_MODULES_OK:
                    return jsonify([])
                    
                rooms = get_rooms()
                return jsonify([{'id': r[0], 'name': r[1]} for r in rooms])
            
            # Simple health check endpoint
            @app.route('/health')
            def health():
                return jsonify({
                    'status': 'ok', 
                    'modules': LOCAL_MODULES_OK,
                    'timestamp': datetime.datetime.now().isoformat()
                })
                
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
