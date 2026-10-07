from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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


def test_agregar_producto_al_carrito(driver):
    """Agrega el primer producto y verifica su presencia en el carrito."""
    iniciar_sesion(driver)
    espera = WebDriverWait(driver, 15)

    primer_producto = driver.find_elements(
        By.CLASS_NAME, "inventory_item"
    )[0]
    nombre = primer_producto.find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text

    # Verificamos que el carrito comience vacío.
    assert not driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")

    # Agregamos el primer producto.
    primer_producto.find_element(By.TAG_NAME, "button").click()

    # Esperamos que el contador indique un producto.
    espera.until(
        EC.text_to_be_present_in_element(
            (By.CLASS_NAME, "shopping_cart_badge"), "1"
        )
    )
    assert driver.find_element(
        By.CLASS_NAME, "shopping_cart_badge"
    ).text == "1"

    # Abrimos el carrito y esperamos que aparezca el producto.
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    espera.until(EC.url_contains("/cart.html"))
    espera.until(
        EC.visibility_of_element_located((By.CLASS_NAME, "cart_item"))
    )

    # Validamos el nombre y la cantidad del producto agregado.
    productos_carrito = driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(productos_carrito) == 1
    assert productos_carrito[0].find_element(
        By.CLASS_NAME, "inventory_item_name"
    ).text == nombre
    assert productos_carrito[0].find_element(
        By.CLASS_NAME, "cart_quantity"
    ).text == "1"