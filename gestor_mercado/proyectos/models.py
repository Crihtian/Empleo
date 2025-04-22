from django.db import models
from usuarios.models import UserProfile

class Proyecto(models.Model):
    ESTADOS = (
        ('PLAN', 'Planeación'),
        ('ACT', 'En Progreso'),
        ('SUSP', 'Suspendido'),
        ('COMP', 'Completado'),
    )
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=4, choices=ESTADOS, default='PLAN')
    fecha_inicio = models.DateField()
    fecha_limite = models.DateField()
    colaboradores = models.ManyToManyField(UserProfile, related_name='proyectos_asignados')
    
    class Meta:
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_limite']),
        ]

    def __str__(self):
        return self.nombre

class Tarea(models.Model):
    ESTADOS_TAREA = (
        ('PEND', 'Pendiente'),
        ('PROG', 'En Progreso'),
        ('COMP', 'Completada'),
    )
    
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='tareas')
    asignados = models.ManyToManyField(UserProfile, related_name='tareas_asignadas')
    estado = models.CharField(max_length=4, choices=ESTADOS_TAREA, default='PEND')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_limite = models.DateTimeField()
    
    class Meta:
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_limite']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.proyecto.nombre}"