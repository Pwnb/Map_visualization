#!/usr/bin/env python
# coding: utf-8

# # 0 Environment Setup

# In[2]:


# Change output format
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
# InteractiveShell.ast_node_interactivity = "last_expr"

# Import packages
import warnings
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from sklearn.cluster import KMeans
import json
import requests
#!pip install folium
import folium
import random

# Other settings
warnings.filterwarnings('ignore')
get_ipython().run_line_magic('matplotlib', 'inline')
pd.set_option('display.max_columns',None)
sns.set(font='SimHei')

# -*- coding: utf-8 -*- 
import cx_Oracle
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


# # 1 Data Importing & Preprocessing

# ## you can create a list of longitudes and latitudes here

# # Map

# #### world map

# In[9]:


#### define the world map
world_map = folium.Map()

# display world map
world_map


# #### china map

# In[10]:


# San Francisco latitude and longitude values
latitude = 36.236493
longitude = 106.482988

# Create map and display it
san_map = folium.Map(location=[latitude, longitude], zoom_start=4)

# Display the map of San Francisco
san_map


# #### points on map

# In[12]:


# get the first 200 crimes in the cdata


# Instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# Loop through the 200 crimes and add each to the incidents feature group
for lat, lng, in zip(good_retailers_have_location.SHOP_LATITUDE, good_retailers_have_location.SHOP_LONGITUDE):
    incidents.add_child(
        folium.CircleMarker(
            [lat, lng],
            radius=7, # define how big you want the circle markers to be
            color='green',
            fill=True,
            fill_color='green',
            fill_opacity=0.4
        )
    )

# Add incidents to map
san_map = folium.Map(location=[latitude, longitude], zoom_start=4)
san_map.add_child(incidents)


# #### points with labels

# In[ ]:


# add pop-up text to each marker on the map
latitudes = list(retailers_have_location.SHOP_LATITUDE)
longitudes = list(retailers_have_location.SHOP_LONGITUDE)
labels = list(retailers_have_location.STORE_NAME_NOW)

for lat, lng, label in zip(latitudes, longitudes, labels):
    folium.Marker([lat, lng], popup = label).add_to(san_map)    
    
# add incidents to map
san_map.add_child(incidents)


# #### points with auto aggregation

# In[13]:


from folium import plugins
# let's start again with a clean copy of the map of San Francisco
san_map = folium.Map(location = [latitude, longitude], zoom_start = 4)

# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(san_map)

# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, in zip(good_retailers_have_location.SHOP_LATITUDE, good_retailers_have_location.SHOP_LONGITUDE, good_retailers_have_location.STORE_NAME_NOW):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

# add incidents to map
san_map.add_child(incidents)


# #### with grid lines

# In[15]:


import json
import requests

url = 'https://cocl.us/sanfran_geojson'
san_geo = 'Data/china.json'
san_map = folium.Map(location=[36, 106], zoom_start=4)
folium.GeoJson(
    san_geo,
    style_function=lambda feature: {
        'fillColor': '#ffff00',
        'color': 'black',
        'weight': 2,
        'dashArray': '5, 5'
    }
).add_to(san_map)

#display map
san_map


# #### heat map preparation - make freq list

# In[351]:


# Count crime numbers in each neighborhood
disdata = pd.DataFrame(good_retailers_have_location['PROVINCE_NAME'].value_counts())
disdata.reset_index(inplace=True)
disdata.rename(columns={'index':'PROVINCE_NAME','PROVINCE_NAME':'Count'},inplace=True)
disdata


# #### heat map

# In[ ]:


m = folium.Map(location=[36,106], zoom_start=4)
folium.Choropleth(
    geo_data=san_geo,
    data=disdata,
    columns=['PROVINCE_NAME','Count'],
    key_on='feature.properties.name',
    #fill_color='red',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    highlight=True,
    legend_name='Counts'
).add_to(m)
m


# #### heat map + amount aggregation

# In[ ]:


## 数量汇总（所有）
from folium import plugins
# let's start again with a clean copy of the map of San Francisco
san_map = folium.Map(location = [latitude, longitude], zoom_start = 4)

# instantiate a mark cluster object for the incidents in the dataframe
incidents = plugins.MarkerCluster().add_to(san_map)

# loop through the dataframe and add each data point to the mark cluster
for lat, lng, label, in zip(retailers_have_location.SHOP_LATITUDE, retailers_have_location.SHOP_LONGITUDE, retailers_have_location.STORE_NAME_NOW):
    folium.Marker(
        location=[lat, lng],
        icon=None,
        popup=label,
    ).add_to(incidents)

# add incidents to map
san_map.add_child(incidents)


# In[ ]:


# good_retailers_have_location['19年坪效']//2000
heat_list = []
for index, row in retailers_px_have_location.iterrows():
    for i in range(list((retailers_px_have_location['px']//20000).astype(int))[index]):
        heat_list.append([row['SHOP_LATITUDE'], row['SHOP_LONGITUDE']])


# In[23]:


## 热力图（所有）
from folium.plugins import HeatMap

# let's start again with a clean copy of the map of San Francisco
#san_map = folium.Map(location = [latitude, longitude], zoom_start = 4)

# Convert data format
#heatdata = good_retailers_have_location[['SHOP_LATITUDE','SHOP_LONGITUDE']].values.tolist()

# add incidents to map
HeatMap(heat_list).add_to(san_map)

san_map

