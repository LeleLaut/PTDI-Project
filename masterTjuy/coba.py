import folium
from folium import plugins

# Read and process data from CSV file
graph_data = open('android ini.csv', 'r').readlines()
lines = graph_data[1:]  # Skip header line
lines = [elem.replace('"', '') for elem in lines]

Long = []
Lat = []
Alt = []

for line in lines:
    if len(line) > 1:
        _, _, _, _, _, _, _, _, _, _, long, lat, alt, _, _ = line.split(',')
        Long.append(float(long))
        Lat.append(float(lat))
        Alt.append(float(alt))

# Create a base map centered at a specific location
map_center = [sum(Lat) / len(Lat), sum(Long) / len(Long)]
mymap = folium.Map(location=map_center, zoom_start=17)

# Add lines connecting consecutive points
for i in range(len(Lat) - 1):
    line_points = [(Lat[i], Long[i]), (Lat[i+1], Long[i+1])]
    folium.PolyLine(locations=line_points, color='red').add_to(mymap)

# Display the map
mymap.save("gps_map_with_trackers.html")
