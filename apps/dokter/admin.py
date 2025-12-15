from django.contrib import admin
from .models import Spesialisasi, Dokter


@admin.register(Spesialisasi)
class SpesialisasiAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)


@admin.register(Dokter)
class DokterAdmin(admin.ModelAdmin):
    list_display = ('no_dokter', 'nama', 'spesialisasi', 'no_lisensi', 'is_available', 'no_telepon', 'created_at')
    list_filter = ('spesialisasi', 'is_available', 'created_at')
    search_fields = ('nama', 'no_dokter', 'no_lisensi', 'no_str', 'no_telepon')
    readonly_fields = ('created_at', 'updated_at', 'no_dokter')
    date_hierarchy = 'created_at'
    ordering = ('spesialisasi', 'nama')
    actions = ['mark_available', 'mark_unavailable']
    
    def mark_available(self, request, queryset):
        queryset.update(is_available=True)
    mark_available.short_description = 'Tandai sebagai Tersedia'
    
    def mark_unavailable(self, request, queryset):
        queryset.update(is_available=False)
    mark_unavailable.short_description = 'Tandai sebagai Tidak Tersedia'
    
    fieldsets = (
        ('Data Dokter', {'fields': ('user', 'no_dokter', 'nama', 'spesialisasi')}),
        ('Lisensi', {'fields': ('no_lisensi', 'no_str')}),
        ('Kontak', {'fields': ('no_telepon', 'alamat')}),
        ('Jadwal', {'fields': ('jam_kerja_mulai', 'jam_kerja_selesai', 'hari_kerja')}),
        ('Status', {'fields': ('is_available',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
