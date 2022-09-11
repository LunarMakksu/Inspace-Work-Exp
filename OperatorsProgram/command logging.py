#Example code demonstrating a function that logs commands used.

from time import sleep
from tqdm import tqdm
from datetime import date, time, datetime
import csv 

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()
print(today, ' ', current_time)
all_yes = ['yes',  'Y', 'y', 'YES', 'Yes']

print("Please provide all the commands you used one at a time when prompted.")
sleep(1.5)

def validate_date(time):
    try:
        datetime.strptime(time, '%H:%M')
    except ValueError:
            return False
    return True

reporting = True
n=1
with open (f'./COMMANDS-{today}.csv', 'w') as cmds:
    cmd_w = csv.writer(cmds, delimiter=',')
    fieldnames = ["Command", "Reasoning", "Execution time", "Date logged"]
    cmd_w.writerow(fieldnames)
    while reporting == True:
        cmd = input("Please write command and click enter.")
        sleep(0.4)
        reasoning = input("Please provide the thought-process and ovjective of this command/operator intervention, then click enter.")
        sleep(0.4)
        format_correct = False
        while format_correct == False:
            global cmd_time
            cmd_time = str(input("Please provide the time at which you executed this command. Please use the format: HH:MM, UTC & 24-hour time format, then click enter"))
            if validate_date(cmd_time) == True:
                format_correct = True
            else:
                print("Incorrect data format, time should be in the format HH:MM")
                format_correct = False
                sleep(0.4)       
        row = [cmd, reasoning, today, cmd_time]
        cmd_w.writerow(row)
        sleep(0.4)
        print("Command ", n," logged.")
        n += 1
        s_reporting = input("Is this the last command you would like to log? Y/N")
        if str(s_reporting) in all_yes:
            sleep(0.5)
            print("Command logging stopped")
            reporting = False
            cmds.close()
        else:
            reporting = True


