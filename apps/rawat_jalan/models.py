from django.db import models
from apps.pasien.models import Pasien
from apps.dokter.models import Dokter
from apps.rekam_medis.models import RekamMedis


class RawatJalan(models.Model):
    """Model untuk kunjungan rawat jalan pasien"""
    
    STATUS_CHOICES = (
        ('terdaftar', 'Terdaftar'),
        ('menunggu', 'Menunggu'),
        ('diproses', 'Diproses'),
        ('selesai', 'Selesai'),
    )
    
    no_kunjungan = models.CharField(max_length=50, unique=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='rawat_jalan')
    dokter = models.ForeignKey(Dokter, on_delete=models.SET_NULL, null=True, blank=True)
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.SET_NULL, null=True, blank=True)
    
    tanggal_kunjungan = models.DateTimeField(auto_now_add=True)
    tanggal_selesai = models.DateTimeField(blank=True, null=True)
    
    keluhan = models.TextField()
    catatan = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='terdaftar')
    
    total_biaya = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rawat Jalan'
        verbose_name_plural = 'Rawat Jalan'
        ordering = ['-tanggal_kunjungan']
    
    def __str__(self):
        return f'{self.no_kunjungan} - {self.pasien.nama}'


class Antrian(models.Model):
    """Model untuk sistem antrian rawat jalan"""
    
    STATUS_CHOICES = (
        ('menunggu', 'Menunggu'),
        ('dipanggil', 'Dipanggil'),
        ('dilayani', 'Dilayani'),
        ('selesai', 'Selesai'),
    )
    
    rawat_jalan = models.OneToOneField(RawatJalan, on_delete=models.CASCADE, related_name='antrian')
    
    tanggal_antrian = models.DateField(auto_now_add=True)
    nomor_antrian = models.IntegerField()
    
    waktu_tiba = models.DateTimeField(blank=True, null=True)
    waktu_dipanggil = models.DateTimeField(blank=True, null=True)
    waktu_dilayani = models.DateTimeField(blank=True, null=True)
    waktu_selesai = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='menunggu')
    
    class Meta:
        verbose_name = 'Antrian'
        verbose_name_plural = 'Antrian'
        ordering = ['tanggal_antrian', 'nomor_antrian']
    
    def __str__(self):
        return f'Antrian #{self.nomor_antrian} - {self.rawat_jalan.pasien.nama}'
