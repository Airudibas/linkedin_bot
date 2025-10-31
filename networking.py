import os
import os
import re
import time
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import ElementClickInterceptedException


load_dotenv()


def _has_mutual_text(text: str) -> bool:
    if not text:
        return False
    text = text.lower()
    return bool(re.search(r"(mutual|shared|common|connection)", text))


def linkedin_connect_by_title(title: str, max_requests: int = 5, headless: bool = False, dry_run: bool = False, wait_seconds: int = 10):
    """Simple search: looks for `title`, filters by people and sends connection requests to those with mutual connections.

    - dry_run=True only lists candidates without clicking.
    - Uses LINKEDIN_USER / LINKEDIN_PASS from env for automatic login (optional).
    """

    user = os.getenv('LINKEDIN_USER')
    pwd = os.getenv('LINKEDIN_PASS')

    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument('--headless=new')
    opts.add_argument('--start-maximized')

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=opts)
    wait = WebDriverWait(driver, wait_seconds)

    try:
        driver.get('https://www.linkedin.com/login')

        # Login (automático si hay env vars, si no esperar login manual)
        if user and pwd:
            try:
                u = wait.until(
                    EC.presence_of_element_located((By.ID, 'username')))
                p = driver.find_element(By.ID, 'password')
                u.clear()
                u.send_keys(user)
                p.clear()
                p.send_keys(pwd)
                p.send_keys(Keys.RETURN)
                wait.until(EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "input[placeholder='Buscar'], input[placeholder='Search']")))
                print('Automatic login completed')
            except Exception:
                input('Please login manually and press ENTER to continue...')
        else:
            input('Please login manually and press ENTER to continue...')

        # Buscar término
        search = wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "input[placeholder='Buscar'], input[placeholder='Search']")))
        search.clear()
        search.send_keys(title)
        search.send_keys(Keys.RETURN)
        time.sleep(1.5)

        # Click en filtro Personas si está
        try:
            btn = driver.find_element(
                By.XPATH, "//button[contains(., 'Personas') or contains(., 'People')] | //a[contains(., 'Personas') or contains(., 'People')]")
            try:
                btn.click()
                time.sleep(1)
            except Exception:
                pass
        except Exception:
            pass

        sent = 0

        # Recolectar enlaces de perfil y procesarlos
        page = 0
        seen = set()
        while sent < max_requests and page < 25:
            page += 1
            links = driver.find_elements(
                By.XPATH, "//a[contains(@href, '/in/')]")
            if not links:
                break

            for a in links:
                if sent >= max_requests:
                    break
                href = a.get_attribute('href') or ''
                if not href or href in seen:
                    continue
                seen.add(href)

                # tomar contenedor cercano
                try:
                    container = a.find_element(By.XPATH, './ancestor::li[1]')
                except Exception:
                    try:
                        container = a.find_element(
                            By.XPATH, './ancestor::article[1]')
                    except Exception:
                        try:
                            container = a.find_element(
                                By.XPATH, './ancestor::div[1]')
                        except Exception:
                            container = None

                if not container:
                    continue

                snippet = container.text or ''
                if not _has_mutual_text(snippet):
                    continue

                print('Candidate:', href)
                sent += 1
                if dry_run:
                    continue

                # buscar botón Conectar
                connect = None
                try:
                    connect = container.find_element(
                        By.XPATH, ".//button[.//span[contains(., 'Conectar') or contains(., 'Connect')]]")
                except Exception:
                    try:
                        connect = container.find_element(
                            By.XPATH, ".//button[contains(., 'Conectar') or contains(., 'Connect')]")
                    except Exception:
                        connect = None

                if not connect:
                    continue

                try:
                    driver.execute_script(
                        'arguments[0].scrollIntoView({block: "center"});', connect)
                    time.sleep(0.3)
                    connect.click()
                    time.sleep(0.8)

                    # intentar confirmar en modal
                    try:
                        send = None
                        try:
                            send = wait.until(EC.element_to_be_clickable(
                                (By.XPATH, "//button[contains(., 'Enviar ahora') or contains(., 'Send') or contains(., 'Enviar')]")))
                        except Exception:
                            try:
                                modal = driver.find_element(
                                    By.XPATH, "//div[contains(@role,'dialog')]")
                                send = modal.find_element(
                                    By.XPATH, ".//button[contains(., 'Enviar ahora') or contains(., 'Send') or contains(., 'Enviar')]")
                            except Exception:
                                send = None

                        if send:
                            try:
                                send.click()
                                print('Solicitud enviada a', href)
                            except Exception:
                                print(
                                    'No se pudo clicar enviar (quizá ya enviada) para', href)
                        else:
                            print('Conexión solicitada (sin confirmación) a', href)
                    except Exception as e:
                        print('Error modal:', e)

                    sent += 1
                    time.sleep(1)
                except ElementClickInterceptedException:
                    print('Click intercepted for', href)
                except Exception as e:
                    print('Error trying to connect to', href, e)

            # intentar siguiente página
            try:
                nxt = driver.find_element(
                    By.XPATH, "//button[.//span[contains(., 'Siguiente') or contains(., 'Next')]] | //a[contains(., 'Siguiente') or contains(., 'Next')]")
                try:
                    nxt.click()
                    time.sleep(1.5)
                except Exception:
                    break
            except Exception:
                break

        print('Finished. Connection requests sent:', sent)

    finally:
        driver.quit()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Script to connect with people on LinkedIn who have mutual connections')
    parser.add_argument('--title', type=str, default='CTO',
                        help='Title or term to search for')
    parser.add_argument('--max-requests', type=int, default=3,
                        help='Maximum number of connection requests to send')
    parser.add_argument('--dry-run', action='store_true',
                        help='Only list candidates without sending requests')
    parser.add_argument('--headless', action='store_true',
                        help='Run in headless mode (no GUI)')

    args = parser.parse_args()

    linkedin_connect_by_title(
        title=args.title,
        max_requests=args.max_requests,
        dry_run=args.dry_run,
        headless=args.headless
    )
