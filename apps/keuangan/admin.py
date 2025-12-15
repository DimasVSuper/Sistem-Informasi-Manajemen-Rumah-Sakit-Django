from django.contrib import admin
from django.utils.html import format_html
from .models import Invoice, DetailInvoice, Pembayaran, LaporanKeuangan


class DetailInvoiceInline(admin.TabularInline):
    model = DetailInvoice
    extra = 1
    fields = ('tipe_layanan', 'deskripsi', 'jumlah', 'subtotal')
    readonly_fields = ('subtotal',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('no_invoice', 'pasien', 'tanggal_invoice', 'status_badge', 'total', 'get_paid')
    list_filter = ('status', 'tanggal_invoice')
    search_fields = ('no_invoice', 'pasien__nama')
    readonly_fields = ('created_at', 'updated_at', 'no_invoice')
    date_hierarchy = 'tanggal_invoice'
    ordering = ('-tanggal_invoice',)
    inlines = [DetailInvoiceInline]
    actions = ['mark_paid', 'mark_pending']
    
    def status_badge(self, obj):
        colors = {'pending': 'orange', 'paid': 'green', 'cancelled': 'red'}
        color = colors.get(obj.status, 'gray')
        return format_html('<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;\">{}</span>', color, obj.get_status_display())
    status_badge.short_description = 'Status'
    
    def get_paid(self, obj):
        paid_amount = sum(p.jumlah for p in obj.pembayaran_set.filter(status='completed'))
        remaining = obj.total - paid_amount
        if remaining <= 0:
            return format_html('<span style="color: green; font-weight: bold;">✓ Lunas</span>')
        return format_html('<span style="color: red;">Sisa: Rp {:,.0f}</span>', remaining)
    get_paid.short_description = 'Pembayaran'
    
    def mark_paid(self, request, queryset):
        queryset.update(status='paid')
    mark_paid.short_description = 'Tandai Lunas'
    
    def mark_pending(self, request, queryset):
        queryset.update(status='pending')
    mark_pending.short_description = 'Tandai Pending'


@admin.register(DetailInvoice)
class DetailInvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'tipe_layanan', 'deskripsi', 'jumlah', 'subtotal')
    list_filter = ('tipe_layanan', 'invoice__tanggal_invoice')
    search_fields = ('invoice__no_invoice', 'deskripsi')


@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):
    list_display = ('no_pembayaran', 'invoice', 'tanggal_pembayaran', 'metode', 'jumlah', 'status')
    list_filter = ('status', 'metode', 'tanggal_pembayaran')
    search_fields = ('no_pembayaran', 'invoice__no_invoice', 'invoice__pasien__nama')
    readonly_fields = ('created_at', 'updated_at', 'no_pembayaran')
    date_hierarchy = 'tanggal_pembayaran'
    ordering = ('-tanggal_pembayaran',)


@admin.register(LaporanKeuangan)
class LaporanKeuanganAdmin(admin.ModelAdmin):
    list_display = ('bulan', 'tahun', 'total_pendapatan', 'total_pembayaran', 'total_belum_terbayar')
    list_filter = ('tahun', 'bulan')
    readonly_fields = ('created_at', 'updated_at')
