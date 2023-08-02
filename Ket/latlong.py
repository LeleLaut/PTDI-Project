import folium

def main():
    # Koordinat tengah peta
    center_lat, center_lon = -6.1753924, 106.8271528
    
    # Membuat peta
    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=12)
    
    # Contoh titik yang akan ditampilkan pada peta
    # Ganti lat dan lon sesuai dengan titik yang ingin Anda tampilkan
    points = [
        {'lat': -6.1784773, 'lon': 106.8310428, 'name': 'Titik 1'},
        {'lat': -6.1774688, 'lon': 106.8249641, 'name': 'Titik 2'},
        {'lat': -6.173096, 'lon': 106.8266902, 'name': 'Titik 3'},
    ]
    
    # Menambahkan mark pada peta untuk setiap titik
    for point in points:
        folium.Marker(
            location=[point['lat'], point['lon']],
            popup=point['name'],
            icon=folium.Icon(icon='cloud')  # Ganti ikon sesuai keinginan
        ).add_to(my_map)
    
    # Menyimpan peta ke dalam file HTML
    my_map.save('map.html')
    
if __name__ == "__main__":
    main()
