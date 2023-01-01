import requests
import numpy as np
from beyond.dates import Date, timedelta
from beyond.io.tle import Tle
from beyond.frames import create_station
from beyond.config import config

celestrak_fp =  "https://celestrak.org/NORAD/elements/gp.php?CATNR=48924"

data = requests.get(celestrak_fp)
data = data.content.decode("utf-8")
rows = data.splitlines()

tles = {}

        
# In[4]:


tles['fp 15']


# In[5]:


tle = Tle(tles['fp 15'])


# In[6]:


station = create_station('Norwich', (52.5, 1.2, 0)) # obfuscated slightly


# In[7]:


def predictions(tle, station, hours):
    azims, elevs = [], []

    orbit = tle.orbit()

    start = None
    end = None
    max_alt = None

    for orb in station.visibility(orbit, start=Date.now(), stop=timedelta(hours=hours), step=timedelta(seconds=30), events=True):
        elev = np.degrees(orb.phi)
        # Radians are counterclockwise and azimuth is clockwise
        azim = np.degrees(-orb.theta) % 360

        # Archive for plotting
        azims.append(azim)
        # Matplotlib actually force 0 to be at the center of the polar plot,
        # so we trick it by inverting the values
        elevs.append(90 - elev)

        #r = orb.r / 1000.

        if orb.event is not None:
            if orb.event.info =='AOS': # aquisition of signal
                start = orb.date
            if orb.event.info  == 'MAX': 
                max_alt = elev

            if orb.event.info  == 'LOS': # loss of signal

                end = orb.date
                if max_alt and max_alt >= 10:
                    print("Pass: %s %s %s" % (start, max_alt, end))
                    start = None
                    end = None
                    max_alt = None

    


# In[8]:


predictions(Tle(tles['fp 19']), station, 24)


# In[9]:


predictions(Tle(tles['fp 18']), station, 24)


# In[10]:


predictions(Tle(tles['fp 15']), station, 24)


# In[ ]:

