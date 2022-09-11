#Example code for nominal/recovery pass dialog
#Not fully functioning yet

from time import sleep
from tkinter import Y
from tqdm import tqdm
from datetime import date, time, datetime
import csv

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()
print(today, ' ', current_time)
all_yes = ['yes',  'Y', 'y', 'YES', 'Yes']
sleep(1)



def writedata(n, r, day, time, ops):
    with open ("./Nominal_or_Recovery_Passes.csv", 'w') as logged:
        fieldnames = ["Was Nominal?", "Was Recovery?", "Date Logged", "Time Logged", "Operators Alerted"]
        csv_w = csv.writer(logged, delimiter=',')
        csv_w.writerow(fieldnames)
        row = [n, r, day, time, ops]
        csv_w.writerow(row)
    logged.close()

def nominal():
    nominal_answer = str(input("Was the pass nominal? Y/N"))
    if str(nominal_answer) in all_yes:
        pbar = tqdm(total=100)
        for i in tqdm(range(10)):
            sleep(0.2)                     #Loading bar created, this, taking 2 seconds to load.
            pbar.update(10)
        pbar.close()
        writedata('Y', 'N', today, current_time, 'N')
        sleep(0.4)
        print("Logged! Thank you for your response.")
        #store this response, indicating a nominal pass on the date, can be stored on an excel or CSV file
    else:
        sleep(0.4)
        recovery()

def recovery():
    #store this response, indicating a the pass was not nominal on the date 
    recovery_answer = input("Was it a recovery pass? Y/N")
    if str(recovery_answer) in all_yes:
        sleep(0.2)
        alert()
    else:
        writedata('N', 'N', today, current_time, 'N')
        sleep(0.4)
        print("Issue logged.")
    
def alert():
    alert_response = input("Alert other operators? Y/N")
    if str(alert_response) in all_yes:
        writedata('N', 'Y', today, current_time, 'Y')
        alert_all = input("Alert all operators?")
        if str(alert_all) in all_yes:
            #alert all operators function, emails all on-duty operatoes on a mailing list a scripted message detailing the problem
            print("Alerting all on-duty operators")
        else:
            operators_to_alert = input("Please provide the first name(s) or job title(s) of operators you would like to alert.")
            #alerts operators by matching the email address to the provided details
    else:
        operators_alerted = "N"
        writedata('N', 'Y', today, current_time, 'N')
        sleep(0.4)
        print("Issue logged for ,", today, ' ', current_time)



nominal()
