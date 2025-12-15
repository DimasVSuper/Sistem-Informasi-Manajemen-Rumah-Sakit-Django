from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from faker import Faker
from apps.accounts.models import User
from apps.pasien.models import Pasien
from apps.dokter.models import Dokter, Spesialisasi
from apps.apotek.models import KategoriObat, Obat, Resep, DetailResep
from apps.laboratorium.models import JenisPemeriksaan, ParameterLab, PermintaanLab
from apps.rekam_medis.models import RekamMedis, Diagnosis
from apps.rawat_inap.models import Ruangan, RawatInap
from apps.rawat_jalan.models import RawatJalan, Antrian
from apps.keuangan.models import Invoice, DetailInvoice, Pembayaran
import random
from decimal import Decimal


class Command(BaseCommand):
    help = 'Seed database dengan sample data realistis menggunakan Faker'

    def handle(self, *args, **options):
        fake = Faker('id_ID')
        self.stdout.write(self.style.WARNING('🚀 Starting database seeding with Faker...'))
        
        # Check if data already exists
        if User.objects.filter(role='pasien').exists():
            self.stdout.write(self.style.ERROR('❌ Database sudah terisi! Jalankan: python manage.py flush'))
            return
        
        # 1. Create Users (staff roles)
        self.stdout.write('👥 Creating users...')
        users = []
        roles = ['perawat', 'apoteker', 'kasir', 'lab_staff']
        
        for i, role in enumerate(roles):
            for j in range(3):
                user = User.objects.create_user(
                    username=f'{role}_{i+1}_{j+1}',
                    email=fake.unique.email(),
                    password='password123',
                    nama_lengkap=fake.name(),
                    role=role,
                    is_staff=True
                )
                users.append(user)
        
        # 2. Create Patients (50)
        self.stdout.write('🏥 Creating 50 patients...')
        patients = []
        jenis_kelamin = ['L', 'P']
        asuransi = ['BPJS', 'Asuransi Pribadi', 'Umum', 'Mandiri']
        golongan = ['A', 'B', 'AB', 'O']
        
        for i in range(50):
            pasien_user = User.objects.create_user(
                username=f'pasien_{i+1}',
                email=fake.unique.email(),
                password='password123',
                nama_lengkap=fake.name(),
                role='pasien'
            )
            pasien = Pasien.objects.create(
                user=pasien_user,
                no_pasien=f'PS{i+1:05d}',
                nama=pasien_user.nama_lengkap,
                no_identitas=fake.unique.bothify(text='################'),
                jenis_kelamin=random.choice(jenis_kelamin),
                tanggal_lahir=fake.date_of_birth(minimum_age=5, maximum_age=80),
                alamat=fake.address(),
                kelurahan=fake.word(),
                kecamatan=fake.word(),
                kabupaten=fake.city(),
                provinsi=fake.state(),
                kode_pos=fake.postcode(),
                no_telepon=fake.phone_number(),
                email=pasien_user.email,
                jenis_asuransi=random.choice(asuransi),
                no_asuransi=fake.bothify(text='ASU##########'),
                alergi=fake.word() if random.random() > 0.7 else 'Tidak ada',
                riwayat_penyakit=fake.sentence(nb_words=5) if random.random() > 0.6 else 'Tidak ada',
                golongan_darah=random.choice(golongan)
            )
            patients.append(pasien)
        
        # 3. Create Specializations & Doctors
        self.stdout.write('👨‍⚕️ Creating doctors with specializations...')
        spesialisasi_list = [
            'Umum', 'Penyakit Dalam', 'Bedah', 'Pediatri', 'Kardiologi',
            'Neurologi', 'Oftalmologi', 'THT', 'Dermatologi', 'Orthopedi'
        ]
        
        spesialisasis = []
        for spec_name in spesialisasi_list:
            spec = Spesialisasi.objects.create(nama=spec_name)
            spesialisasis.append(spec)
        
        doctors = []
        for i, spec in enumerate(spesialisasis):
            for j in range(2):
                dokter_user = User.objects.create_user(
                    username=f'dokter_{spec.nama.lower().replace(" ", "_")}_{j+1}',
                    email=fake.unique.email(),
                    password='password123',
                    nama_lengkap=fake.name(),
                    role='dokter',
                    is_staff=True
                )
                dokter = Dokter.objects.create(
                    user=dokter_user,
                    nama=dokter_user.nama_lengkap,
                    no_dokter=f'DK{1000+i*2+j:05d}',
                    spesialisasi=spec,
                    no_lisensi=fake.unique.bothify(text='LIS##########'),
                    no_str=fake.bothify(text='STR##########'),
                    no_telepon=fake.phone_number(),
                    alamat=fake.address(),
                    jam_kerja_mulai='08:00',
                    jam_kerja_selesai='17:00',
                    hari_kerja='Senin-Jumat',
                    is_available=random.choice([True, True, False])
                )
                doctors.append(dokter)
        
        # 4. Create Medicine Categories & Medicines
        self.stdout.write('💊 Creating medicines...')
        kategori_list = [
            'Antibiotik', 'Analgesik', 'Antipiretik', 'Vitamin', 'Antihipertensi',
            'Antidiabetik', 'Antasida', 'Antihistamin', 'Antimual', 'Laxative'
        ]
        
        kategoris = []
        for kat_name in kategori_list:
            kat = KategoriObat.objects.create(nama=kat_name)
            kategoris.append(kat)
        
        obat_names = [
            'Amoksisilin', 'Paracetamol', 'Ibuprofen', 'Vitamin C', 'Amlodipine',
            'Metformin', 'Omeprazole', 'Cetirizine', 'Loratadine', 'Domperidone',
            'Phenolphthalein', 'Aspirin', 'Naproxen', 'Diclofenac', 'Piroxicam',
            'Gabapentin', 'Pregabalin', 'Sertraline', 'Fluoxetine', 'Amitriptyline',
            'Levothyroxine', 'Propranolol', 'Metoprolol', 'Lisinopril', 'Enalapril',
        ]
        
        obats = []
        for i, nama in enumerate(obat_names):
            kat = random.choice(kategoris)
            obat = Obat.objects.create(
                nama=nama,
                kategori=kat,
                kode_obat=f'OB{1000+i:05d}',
                kandungan=f'{nama} {random.choice([250, 500, 750, 1000])}mg',
                dosis=f'{random.randint(1, 3)}x{random.randint(1, 3)} tablet',
                bentuk=random.choice(['Tablet', 'Kapsul', 'Sirup', 'Injeksi']),
                stok=random.randint(20, 500),
                harga=random.randint(5000, 150000),
                efek_samping=fake.sentence(nb_words=6),
                kontraindikasi=fake.sentence(nb_words=4) if random.random() > 0.5 else 'Tidak ada',
                tanggal_kadaluarsa=timezone.now().date() + timedelta(days=random.randint(60, 365))
            )
            obats.append(obat)
        
        # 5. Create Lab Examination Types
        self.stdout.write('🔬 Creating lab examination types...')
        jenis_pemeriksaan_list = [
            ('Darah Rutin', 'DR001', 150000, 1),
            ('Urinalisis', 'UR001', 75000, 1),
            ('Kimia Darah', 'KD001', 250000, 2),
            ('Kolesterol', 'KL001', 100000, 1),
            ('Fungsi Hati', 'FH001', 200000, 2),
            ('Fungsi Ginjal', 'FG001', 180000, 2),
            ('Tes Kehamilan', 'TK001', 50000, 1),
            ('Kultur Darah', 'CB001', 300000, 3),
        ]
        
        jenis_periksa = []
        for nama, kode, tarif, waktu in jenis_pemeriksaan_list:
            jp = JenisPemeriksaan.objects.create(
                nama=nama,
                kode=kode,
                tarif=tarif,
                waktu_hasil=waktu
            )
            jenis_periksa.append(jp)
        
        # 6. Create Rekam Medis (tanggal_pemeriksaan is auto_now_add)
        self.stdout.write('📋 Creating medical records...')
        rekam_medis_list = []
        for i in range(30):
            rm = RekamMedis.objects.create(
                no_rekam_medis=f'RM{i+1:05d}',
                pasien=random.choice(patients),
                dokter=random.choice(doctors),
                keluhan_utama=fake.sentence(nb_words=5),
                riwayat_keluhan=fake.sentence(nb_words=10),
                diagnosa=fake.sentence(nb_words=4),
                tekanan_darah=f'{random.randint(100, 160)}/{random.randint(60, 100)}',
                denyut_nadi=random.randint(60, 100),
                suhu_badan=round(random.uniform(36.0, 39.0), 1),
                respirasi=random.randint(16, 24),
                berat_badan=round(random.uniform(40.0, 100.0), 1),
                tinggi_badan=round(random.uniform(150.0, 190.0), 1),
                pemeriksaan_fisik=fake.sentence(nb_words=10),
                status=random.choice(['baru', 'proses', 'selesai'])
            )
            rekam_medis_list.append(rm)
        
        # 7. Create Rawat Inap (tanggal_masuk is auto_now_add)
        self.stdout.write('🏨 Creating inpatient records...')
        ruangan_list = []
        for tipe in ['VIP', 'Kelas 1', 'Kelas 2', 'Kelas 3']:
            for i in range(3):
                ruang = Ruangan.objects.create(
                    nama=f'Ruangan {tipe} {i+1}',
                    tipe=tipe,
                    jumlah_kasur=4,
                    kasur_tersedia=random.randint(0, 4),
                    tarif_per_hari=Decimal(random.choice([100000, 200000, 300000, 500000])),
                    fasilitas='AC, TV, Kamar Mandi Dalam',
                    is_active=True
                )
                ruangan_list.append(ruang)
        
        rawat_inap_list = []
        for i in range(20):
            ri = RawatInap.objects.create(
                no_rawat_inap=f'RI{i+1:05d}',
                pasien=random.choice(patients),
                dokter=random.choice(doctors),
                rekam_medis=random.choice(rekam_medis_list),
                ruangan=random.choice(ruangan_list),
                no_kasur=f'K{random.randint(1, 10)}',
                tanggal_keluar=timezone.now() + timedelta(days=random.randint(1, 14)) if random.random() > 0.3 else None,
                diagnosa_awal=fake.sentence(nb_words=4),
                catatan_perawatan=fake.paragraph(nb_sentences=5),
                status=random.choice(['aktif', 'selesai', 'transfer']),
                total_biaya=Decimal(random.randint(500000, 10000000))
            )
            rawat_inap_list.append(ri)
        
        # 8. Create Rawat Jalan (tanggal_kunjungan is auto_now_add)
        self.stdout.write('🚶 Creating outpatient records...')
        rawat_jalan_list = []
        for i in range(30):
            rj = RawatJalan.objects.create(
                no_kunjungan=f'RJ{i+1:05d}',
                pasien=random.choice(patients),
                dokter=random.choice(doctors),
                rekam_medis=random.choice(rekam_medis_list),
                keluhan=fake.sentence(nb_words=5),
                catatan=fake.text(max_nb_chars=200) if random.random() > 0.5 else '',
                status=random.choice(['terdaftar', 'menunggu', 'diproses', 'selesai']),
                total_biaya=Decimal(random.randint(50000, 500000))
            )
            rawat_jalan_list.append(rj)
            
            # Create Antrian (tanggal_antrian is auto_now_add, nomor_antrian is IntegerField)
            Antrian.objects.create(
                rawat_jalan=rj,
                nomor_antrian=i+1,
                waktu_tiba=timezone.now() if random.random() > 0.5 else None,
                status=random.choice(['menunggu', 'dipanggil', 'dilayani', 'selesai'])
            )
        
        # 9. Create Resep (tanggal_resep is auto_now_add)
        self.stdout.write('💊 Creating prescriptions...')
        for i in range(25):
            resep = Resep.objects.create(
                no_resep=f'RES{i+1:05d}',
                rekam_medis=random.choice(rekam_medis_list),
                catatan=fake.sentence(nb_words=5) if random.random() > 0.5 else '',
                status=random.choice(['baru', 'diproses', 'selesai', 'batal']),
                total_harga=Decimal(random.randint(50000, 500000))
            )
            
            # Add detail resep (uses dosis_pemberian, cara_pemakaian, lama_penggunaan)
            for j in range(random.randint(1, 3)):
                obat = random.choice(obats)
                jumlah = random.randint(1, 10)
                DetailResep.objects.create(
                    resep=resep,
                    obat=obat,
                    jumlah=jumlah,
                    dosis_pemberian=f'{random.randint(1, 3)}x{random.randint(1, 3)} sehari',
                    cara_pemakaian=random.choice(['Sebelum makan', 'Sesudah makan', 'Saat makan']),
                    lama_penggunaan=f'{random.randint(3, 14)} hari',
                    subtotal=Decimal(jumlah) * obat.harga
                )
        
        # 10. Create Invoices (tanggal_invoice is auto_now_add DateField)
        self.stdout.write('💰 Creating invoices...')
        for i in range(40):
            pasien = random.choice(patients)
            subtotal_val = Decimal(random.randint(100000, 5000000))
            diskon_val = Decimal(random.randint(0, 50000))
            pajak_val = subtotal_val * Decimal('0.1')
            total_val = subtotal_val - diskon_val + pajak_val
            
            invoice = Invoice.objects.create(
                no_invoice=f'INV{i+1:05d}',
                pasien=pasien,
                tanggal_jatuh_tempo=timezone.now().date() + timedelta(days=random.randint(7, 30)),
                rekam_medis=random.choice(rekam_medis_list) if random.random() > 0.5 else None,
                rawat_inap=random.choice(rawat_inap_list) if random.random() > 0.7 else None,
                rawat_jalan=random.choice(rawat_jalan_list) if random.random() > 0.7 else None,
                subtotal=subtotal_val,
                diskon=diskon_val,
                pajak=pajak_val,
                total=total_val,
                status=random.choice(['draft', 'dikirim', 'sebagian', 'lunas', 'batal']),
                catatan=fake.sentence(nb_words=5) if random.random() > 0.7 else ''
            )
            
            # Add detail invoice (needs harga_satuan)
            for j in range(random.randint(1, 3)):
                harga_satuan = Decimal(random.randint(50000, 500000))
                jumlah = random.randint(1, 5)
                DetailInvoice.objects.create(
                    invoice=invoice,
                    tipe_layanan=random.choice(['dokter', 'obat', 'lab', 'tindakan', 'rawat_inap', 'lainnya']),
                    deskripsi=fake.sentence(nb_words=4),
                    jumlah=jumlah,
                    harga_satuan=harga_satuan,
                    subtotal=harga_satuan * jumlah
                )
            
            # Add pembayaran (tanggal_pembayaran is auto_now_add)
            if random.random() > 0.3:
                Pembayaran.objects.create(
                    no_pembayaran=f'PAY{i+1:05d}',
                    invoice=invoice,
                    metode=random.choice(['tunai', 'debit', 'kredit', 'transfer', 'cek']),
                    jumlah=Decimal(random.randint(int(total_val * Decimal('0.5')), int(total_val))),
                    keterangan=fake.sentence(nb_words=4) if random.random() > 0.7 else '',
                    status=random.choice(['pending', 'sukses', 'gagal'])
                )
        
        self.stdout.write(self.style.SUCCESS('✅ Database seeding completed!'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 50+ patients'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 20+ doctors'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 25+ medicines'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 30+ medical records'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 20+ inpatient records'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 30+ outpatient records'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 25+ prescriptions'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created 40+ invoices'))
