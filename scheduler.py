import win32com.client
import traceback
import datetime

outlook = win32com.client.Dispatch("Outlook.Application")

def start(times):
    time_start = {
        0: times[0],
        1: times[1],
        2: times[2],
        3: times[3],
        4: times[4],
        5: times[5],
        6: times[6]
    }
    today = datetime.datetime.today().weekday()
    fourteen = datetime.datetime.today() + datetime.timedelta(days=14)
    sched = fourteen.strftime(f"%Y-%m-%d {time_start.get(today, '')}")
    return sched

def duration(extns):
    timeEnd = {
        0: extns[0],
        1: extns[1],
        2: extns[2],
        3: extns[3],
        4: extns[4],
        5: extns[5],
        6: extns[6]
    }

    return timeEnd

def sendMeeting(mail, qbic, times, extns):   
    startTime = start(times)
    duradura = duration(extns)
    where = "Cubículo P-204"
    queEs = "Hueco" 
    try:
        if not startTime:
            print("No hay hora de inicio definida para este día.")
            return

        appt = outlook.CreateItem(1) 
        appt.Start = startTime
        appt.Subject = queEs
        appt.Duration = duradura
        appt.Location = where
        appt.MeetingStatus = 1

        appt.Recipients.Add(mail)
        appt.Recipients.Add(qbic)
        
        appt.Save() 
        appt.Send()
        print(appt.Subject)
        print(appt.Start)
        print(appt.Duration)
        print("Reunión programada y enviada.")
    
    except Exception as e:
        print("Error al crear la reunión:", e)
        traceback.print_exc()