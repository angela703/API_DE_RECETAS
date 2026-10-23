from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Ingrediente, Receta, RecetaIngrediente


class APIRecetasCRUDTests(APITestCase):
    def setUp(self):
        self.usuario = get_user_model().objects.create_user(
            username='usuario_prueba',
            password='clave-solo-para-pruebas',
        )
        self.categoria = Categoria.objects.create(
            nombre='Categoria de prueba',
            descripcion='Descripcion inicial',
        )
        self.ingrediente = Ingrediente.objects.create(nombre='Ingrediente de prueba')
        self.receta = Receta.objects.create(
            nombre='Receta de prueba',
            descripcion='Descripcion inicial',
            instrucciones='Pasos de prueba',
            tiempo_preparacion=20,
            porciones=2,
            estado='BORRADOR',
            categoria=self.categoria,
            creador=self.usuario,
        )

    def assert_resource_crud(self, url, create_data, update_data, partial_data):
        response = self.client.post(url, create_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        resource_id = response.data['id']
        detail_url = f'{url}{resource_id}/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(resource_id, [item['id'] for item in response.data])

        response = self.client.get(detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], resource_id)

        response = self.client.put(detail_url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        response = self.client.patch(detail_url, partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(detail_url).status_code, status.HTTP_404_NOT_FOUND)

    def test_categorias_crud(self):
        self.assert_resource_crud(
            '/api_recetas/categorias/',
            {'nombre': 'Categoria nueva', 'descripcion': 'Descripcion'},
            {'nombre': 'Categoria nueva', 'descripcion': 'Descripcion completa'},
            {'descripcion': 'Descripcion parcial'},
        )

    def test_ingredientes_crud(self):
        self.assert_resource_crud(
            '/api_recetas/ingredientes/',
            {'nombre': 'Ingrediente nuevo'},
            {'nombre': 'Ingrediente actualizado'},
            {'nombre': 'Ingrediente parcial'},
        )

    def test_recetas_crud(self):
        receta = {
            'nombre': 'Receta nueva',
            'descripcion': 'Descripcion',
            'instrucciones': 'Pasos',
            'tiempo_preparacion': 30,
            'porciones': 4,
            'estado': 'BORRADOR',
            'categoria': self.categoria.pk,
            'creador': self.usuario.pk,
        }
        actualizada = {
            **receta,
            'nombre': 'Receta actualizada',
            'descripcion': 'Descripcion completa',
        }
        self.assert_resource_crud(
            '/api_recetas/recetas/',
            receta,
            actualizada,
            {'descripcion': 'Descripcion parcial'},
        )

    def test_relaciones_receta_ingrediente_crud(self):
        relacion = {
            'receta': self.receta.pk,
            'ingrediente': self.ingrediente.pk,
            'cantidad': '1.00',
            'unidad': 'unidad',
        }
        actualizada = {**relacion, 'cantidad': '2.00'}
        self.assert_resource_crud(
            '/api_recetas/recetas_ingredientes/',
            relacion,
            actualizada,
            {'cantidad': '3.00'},
        )

    def test_receta_expone_relacion_a_traves_de_receta_ingrediente(self):
        RecetaIngrediente.objects.create(
            receta=self.receta,
            ingrediente=self.ingrediente,
            cantidad='2.50',
            unidad='tazas',
        )

        response = self.client.get(f'/api_recetas/recetas/{self.receta.pk}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['ingredientes'],
            [
                {
                    'id': RecetaIngrediente.objects.get(
                        receta=self.receta,
                        ingrediente=self.ingrediente,
                    ).pk,
                    'receta': self.receta.pk,
                    'ingrediente': self.ingrediente.pk,
                    'cantidad': '2.50',
                    'unidad': 'tazas',
                }
            ],
        )

    def test_historial_recetas_crud(self):
        historial = {
            'receta': self.receta.pk,
            'usuario': self.usuario.pk,
            'accion': 'Creacion',
            'descripcion': 'Se creo para la prueba',
        }
        actualizada = {**historial, 'descripcion': 'Descripcion completa'}
        self.assert_resource_crud(
            '/api_recetas/historial_recetas/',
            historial,
            actualizada,
            {'descripcion': 'Descripcion parcial'},
        )

    def test_api_navegable_y_recursos_json(self):
        response = self.client.get('/api_recetas/', HTTP_ACCEPT='text/html')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text/html', response['Content-Type'])

        for recurso in (
            'categorias',
            'ingredientes',
            'recetas',
            'recetas_ingredientes',
            'historial_recetas',
        ):
            with self.subTest(recurso=recurso):
                response = self.client.get(f'/api_recetas/{recurso}/', format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response['Content-Type'], 'application/json')
