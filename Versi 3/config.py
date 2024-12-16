# config.py
# Galih Hermawan (https://galih.eu)

import os
from dotenv import load_dotenv

# Coba muat .env, jika gagal, abaikan
try:
    load_dotenv()
except FileNotFoundError:
    pass

# Konfigurasi Database Lokal
DB_LOCAL = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'proyek_hobimahasiswa'
}

# Konfigurasi Database Online (sesuaikan dengan kredensial hosting Anda)
DB_ONLINE = {
    'host': os.getenv('HOST_ONLINE', 'host_online'),
    'port': int(os.getenv('PORT_ONLINE', 3306)),
    'user': os.getenv('USER_ONLINE', 'user_online'),
    'password': os.getenv('PASSWORD_ONLINE', 'passw_online'),
    'database': os.getenv('DATABASE_ONLINE', 'db_online')
}

# Mode database default
DEFAULT_MODE = os.getenv('DB_MODE', 'local')  # 'local' atau 'online'

def get_db_config(mode=None):
    """
    Mendapatkan konfigurasi database berdasarkan mode yang dipilih
    :param mode: 'local' atau 'online'
    :return: dictionary konfigurasi database
    """
    if mode is None:
        mode = DEFAULT_MODE
    
    if mode.lower() == 'online':
        return DB_ONLINE
    return DB_LOCAL

def switch_mode():
    """
    Mengganti mode database antara local dan online
    :return: mode baru ('local' atau 'online')
    """
    current_mode = DEFAULT_MODE
    new_mode = 'online' if current_mode == 'local' else 'local'
    os.environ['DB_MODE'] = new_mode
    return new_mode
