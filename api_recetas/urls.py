from django.urls import path, include
from rest_framework import routers
from api_recetas import views

enrutador = routers.DefaultRouter()
enrutador.register(r'categorias', views.CategoriaViewSet)
enrutador.register(r'ingredientes', views.IngredienteViewSet)
enrutador.register(r'recetas', views.RecetaViewSet)
enrutador.register(r'recetas_ingredientes', views.RecetaIngredienteViewSet)
enrutador.register(r'historial_recetas', views.HistorialRecetaViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api_recetas/', include(enrutador.urls)),
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
]

