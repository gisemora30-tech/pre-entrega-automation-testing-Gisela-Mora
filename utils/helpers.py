from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def iniciar_sesion(driver):
    """Ingresa a SauceDemo con el usuario de prueba."""
    driver.get("https://www.saucedemo.com/")
    espera = WebDriverWait(driver, 15)

    # Esperamos a que el campo de usuario esté visible.
    usuario = espera.until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    )
    usuario.send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Esperamos la llegada al catálogo.
    espera.until(EC.url_contains("/inventory.html"))
    espera.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
    )