import os
from dotenv import load_dotenv
import datetime
from playwright.sync_api import sync_playwright
from scraper import crumble

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

crumble(daysAway=dayS, start=startTimE, end=endTimE, q=cubiclE, name=topiC, a=attendeeS, email=mE, pw=qocupaS)