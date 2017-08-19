import numpy as np
import sys, os
import googlemaps
from datetime import datetime
from matplotlib import pyplot as plt
#address = "3000 Broadway, New York"
address = sys.argv[1]

#get lat lon from address:
key_file=open('./key', 'r')
gmaps = googlemaps.Client(key=key_file.readline().strip('\n'))
geocode_result = gmaps.geocode(address)
#print(geocode_result[0]['geometry'].get('location'))
lat = geocode_result[0]['geometry'].get('location').get('lat')
lng = geocode_result[0]['geometry'].get('location').get('lng')
lat = 40.6798988 
lng = -73.9778685


del_x = 0.007
del_y = 0.007


x_hi = lng + del_x*0.5
x_lo = lng - del_x*0.5
y_hi = lat + del_y*0.5
y_lo = lat - del_y*0.5


print(lat,lng)

#get street segment data
map_file = "nyc.kml"
f = open(map_file, "r")
raw_map_data = f.readlines()
f.close()
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

IN = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8

def CS_line_clip_code(point):
    code = 0
    if(point[0] < x_lo):
        code |= 1
    elif (point[0] > x_hi):
        code |= 2
    if (point[1] < y_lo):
        code |= 4
    elif (point[1] > y_hi):
        code |= 8
    return code

def CS_line_clip(segment):
    seg = segment
    c0 = CS_line_clip_code(seg[0])
    c1 = CS_line_clip_code(seg[1])
    accept = False
    while(True):
        if not (c0 | c1):
            accept = True
            break
        elif(c0 & c1):
            break
        else:
            #ternary operator:
            out = c0 if c0 else c1#c0 ? c0 : c1
            if out & TOP:
                x = seg[0][0] + (seg[1][0] - seg[0][0])*(y_hi - seg[0][1])/(seg[1][1] - seg[0][1])
                y = y_hi
            elif out & BOTTOM:
                x = seg[0][0] + (seg[1][0] - seg[0][0])*(y_lo - seg[0][1])/(seg[1][1] - seg[0][1])
                y = y_lo
            elif out & RIGHT:
                y = seg[0][1] + (seg[1][1] - seg[0][1])*(x_hi - seg[0][0])/(seg[1][0] - seg[0][0])
                x = x_hi
            elif out & LEFT:
                y = seg[0][1] + (seg[1][1] - seg[0][1])*(x_lo - seg[0][0])/(seg[1][0] - seg[0][0])
                x = x_lo
            if out == c0:
                seg[0][0] = x
                seg[0][1] = y
                c0 = CS_line_clip_code(seg[0])
            else:
                seg[1][0] = x
                seg[1][1] = y
                c1 = CS_line_clip_code(seg[1])
    if accept:
        return seg
    else:
        return False


lines_in_region = []
#iterate through streets
for segment in segment_data:
    for i in range(len(segment) - 1):
        #Cohen-Sutherland to filter out lines that intersect:
        clipped_line = CS_line_clip([segment[i],segment[i+1]])
        if clipped_line:
            lines_in_region.append(clipped_line)
print(lines_in_region)

a = np.asarray(lines_in_region)
print(a)
plt.plot(a[:,:,0].T,a[:,:,1].T)
plt.show()



