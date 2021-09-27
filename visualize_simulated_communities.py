import json
from geopy.distance import geodesic
import folium

# Create map
m = folium.Map(location=[52.521918, 13.413215], zoom_start=7.5)



with open('150_no_locals_community.json','r') as f:
    data = json.loads(f.read())

#with open('micro_local_clusters.json', 'r') as f:
 #   data = json.loads(f.read())

#with open('local_clusters.json','r') as f:
 #   data = json.loads(f.read())



    print(data['producers'])

    for producer in data['producers']:
        print(producer['coordinates'])

        # tooltip
        tooltip = producer['meterId'], 'producer'



        lat = producer['coordinates'][0]
        lng = producer['coordinates'][1]

        # create markers
        folium.Marker([lat, lng],
                      popup='<strong> Producer </strong>',
                      color='darkgreen',
                      icon=folium.Icon(color='darkgreen', icon='flash'),
                      tooltip=tooltip).add_to(m)


    for consumer in data['consumers']:

        lat = consumer['coordinates'][0]
        lng = consumer['coordinates'][1]

        # tooltip
        tooltip = producer['meterId'], 'consumer'


        folium.Marker([lat, lng],
                      popup='<strong> Consumer </strong>',
                      color='lightred',
                      icon=folium.Icon(color='lightred', icon='fas fa-plug', prefix='fa'),
                      tooltip=tooltip).add_to(m)

# generate map
m.save('no_locals_Map.html')



