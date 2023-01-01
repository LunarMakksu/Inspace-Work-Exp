from datetime import datetime, date, time
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()

'''
text = "183y4184.1456346-21215"

texts = text.strip().split('.')


time = 54.38063
split = str(time).split('.')
print(split[1])
'''


with open ("Phoenix_TLEs_Only.txt", 'r') as f:
    lines = f.readlines()

line0 = lines[0].strip()#name
line1 = lines[1].split()
line2 = lines[2].split()


epoch = line1[3]

year_idx = int(epoch[0:2])
print(year_idx)

if year_idx > int((str(today.year).lstrip('2').lstrip('0'))):
    year = int(1900 + year_idx)
else:
    year = int(2000 + year_idx)
print(year)

epochSplit = str(epoch[2:]).split('.')

day = int(epochSplit[0])
print(day)
month = int(round((day)/30))
print(month)

time = epochSplit[1]
print(time)
power = int(len(str(time)))
t = (float(time)*10**-power)*24
print(t)
time_hour = str(t)[0:2]
print(time_hour)
time_minute = round((float(t)-float(time_hour))*60)
print(time_minute)
time = (f"{time_hour}:{time_minute}")

date_UK = (time, day, month, year)
print(date_UK)
#date_v2_GB = (day+1+", "+month+", "+year)





    

'''
time = 82391472
power = int(len(str(time)))
t = float(time*10**-power) * 24
print(t)
time_hour = str(t)[0:2]
print(time_hour)
time_minute = round((float(t)-float(time_hour))*60)
print(time_minute)
time = "{time_hour}:{time_minute}"'''

'''
time = 12.369835646
min = str(time)[2:]
print(min)'''
#print(texts[0])
#print(texts[1][0:5])
#print(str(today.year).lstrip('2').lstrip('0'))
#print(texts[1][0:-2])
#print(texts[1][-5:])
