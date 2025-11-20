# 🎓 Sistem Manajemen Mahasiswa dan Hobi

Aplikasi web berbasis Flask untuk mengelola data mahasiswa dan hobi mereka dengan fitur CRUD lengkap, dashboard interaktif, dan laporan.

## 🎯 Tujuan Proyek

Proyek ini dikembangkan sebagai **materi demonstrasi CRUD (Create, Read, Update, Delete)** untuk:

### 📚 Mata Kuliah Pemrograman Basis Data
- **Program Studi**: Teknik Informatika
- **Institusi**: Universitas Komputer Indonesia (UNIKOM)
- **Fokus**: Implementasi operasi database dengan Python Flask dan MySQL

### 🌐 Pembelajaran Umum
Proyek ini juga cocok untuk:
- Mahasiswa yang belajar web development
- Developer pemula yang ingin memahami Flask dan MySQL
- Siapa saja yang ingin belajar membuat aplikasi CRUD lengkap
- Referensi untuk tugas akhir atau project pribadi

## 📋 Deskripsi

Proyek ini adalah sistem informasi yang memungkinkan pengelolaan data mahasiswa, hobi, dan relasi antara keduanya. Aplikasi ini dikembangkan dalam 3 versi dengan peningkatan fitur bertahap, menunjukkan evolusi dari aplikasi sederhana hingga aplikasi production-ready.

## 🚀 Versi Aplikasi

### Versi 1 - Basic (Raw HTML)
- CRUD dasar untuk Mahasiswa, Hobi, dan Relasi
- Tanpa JavaScript dan CSS framework
- Template HTML sederhana

### Versi 2 - Enhanced UI
- Penambahan Bootstrap untuk UI yang lebih baik
- JavaScript untuk interaktivitas
- Tampilan yang lebih modern

### Versi 3 - Full Featured ⭐ (Recommended)
- Dashboard interaktif dengan Chart.js
- Fitur sorting pada semua tabel
- Export laporan ke Excel
- Statistik lengkap dan visualisasi data
- Dual database support (lokal & cloud)
- Responsive design

## ✨ Fitur Utama (Versi 3)

### 📊 Dashboard
- Ringkasan statistik (total mahasiswa, hobi, dll)
- Grafik distribusi hobi (bar chart)
- Pie chart kota tinggal dan tempat lahir
- Distribusi bulan lahir
- Info mahasiswa tertua/termuda
- Statistik tinggi badan

### 👥 Manajemen Data
- **CRUD Mahasiswa**: Tambah, edit, hapus data mahasiswa
- **CRUD Hobi**: Kelola daftar hobi
- **Relasi Mahasiswa-Hobi**: Assign multiple hobi per mahasiswa
- **Pencarian**: Search di semua kolom
- **Sorting**: Klik header kolom untuk sort ASC/DESC

### 📄 Laporan
- Filter berdasarkan tanggal/bulan/tahun masuk
- Export ke Excel (.xlsx)
- Print-friendly layout
- Statistik ringkasan
- Perhitungan usia otomatis

### 🎨 UI/UX
- Bootstrap 5 responsive design
- Font Awesome icons
- Flash messages untuk feedback
- Dark navbar dengan gradient footer
- Sortable tables dengan visual indicator

## 🛠️ Teknologi

**Backend:**
- Python 3.x
- Flask 2.0.2
- MySQL Connector Python 8.2.0

**Frontend:**
- Bootstrap 5.1.3
- Chart.js
- Font Awesome 6.0.0
- jQuery 3.6.0
- SheetJS (untuk export Excel)

**Database:**
- MySQL / MariaDB
- TiDB Cloud (optional)

## 📦 Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/galihboy/HobiMahasiswaMysql.git
cd HobiMahasiswaMysql
```

### 2. Pilih Versi
```bash
cd "Versi 3"  # Recommended
```

### 3. Setup Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Database

**Opsi A - Database Lokal:**
```bash
mysql -u root -p < HobiMahasiswa.sql
```

**Opsi B - Database Cloud:**
Edit file `.env`:
```env
DB_MODE=online
HOST_ONLINE=your_host
PORT_ONLINE=your_port
USER_ONLINE=your_username
PASSWORD_ONLINE=your_password
DATABASE_ONLINE=proyek_hobimahasiswa
```

### 6. Jalankan Aplikasi
```bash
python app.py
```

Akses aplikasi di: `http://127.0.0.1:5000`

## 📁 Struktur Database

