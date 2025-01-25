import os
import time
import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser

load_dotenv(".secrets")
mail = os.getenv("me")
password = os.getenv("qocupas")

def reservar_cubiculo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # **Abrir la página de login**
            page.goto("https://iteso.smartway2book.com/scheduler.aspx?useClassic=true")
            
            # **Ingresar el correo**
            page.fill("#i0116", mail)
            page.press("#i0116", "Enter")
            time.sleep(3)
            
            # **Ingresar la contraseña**
            page.fill("#i0118", password)
            page.press("#i0118", "Enter")
            time.sleep(5)
            print("✅ Inicio de sesión exitoso.")
            
            # **Seleccionar la fecha (14 días en el futuro)**
            today = datetime.datetime.today()
            target_date = today + datetime.timedelta(days=14)
            date_str = target_date.strftime("%Y-%m-%d")  # Formato YYYY-MM-DD
            
            page.fill("#datePicker", date_str)
            page.press("#datePicker", "Enter")
            time.sleep(3)
            print(f"📅 Fecha seleccionada: {date_str}")
            
            # **Seleccionar el cubículo**
            page.select_option("#cubicleDropdown", "P-215")  # Ajusta ID si es necesario
            time.sleep(2)
            print("🏢 Cubículo seleccionado: P-215")
            
            # **Seleccionar la hora**
            times = ["", "11:00", "", "14:00", "15:00", "", ""]  # Horarios por día
            today_idx = today.weekday()
            start_time = times[today_idx] if today_idx < len(times) else "15:00"
            
            page.fill("#timePicker", start_time)
            page.press("#timePicker", "Enter")
            time.sleep(3)
            print(f"⏰ Hora seleccionada: {start_time}")
            
            # **Confirmar la reserva**
            page.click("#submitReservation")  # Ajusta ID si es necesario
            time.sleep(5)
            print("🎉 ¡Reserva confirmada!")
            
        except Exception as e:
            print("❌ Error:", e)
        
        finally:
            time.sleep(10)  # Para ver qué sucede antes de cerrar
            browser.close()

# Ejecutar la función de reserva
if __name__ == "__main__":
    reservar_cubiculo()
