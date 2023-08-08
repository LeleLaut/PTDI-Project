for data_point in gps_data:
    folium.Marker(
        location=[data_point['latitude'], data_point['longitude']],
        popup=f"Altitude: {data_point['altitude']}",
        icon=folium.Icon(color='transparent')
    ).add_to(mymap)