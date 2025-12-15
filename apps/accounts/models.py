from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom user manager untuk authentication dengan email dan username"""
    
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_('Username harus diisi'))
        if not email:
            raise ValueError(_('Email harus diisi'))
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser harus memiliki is_staff=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser harus memiliki is_superuser=True'))
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Model User Custom untuk SIMRS"""
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('dokter', 'Dokter'),
        ('perawat', 'Perawat'),
        ('apoteker', 'Apoteker'),
        ('kasir', 'Kasir'),
        ('pasien', 'Pasien'),
        ('lab_staff', 'Lab Staff'),
    )
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    nama_lengkap = models.CharField(max_length=255)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='pasien')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nama_lengkap']
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.nama_lengkap} ({self.get_role_display()})'
    
    def get_full_name(self):
        return self.nama_lengkap
    
    def get_short_name(self):
        return self.nama_lengkap.split()[0]
