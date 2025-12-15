from django.contrib import admin
from .models import Ruangan, RawatInap


@admin.register(Ruangan)
class RuanganAdmin(admin.ModelAdmin):
    list_display = ('nama', 'tipe', 'kasur_tersedia', 'jumlah_kasur', 'tarif_per_hari', 'is_active')
    list_filter = ('tipe', 'is_active', 'created_at')
    search_fields = ('nama',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(RawatInap)
class RawatInapAdmin(admin.ModelAdmin):
    list_display = ('no_rawat_inap', 'pasien', 'dokter', 'ruangan', 'tanggal_masuk', 'status', 'total_biaya')
    list_filter = ('status', 'tanggal_masuk', 'ruangan', 'dokter')
    search_fields = ('no_rawat_inap', 'pasien__nama', 'no_kasur')
    readonly_fields = ('created_at', 'updated_at', 'lama_menginap', 'no_rawat_inap')
    date_hierarchy = 'tanggal_masuk'
    ordering = ('-tanggal_masuk',)
    actions = ['mark_active', 'mark_discharged']
    
    def mark_active(self, request, queryset):
        queryset.update(status='active')
    mark_active.short_description = 'Tandai Aktif'
    
    def mark_discharged(self, request, queryset):
        queryset.update(status='discharged')
    mark_discharged.short_description = 'Tandai Pulang'
    
    fieldsets = (
        ('Identitas', {'fields': ('no_rawat_inap', 'pasien', 'dokter', 'rekam_medis')}),
        ('Ruangan', {'fields': ('ruangan', 'no_kasur')}),
        ('Tanggal', {'fields': ('tanggal_masuk', 'tanggal_keluar')}),
        ('Medis', {'fields': ('diagnosa_awal', 'catatan_perawatan')}),
        ('Finansial', {'fields': ('status', 'total_biaya')}),
        ('Info Tambahan', {'fields': ('lama_menginap',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
