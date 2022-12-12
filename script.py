# Developer : Mohammed J Hossain
# Dev-Github : @mjhossain
# Date : Nov 29, 2022

import folium
import csv
import re

import pandas as pd
from sodapy import Socrata

from folium import plugins
from folium.plugins import HeatMap


# Createing Folium Map
map = folium.Map(location=[40.730610, -73.935242], tiles='Stamen Toner',zoom_start = 11)


# Importing AirBnb Data (2019) and creating pandas data frame
airbnb_data = pd.read_csv('./AB_NYC_2019.csv', delimiter=',', nrows=1000)
abnb_df = pd.DataFrame.from_records(airbnb_data)


# Importing NYPD Complaints Data (2019)
# Important Fields || rpt_dt (Report Date) | latitude | longitude
client = Socrata("data.cityofnewyork.us", None)
results = client.get("qgea-i56i", limit=200)
nypd_df = pd.DataFrame.from_records(results)


# Using to_datetime() & astype()
# df['ConvertedDate']=pd.to_datetime(df['DateTypeCol'].astype(str), format='%Y/%m/%d')


date_record = nypd_df['rpt_dt'].astype(str)
heat_lat = nypd_df['latitude'].apply(lambda x: float(x))
heat_lon = nypd_df['longitude'].apply(lambda x: float(x))

for i in nypd_df.index:
  if date_record[i][0:4] == '2018':
    heat_data = [[heat_lat[i], heat_lon[i]]]
    HeatMap(heat_data).add_to(map)




# print(abnb_df[['latitude', 'longitude']])

#  df_acc['Latitude'] = df_acc['Latitude'].astype(float)
# abnb_df['latitude'] = abnb_df['latitude'].astype(float)
# abnb_df['longitude'] = abnb_df['longitude'].astype(float)

lat = abnb_df['latitude'].apply(lambda x: float(x))
lon = abnb_df['longitude'].apply(lambda x: float(x))


for index in abnb_df.index:
  # folium.Marker([lat[index], lon[index]]).add_to(map)
  folium.Circle(
    radius=10,
    location=[lat[index], lon[index]],
    color="green",
    fill=False,
  ).add_to(map)


# Calling Folium Map
map