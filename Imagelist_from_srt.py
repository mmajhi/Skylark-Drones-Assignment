import piexif
import os
import csv
from math import sin,cos,asin,radians,sqrt

#Converting srt times into seconds
def srt_seconds(time):
    split_time=time.split(',')
    major=list(map(int,split_time[0].split(':')))
    minor=int(split_time[1])
    return major[0]*3600+major[1]*60+major[2]+minor/1000

#Creating a list of the subtitle files
def subtitles(file):
    srt_txt = file.read().split('\n\n')
    subs=[]
    for srt in srt_txt:
        if srt:
            s = srt.split('\n')[1:]
            st = s[0].split(' --> ')
            co = list(map(float,s[1].split(',')))
            subs.append({'start':srt_seconds(st[0].strip()),'end':srt_seconds(st[1].strip()),'longitude':co[0],'latitude':co[1]})
    return subs

#Find the co-ordinate of the respective latitude and longitude
def coordinate(a):
    dd = a[0]+a[1]/60+a[2]/3600
    if a[3]=='W' or a[3]=='S':
        dd*=-1
    return dd

#Haversine formula to find distance between two coordiantes
def distance_between_points(lon1,lat1,lon2,lat2):
    lat1,lon1,lat2,lon2 = map(radians,[lat1,lon1,lat2,lon2])

    dlat = lat2-lat1
    dlon = lon2-lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    r = 6371000 # radius of earth in m
    return c*r

# Provides a list with image name,it's latitude and longitude
def imagelist(path):
    images = []
    for x in os.listdir(path):
        if x.endswith('JPG'):
            try:        # In some photos location metadata is not available
                exif_dict=piexif.load(path+x,key_is_name='GPS')
                # Parsing the latitudes and longitudes
                latitude = exif_dict['GPS']['GPSLatitude']
                longitude = exif_dict['GPS']['GPSLongitude']
                direction = exif_dict['GPS']['GPSLatitudeRef']
                lat = [latitude[i][0]/latitude[i][1] for i in range(3)]+[chr(direction[0])]
                direction = exif_dict['GPS']['GPSLongitudeRef']
                long = [longitude[i][0]/longitude[i][1] for i in range(3)]+[chr(direction[0])]
                lat = coordinate(lat)
                long = coordinate(long)
                images.append([x,long,lat])
            except KeyError:
                pass
    return images

def main():
    radius=35
    images = imagelist(path='images/')
    file = open('videos/DJI_0301.SRT','r')
    a = subtitles(file) # Getting the subtitle array
    line = ['Start(s)','End(s)','Longitude','Latitude','image_names']
    with open('image_list.csv', 'w', newline='') as csvfile:
        my_file = csv.writer(csvfile)
        my_file.writerow(line)

    for i in range(len(a)):
        list=[]
        #making the list of list of images for every concerned co-ordinate
        for j in range(len(images)):
            if distance_between_points(a[i]['longitude'],a[i]['latitude'],images[j][1],images[j][2])<=radius:
                list.append(images[j][0])

        #Pushing the list of images and other parameters in the csv file
        row=[a[i]['start'],a[i]['end'],a[i]['longitude'],a[i]['latitude'],list]
        with open('image_list.csv','a',newline='') as csvfile:
            my_file = csv.writer(csvfile)
            my_file.writerow(row)

if __name__=='__main__':
    main()