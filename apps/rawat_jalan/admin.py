from django.contrib import admin
from .models import RawatJalan, Antrian


@admin.register(RawatJalan)
class RawatJalanAdmin(admin.ModelAdmin):
    list_display = ('no_kunjungan', 'pasien', 'dokter', 'tanggal_kunjungan', 'status', 'total_biaya')
    list_filter = ('status', 'tanggal_kunjungan', 'dokter')
    search_fields = ('no_kunjungan', 'pasien__nama', 'keluhan', 'diagnosa')
    readonly_fields = ('created_at', 'updated_at', 'no_kunjungan')
    date_hierarchy = 'tanggal_kunjungan'
    ordering = ('-tanggal_kunjungan',)
    actions = ['mark_completed', 'mark_pending']
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = 'Tandai Selesai'
    
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_pending.short_description = 'Tandai Pending'


@admin.register(Antrian)
class AntrianAdmin(admin.ModelAdmin):
    list_display = ('nomor_antrian', 'rawat_jalan', 'tanggal_antrian', 'status')
    list_filter = ('status', 'tanggal_antrian')
    search_fields = ('rawat_jalan__pasien__nama', 'nomor_antrian')
