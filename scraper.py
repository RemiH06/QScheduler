import os
from dotenv import load_dotenv
import datetime
from playwright.sync_api import sync_playwright

# Private info
load_dotenv(".secrets")
mE = os.getenv("me")
qocupaS = os.getenv("qocupas")

# Params
dayS = 14
startTimE = "11:00"       # HH:MM
endTimE = "15:00"         # also HH:MM
cubiclE = "P-213"         # Q
topiC = "Hueco"           # Topic (strictly necessary)
attendeeS = "3"           # Attendees amount

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
        page.wait_for_timeout(3500)

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
        page.wait_for_timeout(12000)

        # 3. Reservar un cubículo (usamos inyección de JS porque está dentro de un iframe)
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
        page.wait_for_timeout(1500)

        # 4. Fecha y hora inicio "dd/mm/yyyy"
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
        page.wait_for_timeout(500)
        
        # 5. Fecha y hora fin "dd/mm/yyyy"
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
        page.wait_for_timeout(500)

        # 6. Le ponemos nombre
        page.evaluate(f"""
            () => {{
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {{
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {{
                        const topicInput = innerDoc.querySelector("input#ctl4");
                        if (topicInput) {{
                            topicInput.value = "{TOPIC}";
                            topicInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    }}
                }}
            }}
        """)
        page.wait_for_timeout(500)


        # 7. En el input de ubicación se pone el nombre del cubículo, también se hace click para entrar en su selección
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

        # 8: Click en el cubículo para seleccionarlo
        page.evaluate(
            """
            () => {
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {
                        const labelSpans = innerDoc.querySelectorAll("div.ll-location-name label span");
                        for (const span of labelSpans) {
                            if (span.textContent.trim() === "Cubículo P-213") {
                                span.click();
                                break;
                            }
                        }
                    }
                }
            }
            """
        )
        page.wait_for_timeout(1000)

        # 9. Confirmamos cubículo
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

        # 10. Llenamos campo de cantidad de asistentes
        page.evaluate(f"""
            () => {{
                const iframe = document.querySelector("iframe#reservation");
                if (iframe) {{
                    const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
                    if (innerDoc) {{
                        const attendeesInput = innerDoc.querySelector("input#ctl8");
                        if (attendeesInput) {{
                            attendeesInput.value = "{ATTENDEES}";
                            attendeesInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        }}
                    }}
                }}
            }}
        """)
        page.wait_for_timeout(500)

        # 11. Guardamos
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
        browser.close()

if __name__ == "__main__":
    crumble(daysAway=dayS, start=startTimE, end=endTimE, q=cubiclE, name=topiC, a=attendeeS, email=mE, pw=qocupaS)
