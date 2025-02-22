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
DURATION = "60"            # Duración en minutos (por ejemplo, 60 para 1 hora)
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
        page.wait_for_timeout(3500)

        # 2. Pantalla de login:
        # Rellenar el campo de correo y pulsar "Siguiente"
        page.wait_for_selector("input[name='loginfmt']", timeout=5000)
        page.fill("input[name='loginfmt']", EMAIL)
        page.wait_for_selector("input#idSIButton9[value='Siguiente']", timeout=10000)
        page.click("input#idSIButton9[value='Siguiente']")
        page.wait_for_timeout(3500)

        # Rellenar el campo de contraseña y pulsar "Iniciar sesión"
        page.wait_for_selector("input[name='passwd']", timeout=5000)
        page.fill("input[name='passwd']", PASSWORD)
        page.wait_for_selector("input#idSIButton9[value='Iniciar sesión']", timeout=10000)
        page.click("input#idSIButton9[value='Iniciar sesión']")
        page.wait_for_timeout(3500)

        # 3. Pantalla "¿Quieres mantener la sesión iniciada?" -> pulsar "No"
        page.wait_for_selector("input#idBtn_Back[value='No']", timeout=5000)
        page.click("input#idBtn_Back[value='No']")
        page.wait_for_timeout(8000)



        # 4. Pantalla de agendado:
        # Seleccionar la fecha usando el calendario:
        # Convertir RESERVATION_DATE ("YYYY-MM-DD") al formato que usa el atributo data-value
        # (el mes se indexa desde 0, por lo que se resta 1 al mes)
        reservation_date_obj = datetime.datetime.strptime(RESERVATION_DATE, "%Y-%m-%d")
        calendar_date_value = f"{reservation_date_obj.year}/{reservation_date_obj.month - 1}/{reservation_date_obj.day}"
        page.wait_for_selector("#calendar", timeout=5000)
        page.click(f"#calendar a[data-value='{calendar_date_value}']")
        page.wait_for_timeout(2000)
        
        # Seleccionar el cubículo (en este caso, se asume que ya se muestra en la pantalla de reserva)
        # Si el cubículo se selecciona mediante otro método (por ejemplo, haciendo clic en un botón o en un slider), ajustar aquí.
        # (En este ejemplo se omite la acción de selección si no se usa un <select>.)
        
        # Configurar el slider de "Comienzo" (hora de inicio)
        # Rango del slider: 510 a 1110 (minutos). Ejemplo: "11:00" = 11*60 = 660 minutos.
        desired_hour, desired_minute = map(int, START_TIME.split(":"))
        desired_minutes = desired_hour * 60 + desired_minute
        min_minutes = 510
        max_minutes = 1110
        fraction_time = (desired_minutes - min_minutes) / (max_minutes - min_minutes)
        track_time = page.wait_for_selector("#ctl2-slider .track", timeout=5000)
        track_time_box = track_time.bounding_box()
        target_x_time = track_time_box["x"] + fraction_time * track_time_box["width"]
        target_y_time = track_time_box["y"] + track_time_box["height"] / 2
        page.mouse.click(target_x_time, target_y_time)
        page.wait_for_timeout(1000)
        
        # Configurar el slider de "Duración"
        # Rango del slider: 30 a 600 minutos. Se desea DURATION minutos.
        desired_duration = int(DURATION)
        min_duration = 30
        max_duration = 600
        fraction_duration = (desired_duration - min_duration) / (max_duration - min_duration)
        track_duration = page.wait_for_selector("#ctl3-slider .track", timeout=5000)
        track_duration_box = track_duration.bounding_box()
        target_x_duration = track_duration_box["x"] + fraction_duration * track_duration_box["width"]
        target_y_duration = track_duration_box["y"] + track_duration_box["height"] / 2
        page.mouse.click(target_x_duration, target_y_duration)
        page.wait_for_timeout(1000)

        # Primero, hacer clic en "Reservar un Cubículo"
        page.wait_for_selector("a#home-page-create-res", timeout=5000)
        page.click("a#home-page-create-res")
        page.wait_for_timeout(2000)
        
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
