# db.py
# Galih Hermawan (https://galih.eu)

import os
from dotenv import load_dotenv
import mysql.connector
from config import get_db_config, switch_mode
import datetime

# Coba muat .env, jika gagal, abaikan
try:
    load_dotenv()  # Cari file .env di direktori saat ini
except FileNotFoundError:
    pass

# Fungsi untuk membuat koneksi ke database - hybrid (bisa lokal atau online)
def buat_koneksi(mode=None):
    try:
        config = get_db_config(mode)
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Jika koneksi gagal, coba mode lainnya
        if mode != 'local':
            print("Mencoba koneksi ke database lokal...")
            return buat_koneksi('local')
        return None

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
    query += "GROUP BY mahasiswa.nim, mahasiswa.nama ORDER BY mahasiswa.nim"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result



# Fungsi untuk mendapatkan data mahasiswa
def get_mahasiswa_data(search_query='', filter_tanggal_masuk=None):
    """Mendapatkan data mahasiswa dengan filter pencarian di semua kolom dan filter tanggal masuk"""
    db = buat_koneksi()
    if not db:
        return []
    
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM mahasiswa "
    conditions = []
    values = []
    
    if search_query:
        conditions.append("(nim LIKE %s OR nama LIKE %s OR tempat_lahir LIKE %s OR DATE_FORMAT(tanggal_lahir, '%d-%m-%Y') LIKE %s OR kota LIKE %s OR DATE_FORMAT(tanggal_masuk, '%d-%m-%Y') LIKE %s OR CAST(tinggi_badan AS CHAR) LIKE %s)")
        search_pattern = f"%{search_query}%"
        values.extend([search_pattern] * 7)
    
    if filter_tanggal_masuk:
        if 'date' in filter_tanggal_masuk and filter_tanggal_masuk['date']:
            conditions.append("DATE_FORMAT(tanggal_masuk, '%Y-%m-%d') = %s")
            values.append(filter_tanggal_masuk['date'])
        elif 'year' in filter_tanggal_masuk and filter_tanggal_masuk['year'].isdigit():
            conditions.append("YEAR(tanggal_masuk) = %s")
            values.append(filter_tanggal_masuk['year'])
        elif 'month' in filter_tanggal_masuk and filter_tanggal_masuk['month'].isdigit():
            conditions.append("MONTH(tanggal_masuk) = %s")
            values.append(filter_tanggal_masuk['month'])

    if conditions:
        query += "WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY nim"
    
    try:
        cursor.execute(query, values)
        result = cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        print(f"Query: {query}")
        print(f"Values: {values}")
        result = []
    finally:
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
    
    # Query untuk mendapatkan data mahasiswa dan hobi mereka
    query = """
        SELECT 
            m.nim,
            m.nama,
            GROUP_CONCAT(h.namahobi ORDER BY h.namahobi SEPARATOR ', ') as daftar_hobi,
            GROUP_CONCAT(CAST(h.kodehobi AS CHAR) ORDER BY h.namahobi) as hobi_ids
        FROM mahasiswa m
        LEFT JOIN mhshobi mh ON m.nim = mh.nim
        LEFT JOIN hobi h ON mh.kodehobi = h.kodehobi
        GROUP BY m.nim, m.nama
        ORDER BY m.nim
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Konversi string hobi_ids menjadi list dan pastikan tipe data string
    for row in result:
        if row['hobi_ids']:
            row['hobi_ids'] = [str(kodehobi) for kodehobi in row['hobi_ids'].split(',')]
        else:
            row['hobi_ids'] = []
            
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

# Fungsi untuk mendapatkan daftar hobi yang belum memiliki peminat
def get_hobi_tanpa_peminat():
    """Mendapatkan daftar hobi yang belum memiliki peminat"""
    db = buat_koneksi()
    if not db:
        return []
    
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT h.kodehobi, h.namahobi
        FROM hobi h
        LEFT JOIN mhshobi mh ON h.kodehobi = mh.kodehobi
        WHERE mh.kodehobi IS NULL
        ORDER BY h.namahobi
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# Fungsi-fungsi untuk statistik dashboard
def get_statistik_hobi():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    # Hitung total entri di tabel mhshobi
    cursor.execute("""
        SELECT COUNT(*) as total 
        FROM mhshobi
    """)
    total_peminat = cursor.fetchone()['total']
    
    if total_peminat == 0:
        cursor.close()
        return []
        
    # Ambil statistik hobi
    query = """
        SELECT 
            h.namahobi,
            COUNT(mh.nim) as jumlah_mahasiswa,
            ROUND(COUNT(mh.nim) * 100.0 / %s, 2) as persentase
        FROM hobi h
        LEFT JOIN mhshobi mh ON h.kodehobi = mh.kodehobi
        LEFT JOIN mahasiswa m ON mh.nim = m.nim
        GROUP BY h.kodehobi, h.namahobi
        ORDER BY jumlah_mahasiswa DESC, h.namahobi
    """
    
    cursor.execute(query, (total_peminat,))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_kota():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            kota,
            COUNT(*) as jumlah_mahasiswa,
            ROUND(AVG(tinggi_badan), 1) as rata_rata_tinggi,
            MIN(tinggi_badan) as min_tinggi,
            MAX(tinggi_badan) as max_tinggi
        FROM mahasiswa
        WHERE kota IS NOT NULL AND kota != ''
        GROUP BY kota
        ORDER BY jumlah_mahasiswa DESC
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_hobi_tanpa_peminat():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            h.kodehobi,
            h.namahobi
        FROM hobi h
        LEFT JOIN mhshobi mh ON h.kodehobi = mh.kodehobi
        WHERE mh.nim IS NULL
        ORDER BY h.namahobi
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_tinggi_badan():
    """Mendapatkan statistik tinggi badan mahasiswa"""
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    # Query untuk statistik dasar
    query = """
        SELECT 
            ROUND(AVG(tinggi_badan), 1) as rata_rata,
            ROUND(MAX(tinggi_badan), 1) as tertinggi,
            ROUND(MIN(tinggi_badan), 1) as terendah,
            (
                SELECT ROUND(tinggi_badan, 1)
                FROM (
                    SELECT tinggi_badan, COUNT(*) as freq
                    FROM mahasiswa
                    GROUP BY tinggi_badan
                    ORDER BY freq DESC
                    LIMIT 1
                ) as mode_table
            ) as modus,
            (
                SELECT ROUND(AVG(tinggi_badan), 1) as median
                FROM (
                    SELECT tinggi_badan,
                           @rownum := @rownum + 1 as rownum,
                           @total_rows := @rownum as total
                    FROM mahasiswa, (SELECT @rownum := 0) r
                    WHERE tinggi_badan IS NOT NULL
                    ORDER BY tinggi_badan
                ) as t
                WHERE rownum IN (FLOOR((@total_rows + 1)/2), CEIL((@total_rows + 1)/2))
            ) as median
        FROM mahasiswa
        WHERE tinggi_badan IS NOT NULL
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result

