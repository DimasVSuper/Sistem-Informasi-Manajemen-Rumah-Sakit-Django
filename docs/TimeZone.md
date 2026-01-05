# Panduan Timezone di SIMRS Django + MySQL

## Pendahuluan

Dokumen ini menjelaskan masalah timezone yang sering terjadi saat menggunakan Django dengan MySQL, khususnya di proyek SIMRS. Django menggunakan timezone-aware datetime, sedangkan MySQL memerlukan konfigurasi khusus untuk mendukung timezone.

## Konfigurasi Django

Di `config/settings.py`:

```python
TIME_ZONE = 'Asia/Jakarta'  # Zona waktu Indonesia
USE_I18N = True
USE_TZ = True  # Atau False jika ada masalah
```

- `TIME_ZONE`: Zona waktu aplikasi.
- `USE_TZ`: Jika `True`, Django gunakan timezone-aware datetime. Jika `False`, naive datetime.

## Masalah Umum

### Error: "Database returned an invalid datetime value"

**Gejala:**
- Error saat akses admin atau query database.
- Pesan: "Are time zone definitions for your database installed?"

**Penyebab:**
- MySQL tidak memiliki timezone tables terinstall.
- Django mencoba convert datetime dengan timezone, tapi MySQL tidak mendukung.

**Cek Timezone Tables:**
```bash
mysql -u root -p -e "SELECT COUNT(*) FROM mysql.time_zone_name;"
```
Jika hasil 0, tables belum terinstall.

## Solusi

### Solusi Sementara: Disable USE_TZ

Set `USE_TZ = False` di settings.py. Ini membuat Django gunakan naive datetime, menghindari error.

**Kelemahan:** Tidak akurat untuk multi-timezone, tapi cukup untuk development.

### Solusi Permanen: Install Timezone Tables di MySQL

#### Untuk Linux/Mac:
```bash
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root -p mysql
```

#### Untuk Windows:
1. Download `timezone_2023a_posix_sql.zip` dari https://dev.mysql.com/downloads/timezones.html
2. Extract dan import:
```bash
mysql -u root -p mysql < timezone_posix.sql
```

**Verifikasi:**
```bash
mysql -u root -p -e "SELECT COUNT(*) FROM mysql.time_zone_name;"
```
Harus > 0.

### Alternatif: Gunakan UTC

- Set `TIME_ZONE = 'UTC'` di settings.py.
- Pastikan aplikasi handle convert timezone jika perlu.

## Testing

Setelah fix, jalankan:
```bash
python manage.py runserver
```
Akses admin dan cek tidak ada error datetime.

## Tips

- Selalu backup database sebelum ubah timezone.
- Untuk production, gunakan `USE_TZ = True` dengan timezone tables terinstall.
- Jika menggunakan Docker, pastikan MySQL image include timezone.

## Referensi

- Django Docs: Timezones
- MySQL Docs: Timezone Support