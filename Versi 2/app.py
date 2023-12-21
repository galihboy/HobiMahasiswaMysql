# Galih Hermawan (https://galih.eu)

from flask import Flask, render_template, request, redirect, url_for
from db import buat_koneksi, get_mahasiswa_data, get_hobi_data, get_mhshobi_data, get_mahasiswa_hobi, get_mahasiswa_without_hobi

app = Flask(__name__)

# Konfigurasi koneksi MySQL
db = buat_koneksi()

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
    search_query = request.args.get('search', default='', type=str)
    mahasiswa_data = get_mahasiswa_data(search_query)
    return render_template('mahasiswa.html', mahasiswa_data=mahasiswa_data, search_query=search_query)

# Rute untuk menampilkan form tambah mahasiswa
@app.route('/tambah', methods=['GET', 'POST'])
def tambah_mahasiswa():
    if request.method == 'POST':
        # Ambil data dari form
        nim = request.form['nim']
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        kota = request.form['kota']
        tanggal_masuk = request.form['tanggal_masuk']
        tinggi_badan = request.form['tinggi_badan']

        # Lakukan operasi penambahan data ke dalam database
        cursor = db.cursor()
        query = "INSERT INTO mahasiswa (nim, nama, tempat_lahir, tanggal_lahir, kota, tanggal_masuk, tinggi_badan) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (nim, nama, tempat_lahir, tanggal_lahir, kota, tanggal_masuk, tinggi_badan)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect(url_for('data_mahasiswa'))

    return render_template('tambah_mahasiswa.html')

# Rute untuk menampilkan form edit mahasiswa
@app.route('/edit/<nim>', methods=['GET', 'POST'])
def edit_mahasiswa(nim):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM mahasiswa WHERE nim = %s"
    cursor.execute(query, (nim,))
    mahasiswa = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        # Ambil data dari form
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        kota = request.form['kota']
        tanggal_masuk = request.form['tanggal_masuk']
        tinggi_badan = request.form['tinggi_badan']

        # Lakukan operasi update data ke dalam database
        cursor = db.cursor()
        query = "UPDATE mahasiswa SET nama=%s, tempat_lahir=%s, tanggal_lahir=%s, kota=%s, tanggal_masuk=%s, tinggi_badan=%s " \
                "WHERE nim=%s"
        values = (nama, tempat_lahir, tanggal_lahir, kota, tanggal_masuk, tinggi_badan, nim)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect(url_for('data_mahasiswa'))

    return render_template('edit_mahasiswa.html', mahasiswa=mahasiswa)

# Rute untuk menghapus data mahasiswa
@app.route('/hapus/<nim>')
def hapus_mahasiswa(nim):
    cursor = db.cursor()
    query = "DELETE FROM mahasiswa WHERE nim = %s"
    cursor.execute(query, (nim,))
    db.commit()
    cursor.close()

    return redirect(url_for('data_mahasiswa'))

#----------- HOBI -----------
# Rute untuk halaman data hobi (CRUD)
@app.route('/hobi')
def data_hobi():
    search_query = request.args.get('search', default='', type=str)
    hobi_data = get_hobi_data(search_query)
    return render_template('hobi.html', hobi_data=hobi_data, search_query=search_query)

# Rute untuk menampilkan form tambah hobi
@app.route('/tambah_hobi', methods=['GET', 'POST'])
def tambah_hobi():
    if request.method == 'POST':
        # Ambil data dari form
        kodehobi = request.form['kodehobi']
        namahobi = request.form['namahobi']

        # Lakukan operasi penambahan data ke dalam database
        cursor = db.cursor()
        query = "INSERT INTO hobi (kodehobi, namahobi) VALUES (%s, %s)"
        values = (kodehobi, namahobi)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect(url_for('data_hobi'))

    return render_template('tambah_hobi.html')

# Rute untuk menampilkan form edit hobi
@app.route('/edit_hobi/<kodehobi>', methods=['GET', 'POST'])
def edit_hobi(kodehobi):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM hobi WHERE kodehobi = %s"
    cursor.execute(query, (kodehobi,))
    hobi = cursor.fetchone()
    cursor.close()

    if request.method == 'POST':
        # Ambil data dari form
        namahobi = request.form['namahobi']

        # Lakukan operasi update data ke dalam database
        cursor = db.cursor()
        query = "UPDATE hobi SET namahobi=%s WHERE kodehobi=%s"
        values = (namahobi, kodehobi)
        cursor.execute(query, values)
        db.commit()
        cursor.close()

        return redirect(url_for('data_hobi'))

    return render_template('edit_hobi.html', hobi=hobi)

