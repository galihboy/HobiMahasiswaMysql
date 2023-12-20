# db.py
# Galih Hermawan (https://galih.eu)

import mysql.connector

# Fungsi untuk membuat koneksi ke database
def buat_koneksi():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='proyek_hobimahasiswa'
    )

# Fungsi untuk mendapatkan data mahasiswa beserta hobi
def get_mahasiswa_hobi(db):
    cursor = db.cursor(dictionary=True)
    query = "SELECT mahasiswa.nim, mahasiswa.nama, GROUP_CONCAT(hobi.namahobi SEPARATOR ', ') as daftar_hobi " \
            "FROM mahasiswa " \
            "LEFT JOIN mhshobi ON mahasiswa.nim = mhshobi.nim " \
            "LEFT JOIN hobi ON mhshobi.kodehobi = hobi.kodehobi " \
            "GROUP BY mahasiswa.nim, mahasiswa.nama"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Fungsi untuk mendapatkan data mahasiswa
def get_mahasiswa_data(db):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM mahasiswa"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Fungsi untuk mendapatkan data hobi
def get_hobi_data(db):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM hobi"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Fungsi untuk mendapatkan data mhshobi
def get_mhshobi_data(db):
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
def get_mahasiswa_without_hobi(db):
    cursor = db.cursor(dictionary=True)
    query = "SELECT nim, nama FROM mahasiswa " \
            "WHERE nim NOT IN (SELECT nim FROM mhshobi)"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result