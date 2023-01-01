'''
                    TLEtool.py
                    Max Bird 31/12/22
                    Specific to Phoenix TLE set Inspace provided
'''        
from datetime import datetime, date
import string
                                                    # NEEDS DEBUGGING

orig_TLE_filename = "Phoenix_TLEs.txt"
new_TLE_filename = "Phoenix_TLEs_Only.txt"
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()
print(today, ' | ', current_time)


with open (orig_TLE_filename) as fp:
    lines = fp.readlines()
    #need lines 1753-1755
    n = 0
    min = 1752
    with open (f"./{new_TLE_filename}", 'w') as nf:
        while n<3:
            nf.write(lines[min])  # EXTRACTS LATEST TLE SET FROM FILE
            min += 1
            n += 1


def calcEpoch(epoch):
        
    year_idx = int(epoch[0:2])

    if year_idx > int((str(today.year).lstrip('2').lstrip('0'))):
        year = int(1900 + year_idx)
    else:
        year = int(2000 + year_idx)

    epochSplit = str(epoch[2:]).split('.')

    day = int(epochSplit[0])

    month = int(round((day)/30))

    time0 = epochSplit[1]

    power = int(len(str(time0)))
    t = (float(time0)*10**-power)*24

    time_hour = str(t)[0:2]

    time_minute = round((float(t)-float(time_hour))*60)

    time = (f"{time_hour}:{time_minute}")

    date_UK = (time, day, month, year)

    return time, day, month, year, date_UK


class calcComponants:
        with open (new_TLE_filename) as f:
            lines = f.readlines()

        line0 = lines[0].strip()#name
        line1 = lines[1].split()
        line2 = lines[2].split()
        
        # LINE 0

        Satellite_name = str(line0)

        # LINE 1

        catalogNum = line1[1][0:4]
        classification = str(line1[1][5]) # spacecraft classification 
        if classification == 'U':
            classification = "unclassified"
        if classification == 'C':
            classification == "classified"
        if classification == 'S':
            classification == "secret"
        int_desig = int(line1[2][0:2]) # (last two digits of launch year)
        if int_desig > int((str(today.year).lstrip('2').lstrip('0'))):
            launch_year = int(1900 + int_desig)
        else:
            launch_year = int(2000 + int_desig)
        launch_num = int((line1[2][2:5])) # luanch number of year
        if launch_num > 100:
            launch_num = launch_num.lstrip('0')
        if len(line1[2]) < 6:       # no launch part
            launch_part = "None"
        else: 
            launch_part = line1[2][5:] #might be more than one unit
            if len(launch_part) == 1:
                launch_part_num = (string.ascii_uppercase.index(launch_part) + 1) #gives the index of the launch piece in terms of its position in the alphabet
        epoch = line1[3]
        epoch_time, epoch_day, epoch_month, epoch_year, epoch_date_UK = calcEpoch(epoch)
        ballistic_coeff = line1[3][15:24] # first derivative of mean motion
        ballistic_coeff_second_deriv = line1[4]
        radiation_press_coef = line1[5]
        ephemeris_type = line1[6]
        element_set_num = line1[7][0:-1]
        checkSum = line1[7][-1] # Not sure what this is

        # LINE 2

        inclination = line2[2]
        right_ascension = line2[3]
        eccentricity = line2[4]
        arg_of_perigee = line2[5]
        mean_anomaly = line2[6]
        mean_motion = line2[7][0:-6] # revs per day
        rev_num = line2[7][-6:]# at epoch
        #checkSum2 = checkSum

# PUT YOUR PRINT COMMANDS HERE
