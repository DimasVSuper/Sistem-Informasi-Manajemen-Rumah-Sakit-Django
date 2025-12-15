from django.contrib import admin
from django.utils.html import format_html
from .models import KategoriObat, Obat, Resep, DetailResep


@admin.register(KategoriObat)
class KategoriObatAdmin(admin.ModelAdmin):
    list_display = ('nama',)
    search_fields = ('nama',)


@admin.register(Obat)
class ObatAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kategori', 'kode_obat', 'dosis', 'stok', 'harga', 'stok_status')
    list_filter = ('kategori', 'bentuk', 'created_at')
    search_fields = ('nama', 'kode_obat', 'kandungan')
    readonly_fields = ('created_at', 'updated_at', 'kode_obat')
    date_hierarchy = 'created_at'
    ordering = ('kategori', 'nama')
    
    def stok_status(self, obj):
        if obj.stok <= 10:
            return format_html('<span style="color: red; font-weight: bold;">⚠️ Rendah ({} unit)</span>', obj.stok)
        elif obj.stok <= 50:
            return format_html('<span style="color: orange;">⚠️ Sedang ({} unit)</span>', obj.stok)
        return format_html('<span style="color: green;">✓ Cukup ({} unit)</span>', obj.stok)
    stok_status.short_description = 'Status Stok'
    
    fieldsets = (
        ('Informasi Obat', {'fields': ('nama', 'kategori', 'kode_obat')}),
        ('Detail Obat', {'fields': ('kandungan', 'dosis', 'bentuk')}),
        ('Stok & Harga', {'fields': ('stok', 'harga')}),
        ('Informasi Penting', {'fields': ('efek_samping', 'kontraindikasi', 'tanggal_kadaluarsa')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(Resep)
class ResepAdmin(admin.ModelAdmin):
    list_display = ('no_resep', 'rekam_medis', 'tanggal_resep', 'status', 'total_harga')
    list_filter = ('status', 'tanggal_resep')
    readonly_fields = ('no_resep', 'total_harga')
    date_hierarchy = 'tanggal_resep'
    ordering = ('-tanggal_resep',)
    actions = ['mark_approved', 'mark_pending']
    
    def mark_approved(self, request, queryset):
        queryset.filter(status='pending').update(status='approved')
    mark_approved.short_description = 'Setujui Resep'
    
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_pending.short_description = 'Ubah ke Pending'
    search_fields = ('no_resep', 'rekam_medis__pasien__nama')
    readonly_fields = ('created_at', 'updated_at', 'total_harga')


@admin.register(DetailResep)
class DetailResepAdmin(admin.ModelAdmin):
    list_display = ('resep', 'obat', 'jumlah', 'subtotal')
    list_filter = ('resep__tanggal_resep',)
    search_fields = ('resep__no_resep', 'obat__nama')
