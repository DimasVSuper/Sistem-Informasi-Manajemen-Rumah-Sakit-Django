from django.contrib import admin
from .models import RekamMedis, Diagnosis, TindakanMedis


@admin.register(RekamMedis)
class RekamMedisAdmin(admin.ModelAdmin):
    list_display = ('no_rekam_medis', 'pasien', 'dokter', 'tanggal_pemeriksaan', 'status')
    list_filter = ('status', 'tanggal_pemeriksaan', 'dokter')
    search_fields = ('no_rekam_medis', 'pasien__nama', 'diagnosa', 'keluhan_utama')
    readonly_fields = ('created_at', 'updated_at', 'no_rekam_medis')
    date_hierarchy = 'tanggal_pemeriksaan'
    ordering = ('-tanggal_pemeriksaan',)
    
    fieldsets = (
        ('Identitas', {'fields': ('no_rekam_medis', 'pasien', 'dokter')}),
        ('Pemeriksaan', {'fields': ('tanggal_pemeriksaan', 'keluhan_utama', 'riwayat_keluhan', 'diagnosa')}),
        ('Vital Signs', {'fields': ('tekanan_darah', 'denyut_nadi', 'suhu_badan', 'respirasi', 'berat_badan', 'tinggi_badan')}),
        ('Pemeriksaan Fisik', {'fields': ('pemeriksaan_fisik',)}),
        ('Status', {'fields': ('status',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('nama_diagnosis', 'rekam_medis')
    search_fields = ('nama_diagnosis', 'kode_icd10')


@admin.register(TindakanMedis)
class TindakanMedisAdmin(admin.ModelAdmin):
    list_display = ('nama_tindakan', 'rekam_medis', 'tarif')
    list_filter = ('created_at',)
    search_fields = ('nama_tindakan',)
