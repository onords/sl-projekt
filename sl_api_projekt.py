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
software_version = "v1.0"

my_key_plats = "af4e79dc1e6e4edea4c7de081f32f259"    # Platsuppslag
my_key_real_time = "7c6e6911b6484549a3211fb2c1a1c426"   # Realtidsinformation
stations = {
    "kärrtorp": "9142",
    "kärrtorpsvägen": "1570",
    "de gamlas väg": "1572"
}
# search_string = "De gamlas väg"                # "kärrtorp"
# response = requests.get(f"https://api.sl.se/api2/typeahead.json?key={my_key_plats}&searchstring={search_string}]&stationsonly=True&maxresults50")
                     # since the content was in application/json, we can show the json format
class DeparturesRESTAPI():
    """
    Class that handles REST API query and parses json data
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
            if key == "kärrtorp":
                transport_method = "Metros"
                out_string = "Tunnelbana från " + key
            else:
                transport_method = "Buses"
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


window = DeparturesRESTAPI()

app = Tk()
app.geometry("710x480+600+300")                         # width x height + x + y position of top left corner
app.title(f"Kollektivtrafiken i hallen {software_version}")
app.resizable(False, False)
app.config(background="#293241")

# Add frames

frame1 = Frame(app, height=120, width=720, bg="lightblue", bd=1, relief=FLAT)  # FLAT/RAISED/SUNKEN/GROOVE/RIDGE
frame1.place(x=0,y=0)
frame2 = Frame(app, height=330, width=240, bg="#293242", bd=1, relief=FLAT)
frame2.place(x=0, y=150)
frame3 = Frame(app, height=30, width=720, bg="black", bd=1, relief=FLAT)
frame3.place(x=0, y=120)
frame4 = Frame(app, height=330, width=240, bg="#293242", bd=1, relief=FLAT)
frame4.place(x=240, y=150)
frame5 = Frame(app, height=330, width=240, bg="#293242", bd=1, relief=FLAT) #293242
frame5.place(x=480, y=150)


# Labels

label_time = Label(text="Current Time", bg="lightblue", font="verdana 12 bold")
label_time.place(x=30, y=30)

label_time_input = Label(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), bg="lightblue", font="verdana 12")
label_time_input.place(x=30, y=50)

# Texts

text_karrtorp = Text(frame2, height=20, width=25, bg="#293242", fg="white", relief=FLAT, font="verdana 10")
text_karrtorp.place(x=0, y=0)
text_karrtorp.insert("1.0", window.real_time_info["kärrtorp"])

text_karrtorpsvagen = Text(frame4, height=20, width=25, bg="#293242", fg="white", relief=FLAT, font="verdana 10")
text_karrtorpsvagen.place(x=0, y=0)
text_karrtorpsvagen.insert("1.0", window.real_time_info["kärrtorpsvägen"])
print(window.real_time_info["kärrtorpsvägen"])

text_de_gamlas_vag = Text(frame5, height=20, width=25, bg="#293242", fg="white", relief=FLAT, font="verdana 10")
text_de_gamlas_vag.place(x=0, y=0)
text_de_gamlas_vag.insert("1.0", window.real_time_info["de gamlas väg"])
print(window.real_time_info["de gamlas väg"])


def update_clock():
    label_time_input.config(text=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    label_time_input.after(1000, update_clock)



def clear_text():
    text_karrtorp.delete("1.0", END)
    text_karrtorpsvagen.delete("1.0", END)
    text_de_gamlas_vag.delete("1.0", END)

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
