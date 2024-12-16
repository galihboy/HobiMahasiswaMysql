# Sistem Manajemen Mahasiswa dan Hobi

Proyek ini adalah aplikasi berbasis web untuk mengelola data mahasiswa dan hobi mereka. Aplikasi ini dibangun menggunakan Flask dan MySQL.

## Fitur

- **Operasi CRUD untuk Mahasiswa**: Tambah, edit, hapus, dan lihat data mahasiswa.
- **Operasi CRUD untuk Hobi**: Tambah, edit, hapus, dan lihat data hobi.
- **Kelola Hobi Mahasiswa**: Tetapkan hobi untuk mahasiswa dan kelola mereka.
- **Laporan dan Dashboard**: Buat laporan dan lihat statistik di dashboard.
- **Beralih Mode Database**: Beralih antara mode database lokal dan cloud.

## Instalasi

1. **Clone repository**:
    ```sh
    git clone https://github.com/galihboy/HobiMahasiswaMysql.git
    cd HobiMahasiswaMysql
    ```

2. **Buat virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # Pada Windows gunakan `venv\Scripts\activate`
    ```

3. **Instal dependensi**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Konfigurasi database**:
    - Perbarui file `config.py` dengan kredensial database Anda.

5. **Inisialisasi database**:
    - Jalankan skrip SQL yang disediakan di folder `sql` untuk membuat tabel yang diperlukan.

## Penggunaan

1. **Jalankan aplikasi**:
    ```sh
    flask run
    ```

2. **Akses aplikasi**:
    - Buka browser web Anda dan pergi ke `http://127.0.0.1:5000`.

## Struktur Proyek

- `app.py`: File aplikasi utama.
- `db.py`: Koneksi database dan fungsi query.
- `templates/`: Template HTML untuk aplikasi.
- `static/`: File statis (CSS, JavaScript, gambar).
- `config.py`: File konfigurasi untuk pengaturan database.
- `sql/`: Skrip SQL untuk inisialisasi database.

## Kontribusi

1. Fork repository ini.
2. Buat branch baru (`git checkout -b feature-branch`).
3. Lakukan perubahan Anda.
4. Commit perubahan Anda (`git commit -m 'Tambahkan fitur baru'`).
5. Push ke branch (`git push origin feature-branch`).
6. Buka pull request.

## Lisensi

Proyek ini dilisensikan di bawah MIT License.


## Pengembang

- Galih Hermawan
- Website: [https://galih.eu](https://galih.eu)