### Tabel `mahasiswa`
- `nim` (PK) - Nomor Induk Mahasiswa
- `nama` - Nama lengkap
- `tempat_lahir` - Tempat kelahiran
- `tanggal_lahir` - Tanggal lahir
- `kota` - Kota tinggal saat ini
- `tanggal_masuk` - Tanggal masuk kuliah
- `tinggi_badan` - Tinggi badan (cm)

### Tabel `hobi`
- `kodehobi` (PK) - Kode hobi
- `namahobi` - Nama hobi

### Tabel `mhshobi`
- `nim` (FK) - Referensi ke mahasiswa
- `kodehobi` (FK) - Referensi ke hobi

## 🎯 Fitur Unggulan

### Dashboard Interaktif
- 📈 Visualisasi data dengan Chart.js
- 🎨 Warna-warni yang informatif
- 📊 Multiple chart types (bar, pie, donut)

### Sorting & Filtering
- 🔄 Sort semua kolom dengan klik
- 🔍 Filter laporan berdasarkan periode
- 🎯 Pencarian real-time

### Export & Print
- 📥 Export ke Excel dengan satu klik
- 🖨️ Print-friendly layout
- 📄 Format yang rapi

## 🔧 Konfigurasi

### Database Mode
Edit `.env` untuk switch antara lokal dan cloud:
```env
DB_MODE=local   # atau 'online'
```

### Secret Key
Ganti secret key di `app.py` untuk production:
```python
app.secret_key = 'your-secret-key-here'
```

## 📸 Screenshots

*(Tambahkan screenshots aplikasi Anda di sini)*

## 🤝 Kontribusi

1. Fork repository
2. Buat branch fitur (`git checkout -b feature-amazing`)
3. Commit perubahan (`git commit -m 'Add amazing feature'`)
4. Push ke branch (`git push origin feature-amazing`)
5. Buat Pull Request

## 📝 Changelog

### Versi 3.0 (Latest)
- ✅ Dashboard dengan Chart.js
- ✅ Sortable tables
- ✅ Export to Excel
- ✅ Dual database support
- ✅ Responsive design
- ✅ Enhanced UI/UX

### Versi 2.0
- ✅ Bootstrap integration
- ✅ JavaScript interactivity
- ✅ Improved layout

### Versi 1.0
- ✅ Basic CRUD operations
- ✅ Raw HTML templates

## 📄 Lisensi

MIT License - Lihat file [LICENSE](LICENSE) untuk detail

## 👨‍💻 Pengembang

**Galih Hermawan**
- Website: [https://galih.eu](https://galih.eu)
- Blog: [https://blog.galih.eu](https://blog.galih.eu)
- GitHub: [@galihboy](https://github.com/galihboy)
- YouTube: [@galihhermawan](https://www.youtube.com/@galihhermawan)

## 🎓 Untuk Mahasiswa & Pembelajar

### Konsep yang Dipelajari:
- ✅ **CRUD Operations** - Create, Read, Update, Delete
- ✅ **Database Design** - Normalisasi, relasi tabel, foreign key
- ✅ **Web Framework** - Flask routing, templates, forms
- ✅ **SQL Queries** - SELECT, INSERT, UPDATE, DELETE, JOIN
- ✅ **Frontend Integration** - HTML, CSS, JavaScript
- ✅ **Data Visualization** - Chart.js untuk grafik
- ✅ **Best Practices** - MVC pattern, code organization

### Cocok untuk:
- 📖 Tugas mata kuliah Pemrograman Basis Data
- 🎯 Project akhir semester
- 💼 Portfolio web development
- 🚀 Belajar mandiri full-stack development

## 🙏 Acknowledgments

- **UNIKOM** - Universitas Komputer Indonesia
- **Prodi Teknik Informatika** - Untuk kesempatan mengembangkan materi pembelajaran
- Bootstrap team untuk framework CSS yang luar biasa
- Chart.js untuk library visualisasi data
- Flask community untuk framework yang powerful
- Semua mahasiswa dan pembelajar yang menggunakan project ini

---

## 📞 Kontak & Dukungan

Jika Anda mahasiswa yang menggunakan project ini untuk pembelajaran atau memiliki pertanyaan:
- 📧 Email: [Kontak via website](https://galih.eu)
- 💬 Diskusi: Gunakan GitHub Issues untuk pertanyaan teknis
- 📺 Tutorial: Cek channel YouTube untuk video tutorial

---

⭐ **Jika project ini membantu pembelajaran Anda, berikan star di GitHub!**

**Made with ❤️ for Education by Galih Hermawan**
