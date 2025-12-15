from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.accounts.models import User


class Pasien(models.Model):
    """Model untuk data pasien"""
    
    GENDER_CHOICES = (
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pasien_profile')
    no_pasien = models.CharField(max_length=50, unique=True)
    
    # Data Pribadi
    nama = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=1, choices=GENDER_CHOICES)
    tanggal_lahir = models.DateField()
    no_identitas = models.CharField(max_length=20, unique=True)
    
    # Kontak
    alamat = models.TextField()
    kelurahan = models.CharField(max_length=100, blank=True)
    kecamatan = models.CharField(max_length=100, blank=True)
    kabupaten = models.CharField(max_length=100, blank=True)
    provinsi = models.CharField(max_length=100, blank=True)
    kode_pos = models.CharField(max_length=10, blank=True)
    no_telepon = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Asuransi
    jenis_asuransi = models.CharField(max_length=50, blank=True)
    no_asuransi = models.CharField(max_length=50, blank=True)
    
    # Riwayat Medis
    alergi = models.TextField(blank=True)
    riwayat_penyakit = models.TextField(blank=True)
    golongan_darah = models.CharField(max_length=5, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Pasien'
        verbose_name_plural = 'Pasien'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.no_pasien} - {self.nama}'
    
    @property
    def umur(self):
        from datetime import date
        today = date.today()
        return today.year - self.tanggal_lahir.year - ((today.month, today.day) < (self.tanggal_lahir.month, self.tanggal_lahir.day))
