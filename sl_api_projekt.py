#-*- coding: utf-8 -*-
"""
Learning REST APIs
In the goal of learning about RESTful API system, this code uses get request to query json data
The data query contains SL real time information about public transport departures from a given set of stations.

This code handles learning aspect by utilizing get request to learn about how to use RESTful api.
The second part handles json data parsing and presenting on a readable format.
Many RESTful APIs send data on json format, this has allowed the author to learn how to parse
json data on a practical level.

Author: Oskar Nordström
"""
import requests
from tkinter import *
import json
from datetime import datetime
import sys
software_version = "v1.2"

# Open a local config file with API your SL API Keys
# Get your personal API keys from trafiklab.se
# To lookup stations use this link for API key: https://www.trafiklab.se/sv/api/trafiklab-apis/sl/stop-lookup/
# To lookup realtime data use this link for API key: https://www.trafiklab.se/sv/api/trafiklab-apis/sl/departures-4/
with open("./api_config.json") as f:
    api_dict = json.load(f)

# Store the API keys from config json file
my_key_plats = api_dict["API_PLACE"]
my_key_real_time = api_dict["API_REAL_TIME"]

# Input the stations and station number that you want to display, currently GUI support 3 stations
stations = {
    "kärrtorp": "9142",
    "kärrtorpsvägen": "1570",
    "de gamlas väg": "1572"
}
# Kista 9302
# Input the station name that you want to find the station ID number for. Each bus/metro/.. stop has its own site number
# Check the print to find your station, use the query multiple time until you have found all stops you want to find
search_string = "Kista"                # "kärrtorp"

#
response = requests.get(f"https://api.sl.se/api2/typeahead.json?key={my_key_plats}&searchstring={search_string}]&stationsonly=True&maxresults50")
                     # since the content was in application/json, we can show the json format

# Indent print for easier readability
print(response.json())
print(json.dumps(response.json(), indent=4))
class DeparturesRESTAPI():
    """
    Class that handles REST API query and parses json data
    time_window is the time that you want to find departures from now
    """
    def __init__(self):
        self.stations = stations
        self.time_window = 30
        self.formats = "json" #formats
        self.real_time_info = {}
        self.DEBUG = True
        self.station_departures()

    def get_sl_info(self, site_ids):
        """
        :param site_ids: the string that is the station number from which the departure is querried
        :return: the json data from the station
        """
        response_real_times = requests.get(
            f"https://api.sl.se/api2/realtimedeparturesV4.{self.formats}?key={my_key_real_time}&siteid={site_ids}&timewindow={self.time_window}&bus=True")
        return response_real_times.json()

    def station_departures(self):
        """
        Loops through the given stations and extracts departures information via SL API key and stores into a class dictionary
        :return:
        """
        for key, value in self.stations.items():
            json_data = self.get_sl_info(value)
            # Replace "kärrtorp" with the metro station of your choice, for multiple metro stations add more elif statements
            if key == "kärrtorp":
                transport_method = "Metros"
                # Replace with Metro from
                out_string = "Tunnelbana från " + key
            else:
                transport_method = "Buses"
                # Replace with Bus from for english
                out_string = "Buss från " + key
            loops = len(json_data["ResponseData"][transport_method])
            for i in range(0, loops):
                if key == "kärrtorpsvägen" and json_data["ResponseData"][transport_method][i]['LineNumber'] == "816":
                    continue
                else:
                    out_string += "\n" + json_data['ResponseData'][transport_method][i]['LineNumber'] + " " + json_data['ResponseData'][transport_method][i]['Destination'] + " " + json_data['ResponseData'][transport_method][i]['DisplayTime']
            self.real_time_info[key] = out_string
        if self.DEBUG:
            for keys, value in self.stations.items():
                print(self.real_time_info[keys])


# Instantiate the class
window = DeparturesRESTAPI()

# Creates the window to display station departures with Tkinter

app = Tk()
# Adapt geometry to the size of your display
app.geometry("990x550+600+300")                         # width x height + x + y position of top left corner
app.title(f"Kollektivtrafiken i hallen {software_version}")
# Disable window resize, set to True if you want to manually change window size
app.resizable(False, False)
# Window colour background
app.config(background="#293241")

# Add frames

frame1 = Frame(app, height=120, width=990, bg="lightblue", bd=1, relief=FLAT)  # FLAT/RAISED/SUNKEN/GROOVE/RIDGE
frame1.place(x=0,y=0)
frame2 = Frame(app, height=330, width=330, bg="#293242", bd=1, relief=FLAT)
frame2.place(x=0, y=150)
frame3 = Frame(app, height=30, width=990, bg="black", bd=1, relief=FLAT)
frame3.place(x=0, y=120)
frame4 = Frame(app, height=330, width=330, bg="#293242", bd=1, relief=FLAT)
frame4.place(x=330, y=150)
frame5 = Frame(app, height=330, width=330, bg="#293242", bd=1, relief=FLAT) #293242
frame5.place(x=660, y=150)


# Add Tkinter Labels to display text or numbers to Display
# Add Current Time text
label_time = Label(text="Current Time", bg="lightblue", font="verdana 12 bold")
label_time.place(x=30, y=30)
# Add time in numbers
label_time_input = Label(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bg="lightblue", font="verdana 17")
label_time_input.place(x=30, y=50)

# Texts
# Add textboxes with station info
text_karrtorp = Text(frame2, height=20, width=25, bg="#293242", fg="white", relief=FLAT, font="verdana 17")
text_karrtorp.place(x=0, y=0)
text_karrtorp.insert("1.0", window.real_time_info["kärrtorp"])

text_karrtorpsvagen = Text(frame4, height=20, width=25, bg="#293242", fg="white", relief=FLAT, font="verdana 17")
text_karrtorpsvagen.place(x=0, y=0)
text_karrtorpsvagen.insert("1.0", window.real_time_info["kärrtorpsvägen"])
print(window.real_time_info["kärrtorpsvägen"])

text_de_gamlas_vag = Text(frame5, height=20, width=25, bg="#293242", fg="white", relief=FLAT, font="verdana 17")
text_de_gamlas_vag.place(x=0, y=0)
text_de_gamlas_vag.insert("1.0", window.real_time_info["de gamlas väg"])
print(window.real_time_info["de gamlas väg"])


# Continuously update clock every second
def update_clock():
    label_time_input.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label_time_input.after(1000, update_clock)


# Clear the text in station text boxes
def clear_text():
    text_karrtorp.delete("1.0", END)
    text_karrtorpsvagen.delete("1.0", END)
    text_de_gamlas_vag.delete("1.0", END)


# Updates the station info every 90s
def update_real_time():
    if window.DEBUG:
        print("Nya avgångar")
    window.station_departures()
    clear_text()
    text_karrtorp.insert("1.0", window.real_time_info["kärrtorp"])
    text_karrtorpsvagen.insert("1.0", window.real_time_info["kärrtorpsvägen"])
    text_de_gamlas_vag.insert("1.0", window.real_time_info["de gamlas väg"])
    app.after(90000, update_real_time)


update_clock()
update_real_time()
app.mainloop()
