# Sistem Manajemen Mahasiswa dan Hobi

Proyek ini adalah aplikasi berbasis web untuk mengelola data mahasiswa dan hobi mereka. Aplikasi ini dibangun menggunakan Flask dan MySQL dengan dukungan database lokal dan cloud.

## 📊 Data Terkini

Database memiliki:
- **30 Mahasiswa** dari 6 kota berbeda
- **25 Hobi** yang bervariasi
- **Relasi** mahasiswa-hobi yang bervariasi (setiap mahasiswa memiliki 0-5 hobi)

## ✨ Fitur

- **Operasi CRUD untuk Mahasiswa**: Tambah, edit, hapus, dan lihat data mahasiswa dengan pencarian di semua kolom.
- **Operasi CRUD untuk Hobi**: Tambah, edit, hapus, dan lihat data hobi dengan tracking peminat.
- **Kelola Hobi Mahasiswa**: Tetapkan multiple hobi untuk mahasiswa dan kelola relasi mereka.
- **Dashboard Interaktif**: Visualisasi data dengan Chart.js (bar chart, pie chart).
- **Laporan Lengkap**: Filter berdasarkan tanggal, bulan, atau tahun masuk.
- **Statistik Detail**: Analisis tinggi badan, distribusi per kota, hobi populer.
- **Beralih Mode Database**: Switch antara database lokal dan cloud (TiDB) secara dinamis.

## 🚀 Instalasi

1. **Clone repository**:
    ```bash
    git clone https://github.com/galihboy/HobiMahasiswaMysql.git
    cd HobiMahasiswaMysql/Versi\ 3
    ```

2. **Buat virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Pada Windows: venv\Scripts\activate
    ```

3. **Instal dependensi**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Setup database**:
    
    **Opsi A - Database Lokal:**
    ```bash
    # Import database
    mysql -u root -p < HobiMahasiswa.sql
    ```
    
    **Opsi B - Database Cloud:**
    - Edit file `.env` dan set `DB_MODE=online`
    - Konfigurasi kredensial database di file `.env`

## 💻 Penggunaan

1. **Jalankan aplikasi**:
    ```bash
    python app.py
    # atau
    flask run
    ```

2. **Akses aplikasi**:
    - Buka browser: `http://127.0.0.1:5000`

## 📁 Struktur Proyek

```
Versi 3/
├── app.py                      # Aplikasi Flask utama dengan routing
├── db.py                       # Layer database dengan fungsi query
├── config.py                   # Konfigurasi database (lokal & cloud)
├── requirements.txt            # Dependencies Python
├── HobiMahasiswa.sql          # Database schema
├── templates/                 # Template HTML
│   ├── base.html             # Base template
│   ├── dashboard.html        # Dashboard dengan chart
│   ├── mahasiswa.html        # CRUD mahasiswa
│   ├── hobi.html             # CRUD hobi
│   ├── mhshobi.html          # Relasi mahasiswa-hobi
│   ├── laporan.html          # Laporan dan filter
│   └── index.html            # Halaman utama
└── static/
    └── css/
        └── style.css         # Custom CSS
```

## 🎯 Fitur Unggulan

### Dashboard Interaktif
- Grafik distribusi hobi (bar chart)
- Pie chart distribusi kota dan tahun masuk
- Statistik tinggi badan (rata-rata, median, modus, min, max)
- Ringkasan mahasiswa dengan/tanpa hobi

### Pencarian & Filter
- Pencarian di semua kolom mahasiswa
- Filter laporan berdasarkan tanggal/bulan/tahun masuk
- Tracking hobi tanpa peminat

### Analitik Lanjutan
- Top 5 hobi paling populer
- Statistik per kota (jumlah, rata-rata tinggi, hobi populer)
- Mahasiswa dengan hobi terbanyak
- Distribusi mahasiswa per tahun masuk

## 🔧 Konfigurasi Database

### Mode Lokal (Default)
```python
DB_LOCAL = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'proyek_hobimahasiswa'
}
```

### Mode Online (Cloud Database)
Edit file `.env`:
```env
DB_MODE=online
HOST_ONLINE=your_host
PORT_ONLINE=your_port
USER_ONLINE=your_username
PASSWORD_ONLINE=your_password
DATABASE_ONLINE=proyek_hobimahasiswa
```

## 📊 Contoh Data

### Mahasiswa
- 30 mahasiswa dari 6 kota (Bandung, Jakarta, Surabaya, Semarang, Yogyakarta, Malang)
- Tinggi badan: 158-180 cm
- Tahun masuk: 2009-2011

### Hobi (25 jenis)
Game, Sepak bola, Basket, Musik, Membaca, Tidur, Koding, Renang, Travelling, Makan, Fotografi, Memasak, Menulis, Menggambar, Berkebun, Yoga, Hiking, Memancing, Vlogging, Desain Grafis, Bermain Alat Musik, Menari, Bersepeda, Skateboard, Badminton

## 🤝 Kontribusi

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature-branch`)
3. Commit perubahan (`git commit -m 'Tambahkan fitur baru'`)
4. Push ke branch (`git push origin feature-branch`)
5. Buat Pull Request

## Lisensi

Proyek ini dilisensikan di bawah MIT License.


## Pengembang

- Galih Hermawan
- Website: [https://galih.eu](https://galih.eu)