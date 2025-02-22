import time
import os
from dotenv import load_dotenv
import datetime
from playwright.sync_api import sync_playwright

# VARIABLES DE CONFIGURACIÓN
load_dotenv(".secrets")
EMAIL = os.getenv("me")
PASSWORD = os.getenv("qocupas")

# Parámetros de la reserva (modificables según necesidad)
RESERVATION_DATE = (datetime.datetime.today() + datetime.timedelta(days=14)).strftime("%Y-%m-%d")
START_TIME = "11:00"       # Hora de inicio en formato HH:MM
DURATION = "60"            # Duración en minutos
CUBICLE = "P-213"          # Cubículo a reservar
TOPIC = "reserva"          # Tema de la reserva
ATTENDEES = "3"            # Número de asistentes

def reservar_cubiculo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 1. Acceder a la página principal y esperar 2 segundos
        page.goto("https://iteso.smartway2book.com")
        page.wait_for_timeout(2000)

        # 2. Pantalla de login:
        # Rellenar el campo de correo y pulsar "Siguiente"
        page.wait_for_selector("input[name='loginfmt']", timeout=5000)
        page.fill("input[name='loginfmt']", EMAIL)
        page.wait_for_selector("input#idSIButton9[value='Siguiente']", timeout=10000)
        page.click("input#idSIButton9[value='Siguiente']")
        page.wait_for_timeout(2000)

        # Rellenar el campo de contraseña y pulsar "Iniciar sesión"
        page.wait_for_selector("input[name='passwd']", timeout=5000)
        page.fill("input[name='passwd']", PASSWORD)
        page.wait_for_selector("input#idSIButton9[value='Iniciar sesión']", timeout=10000)
        page.click("input#idSIButton9[value='Iniciar sesión']")
        page.wait_for_timeout(3000)

        # 3. Pantalla "¿Quieres mantener la sesión iniciada?" -> pulsar "No"
        page.wait_for_selector("input#idBtn_Back[value='No']", timeout=5000)
        page.click("input#idBtn_Back[value='No']")
        page.wait_for_timeout(3000)

        # 4. Pantalla de agendado:
        # Seleccionar la fecha
        page.wait_for_selector("input#datePicker", timeout=5000)
        page.fill("input#datePicker", RESERVATION_DATE)
        page.press("input#datePicker", "Enter")
        page.wait_for_timeout(2000)
        
        # Seleccionar el cubículo (asumiendo que es un <select>)
        page.wait_for_selector("select#cubicleDropdown", timeout=5000)
        page.select_option("select#cubicleDropdown", CUBICLE)
        page.wait_for_timeout(1000)
        
        # Ingresar la hora de inicio
        page.wait_for_selector("input#timePicker", timeout=5000)
        page.fill("input#timePicker", START_TIME)
        page.press("input#timePicker", "Enter")
        page.wait_for_timeout(1000)
        
        # Ingresar la duración
        page.wait_for_selector("input#duration", timeout=5000)
        page.fill("input#duration", DURATION)
        page.wait_for_timeout(1000)
        
        # Ingresar el tema
        page.wait_for_selector("input#topic", timeout=5000)
        page.fill("input#topic", TOPIC)
        page.wait_for_timeout(1000)
        
        # Ingresar el número de asistentes
        page.wait_for_selector("input#attendees", timeout=5000)
        page.fill("input#attendees", ATTENDEES)
        page.wait_for_timeout(1000)
        
        # Confirmar la reserva
        page.wait_for_selector("button:has-text('Confirmar Reserva')", timeout=5000)
        page.click("button:has-text('Confirmar Reserva')")
        page.wait_for_timeout(5000)

        print("✅ Reserva completada exitosamente.")
        browser.close()

if __name__ == "__main__":
    reservar_cubiculo()
