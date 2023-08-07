# Add lines connecting consecutive points
for i in range(len(gps_data) - 1):
    line_points = [(gps_data[i]['latitude'], gps_data[i]['longitude']),
                   (gps_data[i+1]['latitude'], gps_data[i+1]['longitude'])]
    folium.PolyLine(locations=line_points, color='green').add_to(mymap)

# Display the map
mymap.save("gps_map_with_trackers.html")