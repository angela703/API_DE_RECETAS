from rest_framework import viewsets

from django.shortcuts import render

from api_recetas.serializer import (
    CategoriaSerializer,
    HistorialRecetaSerializer,
    IngredienteSerializer,
    RecetaIngredienteSerializer,
    RecetaSerializer
)

from .models import (
    Categoria,
    HistorialReceta,
    Ingrediente,
    Receta,
    RecetaIngrediente,
)


def home(request):
    return render(request, 'api_recetas/home.html')


def page_not_found(request, exception):
    return render(request, 'api_recetas/404.html', status=404)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class HistorialRecetaViewSet(viewsets.ModelViewSet):
    queryset = HistorialReceta.objects.all()
    serializer_class = HistorialRecetaSerializer


class IngredienteViewSet(viewsets.ModelViewSet):
    queryset = Ingrediente.objects.all()
    serializer_class = IngredienteSerializer


class RecetaIngredienteViewSet(viewsets.ModelViewSet):
    queryset = RecetaIngrediente.objects.all()
    serializer_class = RecetaIngredienteSerializer


class RecetaViewSet(viewsets.ModelViewSet):
    queryset = Receta.objects.all()
    serializer_class = RecetaSerializer