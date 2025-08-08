from models import get_all_admins

try:
    admins = get_all_admins()
    print('=== LISTA ADMINISTRATOROW ===')
    print(f'Liczba: {len(admins)}')
    
    for admin in admins:
        print(f'  - {admin["username"]} ({admin["email"]})')
        
except Exception as e:
    print(f'Blad: {e}')
