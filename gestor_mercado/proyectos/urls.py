from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_proyectos, name='listar_proyectos'),
    path('nuevo/', views.crear_proyecto, name='crear_proyecto'),
    path('<int:proyecto_id>/', views.detalle_proyecto, name='detalle_proyecto'),
]