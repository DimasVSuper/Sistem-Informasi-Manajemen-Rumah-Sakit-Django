from django.db import models
from apps.pasien.models import Pasien
from apps.rekam_medis.models import RekamMedis


class JenisPemeriksaan(models.Model):
    """Model untuk jenis pemeriksaan laboratorium"""
    
    nama = models.CharField(max_length=255)
    kode = models.CharField(max_length=50, unique=True)
    deskripsi = models.TextField(blank=True)
    
    # Harga
    tarif = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Waktu Pengerjaan
    waktu_hasil = models.IntegerField(default=1, help_text='Dalam hari')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Jenis Pemeriksaan'
        verbose_name_plural = 'Jenis Pemeriksaan'
    
    def __str__(self):
        return self.nama


class ParameterLab(models.Model):
    """Model untuk parameter/hasil pemeriksaan lab"""
    
    jenis_pemeriksaan = models.ForeignKey(JenisPemeriksaan, on_delete=models.CASCADE, related_name='parameters')
    
    nama_parameter = models.CharField(max_length=255)
    satuan = models.CharField(max_length=50, blank=True)
    nilai_normal_min = models.FloatField(blank=True, null=True)
    nilai_normal_max = models.FloatField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Parameter Lab'
        verbose_name_plural = 'Parameter Lab'
    
    def __str__(self):
        return f'{self.jenis_pemeriksaan.nama} - {self.nama_parameter}'


class PermintaanLab(models.Model):
    """Model untuk permintaan pemeriksaan lab"""
    
    STATUS_CHOICES = (
        ('baru', 'Baru'),
        ('proses', 'Proses'),
        ('selesai', 'Selesai'),
    )
    
    no_permintaan = models.CharField(max_length=50, unique=True)
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE, related_name='permintaan_lab')
    jenis_pemeriksaan = models.ManyToManyField(JenisPemeriksaan, related_name='permintaan')
    
    tanggal_permintaan = models.DateTimeField(auto_now_add=True)
    tanggal_diproses = models.DateTimeField(blank=True, null=True)
    tanggal_selesai = models.DateTimeField(blank=True, null=True)
    
    catatan_dokter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='baru')
    
    total_harga = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Permintaan Lab'
        verbose_name_plural = 'Permintaan Lab'
        ordering = ['-tanggal_permintaan']
    
    def __str__(self):
        return f'{self.no_permintaan} - {self.rekam_medis.pasien.nama}'


class HasilLab(models.Model):
    """Model untuk hasil pemeriksaan lab"""
    
    permintaan = models.OneToOneField(PermintaanLab, on_delete=models.CASCADE, related_name='hasil')
    
    tanggal_hasil = models.DateTimeField(auto_now_add=True)
    dokter_pemeriksa = models.CharField(max_length=255, blank=True)
    
    # Hasil dan Interpretasi
    hasil_pemeriksaan = models.TextField()
    interpretasi = models.TextField(blank=True)
    catatan = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Hasil Lab'
        verbose_name_plural = 'Hasil Lab'
        ordering = ['-tanggal_hasil']
    
    def __str__(self):
        return f'Hasil - {self.permintaan.no_permintaan}'


class DetailHasil(models.Model):
    """Model untuk detail hasil per parameter"""
    
    hasil = models.ForeignKey(HasilLab, on_delete=models.CASCADE, related_name='detail_hasil')
    parameter = models.ForeignKey(ParameterLab, on_delete=models.CASCADE)
    
    nilai = models.FloatField()
    normal = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Detail Hasil'
        verbose_name_plural = 'Detail Hasil'
    
    def __str__(self):
        return f'{self.parameter.nama_parameter} - {self.nilai}'
