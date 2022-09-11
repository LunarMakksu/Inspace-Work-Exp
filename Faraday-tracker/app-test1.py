import turtle
import urllib.request
import time
import webbrowser
import csv
from PIL import Image
#import geocoder


# Setup the world map in turtle module
screen = turtle.Screen()
screen.setup(1280, 720)
screen.setworldcoordinates(-180, -90, 180, 90)

image = Image.open("satt.gif")
new = image.resize((32,32))
new.save("satt2.gif")


# load the world map image
screen.bgpic("map.png")
screen.register_shape("satt2.gif")
sat = turtle.Turtle()
sat.shape("satt2.gif")
sat.setheading(45)
#sat.penup() -  draws line to show orbit when down, keep this suppressed to show orbit

while True:
    # load the current status of the "sat. in real-time
    with open ("./gps_data_m_0.csv", 'r') as pos:
        csv_r=csv.reader(pos)
        next(csv_r)
        for line in csv_r:
                
            # Extract the ISS location
            #location = result["iss_position"]
            lat = line[0]
            lon = line[1]

        # Ouput lon and lat to the terminal
        lat = float(lat)
        lon = float(lon)
        print("\nLatitude: " + str(lat))
        print("\nLongitude: " + str(lon))

        # Update the ISS location on the map
    sat.goto(lon, lat)

        # Refresh each 3 seconds
    time.sleep(3)