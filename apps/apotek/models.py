from django.db import models
from apps.rekam_medis.models import RekamMedis


class KategoriObat(models.Model):
    """Model untuk kategori obat"""
    
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Kategori Obat'
        verbose_name_plural = 'Kategori Obat'
    
    def __str__(self):
        return self.nama


class Obat(models.Model):
    """Model untuk obat-obatan"""
    
    nama = models.CharField(max_length=255)
    kategori = models.ForeignKey(KategoriObat, on_delete=models.SET_NULL, null=True)
    
    # Detail Obat
    kode_obat = models.CharField(max_length=50, unique=True)
    kandungan = models.CharField(max_length=255, blank=True)
    dosis = models.CharField(max_length=100, blank=True)
    bentuk = models.CharField(max_length=100, blank=True, help_text='Tablet, Kapsul, Sirup, dll')
    
    # Stok & Harga
    stok = models.IntegerField(default=0)
    harga = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Info Penting
    efek_samping = models.TextField(blank=True)
    kontraindikasi = models.TextField(blank=True)
    tanggal_kadaluarsa = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Obat'
        verbose_name_plural = 'Obat'
        ordering = ['nama']
    
    def __str__(self):
        return f'{self.nama} - {self.dosis}'


class Resep(models.Model):
    """Model untuk resep obat"""
    
    STATUS_CHOICES = (
        ('baru', 'Baru'),
        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),
        ('batal', 'Batal'),
    )
    
    no_resep = models.CharField(max_length=50, unique=True)
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE, related_name='resep')
    
    tanggal_resep = models.DateTimeField(auto_now_add=True)
    catatan = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='baru')
    
    total_harga = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Resep'
        verbose_name_plural = 'Resep'
        ordering = ['-tanggal_resep']
    
    def __str__(self):
        return f'{self.no_resep} - {self.rekam_medis.pasien.nama}'


class DetailResep(models.Model):
    """Model untuk detail resep (obat yang diresepkan)"""
    
    resep = models.ForeignKey(Resep, on_delete=models.CASCADE, related_name='detail_resep')
    obat = models.ForeignKey(Obat, on_delete=models.CASCADE)
    
    jumlah = models.IntegerField()
    dosis_pemberian = models.CharField(max_length=255, blank=True)
    cara_pemakaian = models.TextField(blank=True)
    lama_penggunaan = models.CharField(max_length=100, blank=True)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = 'Detail Resep'
        verbose_name_plural = 'Detail Resep'
    
    def __str__(self):
        return f'{self.resep.no_resep} - {self.obat.nama}'
