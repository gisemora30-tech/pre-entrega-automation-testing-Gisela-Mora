import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    """Crea un navegador nuevo para cada prueba."""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--start-maximized")

    navegador = webdriver.Chrome(options=opciones)
    navegador.set_page_load_timeout(30)

    try:
        yield navegador
    finally:
        # Cerramos el navegador incluso si la prueba falla.
        navegador.quit()