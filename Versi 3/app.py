# Galih Hermawan (https://galih.eu)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from datetime import datetime
import db
from db import (buat_koneksi, get_mahasiswa_data, get_hobi_data, get_mhshobi_data,
                get_mahasiswa_hobi, get_mahasiswa_without_hobi, get_statistik_hobi,
                get_statistik_tinggi_badan, get_statistik_kota, get_ringkasan_dashboard, get_hobi_tanpa_peminat,
                get_statistik_tahun_masuk, get_statistik_tinggi_per_kota, get_statistik_bulan_lahir, 
                get_statistik_tempat_lahir, get_statistik_ringkasan_tinggi, get_top_tempat_lahir,
                get_statistik_tinggi_per_tahun, get_statistik_hobi_per_kota, get_statistik_tanggal_lahir, get_statistik_usia,
                get_ringkasan_tinggi_badan, get_kombinasi_hobi_populer, get_statistik_jumlah_hobi, get_distribusi_usia_kota, 
                get_tren_mahasiswa_per_bulan, get_hobi_per_kelompok_usia, get_hobi_dengan_peminat, get_mahasiswa_tertua_termuda)
from config import switch_mode, get_db_config

app = Flask(__name__)
app.secret_key = 'rahasia123'  # diperlukan untuk flash message

# Variabel global untuk menyimpan koneksi database
db = None

def init_db(mode=None):
    global db
    db = buat_koneksi(mode)
    return db is not None

# Inisialisasi koneksi database
init_db()

# Route untuk switch mode database
@app.route('/switch-mode', methods=['POST'])
def switch_db_mode():
    new_mode = switch_mode()
    success = init_db(new_mode)
    return jsonify({
        'success': success,
        'mode': new_mode,
        'message': f"Berhasil beralih ke mode {new_mode}" if success else f"Gagal beralih ke mode {new_mode}"
    })

# Route untuk mendapatkan status koneksi
@app.route('/connection-status')
def connection_status():
    config = get_db_config()
    is_connected = db is not None
    return jsonify({
        'connected': is_connected,
        'host': config['host'],
        'database': config['database'],
        'mode': 'online' if config['host'] != 'localhost' else 'local'
    })

# Route untuk halaman utama
@app.route('/')
def index():
    search_query = request.args.get('search', '')
    mahasiswa_hobi_data = get_mahasiswa_hobi(search_query)
    return render_template('index.html', mahasiswa_hobi_data=mahasiswa_hobi_data)

#------------ MAHASISWA ---------------

# Rute untuk halaman data mahasiswa (CRUD)
@app.route('/mahasiswa')
def data_mahasiswa():
    search = request.args.get('search', '')
    data_mahasiswa = get_mahasiswa_data(search)
    return render_template('mahasiswa.html', data_mahasiswa=data_mahasiswa)

