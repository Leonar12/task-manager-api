# 📋 Task Manager API — Leonardo Azamar

API REST para gestión de tareas personales, desarrollada como proyecto de portafolio.

## Stack

- **Framework**: Django 5 + Django REST Framework
- **Base de datos**: PostgreSQL
- **Autenticación**: JWT (SimpleJWT) — access + refresh tokens
- **Documentación**: drf-spectacular → Swagger UI + ReDoc
- **Entorno**: Virtualenv + python-decouple
- **Lenguaje**: Python 3.12

---

## ⚡ Inicio rápido

```bash
# 1. Clonar el repositorio
git clone https://github.com/Leonar12/task-manager-api.git
cd task-manager-api

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL

# 5. Crear la base de datos en PostgreSQL
# CREATE DATABASE task_api_db;

# 6. Aplicar migraciones
python manage.py makemigrations users
python manage.py makemigrations tasks
python manage.py migrate

# 7. Ejecutar servidor
python manage.py runserver

# 8. Abrir documentación
# http://localhost:8000/api/docs/
```

---

## 📁 Estructura del proyecto

```
task_api/
├── config/                  
│   ├── settings.py          → Configuración principal del proyecto
│   ├── urls.py              → Rutas globales + Swagger
│   └── wsgi.py              → Punto de entrada WSGI
├── apps/
│   ├── users/               → Modelo de usuario + autenticación
│   │   ├── models.py        → Usuario personalizado (email como login)
│   │   ├── serializers.py   → Register, Login, Profile, ChangePassword
│   │   ├── views/           → Vistas de auth y perfil
│   │   └── urls/            → Rutas de auth y usuario
│   └── tasks/               → CRUD de tareas
│       ├── models.py        → Modelo Task con prioridad y estado
│       ├── serializers.py   → Serializers de creación y lectura
│       ├── views.py         → ViewSet con filtros y endpoint summary
│       └── urls.py          → Rutas del router
├── requirements.txt
├── .env.example
└── manage.py
```

---

## 🗺️ Endpoints

### Auth — `/api/auth/`

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/register/` | Crear cuenta nueva |
| POST | `/login/` | Obtener tokens JWT |
| POST | `/token/refresh/` | Renovar access token |
| POST | `/logout/` | Invalidar sesión |
| PUT | `/change-password/` | Cambiar contraseña |

### Usuarios — `/api/users/`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/me/` | Ver perfil propio |
| PATCH | `/me/` | Actualizar perfil |

### Tareas — `/api/tasks/`

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/` | Listar tareas (`?status=`, `?priority=`, `?search=`) |
| POST | `/` | Crear tarea |
| GET | `/{id}/` | Ver tarea por ID |
| PUT | `/{id}/` | Actualizar tarea completa |
| PATCH | `/{id}/` | Actualizar tarea parcial |
| DELETE | `/{id}/` | Eliminar tarea |
| GET | `/summary/` | Conteo de tareas por estado |

---

## 🔑 Flujo de autenticación

```json
// POST /api/auth/login/
{
  "email": "usuario@example.com",
  "password": "contraseña"
}

// Respuesta:
{
  "access":  "<token de corta duración — 60 min>",
  "refresh": "<token de larga duración — 7 días>",
  "user": { ... }
}
```

Usar el `access` token en cada petición:
```
Authorization: Bearer <access_token>
```

---

## 📦 Modelo de tarea

```json
{
  "id": 1,
  "owner": "usuario@example.com",
  "title": "Implementar autenticación JWT",
  "description": "Agregar login y refresh tokens",
  "priority": "high",
  "status": "in_progress",
  "due_date": "2026-12-31",
  "created_at": "2026-06-07T10:00:00Z",
  "updated_at": "2026-06-07T08:30:00Z"
}
```

**Valores de priority:** `low` · `medium` · `high`  
**Valores de status:** `pending` · `in_progress` · `done`

---

## 🌐 Variables de entorno

Crea un archivo `.env` basado en `.env.example`:

```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=task_api_db
DB_USER=postgres
DB_PASSWORD=tu-contraseña
DB_HOST=localhost
DB_PORT=5432
```
---
## 🌐 Demo en vivo

API desplegada en Railway:  
https://task-manager-api-production-5ce7.up.railway.app/api/docs/

---

Desarrollado por **Leonardo de Jesús Azamar Tegoma** · México 🇲🇽  