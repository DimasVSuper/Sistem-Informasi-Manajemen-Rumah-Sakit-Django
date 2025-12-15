from django.db import models
from apps.pasien.models import Pasien
from apps.dokter.models import Dokter
from apps.rekam_medis.models import RekamMedis


class Ruangan(models.Model):
    """Model untuk ruangan rawat inap"""
    
    nama = models.CharField(max_length=100)
    tipe = models.CharField(max_length=50, blank=True, help_text='VIP, Kelas 1, Kelas 2, dll')
    
    # Kapasitas
    jumlah_kasur = models.IntegerField(default=1)
    kasur_tersedia = models.IntegerField(default=1)
    
    # Harga
    tarif_per_hari = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Fasilitas
    fasilitas = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Ruangan'
        verbose_name_plural = 'Ruangan'
    
    def __str__(self):
        return f'{self.nama} ({self.kasur_tersedia}/{self.jumlah_kasur})'


class RawatInap(models.Model):
    """Model untuk data pasien rawat inap"""
    
    STATUS_CHOICES = (
        ('aktif', 'Aktif'),
        ('selesai', 'Selesai'),
        ('transfer', 'Transfer'),
    )
    
    no_rawat_inap = models.CharField(max_length=50, unique=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='rawat_inap')
    dokter = models.ForeignKey(Dokter, on_delete=models.SET_NULL, null=True, blank=True)
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.SET_NULL, null=True, blank=True)
    
    ruangan = models.ForeignKey(Ruangan, on_delete=models.SET_NULL, null=True)
    no_kasur = models.CharField(max_length=20)
    
    tanggal_masuk = models.DateTimeField(auto_now_add=True)
    tanggal_keluar = models.DateTimeField(blank=True, null=True)
    
    diagnosa_awal = models.TextField()
    catatan_perawatan = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aktif')
    
    total_biaya = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rawat Inap'
        verbose_name_plural = 'Rawat Inap'
        ordering = ['-tanggal_masuk']
    
    def __str__(self):
        return f'{self.no_rawat_inap} - {self.pasien.nama}'
    
    @property
    def lama_menginap(self):
        from datetime import datetime
        tanggal_keluar = self.tanggal_keluar if self.tanggal_keluar else datetime.now()
        return (tanggal_keluar - self.tanggal_masuk).days
