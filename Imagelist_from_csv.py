import piexif
import os
import csv
from math import sin,cos,asin,radians,sqrt

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
        if x.endswith('.JPG'):
            try:
                # In some photos location metadata is not available
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
    radius = 50
    images = imagelist(path='images/')
    #Getting the values from the given csv file
    with open('assets.csv','r') as csvfile:
        my_file = csv.DictReader(csvfile)
        a=[]
        for line in my_file:
            a.append([line['asset_name'],float(line['longitude']),float(line['latitude'])])

    #Initializing the new csv file
    line = ['asset_name','longitude','latitude','image_names']
    with open('imagelist_assets.csv','w',newline='') as csvfile:
        my_file = csv.writer(csvfile)
        my_file.writerow(line)


    for i in range(len(a)):
        list=[]
        #making the list of list of images for every concerned co-ordinate
        for j in range(len(images)):
            if distance_between_points(a[i][1],a[i][2],images[j][1],images[j][2])<=radius:
                list.append(images[j][0])
        #Pushing the list of images and other parameters in the csv file
        row = [a[i][0],a[i][1], a[i][2], list]
        with open('imagelist_assets.csv', 'a', newline='') as csvfile:
            my_file = csv.writer(csvfile)
            my_file.writerow(row)

if __name__=='__main__':
    main()
