# SIMRS - Sistem Informasi Manajemen Rumah Sakit

Aplikasi web untuk manajemen operasional rumah sakit berbasis Django.

---

## Catatan Proyek

> **Proyek ini dibuat sebagai sarana pembelajaran dan transisi pengenalan framework Django bagi developer yang terbiasa dengan Laravel.**
>
> Dikembangkan oleh **Dimas** dengan bantuan **GitHub Copilot** untuk memenuhi rasa penasaran dan mengeksplorasi potensi Django sebagai alternatif framework untuk proyek hobi.

---

## Tech Stack

| Komponen | Teknologi |
|----------|-----------|
| Backend | Django 5.0 |
| Database | MySQL 8.0 |
| Frontend | Bootstrap 5.3, Bootstrap Icons |
| Font | Plus Jakarta Sans (Google Fonts) |
| Data Faker | Faker 38.2.0 |

---

## Fitur Utama

- **Manajemen Pasien** - Data pasien, riwayat medis, asuransi
- **Manajemen Dokter** - Spesialisasi, jadwal praktek, ketersediaan
- **Rekam Medis Elektronik (EMR)** - Diagnosis, vital signs, tindakan medis
- **Farmasi & Apotek** - Inventaris obat, resep elektronik, stok
- **Laboratorium** - Permintaan pemeriksaan, hasil lab, parameter
- **Rawat Inap** - Manajemen ruangan, kamar, monitoring pasien
- **Rawat Jalan** - Pendaftaran, antrian, kunjungan
- **Keuangan** - Invoice, pembayaran, laporan keuangan

---

## Struktur Proyek

```
Sistem-Informasi-Manajemen-Rumah-Sakit-Djanggo/
├── apps/
│   ├── accounts/       # User & Authentication
│   ├── pasien/         # Data Pasien
│   ├── dokter/         # Data Dokter & Spesialisasi
│   ├── rekam_medis/    # Rekam Medis Elektronik
│   ├── apotek/         # Farmasi & Obat
│   ├── laboratorium/   # Pemeriksaan Lab
│   ├── rawat_inap/     # Rawat Inap & Ruangan
│   ├── rawat_jalan/    # Rawat Jalan & Antrian
│   ├── keuangan/       # Invoice & Pembayaran
│   └── dashboard/      # Landing Page
├── config/             # Django Settings
├── templates/          # HTML Templates
├── static/             # Static Files
├── media/              # Upload Files
└── docs/               # Dokumentasi
```

---

## Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd Sistem-Informasi-Manajemen-Rumah-Sakit-Djanggo
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Environment

Buat file `.env` di root folder:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_ENGINE=mysql
DATABASE_NAME=rumah_sakit_db
DATABASE_USER=root
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

### 5. Migrasi Database

```bash
python manage.py migrate
```

### 6. Buat Superuser

```bash
python manage.py createsuperuser
```

### 7. Seed Data (Opsional)

```bash
python manage.py seed_data
```

### 8. Jalankan Server

```bash
python manage.py runserver
```

Akses aplikasi di: `http://localhost:8000`

---

## Akses Admin

Django Admin tersedia di: `http://localhost:8000/admin/`

Login menggunakan akun superuser yang telah dibuat.

---

## Perbandingan Laravel vs Django

| Aspek | Laravel | Django |
|-------|---------|--------|
| Arsitektur | MVC | MVT |
| Templating | Blade | Django Template |
| ORM | Eloquent | Django ORM |
| Routing | routes/web.php | urls.py |
| Admin Panel | Manual/Nova | Built-in |
| Migrations | Artisan | manage.py |
| Seeder | DatabaseSeeder | Management Command |

---

## Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan eksplorasi.

---

*Dibuat dengan Django 5.0 dan GitHub Copilot*
