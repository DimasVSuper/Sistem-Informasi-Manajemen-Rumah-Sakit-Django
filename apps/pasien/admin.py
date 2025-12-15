from django.contrib import admin
from .models import Pasien


@admin.register(Pasien)
class PasienAdmin(admin.ModelAdmin):
    list_display = ('no_pasien', 'nama', 'jenis_kelamin', 'umur', 'no_telepon', 'jenis_asuransi', 'created_at')
    list_filter = ('jenis_kelamin', 'created_at', 'jenis_asuransi', 'golongan_darah')
    search_fields = ('nama', 'no_pasien', 'no_identitas', 'no_telepon', 'email')
    readonly_fields = ('created_at', 'updated_at', 'umur', 'no_pasien')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Data Pasien', {'fields': ('user', 'no_pasien', 'nama', 'jenis_kelamin', 'tanggal_lahir', 'umur')}),
        ('Identitas', {'fields': ('no_identitas',)}),
        ('Alamat', {'fields': ('alamat', 'kelurahan', 'kecamatan', 'kabupaten', 'provinsi', 'kode_pos')}),
        ('Kontak', {'fields': ('no_telepon', 'email')}),
        ('Asuransi', {'fields': ('jenis_asuransi', 'no_asuransi')}),
        ('Riwayat Medis', {'fields': ('alergi', 'riwayat_penyakit', 'golongan_darah')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
