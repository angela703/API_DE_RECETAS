from django.contrib import admin
from .models import (
	Categoria,
	HistorialReceta,
	Ingrediente,
	Receta,
	RecetaIngrediente,
)
# register your models here.

admin.site.register([
	Categoria,
	Ingrediente,
	Receta,
	RecetaIngrediente,
	HistorialReceta,
])
