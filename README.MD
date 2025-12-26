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








