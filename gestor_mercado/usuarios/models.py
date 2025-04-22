from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class UserProfile(AbstractUser):
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('GESTOR', 'Gestor de Proyectos'),
        ('COLAB', 'Colaborador'),
    )
    
    role = models.CharField(max_length=10, choices=ROLES, default='COLAB')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    groups = models.ManyToManyField(
        Group,
        related_name="userprofile_groups",  # Cambia el related_name
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="userprofile_permissions",  # Cambia el related_name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    
    # Campos básicos heredados de AbstractUser:
    # username, first_name, last_name, email, etc.
    
    class Meta:
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['date_joined']),
        ]

"""
# Comentado para posible uso futuro
class UserHabilidad(models.Model):
    NIVELES = (
        ('B', 'Básico'),
        ('M', 'Intermedio'),
        ('A', 'Avanzado'),
    )
    
    usuario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    habilidad = models.ForeignKey('datos.Habilidad', on_delete=models.CASCADE)
    nivel = models.CharField(max_length=1, choices=NIVELES, default='B')
"""