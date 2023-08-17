import folium
from folium import plugins

graph_data = open('androidbaru.csv', 'r').readlines()
#graph_data = graph_data.replace('"', '')
lines = graph_data[1:]  # Skip header line
lines = [elem.replace('"', '') for elem in lines]

Long = []
Lat = []
Alt = []

for line in lines:
    # print(graph_data)
    if len(line) > 1:
        # _, _, _, _, _, _, _, _, _, _, long, lat, alt, _, _ = line.split(',')
        _, _, _, _, _, _, _, _, _, lat, long, alt, = line.split(',')
        #  ID.append(float(id))
        Long.append(float(long))
        Lat.append(float(lat))
        Alt.append(float(alt))

# Create a base map centered at a specific location
map_center = [-6.89729,107.58]
mymap = folium.Map(location=map_center, zoom_start=17)

# Sample GPS data
gps_data = []
for i in range(len(Lat)):
    print(Lat[i])
    print(Long[i])
    gps_point = {
        'latitude': Lat[i],
        'longitude': Long[i],
        'altitude': Alt[i]
        # 'altitude': 680
    }
    gps_data.append(gps_point)

# Add markers for each GPS data point
# for data_point in gps_data:
#     folium.Marker(
#         location=[data_point['latitude'], data_point['longitude']],
#         popup=f"Altitude: {data_point['altitude']}",
#         icon=folium.Icon(color='blue')
#     ).add_to(mymap)

# Add lines connecting consecutive points
for i in range(len(gps_data) - 1):
    line_points = [(gps_data[i]['latitude'], gps_data[i]['longitude']),
                   (gps_data[i+1]['latitude'], gps_data[i+1]['longitude'])]
    folium.PolyLine(locations=line_points, color='red').add_to(mymap)

# Display the map
mymap.save("gpstrackers.html")
