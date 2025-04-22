# datos/urls.py
from django.urls import path
from .views import ejecutar_scraping

urlpatterns = [
    path('scraping/', ejecutar_scraping, name='ejecutar_scraping'),
    # ... otras URLs
]