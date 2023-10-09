# sl-projekt
A SL (Stockholms Lokaltrafik) Display project (Stockholm Public Transport)

This project creates a display for your own use to show public transport departures from stations of your own choosing

To run this project you need to use your own public API keys from https://trafiklab.se and the "SL Departures v4.0" and "SL Stop Lookup v1.0".

Store these API keys in "api_config.json" file at same folder as the project with the format:

{

    "API_PLACE":"<YourKeyfromStopLookUp>,

    "API_REAL_TIME":"<YourKeyFromSLDepartures>"
}

Software version: 1.2

# Limitations and upcoming upgrades

Currently hard coded to 3 stops. The aim for future design is have variable stations on the display



# Author
Oskar Nordström
