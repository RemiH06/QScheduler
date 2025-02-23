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

        # 1. Acceder a la página principal y esperar
        page.goto("https://iteso.smartway2book.com")
        page.wait_for_timeout(3500)

        # 2. Pantalla de login:
        page.wait_for_selector("input[name='loginfmt']", timeout=5000)
        page.fill("input[name='loginfmt']", EMAIL)
        page.wait_for_selector("input#idSIButton9[value='Siguiente']", timeout=10000)
        page.click("input#idSIButton9[value='Siguiente']")
        page.wait_for_timeout(3500)

        page.wait_for_selector("input[name='passwd']", timeout=5000)
        page.fill("input[name='passwd']", PASSWORD)
        page.wait_for_selector("input#idSIButton9[value='Iniciar sesión']", timeout=10000)
        page.click("input#idSIButton9[value='Iniciar sesión']")
        page.wait_for_timeout(2500)

        page.wait_for_selector("input#idBtn_Back[value='No']", timeout=5000)
        page.click("input#idBtn_Back[value='No']")
        page.wait_for_timeout(12000)

        # 3. Hacer clic en "Reservar un Cubículo" justo antes de seleccionar la fecha.
        # Se inyecta una función que accede al contenido del iframe y busca el div con el texto deseado.
        page.evaluate("""
            () => {
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const elems = innerDoc.querySelectorAll("div.create-reservation-text");
                        for (const el of elems) {
                            if (el.textContent.trim() === "Reservar un Cubículo") {
                                el.click();
                                break;
                            }
                        }
                    }
                }
            }
        """)
        page.wait_for_timeout(2000)

        # 4. Seleccionar la fecha usando el calendario:
        # Convertir RESERVATION_DATE ("YYYY-MM-DD") al formato "YYYY/(mes-1)/D"
        reservation_date_obj = datetime.datetime.strptime(RESERVATION_DATE, "%Y-%m-%d")
        calendar_date_value = f"{reservation_date_obj.year}/{reservation_date_obj.month - 1}/{reservation_date_obj.day}"
        page.wait_for_selector("#calendar", timeout=5000)
        page.click(f"#calendar a[data-value='{calendar_date_value}']")
        page.wait_for_timeout(2000)
        
        # 5. Configurar el slider de "Comienzo" (hora de inicio)
        # Rango del slider: 510 a 1110 (minutos). Ejemplo: "11:00" = 660 minutos.
        desired_hour, desired_minute = map(int, START_TIME.split(":"))
        desired_minutes = desired_hour * 60 + desired_minute
        min_minutes = 510
        max_minutes = 1110
        fraction_time = (desired_minutes - min_minutes) / (max_minutes - min_minutes)
        track = page.wait_for_selector("#ctl2-slider .track", timeout=5000)
        track_box = track.bounding_box()
        target_x_time = track_box["x"] + fraction_time * track_box["width"]
        target_y_time = track_box["y"] + track_box["height"] / 2
        page.mouse.click(target_x_time, target_y_time)
        page.wait_for_timeout(1000)
        
        # 6. Configurar el slider de "Duración"
        # Rango del slider: 30 a 600 minutos.
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

        print("✅ Reserva completada exitosamente.")
        browser.close()

if __name__ == "__main__":
    reservar_cubiculo()
