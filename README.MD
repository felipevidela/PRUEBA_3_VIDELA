# Tienda de Artículos Personalizados (PRUEBA_3_VIDELA)

Projecto Django para catálogo de productos público y administración de pedidos personalizados. 

# Evalución Sumativa N°3 Aplicación CRUD WEB

## Requisitos
- Python3 3.13.0 
- Pip
- Django 5.2.7
- Pillow 11.3.0 

# Instalación y ejecución 
1. Clona el repositorio desde tu terminal: 
    `git clone https://github.com/felipevidela/PRUEBA_3_VIDELA.git`
    `cd PRUEBA_3_VIDELA`
2. Instala dependencias: 
    `pip install -r requirements.txt`
3. Aplica migraciones: 
    `python3 manage.py migrate`
4. Inicia el servidor:
    `python3 manage.py runserver`
5. Accede:
    - URL pública: `http://127.0.0.1:8000/`
    - Admin: `http://127.0.0.1:8000/admin/`

Para hacer la revisión de la aplicación use:
- Usuario: `admin`
- Contraseña: `admin` 

## Funcionalidad extra 
- Resumen de pedidos para el personal administativo en `/admin/appTienda/pedido/resumen/` con conteos por estado, estado de pago y últimos pedidos con enlace para su seguimiento. 

## Estructura principal 
- `appTienda/`: modelos, vistas, forms, urls.
- `appTienda/templates/`: HTML público y admin extra.
- `media/`: imágenes subidas (productos/pedidos).
- `db.sqlite3`: base de datos con datos de prueba (categorías, productos, insumos, pedidos).

# Datos de prueba 
La base de datos `db.sqlite3` incluye categorías, productos, insumos y pedidos de ejemplo para un revisión rápida del sistema 









