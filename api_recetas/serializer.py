from rest_framework import serializers

from .models import (
    Categoria,
    HistorialReceta,
    Ingrediente,
    Receta,
    RecetaIngrediente,
)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class IngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingrediente
        fields = '__all__'


class RecetaIngredienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecetaIngrediente
        fields = '__all__'


class RecetaSerializer(serializers.ModelSerializer):
    ingredientes = RecetaIngredienteSerializer(
        many=True,
        read_only=True,
        source='recetaingrediente_set',
    )

    class Meta:
        model = Receta
        fields = '__all__'


class HistorialRecetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistorialReceta
        fields = '__all__'