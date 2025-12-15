from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Landing page
    path('', views.landing_page, name='landing'),
]
