from django.db import models
from apps.accounts.models import User


class Spesialisasi(models.Model):
    """Model untuk spesialisasi dokter"""
    
    nama = models.CharField(max_length=100, unique=True)
    deskripsi = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Spesialisasi'
        verbose_name_plural = 'Spesialisasi'
    
    def __str__(self):
        return self.nama


class Dokter(models.Model):
    """Model untuk data dokter"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dokter_profile')
    no_dokter = models.CharField(max_length=50, unique=True)
    
    nama = models.CharField(max_length=255)
    spesialisasi = models.ForeignKey(Spesialisasi, on_delete=models.SET_NULL, null=True)
    
    # Lisensi
    no_lisensi = models.CharField(max_length=50, unique=True)
    no_str = models.CharField(max_length=50, blank=True, help_text='Surat Tanda Registrasi')
    
    # Kontak
    no_telepon = models.CharField(max_length=20)
    alamat = models.TextField(blank=True)
    
    # Jadwal
    jam_kerja_mulai = models.TimeField(blank=True, null=True)
    jam_kerja_selesai = models.TimeField(blank=True, null=True)
    hari_kerja = models.CharField(max_length=100, blank=True, help_text='Contoh: Senin-Jumat')
    
    # Status
    is_available = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dokter'
        verbose_name_plural = 'Dokter'
        ordering = ['nama']
    
    def __str__(self):
        return f'{self.nama} - {self.spesialisasi.nama if self.spesialisasi else "Umum"}'
