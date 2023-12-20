# HobiMahasiswaMysql
Aplikasi Flask Python CRUD Database MySQL HobiMahasiswa

## Deskripsi
Proyek ini adalah aplikasi sederhana yang dibangun dengan menggunakan Flask (framework web Python) dan MySQL sebagai database. Aplikasi ini menangani informasi tentang mahasiswa, hobi, dan hubungan antara keduanya.

## Fitur
- Menampilkan daftar mahasiswa beserta hobi-hobinya.
- Menambah, mengedit, dan menghapus data mahasiswa.
- Menambah, mengedit, dan menghapus data hobi.
- Menambah dan menghapus hubungan antara mahasiswa dan hobi.

## Catatan
- Halaman antarmuka tidak menggunakan CSS.
- Tidak menggunakan kode Javascript untuk keperluan apapun.
- Validasi data tidak dilakukan secara menyeluruh.
- Library yang digunakan adalah 
-- `Flask==2.0.2`
-- `mysql-connector-python==8.2.0`
- Pastikan MySQL telah diinstal dan dapat diakses oleh proyek.
- Restore (impor) basis data di fail `HobiMahasiswa.sql`
- Jika Anda menggunakan virtual environment, pastikan untuk mengaktifkannya sebelum menginstal pustaka.
- Konfigurasi database dapat diubah pada file `db.py`.

## Penggunaan
1. Pastikan Anda memiliki Python dan MySQL terinstal di komputer Anda.
2. Clone repositori ini: `git clone https://github.com/galihboy/HobiMahasiswaMysql.git`
3. Masuk ke direktori proyek: `cd HobiMahasiswaMysql`
4. (Opsional) Buat dan aktifkan virtual environment (venv):
- `python -m venv venv`
- `source venv/bin/activate`  # Untuk macOS/Linux
- `.\venv\Scripts\activate`  # Untuk Windows
5. Instal pustaka yang diperlukan: `pip install -r requirements.txt`
6. Atur konfigurasi database pada `db.py`.
7. Jalankan aplikasi: `python app.py`
8. Buka browser dan akses [http://localhost:5000](http://localhost:5000).

## Kontribusi
Silakan berkontribusi dengan membuat _pull request_ atau melaporkan _issue_.

## Lisensi
Proyek ini dilisensikan di bawah Lisensi MIT - lihat berkas [LICENSE](LICENSE) untuk informasi lebih lanjut.

## Kontak
Jika Anda memiliki pertanyaan atau saran, jangan ragu untuk menghubungi saya:
- Email: galih.hermawan@gmail.com
- Situs web: [https://galih.eu](https://galih.eu)

Terima kasih atas kontribusi dan dukungan Anda!
