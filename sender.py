import os
from dotenv import load_dotenv
import scheduler
import datetime

load_dotenv('.secrets')

mail = os.getenv('me')
qbic = os.getenv('qbic')

times = ["", "14:00", "", "13:30", "", "", ""]
extns = [1, 240, 1, 150, 1, 1, 1]
# lunes en [0], domingo en [6]

today = datetime.datetime.today().weekday()

if today == 1 or today == 3:
        scheduler.sendMeeting(mail, qbic, times, extns)