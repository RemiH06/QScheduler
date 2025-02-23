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
TOPIC = "reserva"          # Tema de la reserva (se usará "Hueco" para este campo)
ATTENDEES = "3"            # Número de asistentes

END_TIME = "15:00"

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

        # 3. Hacer clic en "Reservar un Cubículo" (dentro del iframe) mediante inyección
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

        # 4. Ajustar la fecha y hora de comienzo dentro del iframe
        # Convertir RESERVATION_DATE a formato "dd/mm/yyyy"
        reservation_date_obj = datetime.datetime.strptime(RESERVATION_DATE, "%Y-%m-%d")
        formatted_date = reservation_date_obj.strftime("%d/%m/%Y")
        page.evaluate(f"""
            () => {{
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {{
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {{
                        // Ajustar el datepicker
                        const dateInput = innerDoc.querySelector("input[data-role='datepicker']");
                        if (dateInput) {{
                            dateInput.value = "{formatted_date}";
                            dateInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                        // Ajustar el timepicker
                        const timeInput = innerDoc.querySelector("input[data-role='timepicker']");
                        if (timeInput) {{
                            timeInput.value = "{START_TIME}";
                            timeInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    }}
                }}
            }}
        """)
        page.wait_for_timeout(2000)
        
        # 6. Inyectar los valores para el campo de fin (endDate2) dentro del iframe:
        # Se establece la misma fecha que la de inicio y la hora final (START_TIME + 4 horas)
        page.evaluate(f"""
            () => {{
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {{
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {{
                        // Campo de fecha final
                        const endDateInput = innerDoc.querySelector("input[data-role='datepicker'][data-bind*='value: endDate2']");
                        if (endDateInput) {{
                            endDateInput.value = "{formatted_date}";
                            endDateInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                        // Campo de hora final
                        const endTimeInput = innerDoc.querySelector("input[data-role='timepicker'][data-bind*='value: endDate2']");
                        if (endTimeInput) {{
                            endTimeInput.value = "{END_TIME}";
                            endTimeInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    }}
                }}
            }}
        """)
        page.wait_for_timeout(2000)

        # 7. Rellenar el campo "Tema" con el texto "Hueco" dentro del iframe
        page.evaluate("""
            () => {
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const topicInput = innerDoc.querySelector("input#ctl4");
                        if (topicInput) {
                            topicInput.value = "Hueco";
                            topicInput.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    }
                }
            }
        """)
        page.wait_for_timeout(1000)

        # 6. Inyectar el valor para el cubículo "Cubículo P-213" dentro del iframe:
        # Se llena el input de filtro y se simula clic en el botón de búsqueda.
        page.evaluate(
        """(cubicleValue) => {
            const iframe = document.querySelector("iframe#reservation");
            if (iframe) {
                const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                if (innerDoc) {
                    // Buscar el input del filtro de cubículo (por su placeholder)
                    const cubicleInput = innerDoc.querySelector("input.sw2-list-item-search-control[placeholder='Filtro de Cubículo']");
                    if (cubicleInput) {
                        cubicleInput.value = `Cubículo ${cubicleValue}`;
                        cubicleInput.dispatchEvent(new Event('input', { bubbles: true }));
                    }
                    // Simular clic en el enlace de búsqueda (se asume que es el único <a> dentro de la tabla)
                    const searchLink = innerDoc.querySelector("table.sw2-list-item-search-table a");
                    if (searchLink) {
                        searchLink.click();
                    }
                }
            }
        }""",
        CUBICLE
        )
        page.wait_for_timeout(2000)

        # 8. Inyección: Dentro del iframe, marcar la checkbox correspondiente (usando click)
        page.evaluate(
            """() => {
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const checkbox = innerDoc.querySelector("input[type='checkbox'][id='4e56b554-5c45-4f3a-9929-48c5f293542a']");
                        if (checkbox) {
                            checkbox.click();
                        }
                    }
                }
            }"""
        )
        page.wait_for_timeout(1000)

        # 9. Inyección: Dentro del iframe, presionar el botón que dice "Correcto"
        page.evaluate(
            """() => {
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const buttons = innerDoc.querySelectorAll("button");
                        for (const btn of buttons) {
                            if (btn.textContent.trim() === "Correcto") {
                                btn.click();
                                break;
                            }
                        }
                    }
                }
            }"""
        )
        page.wait_for_timeout(2000)
        
        # 7. Confirmar la reserva
        page.wait_for_selector("button:has-text('Confirmar Reserva')", timeout=5000)
        page.click("button:has-text('Confirmar Reserva')")
        page.wait_for_timeout(5000)

        print("✅ Reserva completada exitosamente.")
        browser.close()

if __name__ == "__main__":
    reservar_cubiculo()
