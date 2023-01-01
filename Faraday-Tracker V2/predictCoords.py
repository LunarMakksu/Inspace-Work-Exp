from datetime import datetime, date
import ephem # need to pip install or research this
import datetime
from TLEtool import calcComponants

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()
print(today, ' | ', current_time)

TLE_DIRECTORY = "Phoenix_TLEs_Only.txt"


#tle_rec = ephem.readtle(name, line1, line2)
#tle_rec.compute()

#print(tle_rec.sublong, tle_rec.sublat)