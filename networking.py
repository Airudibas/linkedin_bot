from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def linkedin_connect_by_title(title, min_common=5):
    driver = webdriver.Chrome()
    driver.get("https://www.linkedin.com/login")
    # Espera y login manual aquí (por seguridad)
    input("Haz login en LinkedIn y pulsa ENTER aquí...")
    
    # Buscar el título en la barra de búsqueda
    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Buscar']")
    search_box.send_keys(title)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # Filtrar solo personas
    people_tab = driver.find_element(By.XPATH, "//button[contains(., 'Personas')]")
    people_tab.click()
    time.sleep(2)

    persons = driver.find_elements(By.CSS_SELECTOR, ".reusable-search__result-container")
    for person in persons:
        try:
            # Haz click en el perfil para abrir detalles
            profile_link = person.find_element(By.TAG_NAME, 'a')
            profile_link.click()
            time.sleep(2)
            # Cambiar a la nueva pestaña
            driver.switch_to.window(driver.window_handles[-1])
            # Buscar el recuadro de personas en común
            mutuals = driver.find_elements(By.XPATH, "//span[contains(text(),'contactos en común')]")
            for m in mutuals:
                text = m.text
                num = int(''.join(filter(str.isdigit, text)))
                if num >= min_common:
                    # Agregar como amigo (conectar)
                    connect_btn = driver.find_element(By.XPATH, "//button[contains(., 'Conectar')]")
                    connect_btn.click()
                    time.sleep(1)
                    send_btn = driver.find_element(By.XPATH, "//button[contains(., 'Enviar')]")
                    send_btn.click()
                    print(f"Solicitud enviada a {profile_link.text}")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except Exception as e:
            print("Error:", e)
            driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

    driver.quit()

# Ejemplo de uso
linkedin_connect_by_title("CTO", 5)
