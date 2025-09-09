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
dayS = 7                  # A futuro
topiC = "Hueco"           # Topic (strictly necessary)

startTimE   = ["20:00", "13:00", "16:00", "", "13:00", "", ""]
endTimE     = ["21:00", "16:00", "20:00", "", "16:00", "", ""]
cubiclE     = ["P-212", "P-113", "P-113", "", "P-113", "", ""]
attendeeS     = ["7", "3", "3", "", "3", "", ""]
# lunes en [0], domingo en [6]

today = datetime.datetime.today().weekday()

#if today >= 1 and today <= 3:
#        crumble(daysAway=dayS, start=startTimE[today], end=endTimE[today], q=cubiclE, name=topiC, a=attendeeS, email=mE, pw=qocupaS)

for day_offset in range(7):
    target_day = (today + day_offset) % 7
    daysAway = dayS + day_offset
    
    if startTimE[target_day] and endTimE[target_day]:
        crumble(daysAway=daysAway, 
                start=startTimE[target_day], 
                end=endTimE[target_day], 
                q=cubiclE[target_day], 
                name=topiC, 
                a=attendeeS[target_day], 
                email=mE, 
                pw=qocupaS)