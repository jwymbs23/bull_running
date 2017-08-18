import numpy as np
import sys, os
import googlemaps
from datetime import datetime

#address = "3000 Broadway, New York"


#get lat lon from address:
#key_file=open('./key', 'r')
#gmaps = googlemaps.Client(key=key_file.readline().strip('\n'))
#geocode_result = gmaps.geocode(address)
##print(geocode_result[0]['geometry'].get('location'))
#lat = geocode_result[0]['geometry'].get('location').get('lat')
#lng = geocode_result[0]['geometry'].get('location').get('lng')
lat = 40.6798988 
lng = -73.9778685

print(lat,lng)

#get street segment data
map_file = "nyc.kml"
f = open(map_file, "r")
raw_map_data = f.readlines()
segment_data = []
flag = 0
street_count = 0
for ci,i in enumerate(raw_map_data):
    #get all street segments (later, add street names, street widths)
    if flag == 1:
        if "coordinates" in i:# == "</coordinates></LineString>\n":
            segment_data.append(street_data)
            flag = 2
        if flag < 2:
            street_data.append([float(j) for j in i.strip('\n').split(',')])
        #print([float(j) for j in i.strip('\n').split(',')])
    if "coordinates" in i and flag < 2:
        street_data = []
        flag = 1
    if flag == 2:
        street_count += 1
        flag = 0
#    if ci > 500:
raw_map_data = []
print(street_count)





