#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Get's the weather information for a particular city passed as a command-line argument.
'''

import sys
import urllib
import json

locale = sys.argv[1]
query = 'http://api.openweathermap.org/data/2.5/weather?q='+locale+'&units=metric'

response = urllib.urlopen(query)
weather_data = json.load(response)

placename = weather_data['name']
country = weather_data['sys']['country']
lat = weather_data['coord']['lat']
lon = weather_data['coord']['lon']

current_temp = float(weather_data['main']['temp'])
temp_high = float(weather_data['main']['temp_max'])
temp_low  = float(weather_data['main']['temp_min'])
rel_humidity  = float(weather_data['main']['humidity'])
pressure_hPa  = float(weather_data['main']['pressure'])
pressure_atm  = float(weather_data['main']['pressure'])/1013.17
pressure_mmHg = pressure_atm * 760
desc = weather_data['weather'][0]['description']

def heat_index(temp,rel_humidity):
    # NOAA's heat index formula to calculate what the temperature feels like, given the relative humidity
    T = temp * 9./5. + 32.0
    R = rel_humidity/100.0
    feels_like = -42.379 + 2.04901523*T + 10.14333127*R - 0.22475541*T*R - 6.83783e-3*T**2 \
            - 5.481717e-2*R**2 + 1.22874e-3*T**2 * R + 8.5282e-4*T*R**2 - 1.99e-6*T**2 * R**2
    # Convert back to Celsius
    feels_like = (feels_like - 32.0) * 5./9.
    return feels_like

print 'The weather in {0}, {1} right now:'.format(placename,country)
print u'\nTemperature: {0:5.2f}°C. Feels like: {1:5.2f}°C.'.format(current_temp,heat_index(current_temp,rel_humidity))
print 'Today\'s High: {0:5.2f}°C. Today\'s Low: {1:5.2f}°C. '.format(temp_high,temp_low)
print 'Relative Humidity: {0}%'.format(int(rel_humidity))
print 'Atmospheric Pressure: {0:6.4f} atm / {1:5.2f} hPa / {2:5.2f} mmHg'.format(pressure_atm,pressure_hPa,pressure_mmHg)
print desc.capitalize()
