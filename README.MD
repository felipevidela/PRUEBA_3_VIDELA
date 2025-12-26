# Tienda de Artículos Personalizados (PRUEBA_3_VIDELA)

Projecto Django para catálogo de productos público y administración de pedidos personalizados. 

# Evalución Sumativa N°3 Aplicación CRUD WEB

## Requisitos
- Python3 3.13.0 
- pip
- Django 5.2.7
- Pillow 11.3.0 

# Instalación y ejecución 
1. Clona el repositorio desde tu terminal: 
    - `git clone https://github.com/felipevidela/PRUEBA_3_VIDELA.git`
    - `cd PRUEBA_3_VIDELA`
2. Instala las dependencias: 
    `python3 -m pip install -r requirements.txt`
### Base de datos incluida (recomendada para hacer pruebas)

Para usar la base incluida y alinear el historial sin tocar las tablas:

1. Genera las migraciones faltantes (solo la primera vez):  
   `python3 manage.py makemigrations appTienda`
2. Márcalas como aplicadas (las tablas ya existen):  
   `python3 manage.py migrate appTienda --fake`
3. Ejecuta el resto de migraciones pendientes:  
   `python3 manage.py migrate`

Luego inicia el servidor: 

- `python3 manage.py runserver`

Accesos: 

- Sitio público: http://127.0.0.1:8000/
- Admin: http://127.0.0.1.8000/admin/ 
    - Usuario: `admin`
    - Contraseña: `admin` 

# Base de datos limpia (sin datos de prueba)  

Si prefieres empezar de cero: 
- `rm db.sqlite3`
- `python3 manage.py migrate`
- `python3 manage.py runserver`

Nota: Si ya usaste la base de datos incluida, crear migraciones nuevas puede chocar con las tablas ya existentes.

## Estructura principal 
- `appTienda/`: modelos, vistas, forms, urls.
- `appTienda/templates/`: HTML público y admin extra.
- `media/`: imágenes subidas (productos/pedidos).
- `db.sqlite3`: base de datos con datos de prueba (categorías, productos, insumos, pedidos).

## Funcionalidad extra 
- Resumen de pedidos para el personal administativo en `/admin/appTienda/pedido/resumen/` con conteos por estado, estado de pago y últimos pedidos con enlace para su seguimiento. 

## Evaluación Sumativa N°4 - Tienda Online con API y Deploy 

## Deploy

URL pública: https://prueba3videla-production.up.railway.app 

## Endpoints API 

- **Insumos (CRUD)** https://prueba3videla-production.up.railway.app/api/insumos/
- **Pedidos (crear/modificar)**: https://prueba3videla-production.up.railway.app/api/pedidos/
- **Filtrar pedidos**: https://prueba3videla-production.up.railway.app/api/pedidos/filtrar/ 

## Credenciales de acceso: 
- Usuario: `admin`
- Contraseña: `admin`

## Instrucciones de Deploy (Railway)

