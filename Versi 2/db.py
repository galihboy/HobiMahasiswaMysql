# db.py
# Galih Hermawan (https://galih.eu)

import os
from dotenv import load_dotenv
import mysql.connector

# Coba muat .env, jika gagal, abaikan
try:
    load_dotenv()  # Cari file .env di direktori saat ini
except FileNotFoundError:
    pass

# Ambil nilai variabel lingkungan, gunakan nilai default (lokal) jika tidak ada
HOST = os.getenv('HOST', 'localhost')  # Ganti dengan default hosting Anda
PORT = int(os.getenv('PORT', 3306))  # Ganti dengan port hosting Anda
USER = os.getenv('USER', 'root')     # Ganti dengan user hosting Anda
PASSWORD = os.getenv('PASSWORD', '') # Ganti dengan password hosting Anda
DATABASE = os.getenv('DATABASE', 'proyek_hobimahasiswa')  # Ganti dengan nama database Anda

# Fungsi untuk membuat koneksi ke database - hybrid (bisa lokal atau online)
def buat_koneksi():
    try:
        return mysql.connector.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Fungsi untuk membuat koneksi ke database - contoh basis data online
def buat_koneksi_online():
    return mysql.connector.connect(
        host=os.getenv('HOST'),
        port=os.getenv('PORT'),
        user=os.getenv('USER'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DATABASE')
    )

# Pengaturan untuk koneksi lokal
def buat_koneksi_lokal():
    return mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='',
        database='proyek_hobimahasiswa'
    )

# Konfigurasi koneksi MySQL
#db = buat_koneksi()


# Fungsi untuk mendapatkan data mahasiswa beserta hobi
def get_mahasiswa_hobi(search_query=''):
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    query = "SELECT mahasiswa.nim, mahasiswa.nama, " \
            "IFNULL(GROUP_CONCAT(hobi.namahobi SEPARATOR ', '), '-') as daftar_hobi " \
            "FROM mahasiswa " \
            "LEFT JOIN mhshobi ON mahasiswa.nim = mhshobi.nim " \
            "LEFT JOIN hobi ON mhshobi.kodehobi = hobi.kodehobi "
    if search_query:
        query += f"WHERE mahasiswa.nama LIKE '%{search_query}%' OR hobi.namahobi LIKE '%{search_query}%' "
    query += "GROUP BY mahasiswa.nim, mahasiswa.nama"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result



# Fungsi untuk mendapatkan data mahasiswa
def get_mahasiswa_data(search_query=''):
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM mahasiswa"
    if search_query:
        query += f" WHERE nama LIKE '%{search_query}%' OR nim LIKE '%{search_query}%' OR tempat_lahir LIKE '%{search_query}%' OR tanggal_lahir LIKE '%{search_query}%' OR kota LIKE '%{search_query}%' OR tanggal_masuk LIKE '%{search_query}%' OR tinggi_badan LIKE '%{search_query}%'"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


# Fungsi untuk mendapatkan data hobi
def get_hobi_data(search_query=''):
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM hobi"
    if search_query:
        query += f" WHERE namahobi LIKE '%{search_query}%'"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


# Fungsi untuk mendapatkan data mhshobi
def get_mhshobi_data():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    query = "SELECT mhshobi.nim, mahasiswa.nama, GROUP_CONCAT(hobi.namahobi SEPARATOR ', ') as daftar_hobi " \
            "FROM mhshobi " \
            "JOIN mahasiswa ON mhshobi.nim = mahasiswa.nim " \
            "JOIN hobi ON mhshobi.kodehobi = hobi.kodehobi " \
            "GROUP BY mhshobi.nim, mahasiswa.nama"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result


# Fungsi untuk mendapatkan daftar mahasiswa yang belum memiliki hobi
def get_mahasiswa_without_hobi():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    query = "SELECT nim, nama FROM mahasiswa " \
            "WHERE nim NOT IN (SELECT nim FROM mhshobi)"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result
