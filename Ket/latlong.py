import folium
from folium.plugins import PolyLineTextPath

# Create a map centered on a specific location
m = folium.Map(location=[51.5074, -0.1278], zoom_start=13)

track_points = [
    (51.5074, -0.1278),
    (51.5077, -0.1280),
    (51.5080, -0.1282),
    (51.5083, -0.1285),
    (51.5086, -0.1288),
]

# Define the labels (make sure these are strings)
labels = ['Point 1', 'Point 2', 'Point 3', 'Point 4', 'Point 5']

# Create a polyline to represent the track
track_line = folium.PolyLine(locations=track_points, color='blue')

# Add the track polyline to the map
m.add_child(track_line)

# Add labels along the track using PolyLineTextPath
label_feature = PolyLineTextPath(
    track_points, text=labels, offset=8, repeat=True
)
m.add_child(label_feature)

# Save the map to an HTML file
m.save('track_map.html')