def get_statistik_kota():
    """Mendapatkan statistik mahasiswa berdasarkan kota"""
    db = buat_koneksi()
    if not db:
        return []
    
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT 
            kota,
            COUNT(*) as jumlah_mahasiswa,
            ROUND(AVG(tinggi_badan), 1) as rata_tinggi,
            GROUP_CONCAT(DISTINCT h.namahobi ORDER BY h.namahobi SEPARATOR ', ') as hobi_populer
        FROM mahasiswa m
        LEFT JOIN mhshobi mh ON m.nim = mh.nim
        LEFT JOIN hobi h ON mh.kodehobi = h.kodehobi
        WHERE kota IS NOT NULL AND kota != ''
        GROUP BY kota
        ORDER BY jumlah_mahasiswa DESC, kota
    """
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_ringkasan_dashboard():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    # Total mahasiswa
    cursor.execute("SELECT COUNT(*) as total FROM mahasiswa")
    total_mahasiswa = cursor.fetchone()['total']
    
    # Total hobi
    cursor.execute("SELECT COUNT(*) as total FROM hobi")
    total_hobi = cursor.fetchone()['total']
    
    # Mahasiswa dengan hobi
    cursor.execute("SELECT COUNT(DISTINCT nim) as total FROM mhshobi")
    mahasiswa_dengan_hobi = cursor.fetchone()['total']
    
    # Mahasiswa tanpa hobi
    mahasiswa_tanpa_hobi = total_mahasiswa - mahasiswa_dengan_hobi
    
    # Rata-rata usia
    cursor.execute("""
        SELECT AVG(TIMESTAMPDIFF(YEAR, tanggal_lahir, CURDATE())) as rata_rata_usia
        FROM mahasiswa
    """)
    rata_rata_usia = cursor.fetchone()['rata_rata_usia']
    
    cursor.close()
    
    return {
        'total_mahasiswa': total_mahasiswa,
        'total_hobi': total_hobi,
        'mahasiswa_dengan_hobi': mahasiswa_dengan_hobi,
        'mahasiswa_tanpa_hobi': mahasiswa_tanpa_hobi,
        'rata_rata_usia': round(rata_rata_usia, 1) if rata_rata_usia else 0
    }

def get_statistik_tahun_masuk():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            YEAR(tanggal_masuk) as tahun,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa
        WHERE tanggal_masuk IS NOT NULL
        GROUP BY YEAR(tanggal_masuk)
        ORDER BY tahun DESC
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_tinggi_per_kota():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            kota,
            ROUND(AVG(tinggi_badan), 1) as rata_rata_tinggi,
            MIN(tinggi_badan) as min_tinggi,
            MAX(tinggi_badan) as max_tinggi,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa
        WHERE kota IS NOT NULL AND tinggi_badan IS NOT NULL
        GROUP BY kota
        ORDER BY rata_rata_tinggi DESC
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_bulan_lahir():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            MONTH(tanggal_lahir) as bulan,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa
        WHERE tanggal_lahir IS NOT NULL
        GROUP BY MONTH(tanggal_lahir)
        ORDER BY bulan
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Konversi nomor bulan ke nama bulan
    bulan_names = [
        'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
        'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember'
    ]
    
    for row in result:
        row['nama_bulan'] = bulan_names[row['bulan'] - 1]
    
    cursor.close()
    return result

def get_statistik_tempat_lahir():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            tempat_lahir,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa
        WHERE tempat_lahir IS NOT NULL
        GROUP BY tempat_lahir
        ORDER BY jumlah_mahasiswa DESC
        LIMIT 10
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_ringkasan_tinggi():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            COUNT(*) as total_mahasiswa,
            ROUND(AVG(tinggi_badan), 1) as rata_rata_tinggi,
            MIN(tinggi_badan) as min_tinggi,
            MAX(tinggi_badan) as max_tinggi,
            COUNT(CASE WHEN tinggi_badan > 170 THEN 1 END) as tinggi_diatas_170,
            COUNT(CASE WHEN tinggi_badan < 160 THEN 1 END) as tinggi_dibawah_160
        FROM mahasiswa
        WHERE tinggi_badan IS NOT NULL
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result

def get_statistik_tinggi_per_tahun():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            YEAR(tanggal_masuk) as tahun,
            ROUND(AVG(tinggi_badan), 1) as rata_rata_tinggi,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa
        WHERE tanggal_masuk IS NOT NULL AND tinggi_badan IS NOT NULL
        GROUP BY YEAR(tanggal_masuk)
        ORDER BY tahun
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_hobi_per_kota():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            m.kota,
            h.namahobi,
            COUNT(*) as jumlah
        FROM mahasiswa m
        JOIN mhshobi mh ON m.nim = mh.nim
        JOIN hobi h ON mh.kodehobi = h.kodehobi
        WHERE m.kota IS NOT NULL
        GROUP BY m.kota, h.namahobi
        ORDER BY m.kota, jumlah DESC
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Mengorganisir data per kota
    hobi_per_kota = {}
    for row in result:
        if row['kota'] not in hobi_per_kota:
            hobi_per_kota[row['kota']] = []
        hobi_per_kota[row['kota']].append({
            'hobi': row['namahobi'],
            'jumlah': row['jumlah']
        })
    
    cursor.close()
    return hobi_per_kota

def get_statistik_tanggal_lahir():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            MONTH(tanggal_lahir) as bulan,
            DAY(tanggal_lahir) as tanggal,
            COUNT(*) as jumlah
        FROM mahasiswa
        WHERE tanggal_lahir IS NOT NULL
        GROUP BY MONTH(tanggal_lahir), DAY(tanggal_lahir)
        ORDER BY bulan, tanggal
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_usia():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            TIMESTAMPDIFF(YEAR, tanggal_lahir, CURDATE()) as usia,
            COUNT(*) as jumlah
        FROM mahasiswa
        WHERE tanggal_lahir IS NOT NULL
        GROUP BY usia
        ORDER BY usia
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    
    # Menghitung statistik tambahan
    total = sum(row['jumlah'] for row in result)
    if total > 0:
        for row in result:
            row['persentase'] = round((row['jumlah'] / total) * 100, 1)
    
    cursor.close()
    return result

def get_top_tempat_lahir():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            tempat_lahir,
            COUNT(*) as jumlah
        FROM mahasiswa
        WHERE tempat_lahir IS NOT NULL
        GROUP BY tempat_lahir
        ORDER BY jumlah DESC
        LIMIT 10
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_ringkasan_tinggi_badan():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            COUNT(*) as total_mahasiswa,
            ROUND(AVG(tinggi_badan), 1) as rata_rata_tinggi,
            MIN(tinggi_badan) as tinggi_minimum,
            MAX(tinggi_badan) as tinggi_maksimum,
            SUM(CASE WHEN tinggi_badan > 170 THEN 1 ELSE 0 END) as jumlah_diatas_170,
            SUM(CASE WHEN tinggi_badan < 160 THEN 1 ELSE 0 END) as jumlah_dibawah_160
        FROM mahasiswa
        WHERE tinggi_badan IS NOT NULL
    """
    
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    return result

