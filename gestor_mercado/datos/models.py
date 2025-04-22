from django.db import models

class Habilidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Habilidades"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class OfertaEmpleo(models.Model):
    PLATAFORMAS = (
        ('TECNO', 'Tecnoempleo'),
        ('INFO', 'InfoJobs'),
        ('LINKED', 'LinkedIn'),
    )
    
    titulo = models.CharField(max_length=200)
    empresa = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=100)
    plataforma = models.CharField(max_length=6, choices=PLATAFORMAS)
    habilidades = models.ManyToManyField(Habilidad)
    salario = models.CharField(max_length=100, blank=True, null=True)  # Ej: "20.000-30.000 €"
    fecha_publicacion = models.DateField()
    url = models.URLField(max_length=500)
    
    class Meta:
        verbose_name_plural = "Ofertas de empleo"
        ordering = ['-fecha_publicacion']
        indexes = [
            models.Index(fields=['plataforma']),
            models.Index(fields=['empresa']),
            models.Index(fields=['ubicacion']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.empresa}"