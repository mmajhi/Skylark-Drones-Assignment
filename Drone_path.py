import simplekml
import pandas as pd

dataset = pd.read_csv('image_list.csv')

kml = simplekml.Kml()


for start,long,lat,image in zip(dataset['Start(s)'],dataset['Longitude'],dataset['Latitude'],dataset['image_names']):
    point = kml.newpoint(name='{} sec'.format(start),coords=[(long,lat)])
    point.description = image
    #point.stylemap.normalstyle.labelstyle.color = simplekml.Color.blue
    point.stylemap.highlightstyle.labelstyle.color = simplekml.Color.red

kml.save('Drone Path.kml')

