# API de Recetas

API REST para administrar categorías, ingredientes, recetas, sus ingredientes y el historial de cambios. El proyecto está desarrollado con Django y Django REST Framework y conserva MySQL como base de datos de la aplicación.

## Tecnologías

- Python
- Django
- Django REST Framework
- MySQL y `mysqlclient`
- `python-decouple` para leer la configuración desde `.env`

Las versiones instaladas en el entorno de desarrollo están fijadas en `requirements.txt`.

## Estructura principal

```text
.
├── api_recetas/
│   ├── fixtures/             # Datos de ejemplo
│   ├── migrations/           # Migraciones de la aplicación
│   ├── templates/            # Plantillas HTML
│   ├── models.py             # Modelos de datos
│   ├── serializer.py         # Serializers de Django REST Framework
│   ├── views.py              # Vistas y ModelViewSet
│   ├── urls.py               # Router y rutas de la API
│   └── sql.sql               # Creación de la base de datos y permisos
├── motor_django/
│   ├── settings.py           # Configuración de la aplicación y conexión MySQL
│   ├── test_settings.py      # Base SQLite temporal, solo para pruebas
│   └── urls.py               # Rutas principales de Django
├── static/                   # Archivos estáticos
├── manage.py
├── requirements.txt
└── .env.example
```

## Requisitos

- Windows 10/11
- Python compatible con la versión de Django indicada en `requirements.txt`
- MySQL Server accesible desde el equipo
- Git (opcional, para clonar el repositorio)

## Instalación en Windows

Desde PowerShell, sitúate en la carpeta del proyecto:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si PowerShell bloquea la activación del entorno, puedes usar directamente los ejecutables `.\venv\Scripts\python.exe` y `.\venv\Scripts\pip.exe`.

## Configuración de `.env`

En la raíz del proyecto, crea tu archivo local a partir de la plantilla:

```powershell
Copy-Item .env.example .env
```

Edita `.env` en tu equipo. Define una `SECRET_KEY` propia y el nombre de usuario y la contraseña del usuario de MySQL. No compartas ni subas `.env` a GitHub; `.gitignore` lo excluye.

```dotenv
SECRET_KEY=TU_CLAVE_SECRETA_LOCAL
NAME=api_recetas
HOST=localhost
PORT=3306
USER=api_recetas_user
PASSWORD=LA_MISMA_PASSWORD_CONFIGURADA_EN_MYSQL
```

No copies literalmente los valores de ejemplo de `SECRET_KEY` ni `PASSWORD`. La contraseña debe coincidir con la que configures para el usuario de MySQL.

## Base de datos MySQL

El script `api_recetas/sql.sql` crea `api_recetas`, crea el usuario `api_recetas_user` si aún no existe y asigna permisos sobre esa base. Antes de ejecutarlo, reemplaza el marcador de contraseña del script por la misma contraseña que definiste en `.env`. Ejecútalo con una cuenta administradora de MySQL que tenga permiso para crear usuarios y conceder privilegios; no uses esa cuenta administradora para ejecutar la aplicación.

El `GRANT` del script se puede volver a ejecutar para actualizar los permisos. `CREATE USER IF NOT EXISTS` no cambia la contraseña de una cuenta que ya exista. Si la cuenta ya existía, comprueba que su contraseña coincida con `.env`; si no coincide, actualízala conscientemente en MySQL y en `.env`.

El script no se ejecuta automáticamente al iniciar Django. Después de ejecutarlo, vuelve a dejar el marcador en el archivo y no compartas ni subas una contraseña real a GitHub.

Después de reemplazar el marcador de contraseña, ejecútalo desde el Símbolo del sistema con una cuenta administradora de MySQL:

```cmd
mysql -u root -p < api_recetas\sql.sql
```

Esta cuenta se utiliza solo para preparar la base de datos y los permisos; la aplicación se conecta como `api_recetas_user`.

## Migraciones y superusuario

Una vez configurada la conexión y creado el usuario de MySQL:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

Las migraciones crean o actualizan el esquema; no elimines la base de datos para aplicarlas.

## Iniciar el servidor

```powershell
python manage.py runserver
```

La página de inicio está en `http://127.0.0.1:8000/`. El administrador de Django está en `http://127.0.0.1:8000/admin/`.

## Endpoints

Todos los endpoints de la API están bajo `/api_recetas/`. El router de Django REST Framework ofrece respuestas JSON y una interfaz navegable desde el navegador.

| Recurso | Colección |
|---|---|
| Categorías | `http://127.0.0.1:8000/api_recetas/categorias/` |
| Ingredientes | `http://127.0.0.1:8000/api_recetas/ingredientes/` |
| Recetas | `http://127.0.0.1:8000/api_recetas/recetas/` |
| Ingredientes de recetas | `http://127.0.0.1:8000/api_recetas/recetas_ingredientes/` |
| Historial de recetas | `http://127.0.0.1:8000/api_recetas/historial_recetas/` |

Cada colección admite `GET` (listar) y `POST` (crear). Para consultar o modificar un elemento, agrega su identificador, por ejemplo `/api_recetas/categorias/1/`; estas rutas admiten `GET`, `PUT`, `PATCH` y `DELETE`.

### Ejemplos

Listar categorías en PowerShell:

```powershell
Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/api_recetas/categorias/
```

Crear una categoría:

```powershell
$body = @{
    nombre = "Desayunos"
    descripcion = "Preparaciones para comenzar el día."
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/api_recetas/categorias/ `
    -ContentType "application/json" `
    -Body $body
```

Las recetas incluyen una colección de relaciones `ingredientes` con sus cantidades y unidades. Para crear, actualizar o eliminar esas relaciones, utiliza el endpoint `recetas_ingredientes`.

## Pruebas y comprobaciones

Las pruebas CRUD usan una base de datos SQLite en memoria independiente. La configuración normal de la aplicación y sus datos continúan en MySQL.

```powershell
python manage.py test api_recetas --settings=motor_django.test_settings
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py migrate --check
```

Los dos últimos comandos usan la conexión MySQL configurada en `.env`; requieren que el servidor esté disponible y que el usuario de la aplicación tenga permisos suficientes para consultar el estado de las migraciones.