### Requisitos previos 
- Cuenta en [Railway] (https://railway.app)
- Repositorio en Github 

### Pasos para deploy 

1. Conectar repositorio a Railway: 
- Ir a https://railway.app y crear nuevo proyecto 
- Seleccionar "Deploy from Github repo" 
- Autorizar y seleccionar el repositorio 

2. Configurar variables de entorno en Railway (opcional): 
- `DJANGO_SECRET_KEY`: clave secreta para producción (Ya tiene una clave por defecto en el código)
- `DEBUG`: False (ya está por defecto)

3. Configurar comando de inicio en Railway: 
- Ir a tu proyecto en Railway 
- Click en el servicio (el bloque de tu app)
- Ir a "Settings" 
- Buscar sección "Deploy" o "Start Command" 
- En "Custom Start Command" escribir:
``` 
gunicorn PRUEBA_3_VIDELA.wsgi
```
- Guardar cambios

4. Generar dominio público: 
- En Settings > Domains > Generate Domain

**Nota** La base de datos (`db.sqlite3`) está incluida en el repositor con datos de prueba precargados (categorías, productos, insumos y pedidos). No es necesario ejecutar migraciones ni crear datos. 

## Endpoints API 

### API 1 - CRUD Insumos 
**Ruta:** `/api/insumos/`

**Método** **Endpoint**           **Descripción** 
GET     `/api/insumos/`         Listar todos los insumos
POST    `/api/insumos/`         Crear nuevo insumo 
GET     `/api/insumos/{id}/`    Ver detalle de un insumo 
PUT     `/api/insumos/{id}/`    Modificar el insumo completo 
PATCH   `/api/insumos/{id}/`    Modificar insumo parcial 
DELETE  `/api/insumos/{id}/`    Eliminar el insumo 

**Ejemplo - Listar insumos:** 
curl https://prueba3videla-production.up.railway.app/api/insumos/ 

**Ejemplo - Crear insumo:** 
curl -X POST https://prueba3videla-production.up.railway.app/api/insumos/ -H "Content-Type: application/json" -d '{"nombre":"Tela Nueva","tipo":"tela","cantidad_disponible":100,"unidad":"metros","marca":"MarcaX","color":"azul"}'

### API 2 - Crear y Modificar Pedidos 
**Ruta** `/api/pedidos/`

**Método** **Endpoint**      **Descripción** 
POST    `/api/pedidos/`      Crear nuevo pedido 
PUT     `/api/pedidos/{id}/` Modificar pedido completo 
PATCH   `/api/pedidos/{id}/` Modificar pedido parcial 

**Nota:** GET (listar) y DELETE están bloqueados por diseño.

**Ejemplo - Crear pedido:**
curl -X POST https://prueba3videla-production.up.railway.app/api/pedidos/ -H "Content-Type: application/json" -d '{"nombre_cliente":"Juan Pérez","descripcion":"Pedido de prueba","estado":"SOLICITADO","estado_pago":"PENDIENTE","plataforma":"SITIO_WEB"}'


**Ejemplo - Modificar estado de pedido:** 
curl -X PATCH https://prueba3videla-production.up.railway.app/api/pedidos/1/ -H "Content-Type: application/json" -d '{"estado":"APROBADO"}'

### API 3 - Filtrar Pedidos 
**RUTA:** `/api/pedidos/filtrar/`

**Parámetro** **Tipo** **Descripción**
desde         fecha    Fecha inicio (YYYY-MM-DD)
hasta         fecha    Fecha fin (YYYY-MM-DD) 
estados       texto    Estados separados por coma
max           entero   Máximo de resultados (1-200)

**Ejemplo - Filtrar por fechas:** 
curl "https://prueba3videla-production.up.railway.app/api/pedidos/filtrar/?desde=2025-01-01&hasta=2025-12-31"

**Ejemplo - Filrar por estado:** 
curl "https://prueba3videla-production.up.railway.app/api/pedidos/filtrar/?estados=SOLICITADO,APROBADO"

**Ejemplo - Filtrar con límite:** 
curl "https://prueba3videla-production.up.railway.app/api/pedidos/filtrar/?max=10" 

**Ejemplo - Filtro combinado:** 
curl "https://prueba3videla-production.up.railway.app/api/pedidos/filtrar/?desde=2025-01-01&estados=SOLICITADO&max=5"

## Evidencia de consumo de APIs 
-- 
### API 1 - GET Insumos (200 OK)
![API Insumos](evidencias/api_insumos.png)

**Endpoint:** `GET /api/insumos/`

**Respuesta JSON:**
```json
[
  {
    "id": 1,
    "nombre": "Tela Algodón Premium",
    "tipo": "tela",
    "cantidad_disponible": 150,
    "unidad": "metros",
    "marca": "TextilPro",
    "color": "blanco"
  }
]

API 2 - GET Pedidos bloqueado (405)
![API Pedidos GET](evidencias/api_pedidos_get_bloqueado.png)

Request: 

{
  "nombre_cliente": "Juan Pérez",
  "descripcion": "Pedido de prueba",
  "estado": "SOLICITADO",
  "estado_pago": "PENDIENTE",
  "plataforma": "SITIO_WEB"
}

Respuesta: HTTP 201 Created

API 3 - Filtrar Pedidos Created 

URL: /api/pedidos/filtrar/?estados=SOLICITADO&max=5

Respuesta JSON: 

{
  "count": 5,
  "results": [
    {
      "id": 21,
      "nombre_cliente": "Cliente Ejemplo",
      "estado": "SOLICITADO",
      "estado_pago": "PENDIENTE"
    }
  ]
}

### API 2 - POST Crear Pedido (201 Created)
![API Pedidos POST](evidencias/api_pedidos_post.png)

### API 3 - GET Filtrar Pedidos (200 OK)
![API Filtrar](evidencias/api_filtrar.png)

### Reporte del Sistema
![Reporte](evidencias/reporte.png)