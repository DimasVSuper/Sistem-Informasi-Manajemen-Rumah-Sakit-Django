from django.contrib import admin
from .models import JenisPemeriksaan, ParameterLab, PermintaanLab, HasilLab, DetailHasil


@admin.register(JenisPemeriksaan)
class JenisPemeriksaanAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kode', 'tarif', 'waktu_hasil')
    list_filter = ('created_at',)
    search_fields = ('nama', 'kode')


@admin.register(ParameterLab)
class ParameterLabAdmin(admin.ModelAdmin):
    list_display = ('nama_parameter', 'jenis_pemeriksaan', 'satuan')
    list_filter = ('jenis_pemeriksaan',)
    search_fields = ('nama_parameter',)


@admin.register(PermintaanLab)
class PermintaanLabAdmin(admin.ModelAdmin):
    list_display = ('no_permintaan', 'rekam_medis', 'tanggal_permintaan', 'status', 'total_harga')
    list_filter = ('status', 'tanggal_permintaan')
    search_fields = ('no_permintaan', 'rekam_medis__pasien__nama')
    readonly_fields = ('created_at', 'updated_at', 'no_permintaan')
    date_hierarchy = 'tanggal_permintaan'
    ordering = ('-tanggal_permintaan',)
    actions = ['mark_pending', 'mark_approved', 'mark_completed']
    
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_pending.short_description = 'Ubah ke Pending'
    
    def mark_approved(self, request, queryset):
        queryset.update(status='approved')
    mark_approved.short_description = 'Setujui Permintaan'
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = 'Tandai Selesai'


@admin.register(HasilLab)
class HasilLabAdmin(admin.ModelAdmin):
    list_display = ('permintaan', 'tanggal_hasil', 'dokter_pemeriksa')
    list_filter = ('tanggal_hasil',)
    search_fields = ('permintaan__no_permintaan', 'dokter_pemeriksa__nama')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'tanggal_hasil'


@admin.register(DetailHasil)
class DetailHasilAdmin(admin.ModelAdmin):
    list_display = ('hasil', 'parameter', 'nilai', 'normal')
    list_filter = ('normal', 'hasil__tanggal_hasil')