def get_kombinasi_hobi_populer():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            h1.namahobi as hobi1,
            h2.namahobi as hobi2,
            COUNT(*) as jumlah_mahasiswa
        FROM mhshobi mh1
        JOIN mhshobi mh2 ON mh1.nim = mh2.nim AND mh1.kodehobi < mh2.kodehobi
        JOIN hobi h1 ON mh1.kodehobi = h1.kodehobi
        JOIN hobi h2 ON mh2.kodehobi = h2.kodehobi
        GROUP BY h1.kodehobi, h2.kodehobi, h1.namahobi, h2.namahobi
        ORDER BY jumlah_mahasiswa DESC
        LIMIT 10
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_statistik_jumlah_hobi():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        WITH hobi_count AS (
            SELECT 
                nim,
                COUNT(*) as jumlah_hobi
            FROM mhshobi
            GROUP BY nim
        )
        SELECT 
            jumlah_hobi,
            COUNT(*) as jumlah_mahasiswa,
            ROUND(AVG(jumlah_hobi) OVER (), 2) as rata_rata_hobi
        FROM hobi_count
        GROUP BY jumlah_hobi
        ORDER BY jumlah_hobi
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_distribusi_usia_kota():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            kota,
            TIMESTAMPDIFF(YEAR, tanggal_lahir, CURDATE()) as usia,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa
        WHERE kota IS NOT NULL AND tanggal_lahir IS NOT NULL
        GROUP BY kota, TIMESTAMPDIFF(YEAR, tanggal_lahir, CURDATE())
        ORDER BY kota, usia
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_tren_mahasiswa_per_bulan():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            YEAR(tanggal_masuk) as tahun,
            MONTH(tanggal_masuk) as bulan,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa
        WHERE tanggal_masuk IS NOT NULL
        GROUP BY YEAR(tanggal_masuk), MONTH(tanggal_masuk)
        ORDER BY tahun, bulan
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_hobi_per_kelompok_usia():
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    query = """
        SELECT 
            h.namahobi,
            CASE 
                WHEN TIMESTAMPDIFF(YEAR, m.tanggal_lahir, CURDATE()) < 20 THEN '< 20'
                WHEN TIMESTAMPDIFF(YEAR, m.tanggal_lahir, CURDATE()) < 25 THEN '20-24'
                ELSE '25+'
            END as kelompok_usia,
            COUNT(*) as jumlah_mahasiswa
        FROM mahasiswa m
        JOIN mhshobi mh ON m.nim = mh.nim
        JOIN hobi h ON mh.kodehobi = h.kodehobi
        WHERE m.tanggal_lahir IS NOT NULL
        GROUP BY h.namahobi, kelompok_usia
        ORDER BY h.namahobi, kelompok_usia
    """
    
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