# Rute untuk menghapus data hobi
@app.route('/hapus_hobi/<kodehobi>')
def hapus_hobi(kodehobi):
    cursor = db.cursor()
    query = "DELETE FROM hobi WHERE kodehobi = %s"
    cursor.execute(query, (kodehobi,))
    db.commit()
    cursor.close()

    return redirect(url_for('data_hobi'))

#-------- MAHASISWA HOBI ----------
# Rute untuk halaman data mhshobi (CRUD)
@app.route('/mhshobi')
def data_mhshobi():
    mhshobi_data = get_mhshobi_data()
    return render_template('mhshobi.html', mhshobi_data=mhshobi_data)

# Rute untuk menampilkan form tambah mhshobi
@app.route('/tambah_mhshobi', methods=['GET', 'POST'])
def tambah_mhshobi():
    if request.method == 'POST':
        # Ambil data dari form
        nim = request.form['nim']
        kodehobi_list = request.form.getlist('kodehobi')

        # Lakukan operasi penambahan data ke dalam database
        cursor = db.cursor()
        query = "INSERT INTO mhshobi (nim, kodehobi) VALUES (%s, %s)"
        values = [(nim, kodehobi) for kodehobi in kodehobi_list]
        cursor.executemany(query, values)
        db.commit()
        cursor.close()

        return redirect(url_for('data_mhshobi'))

        return redirect(url_for('data_mhshobi'))

    # Ambil data mahasiswa dan hobi untuk ditampilkan di form
    mahasiswa_data = get_mahasiswa_without_hobi()
    hobi_data = get_hobi_data()
    return render_template('tambah_mhshobi.html', mahasiswa_data=mahasiswa_data, hobi_data=hobi_data)

# Rute untuk menampilkan form edit mhshobi
@app.route('/edit_mhshobi/<nim>', methods=['GET', 'POST'])
def edit_mhshobi(nim):
    try:
        cursor = db.cursor(dictionary=True)

        if request.method == 'GET':
            # Dapatkan data mhshobi untuk mahasiswa dengan nim tertentu
            query = "SELECT mhshobi.nim, mahasiswa.nama as mahasiswa_nama, mhshobi.kodehobi, hobi.namahobi as hobi_nama " \
                    "FROM mhshobi " \
                    "JOIN mahasiswa ON mhshobi.nim = mahasiswa.nim " \
                    "JOIN hobi ON mhshobi.kodehobi = hobi.kodehobi " \
                    "WHERE mhshobi.nim = %s"
            cursor.execute(query, (nim,))
            mhshobi = cursor.fetchall()

            # Dapatkan nama mahasiswa
            mahasiswa_nama = mhshobi[0]['mahasiswa_nama'] if mhshobi else ""

            # Dapatkan kodehobi yang sudah dipilih
            kodehobi_checked = [str(row['kodehobi']) for row in mhshobi]

            # Dapatkan data hobi
            query_hobi = "SELECT * FROM hobi"
            cursor.execute(query_hobi)
            hobi_list = cursor.fetchall()

            return render_template('edit_mhshobi.html', nim=nim, mahshobi=mhshobi, mahasiswa_nama=mahasiswa_nama,
                                   kodehobi_checked=kodehobi_checked, hobi_list=hobi_list)

        elif request.method == 'POST':
            kodehobi_checked = request.form.getlist('kodehobi')

            # Lakukan pembaruan data ke dalam database
            delete_query = "DELETE FROM mhshobi WHERE nim = %s"
            cursor.execute(delete_query, (nim,))

            insert_query = "INSERT INTO mhshobi (nim, kodehobi) VALUES (%s, %s)"
            for kodehobi in kodehobi_checked:
                cursor.execute(insert_query, (nim, kodehobi))

            db.commit()

            return redirect(url_for('data_mhshobi'))

    finally:
        cursor.close()

    return redirect(url_for('index'))

# Rute untuk menghapus data mhshobi
@app.route('/hapus_mhshobi/<nim>')
def hapus_mhshobi(nim):
    cursor = db.cursor()
    query = "DELETE FROM mhshobi WHERE nim = %s"
    cursor.execute(query, (nim,))
    db.commit()
    cursor.close()

    return redirect(url_for('data_mhshobi'))

if __name__ == '__main__':
    app.run(debug=True)
