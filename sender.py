import os
from dotenv import load_dotenv
import scheduler
import datetime

load_dotenv('.secrets')

mail = os.getenv('me')
qbic = os.getenv('qbic')

times = ["", "14:00", "", "13:30", "", "", ""]
extns = [1, 4, 1, 3, 1, 1, 1]
# lunes en [0], domingo en [6]

today = datetime.datetime.today().weekday()

if today == 2 or today == 4:
        scheduler.sendMeeting(mail, qbic, times, extns)