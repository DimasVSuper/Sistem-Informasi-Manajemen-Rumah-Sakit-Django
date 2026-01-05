# MVP - Sistem Informasi Manajemen Rumah Sakit (SIMRS)

## Pendahuluan

MVP (Minimum Viable Product) untuk SIMRS adalah versi minimal sistem yang memungkinkan pengelolaan dasar operasi rumah sakit. Fokus pada fitur inti yang mendukung alur pelayanan kesehatan utama: pendaftaran pasien, rekam medis, resep obat, dan pembayaran. MVP ini dirancang untuk validasi konsep, pengujian pengguna, dan iterasi cepat berdasarkan prinsip-prinsip dalam jurnal SIMRS.

## Tujuan MVP

- **Validasi Konsep**: Pastikan sistem dapat mengintegrasikan modul utama (pasien, rekam medis, apotek, keuangan).
- **Pengujian Pengguna**: Uji kemudahan penggunaan oleh admin, dokter, dan staf rumah sakit.
- **Iterasi Cepat**: Kumpulkan feedback untuk pengembangan fitur lanjutan (laboratorium, rawat inap/jalan, dll.).

## Fitur MVP

### 1. Manajemen User & Authentication
- Custom User model dengan 7 roles: admin, dokter, perawat, apoteker, kasir, pasien, lab_staff.
- Login/logout via Django admin.
- Permissions dasar berdasarkan role.

### 2. Manajemen Pasien
- CRUD pasien: nama, tanggal lahir, alamat, nomor HP, asuransi.
- Pencarian pasien berdasarkan nama atau ID.

### 3. Rekam Medis Elektronik (EMR)
- Model RekamMedis: diagnosis, tindakan, vital signs (tekanan darah, suhu, dll.).
- Link ke pasien dan dokter.
- Riwayat kunjungan dasar.

### 4. Apotek & Resep
- Model Obat: nama, stok, harga.
- Model Resep: detail resep dengan obat dan jumlah.
- Pengurangan stok otomatis saat resep dibuat.

### 5. Keuangan & Pembayaran
- Model Invoice: total biaya dari rekam medis dan resep.
- Status pembayaran: pending, paid.
- Laporan sederhana total pendapatan.

### 6. Dashboard
- Ringkasan: jumlah pasien, kunjungan hari ini, stok obat rendah.
- Grafik dasar (opsional, menggunakan Django admin charts).

## Alur Pengguna Utama

1. **Pendaftaran Pasien**: Admin/daftar pasien baru.
2. **Kunjungan**: Dokter buat rekam medis untuk pasien.
3. **Resep**: Dokter buat resep obat.
4. **Pembayaran**: Kasir buat invoice dan update status pembayaran.
5. **Dashboard**: Admin lihat ringkasan harian.

## Teknologi MVP

- **Backend**: Django 5.0 (Python 3.10).
- **Database**: MySQL 8.0.
- **Frontend**: Django Admin (tidak ada custom templates, fokus efisiensi).
- **Dependencies**: mysqlclient, python-dotenv, faker (untuk seeding data).
- **Deployment**: Local development dengan Laragon.

## Timeline Pengembangan MVP

- **Minggu 1**: Setup proyek, model dasar (User, Pasien, RekamMedis, Obat, Invoice), migrations.
- **Minggu 2**: Views dan admin interfaces, seeding data, testing CRUD.
- **Minggu 3**: Integrasi alur (rekam medis -> resep -> invoice), dashboard sederhana.
- **Minggu 4**: Testing end-to-end, bug fixes, dokumentasi.

## Kriteria Sukses MVP

- Sistem dapat menjalankan alur lengkap dari pendaftaran hingga pembayaran tanpa error.
- Response time < 2 detik untuk operasi CRUD.
- Minimal 80% fitur berfungsi sesuai spesifikasi.
- Feedback positif dari minimal 3 pengguna (admin, dokter, kasir).

## Risiko & Mitigasi

- **Risiko**: Integrasi data antar modul rumit.
  - **Mitigasi**: Gunakan foreign keys dan signals Django untuk otomasi.
- **Risiko**: Kurangnya data test.
  - **Mitigasi**: Implementasikan seeder command (`python manage.py seed_data`).

## Next Steps Setelah MVP

- Tambah modul laboratorium, rawat inap/jalan.
- Implementasi API untuk mobile app.
- Integrasi dengan sistem eksternal (asuransi, telemedicine).
- UI custom dengan Bootstrap untuk user non-admin.