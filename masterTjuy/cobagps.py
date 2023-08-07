import folium
from folium import plugins

# Create a base map centered at a specific location
map_center = [-6.89729,107.58]
mymap = folium.Map(location=map_center, zoom_start=17)

# Sample GPS data
gps_data = [
    {'latitude': -6.89729, 'longitude': 107.58, 'altitude': 680},
    {'latitude': -6.8978042, 'longitude': 107.5797249, 'altitude': 680},
    {'latitude': -6.89873, 'longitude': 107.5825, 'altitude': 680},
]

# Add lines connecting consecutive points
for i in range(len(gps_data) - 1):
    line_points = [(gps_data[i]['latitude'], gps_data[i]['longitude']),
                   (gps_data[i+1]['latitude'], gps_data[i+1]['longitude'])]
    folium.PolyLine(locations=line_points, color='red').add_to(mymap)

# Display the map
mymap.save("gps_map_with_trackers.html")
