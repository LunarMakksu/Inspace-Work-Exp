import numpy as np
from beyond.io.tle import Tle
from beyond.frames import create_station
from beyond.dates import Date, timedelta

#tle is two-line element
tle = Tle("""FARADAY-PHOENIX
1 99687A 21001    21181.87027012  .00009242  00000-0  55903-3 0 00008
2 99687 097.5055 303.2998 0010251 146.9415 299.9196 15.10675219000018""")

station = create_station('Svalbard', (78.23079736713065, 15.385103375729368, 400)) #(lat, long, elev)

counter = 0

for orb in station.visibility(tle.orbit(), start=Date.now(), stop=timedelta(days=2), step=timedelta(minutes=2), events=True):

    # As all angles are given in radians,
    # there is some conversion to do
    azim = -np.degrees(orb.theta) % 360
    elev = np.degrees(orb.phi)
    r = orb.r / 1000.

    print("{event:10} {tle.name}  {date:%Y-%m-%dT%H:%M:%S.%f} {azim:7.2f} {elev:7.2f} {r:10.2f}".format(
        date=orb.date, r=r, azim=azim, elev=elev,
        tle=tle, event=orb.event if orb.event is not None else ""
    ))

    # Stop at the end of the first pass
    if orb.event and orb.event.info == "LOS":
        counter += 1
        if counter >= 5:
            break
