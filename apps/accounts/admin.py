from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nama_lengkap', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'nama_lengkap')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informasi Login', {'fields': ('username', 'email', 'password')}),
        ('Informasi Personal', {'fields': ('nama_lengkap', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