def get_hobi_dengan_peminat():
    """Mendapatkan daftar hobi beserta jumlah dan daftar peminatnya"""
    db = buat_koneksi()
    cursor = db.cursor(dictionary=True)
    
    # Hitung total entri di tabel mhshobi
    cursor.execute("""
        SELECT COUNT(*) as total 
        FROM mhshobi
    """)
    total_peminat = cursor.fetchone()['total']
    
    if total_peminat == 0:
        cursor.close()
        return []
        
    # Ambil data hobi dengan peminat
    query = """
        SELECT 
            h.namahobi,
            COUNT(mh.nim) as jumlah_peminat,
            ROUND(COUNT(mh.nim) * 100.0 / %s, 2) as persentase,
            GROUP_CONCAT(m.nama ORDER BY m.nama SEPARATOR ', ') as daftar_peminat
        FROM hobi h
        LEFT JOIN mhshobi mh ON h.kodehobi = mh.kodehobi
        LEFT JOIN mahasiswa m ON mh.nim = m.nim
        GROUP BY h.kodehobi, h.namahobi
        ORDER BY jumlah_peminat DESC, h.namahobi
    """
    
    cursor.execute(query, (total_peminat,))
    result = cursor.fetchall()
    cursor.close()
    return result

def get_mahasiswa_tertua_termuda():
    """Mendapatkan 3 mahasiswa tertua dan termuda beserta detail mereka"""
    db = buat_koneksi()
    if not db:
        return None
    
    cursor = db.cursor(dictionary=True)
    
    # Query untuk 3 mahasiswa tertua
    query_tertua = """
    SELECT m.nama, 
           TIMESTAMPDIFF(YEAR, m.tanggal_lahir, CURDATE()) as usia,
           DATE_FORMAT(m.tanggal_lahir, '%d %M %Y') as tanggal_lahir_formatted
    FROM mahasiswa m
    ORDER BY m.tanggal_lahir ASC
    LIMIT 3
    """
    
    # Query untuk 3 mahasiswa termuda
    query_termuda = """
    SELECT m.nama, 
           TIMESTAMPDIFF(YEAR, m.tanggal_lahir, CURDATE()) as usia,
           DATE_FORMAT(m.tanggal_lahir, '%d %M %Y') as tanggal_lahir_formatted
    FROM mahasiswa m
    ORDER BY m.tanggal_lahir DESC
    LIMIT 3
    """
    
    cursor.execute(query_tertua)
    mahasiswa_tertua = cursor.fetchall()
    
    cursor.execute(query_termuda)
    mahasiswa_termuda = cursor.fetchall()
    
    cursor.close()
    db.close()
    
    return {
        'tertua': mahasiswa_tertua,
        'termuda': mahasiswa_termuda
    }
