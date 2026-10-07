from selenium.webdriver.common.by import By
from utils.helpers import iniciar_sesion


def test_login_exitoso(driver):
    """Verifica que el usuario pueda ingresar al catálogo."""
    iniciar_sesion(driver)

    # Validamos la dirección y los títulos después del login.
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"
    assert driver.find_element(By.CLASS_NAME, "app_logo").text == "Swag Labs"