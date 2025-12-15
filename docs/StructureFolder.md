Sistem-Informasi-Manajemen-Rumah-Sakit-Djanggo/
│
├── 📄 .env                          # Konfigurasi environment
├── 📄 .gitignore                    # Ignore file untuk git
├── 📄 manage.py                     # Django CLI entry point
├── 📄 requirements.txt              # Python dependencies
│
├── 📁 config/                       # Django configuration
│   ├── settings.py                  # Main Django settings
│   ├── urls.py                      # Root URL router (admin only)
│   ├── asgi.py                      # ASGI config
│   ├── wsgi.py                      # WSGI config
│   └── __init__.py
│
├── 📁 apps/                         # Django applications (10 modules)
│   ├── accounts/                    # User & Authentication Management
│   │   ├── models.py                # Custom User model with 7 roles
│   │   ├── admin.py                 # Admin interface
│   │   ├── urls.py                  # App URLs
│   │   ├── views.py                 # Auth views (for future use)
│   │   ├── apps.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── seed_data.py     # Database seeder command
│   │   └── migrations/
│   │
│   ├── pasien/                      # Patient Registration Module
│   │   ├── models.py                # Pasien model
│   │   ├── admin.py                 # Enhanced admin interface
│   │   ├── urls.py                  # CRUD routes
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── dokter/                      # Doctor Module
│   │   ├── models.py                # Dokter & Spesialisasi models
│   │   ├── admin.py                 # Admin with bulk actions
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── rekam_medis/                 # Electronic Medical Records
│   │   ├── models.py                # RekamMedis, Diagnosis, Tindakan
│   │   ├── admin.py                 # Admin with date hierarchy
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── apotek/                      # Pharmacy & Medicines
│   │   ├── models.py                # Obat, Resep, DetailResep
│   │   ├── admin.py                 # Admin with inline editing & status
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── laboratorium/                # Laboratory Module
│   │   ├── models.py                # JenisPemeriksaan, PermintaanLab
│   │   ├── admin.py                 # Admin with actions
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── rawat_inap/                  # Inpatient Service
│   │   ├── models.py                # Ruangan, RawatInap
│   │   ├── admin.py                 # Admin with status actions
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── rawat_jalan/                 # Outpatient Service
│   │   ├── models.py                # RawatJalan, Antrian
│   │   ├── admin.py                 # Admin with date hierarchy
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── keuangan/                    # Billing & Finance Module
│   │   ├── models.py                # Invoice, DetailInvoice, Pembayaran
│   │   ├── admin.py                 # Admin with inline & status badges
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   ├── dashboard/                   # Dashboard & Reports
│   │   ├── models.py
│   │   ├── admin.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── apps.py
│   │   └── migrations/
│   │
│   └── __init__.py
│
├── 📁 static/                       # Static files (CSS, JS, images)
│   ├── css/                         # Custom CSS (empty - using admin defaults)
│   ├── js/                          # Custom JavaScript (empty)
│   └── img/                         # Images (empty)
│
├── 📁 media/                        # User uploaded files (documents, patient photos)
│
├── 📁 templates/                    # HTML Templates
│   └── landing.html                 # Professional landing page (Bootstrap 5)
│
├── 📁 docs/                         # Documentation
│   ├── Jurnal.md                    # Hospital Management System Journal
│   └── StructureFolder.md           # This file
│
└── 📁 venv/                         # Python Virtual Environment

---

## Key Features

✅ **Admin-Only Interface** - All CRUD operations via Django admin
✅ **Landing Page** - Professional Bootstrap 5 landing page with carousel
✅ **10 Django Apps** - Complete hospital management modules
✅ **Custom User Model** - 7 roles: admin, dokter, perawat, apoteker, kasir, pasien, lab_staff
✅ **Database Seeder** - `python manage.py seed_data` for test data
✅ **Enhanced Admin UI** - Custom actions, inline editing, status badges
✅ **MySQL Database** - Docker-based on port 32768
✅ **No Custom Templates** - Minimal frontend, maximum efficiency