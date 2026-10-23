from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


class Receta(models.Model):

    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('PUBLICADA', 'Publicada'),
        ('ARCHIVADA', 'Archivada'),
    ]

    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    instrucciones = models.TextField()
    tiempo_preparacion = models.PositiveIntegerField()
    porciones = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='BORRADOR'
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='recetas'
    )

    creador = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recetas'
    )

    ingredientes = models.ManyToManyField(
        Ingrediente,
        through='RecetaIngrediente',
        related_name='recetas'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(
        Receta,
        on_delete=models.CASCADE
    )

    ingrediente = models.ForeignKey(
        Ingrediente,
        on_delete=models.CASCADE
    )

    cantidad = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    unidad = models.CharField(max_length=50)

    class Meta:
        unique_together = ('receta', 'ingrediente')

    def __str__(self):
        return f"{self.receta} - {self.ingrediente}"


class HistorialReceta(models.Model):
    receta = models.ForeignKey(
        Receta,
        on_delete=models.CASCADE,
        related_name='historial'
    )

    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    accion = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receta} - {self.accion}"