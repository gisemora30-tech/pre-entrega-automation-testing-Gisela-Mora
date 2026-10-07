import logging
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# Preparamos las carpetas y el archivo de registro.
REPORTS = Path(__file__).resolve().parent / "reports"
CAPTURAS = REPORTS / "screenshots"
CAPTURAS.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("pruebas_saucedemo")
logger.setLevel(logging.INFO)

archivo_log = logging.FileHandler(
    REPORTS / "ejecucion.log",
    mode="w",
    encoding="utf-8",
)
archivo_log.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
)
logger.addHandler(archivo_log)


@pytest.fixture
def driver():
    """Crea un navegador nuevo para cada prueba."""
    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--start-maximized")

    logger.info("Abriendo Chrome")
    navegador = webdriver.Chrome(options=opciones)

    try:
        navegador.set_page_load_timeout(30)
        yield navegador
    finally:
        logger.info("Cerrando Chrome")
        navegador.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Registra resultados y captura la pantalla si una prueba falla."""
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when == "call" or reporte.failed:
        logger.info(
            "%s | etapa=%s | resultado=%s",
            item.nodeid,
            reporte.when,
            reporte.outcome,
        )

    if reporte.failed:
        logger.error("%s", reporte.longrepr)

    # Capturamos antes de que la fixture cierre el navegador.
    if reporte.failed and reporte.when in ("setup", "call"):
        navegador = item.funcargs.get("driver")
        if navegador is None:
            return

        fecha = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        ruta = CAPTURAS / f"{item.name}_{fecha}.png"

        try:
            if navegador.save_screenshot(str(ruta)):
                logger.info("Captura guardada: %s", ruta)
            else:
                logger.error("No se pudo guardar la captura: %s", ruta)
        except (WebDriverException, OSError) as error:
            logger.error("No se pudo tomar la captura: %s", error)