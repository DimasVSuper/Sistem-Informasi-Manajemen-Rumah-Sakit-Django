from django.db import models
from apps.pasien.models import Pasien
from apps.dokter.models import Dokter


class RekamMedis(models.Model):
    """Model untuk rekam medis pasien"""
    
    STATUS_CHOICES = (
        ('baru', 'Baru'),
        ('proses', 'Proses'),
        ('selesai', 'Selesai'),
    )
    
    no_rekam_medis = models.CharField(max_length=50, unique=True)
    pasien = models.ForeignKey(Pasien, on_delete=models.CASCADE, related_name='rekam_medis')
    dokter = models.ForeignKey(Dokter, on_delete=models.SET_NULL, null=True, blank=True)
    
    tanggal_pemeriksaan = models.DateTimeField(auto_now_add=True)
    
    # Pemeriksaan
    keluhan_utama = models.TextField()
    riwayat_keluhan = models.TextField(blank=True)
    diagnosa = models.TextField()
    
    # Vital Signs
    tekanan_darah = models.CharField(max_length=20, blank=True)
    denyut_nadi = models.IntegerField(blank=True, null=True)
    suhu_badan = models.FloatField(blank=True, null=True)
    respirasi = models.IntegerField(blank=True, null=True)
    berat_badan = models.FloatField(blank=True, null=True)
    tinggi_badan = models.FloatField(blank=True, null=True)
    
    # Hasil Pemeriksaan Fisik
    pemeriksaan_fisik = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='baru')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rekam Medis'
        verbose_name_plural = 'Rekam Medis'
        ordering = ['-tanggal_pemeriksaan']
    
    def __str__(self):
        return f'{self.no_rekam_medis} - {self.pasien.nama}'


class Diagnosis(models.Model):
    """Model untuk diagnosis pasien"""
    
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE, related_name='diagnoses')
    
    kode_icd10 = models.CharField(max_length=20, blank=True)
    nama_diagnosis = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Diagnosis'
        verbose_name_plural = 'Diagnoses'
    
    def __str__(self):
        return self.nama_diagnosis


class TindakanMedis(models.Model):
    """Model untuk tindakan medis"""
    
    rekam_medis = models.ForeignKey(RekamMedis, on_delete=models.CASCADE, related_name='tindakan_medis')
    
    nama_tindakan = models.CharField(max_length=255)
    deskripsi = models.TextField(blank=True)
    tarif = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Tindakan Medis'
        verbose_name_plural = 'Tindakan Medis'
    
    def __str__(self):
        return self.nama_tindakan
