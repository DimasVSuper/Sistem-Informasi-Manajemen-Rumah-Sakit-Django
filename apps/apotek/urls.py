from django.urls import path
from . import views

app_name = 'apotek'

urlpatterns = [
    # Obat
    path('', views.obat_list, name='list'),
    path('create/', views.obat_create, name='create'),
    path('<int:pk>/', views.obat_detail, name='detail'),
    path('<int:pk>/update/', views.obat_update, name='update'),
    path('<int:pk>/delete/', views.obat_delete, name='delete'),
    
    # Resep
    path('resep/', views.resep_list, name='resep_list'),
    path('resep/<int:pk>/', views.resep_detail, name='resep_detail'),
    path('resep/<int:pk>/approve/', views.resep_approve, name='resep_approve'),
]