@app.route('/mahasiswa/add', methods=['POST'])
def add_mahasiswa():
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_mahasiswa'))
    
    cursor = db.cursor()
    try:
        nim = request.form['nim']
        nama = request.form['nama']
        tempat_lahir = request.form.get('tempat_lahir')
        tanggal_lahir = request.form.get('tanggal_lahir')
        kota = request.form.get('kota')
        tanggal_masuk = request.form.get('tanggal_masuk')
        tinggi_badan = request.form.get('tinggi_badan')
        
        query = """
            INSERT INTO mahasiswa (nim, nama, tempat_lahir, tanggal_lahir, kota, tanggal_masuk, tinggi_badan) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nim, nama, tempat_lahir, tanggal_lahir, kota, tanggal_masuk, tinggi_badan))
        db.commit()
        flash(f'Mahasiswa {nama} berhasil ditambahkan', 'success')
        
    except mysql.connector.Error as err:
        db.rollback()
        if err.errno == 1062:  # Error code untuk duplicate entry
            flash(f'Error: NIM {nim} sudah terdaftar', 'error')
        else:
            flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_mahasiswa'))

@app.route('/mahasiswa/edit/<nim>', methods=['POST'])
def edit_mahasiswa(nim):
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_mahasiswa'))
    
    cursor = db.cursor()
    try:
        nama = request.form['nama']
        tempat_lahir = request.form.get('tempat_lahir')
        tanggal_lahir = request.form.get('tanggal_lahir')
        kota = request.form.get('kota')
        tanggal_masuk = request.form.get('tanggal_masuk')
        tinggi_badan = request.form.get('tinggi_badan')
        
        query = """
            UPDATE mahasiswa 
            SET nama=%s, tempat_lahir=%s, tanggal_lahir=%s, kota=%s, tanggal_masuk=%s, tinggi_badan=%s
            WHERE nim=%s
        """
        cursor.execute(query, (nama, tempat_lahir, tanggal_lahir, kota, tanggal_masuk, tinggi_badan, nim))
        db.commit()
        flash(f'Data mahasiswa {nama} berhasil diperbarui', 'success')
        
    except mysql.connector.Error as err:
        db.rollback()
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_mahasiswa'))

@app.route('/mahasiswa/delete/<nim>', methods=['POST'])
def delete_mahasiswa(nim):
    db = buat_koneksi()
    if db is None:
        return redirect(url_for('data_mahasiswa'))
    
    cursor = db.cursor()
    # Hapus data dari tabel mhshobi terlebih dahulu
    query_mhshobi = "DELETE FROM mhshobi WHERE nim=%s"
    query_mahasiswa = "DELETE FROM mahasiswa WHERE nim=%s"
    
    try:
        cursor.execute(query_mhshobi, (nim,))
        cursor.execute(query_mahasiswa, (nim,))
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        
    return redirect(url_for('data_mahasiswa'))

#----------- HOBI -----------
# Rute untuk halaman data hobi (CRUD)
@app.route('/hobi')
def data_hobi():
    search_query = request.args.get('search', '')
    data_hobi = get_hobi_data(search_query)
    statistik_hobi = get_statistik_hobi()
    return render_template('hobi.html', 
                         data_hobi=data_hobi,
                         statistik_hobi=statistik_hobi)

@app.route('/hobi/add', methods=['POST'])
def add_hobi():
    kodehobi = request.form['kodehobi']
    namahobi = request.form['namahobi']
    
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_hobi'))
    
    cursor = db.cursor()
    query = "INSERT INTO hobi (kodehobi, namahobi) VALUES (%s, %s)"
    values = (kodehobi, namahobi)
    
    try:
        cursor.execute(query, values)
        db.commit()
        flash(f'Hobi {namahobi} berhasil ditambahkan', 'success')
    except mysql.connector.Error as err:
        if err.errno == 1062:  # Error code untuk duplicate entry
            flash(f'Error: Kode hobi {kodehobi} sudah terdaftar', 'error')
        else:
            flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_hobi'))

@app.route('/hobi/edit/<kodehobi>', methods=['POST'])
def edit_hobi(kodehobi):
    namahobi = request.form['namahobi']
    
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_hobi'))
    
    cursor = db.cursor()
    query = "UPDATE hobi SET namahobi=%s WHERE kodehobi=%s"
    values = (namahobi, kodehobi)
    
    try:
        cursor.execute(query, values)
        db.commit()
        flash(f'Hobi {namahobi} berhasil diperbarui', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_hobi'))

@app.route('/hobi/delete/<kodehobi>', methods=['POST'])
def delete_hobi(kodehobi):
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_hobi'))
    
    cursor = db.cursor()
    try:
        # Cek apakah hobi masih digunakan
        cursor.execute("SELECT COUNT(*) as count FROM mhshobi WHERE kodehobi = %s", (kodehobi,))
        result = cursor.fetchone()
        if result[0] > 0:
            flash(f'Error: Hobi ini masih digunakan oleh {result[0]} mahasiswa', 'error')
            return redirect(url_for('data_hobi'))

        # Hapus data dari tabel mhshobi terlebih dahulu
        cursor.execute("DELETE FROM mhshobi WHERE kodehobi=%s", (kodehobi,))
        
        # Ambil nama hobi untuk pesan sukses
        cursor.execute("SELECT namahobi FROM hobi WHERE kodehobi=%s", (kodehobi,))
        hobi = cursor.fetchone()
        nama_hobi = hobi[0] if hobi else kodehobi
        
        # Hapus hobi
        cursor.execute("DELETE FROM hobi WHERE kodehobi=%s", (kodehobi,))
        db.commit()
        
        flash(f'Hobi {nama_hobi} berhasil dihapus', 'success')
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_hobi'))

#-------- MAHASISWA HOBI ----------
# Rute untuk halaman data mhshobi (CRUD)
@app.route('/mhshobi')
def data_mhshobi():
    # Data mahasiswa yang sudah memiliki hobi
    data_mhshobi = get_mhshobi_data()
    # Data mahasiswa yang belum memiliki hobi
    mahasiswa_tanpa_hobi = get_mahasiswa_without_hobi()
    # Data hobi yang belum memiliki peminat
    hobi_tanpa_peminat = get_hobi_tanpa_peminat()
    # Data semua hobi
    hobi_data = get_hobi_data()
    # Data hobi beserta peminatnya
    hobi_dengan_peminat = get_hobi_dengan_peminat()
    
    # Debug: Print data untuk pemeriksaan
    print("\nData MhsHobi:")
    for data in data_mhshobi:
        print(f"NIM: {data['nim']}, Nama: {data['nama']}, Hobi IDs: {data['hobi_ids']}")
    
    print("\nHobi Data:")
    for hobi in hobi_data:
        print(f"Kode: {hobi['kodehobi']}, Nama: {hobi['namahobi']}")
    
    return render_template('mhshobi.html',
                         data_mhshobi=data_mhshobi,
                         mahasiswa_tanpa_hobi=mahasiswa_tanpa_hobi,
                         hobi_tanpa_peminat=hobi_tanpa_peminat,
                         hobi_data=hobi_data,
                         hobi_dengan_peminat=hobi_dengan_peminat)

@app.route('/mhshobi/add', methods=['POST'])
def add_mhshobi():
    nim = request.form['nim']
    hobi_list = request.form.getlist('hobi')
    
    if not hobi_list:
        flash('Error: Pilih minimal satu hobi', 'error')
        return redirect(url_for('data_mhshobi'))
    
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_mhshobi'))
    
    cursor = db.cursor()
    
    try:
        # Ambil nama mahasiswa
        cursor.execute("SELECT nama FROM mahasiswa WHERE nim=%s", (nim,))
        nama_mahasiswa = cursor.fetchone()[0]
        
        hobi_berhasil = []
        hobi_gagal = []
        
        for kodehobi in hobi_list:
            # Cek apakah kombinasi nim dan kodehobi sudah ada
            cursor.execute("SELECT COUNT(*) FROM mhshobi WHERE nim=%s AND kodehobi=%s", (nim, kodehobi))
            count = cursor.fetchone()[0]
            
            if count > 0:
                # Ambil nama hobi untuk pesan error
                cursor.execute("SELECT namahobi FROM hobi WHERE kodehobi=%s", (kodehobi,))
                namahobi = cursor.fetchone()[0]
                hobi_gagal.append(namahobi)
            else:
                # Tambahkan data baru
                cursor.execute("INSERT INTO mhshobi (nim, kodehobi) VALUES (%s, %s)", (nim, kodehobi))
                # Ambil nama hobi untuk pesan sukses
                cursor.execute("SELECT namahobi FROM hobi WHERE kodehobi=%s", (kodehobi,))
                namahobi = cursor.fetchone()[0]
                hobi_berhasil.append(namahobi)
        
        db.commit()
        
        # Tampilkan pesan sesuai hasil
        if hobi_berhasil:
            flash(f'Hobi {", ".join(hobi_berhasil)} berhasil ditambahkan untuk mahasiswa {nama_mahasiswa}', 'success')
        if hobi_gagal:
            flash(f'Hobi {", ".join(hobi_gagal)} sudah ada untuk mahasiswa {nama_mahasiswa}', 'warning')
            
    except mysql.connector.Error as err:
        db.rollback()
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_mhshobi'))

@app.route('/mhshobi/edit/<nim>', methods=['POST'])
def edit_mhshobi(nim):
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_mhshobi'))
    
    cursor = db.cursor()
    try:
        # Ambil nama mahasiswa untuk pesan
        cursor.execute("SELECT nama FROM mahasiswa WHERE nim=%s", (nim,))
        nama = cursor.fetchone()[0]
        
        # Ambil hobi yang dipilih dari form
        hobi_baru = request.form.getlist('hobi')
        
        # Hapus semua hobi yang ada
        cursor.execute("DELETE FROM mhshobi WHERE nim=%s", (nim,))
        
        # Tambahkan hobi-hobi yang baru dipilih
        if hobi_baru:
            values = [(nim, kodehobi) for kodehobi in hobi_baru]
            cursor.executemany("INSERT INTO mhshobi (nim, kodehobi) VALUES (%s, %s)", values)
        
        db.commit()
        flash(f'Hobi mahasiswa {nama} berhasil diperbarui', 'success')
        
    except mysql.connector.Error as err:
        db.rollback()
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_mhshobi'))

@app.route('/mhshobi/delete/<nim>/<kodehobi>', methods=['POST'])
def delete_mhshobi(nim, kodehobi):
    db = buat_koneksi()
    if db is None:
        flash('Error: Tidak dapat terhubung ke database', 'error')
        return redirect(url_for('data_mhshobi'))
    
    cursor = db.cursor()
    try:
        # Ambil nama mahasiswa untuk pesan
        cursor.execute("SELECT nama FROM mahasiswa WHERE nim=%s", (nim,))
        nama = cursor.fetchone()[0]
        
        if kodehobi == 'all':
            # Hapus semua hobi mahasiswa
            cursor.execute("DELETE FROM mhshobi WHERE nim=%s", (nim,))
            flash(f'Semua hobi mahasiswa {nama} berhasil dihapus', 'success')
        else:
            # Hapus hobi spesifik
            cursor.execute("SELECT namahobi FROM hobi WHERE kodehobi=%s", (kodehobi,))
            namahobi = cursor.fetchone()[0]
            
            cursor.execute("DELETE FROM mhshobi WHERE nim=%s AND kodehobi=%s", (nim, kodehobi))
            flash(f'Hobi {namahobi} dari mahasiswa {nama} berhasil dihapus', 'success')
        
        db.commit()
    except mysql.connector.Error as err:
        flash(f'Error: {err}', 'error')
    finally:
        cursor.close()
        
    return redirect(url_for('data_mhshobi'))

# Route untuk laporan
@app.route('/laporan')
def laporan():
    filter_type = request.args.get('filter_type', '')
    filter_value = request.args.get('filter_value', '')
    
    # Debug: print nilai yang diterima
    print(f"Filter Type: {filter_type}")
    print(f"Filter Value: {filter_value}")
    
    if filter_type and filter_value and filter_value.strip():  # Pastikan filter_value tidak kosong
        db = buat_koneksi()
        cursor = db.cursor(dictionary=True)
        
        try:
            if filter_type == 'date':
                query = """
                    SELECT * FROM mahasiswa 
                    WHERE DATE(tanggal_masuk) = DATE(%s)
                    ORDER BY nim
                """
                cursor.execute(query, (filter_value,))
            elif filter_type == 'year':
                year_value = int(filter_value.strip())  # Konversi ke integer
                query = """
                    SELECT * FROM mahasiswa 
                    WHERE YEAR(tanggal_masuk) = %s
                    ORDER BY nim
                """
                cursor.execute(query, (year_value,))
            elif filter_type == 'month':
                month_value = int(filter_value.strip())  # Konversi ke integer
                query = """
                    SELECT * FROM mahasiswa 
                    WHERE MONTH(tanggal_masuk) = %s
                    ORDER BY nim
                """
                cursor.execute(query, (month_value,))
                
            mahasiswa_list = cursor.fetchall()
        except (ValueError, TypeError) as e:
            print(f"Error in filter: {e}")
            mahasiswa_list = []
        finally:
            cursor.close()
    else:
        mahasiswa_list = get_mahasiswa_data()
    
    return render_template('laporan.html', 
                         mahasiswa_list=mahasiswa_list,
                         filter_type=filter_type,
                         filter_value=filter_value)

# Route untuk dashboard
@app.route('/')
@app.route('/dashboard')
def dashboard():
    ringkasan = get_ringkasan_dashboard()
    statistik_hobi = get_statistik_hobi()
    statistik_tinggi = get_statistik_tinggi_badan()
    statistik_kota = get_statistik_kota()
    hobi_tanpa_peminat = get_hobi_tanpa_peminat()
    statistik_tahun = get_statistik_tahun_masuk()
    statistik_bulan = get_statistik_bulan_lahir()
    mahasiswa_tertua_termuda = get_mahasiswa_tertua_termuda()
    
   
    return render_template('dashboard.html', 
                         ringkasan=ringkasan,
                         statistik_hobi=statistik_hobi,
                         statistik_tinggi=statistik_tinggi,
                         statistik_kota=statistik_kota,
                         hobi_tanpa_peminat=hobi_tanpa_peminat,
                         statistik_tahun=statistik_tahun,
                         statistik_bulan=statistik_bulan,
                         mahasiswa_tertua_termuda=mahasiswa_tertua_termuda)

if __name__ == '__main__':
    app.run(debug=True)
