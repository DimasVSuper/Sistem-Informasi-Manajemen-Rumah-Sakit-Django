from django.db import models
from apps.pasien.models import Pasien
from apps.rekam_medis.models import RekamMedis
from apps.rawat_inap.models import RawatInap
from apps.rawat_jalan.models import RawatJalan


class Invoice(models.Model):
    """Model untuk invoice/tagihan pasien"""
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('dikirim', 'Dikirim'),
        ('sebagian', 'Sebagian Bayar'),
        ('lunas', 'Lunas'),
        ('batal', 'Batal'),
    )
    
    no_invoice = models.CharField(max_length=50, unique=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='invoices')
    
    tanggal_invoice = models.DateField(auto_now_add=True)
    tanggal_jatuh_tempo = models.DateField(blank=True, null=True)
    
    # Referensi
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.SET_NULL, null=True, blank=True)
    rawat_inap = models.ForeignKey(RawatInap, on_delete=models.SET_NULL, null=True, blank=True)
    rawat_jalan = models.ForeignKey(RawatJalan, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Total
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    diskon = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pajak = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    catatan = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoice'
        ordering = ['-tanggal_invoice']
    
    def __str__(self):
        return f'{self.no_invoice} - {self.pasien.nama}'


class DetailInvoice(models.Model):
    """Model untuk detail item invoice"""
    
    TIPE_LAYANAN = (
        ('dokter', 'Konsultasi Dokter'),
        ('obat', 'Obat'),
        ('lab', 'Laboratorium'),
        ('tindakan', 'Tindakan'),
        ('rawat_inap', 'Rawat Inap'),
        ('lainnya', 'Lainnya'),
    )
    
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='detail_invoice')
    
    tipe_layanan = models.CharField(max_length=20, choices=TIPE_LAYANAN)
    deskripsi = models.CharField(max_length=255)
    
    jumlah = models.IntegerField(default=1)
    harga_satuan = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detail Invoice'
        verbose_name_plural = 'Detail Invoice'
    
    def __str__(self):
        return f'{self.invoice.no_invoice} - {self.deskripsi}'


class Pembayaran(models.Model):
    """Model untuk pembayaran invoice"""
    
    METODE_PEMBAYARAN = (
        ('tunai', 'Tunai'),
        ('debit', 'Debit'),
        ('kredit', 'Kredit'),
        ('transfer', 'Transfer'),
        ('cek', 'Cek'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('sukses', 'Sukses'),
        ('gagal', 'Gagal'),
    )
    
    no_pembayaran = models.CharField(max_length=50, unique=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='pembayaran')
    
    tanggal_pembayaran = models.DateTimeField(auto_now_add=True)
    
    metode = models.CharField(max_length=20, choices=METODE_PEMBAYARAN)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    
    keterangan = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Bukti pembayaran
    bukti_pembayaran = models.FileField(upload_to='bukti_pembayaran/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pembayaran'
        verbose_name_plural = 'Pembayaran'
        ordering = ['-tanggal_pembayaran']
    
    def __str__(self):
        return f'{self.no_pembayaran} - {self.invoice.pasien.nama}'


class LaporanKeuangan(models.Model):
    """Model untuk laporan keuangan"""
    
    bulan = models.IntegerField()
    tahun = models.IntegerField()
    
    total_pendapatan = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_pembayaran = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_belum_terbayar = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Laporan Keuangan'
        verbose_name_plural = 'Laporan Keuangan'
    
    def __str__(self):
        return f'Laporan {self.bulan}/{self.tahun}'
