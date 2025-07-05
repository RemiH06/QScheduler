import os
from dotenv import load_dotenv
import datetime
from playwright.sync_api import sync_playwright

# Private info
load_dotenv(".secrets")
mE = os.getenv("me")
qocupaS = os.getenv("qocupas")

# Params
dayS = 14                 # A futuro
startTimE = "11:00"       # HH:MM
endTimE = "15:00"         # also HH:MM
cubiclE = "P-213"         # Q
topiC = "Hueco"           # Topic (strictly necessary)
attendeeS = "5"           # Attendees amount

def crumble(daysAway: int = dayS, start: str = startTimE, end: str = endTimE, q: str = cubiclE, name: str = topiC, a=attendeeS, email: str = mE, pw: str = qocupaS):
    RESERVATION_DATE = (datetime.datetime.today() + datetime.timedelta(days=daysAway)).strftime("%Y-%m-%d")
    START_TIME = start
    END_TIME = end
    CUBICLE = q
    TOPIC = name
    ATTENDEES = a
    EMAIL = email
    PASSWORD = pw

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        

        # 1. Página de porquería
        page.goto("https://iteso.smartway2book.com")
        page.wait_for_timeout(6000)


        # 2. Login
        page.wait_for_selector("input[name='loginfmt']", timeout=5000)
        page.fill("input[name='loginfmt']", EMAIL)
        page.wait_for_selector("input#idSIButton9[value='Siguiente']", timeout=10000)
        page.click("input#idSIButton9[value='Siguiente']")
        page.wait_for_timeout(2500)

        page.wait_for_selector("input[name='passwd']", timeout=5000)
        page.fill("input[name='passwd']", PASSWORD)
        page.wait_for_selector("input#idSIButton9[value='Iniciar sesión']", timeout=10000)
        page.click("input#idSIButton9[value='Iniciar sesión']")
        page.wait_for_timeout(2500)

        page.wait_for_selector("input#idBtn_Back[value='No']", timeout=5000)
        page.click("input#idBtn_Back[value='No']")
        page.wait_for_timeout(10000)


        # 3. Seleccionar fecha en el calendario mediante dos clicks
        # Primer click para asomarnos en el calendario
        date_click1 = datetime.datetime.today() + datetime.timedelta(days=daysAway - 7)
        calendar_date_value_1 = f"{date_click1.year}/{date_click1.month - 1}/{date_click1.day}"

        date_click2 = datetime.datetime.today() + datetime.timedelta(days=daysAway)
        calendar_date_value_2 = f"{date_click2.year}/{date_click2.month - 1}/{date_click2.day}"

        page.wait_for_timeout(10000)
        # Intentar encontrar el calendario
        if page.query_selector("#calendar"):
            # Si encuentra calendario, hacer clicks normales
            page.click(f"#calendar a[data-value='{calendar_date_value_1}']")
            page.wait_for_timeout(1000)

            page.click(f"#calendar a[data-value='{calendar_date_value_2}']")
            page.wait_for_timeout(2000)
        else:
            # Si no encuentra calendario, hacer click en botón "Ir a Classic Connect" después de iniciar sesión (otra vez xd)
            page.wait_for_selector("input[name='loginfmt']", timeout=5000)
            page.fill("input[name='loginfmt']", EMAIL)
            page.wait_for_selector("input#idSIButton9[value='Siguiente']", timeout=10000)
            page.click("input#idSIButton9[value='Siguiente']")
            page.wait_for_timeout(2500)

            page.wait_for_selector("input[name='passwd']", timeout=5000)
            page.fill("input[name='passwd']", PASSWORD)
            page.wait_for_selector("input#idSIButton9[value='Iniciar sesión']", timeout=10000)
            page.click("input#idSIButton9[value='Iniciar sesión']")
            page.wait_for_timeout(2500)

            page.wait_for_selector("input#idBtn_Back[value='No']", timeout=5000)
            page.click("input#idBtn_Back[value='No']")
            page.wait_for_timeout(10000)



            page.click("button:has-text('Ir a Classic Connect')")
            page.wait_for_timeout(3000)  # esperar que cargue o actualice

            # Reintentar clicks en calendario después del cambio
            page.wait_for_selector("#calendar", timeout=5000)
            page.click(f"#calendar a[data-value='{calendar_date_value_1}']")
            page.wait_for_timeout(1000)

            page.click(f"#calendar a[data-value='{calendar_date_value_2}']")
            page.wait_for_timeout(2000)


        # 4. Reservar un cubículo (usamos inyección de JS porque está dentro de un iframe)
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


        # 5. Hora inicio
        frame = page.frame_locator("iframe#reservation")
        start_time_input = frame.locator("input[data-role='timepicker'][data-bind*='startDate2']")
        start_time_input.wait_for()
        start_time_input.click()
        start_time_input.fill("")
        start_time_input.type(START_TIME, delay=100)
        page.wait_for_timeout(500)
        
        # 6. Hora fin
        end_time_input = frame.locator("input[data-role='timepicker'][data-bind*='endDate2']")
        end_time_input.wait_for()
        end_time_input.click()
        end_time_input.fill("")
        end_time_input.type(END_TIME, delay=100)
        page.wait_for_timeout(500)


        # 7. Le ponemos nombre
        frame = page.frame_locator("iframe#reservation")
        topic_input = frame.locator("input#ctl4")
        topic_input.click()
        topic_input.fill("")
        topic_input.type(TOPIC, delay=100)
        page.wait_for_timeout(500)


        # 8. En el input de ubicación se pone el nombre del cubículo, también se hace click para entrar en su selección
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
        page.wait_for_timeout(1000)


        # 9. Click en el cubículo para seleccionarlo
        page.evaluate(
        """(cubicleValue) => {
            const iframe = document.querySelector("iframe#reservation");
            if (iframe) {
                const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                if (innerDoc) {
                    const labelSpans = innerDoc.querySelectorAll("div.ll-location-name label span");
                    for (const span of labelSpans) {
                        if (span.textContent.trim() == `Cubículo ${cubicleValue}`) {
                            span.click();
                            break;
                        }
                    }
                }
            }
        }""",
        CUBICLE
        )
        page.wait_for_timeout(1000)


        # 10. Confirmamos cubículo
        page.evaluate(
            """
            () => {
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const correctoButton = innerDoc.querySelector("div.button.green-button[data-bind*='saveAndClose']");
                        if (correctoButton) {
                            correctoButton.click();
                        }
                    }
                }
            }
            """
        )
        page.wait_for_timeout(1500)


        # 11. Llenamos campo de cantidad de asistentes
        frame = page.frame_locator("iframe#reservation")
        attendees_input = frame.locator("input#ctl8")
        attendees_input.click()
        attendees_input.fill("")
        attendees_input.type(ATTENDEES, delay=100)
        page.wait_for_timeout(500)


        # 12. Guardamos
        page.evaluate("""
            () => {
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const saveButton = innerDoc.querySelector("#edit-reservation-save-button");
                        if (saveButton) {
                            saveButton.click();
                        }
                    }
                }
            }
        """)
        page.wait_for_timeout(5000)

        print("Reserva completada exitosamente.")
        #browser.close()

if __name__ == "__main__":
    crumble(daysAway=dayS, start=startTimE, end=endTimE, q=cubiclE, name=topiC, a=attendeeS, email=mE, pw=qocupaS)
