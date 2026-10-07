from selenium.webdriver.common.by import By
from utils.helpers import iniciar_sesion


def test_login_exitoso(driver):
    """Verifica que el usuario pueda ingresar al catálogo."""
    iniciar_sesion(driver)

    # Validamos la dirección y los títulos después del login.
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"
    assert driver.find_element(By.CLASS_NAME, "app_logo").text == "Swag Labs"

    

def test_catalogo_productos(driver):
    """Verifica los productos y los controles del catálogo."""
    iniciar_sesion(driver)

    assert driver.title == "Swag Labs"
    assert driver.find_element(By.CLASS_NAME, "title").text == "Products"

    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0, "El catálogo no tiene productos"
    assert productos[0].is_displayed()

    # Validamos que el menú y el filtro estén visibles.
    assert driver.find_element(By.ID, "react-burger-menu-btn").is_displayed()
    assert driver.find_element(
        By.CLASS_NAME, "product_sort_container"
    ).is_displayed()

    # Mostramos el nombre y el precio del primer producto.
    primer_producto = productos[0]
    nombre = primer_producto.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text
    precio = primer_producto.find_element(
        By.CLASS_NAME, "inventory_item_price"
    ).text

    assert nombre, "El producto no tiene nombre"
    assert precio, "El producto no tiene precio"
    print(f"Primer producto: {nombre} | Precio: {precio}")