# Preentrega de Automation Testing — Gisela Mora

Proyecto de pruebas automatizadas sobre https://www.saucedemo.com/.
Valida el inicio de sesión, el catálogo de productos y la incorporación
de un producto al carrito.

## Tecnologías

- Python
- Selenium WebDriver
- Pytest
- pytest-html
- Git

## Requisitos

- Python instalado y disponible desde la terminal.
- Google Chrome instalado.
- Acceso a Internet para ingresar a SauceDemo y para que Selenium
  gestione el controlador de Chrome.

El proyecto se ejecutó con Python 3.14.7 en Windows 11.
Las versiones de las dependencias están en `requirements.txt`.

## Instalación en Windows (PowerShell)

Abrir una terminal en la carpeta del proyecto y ejecutar:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --no-cache-dir -r requirements.txt
```

Los comandos siguientes utilizan directamente el Python del entorno
virtual, por lo que no es necesario activarlo.

## Ejecutar las pruebas

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py -v -s --tb=short
```

## Generar el reporte HTML

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_saucedemo.py -v --tb=short --html=reports/reporte.html --self-contained-html
```

Para abrir el reporte:

```powershell
Start-Process .\reports\reporte.html
```

## Casos de prueba

1. **Login exitoso:** ingresa con `standard_user` y `secret_sauce`,
   verifica la URL del catálogo y los títulos “Products” y “Swag Labs”.
2. **Catálogo de productos:** verifica el título, la presencia de
   productos, el menú y el filtro. Muestra el nombre y el precio del
   primer producto.
3. **Agregar producto al carrito:** agrega el primer producto, verifica
   que el contador pase de vacío a uno y comprueba el nombre y la
   cantidad del producto dentro del carrito.

Cada prueba abre una sesión nueva de Chrome y cierra el navegador al
terminar. Se utilizan esperas explícitas para el login y el carrito.

## Organización del proyecto

- `tests/test_saucedemo.py`: contiene las tres pruebas.
- `utils/helpers.py`: contiene la función de inicio de sesión.
- `utils/__init__.py`: identifica el paquete de utilidades.
- `conftest.py`: configura el navegador, los registros y las capturas.
- `requirements.txt`: contiene las dependencias.
- `reports/reporte.html`: reporte de resultados.
- `reports/ejecucion.log`: registro de la última ejecución.
- `reports/screenshots/`: capturas automáticas de pruebas fallidas.

## Registros y capturas

El registro incluye la apertura y el cierre del navegador, el resultado
de cada prueba y los detalles de los fallos. Se reemplaza en cada
ejecución.

Si una prueba falla mientras el navegador está disponible, se guarda
una captura PNG con el nombre de la prueba y la fecha y hora.
Si el navegador se cerró o falló y no permite tomar la captura,
el motivo queda registrado en el log.

Las capturas incluidas se generaron durante una verificación con un
fallo intencional. Luego se restauró la validación correcta del login.

## Resultado verificado

El reporte incluido corresponde a una ejecución con:

- 3 pruebas aprobadas.
- 0 pruebas fallidas.
- 0 errores.