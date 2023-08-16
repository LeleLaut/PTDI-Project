import socket
import json
import csv
import threading
import os
import mysql.connector.pooling

# Path untuk berkas CSV
CSV_PATHS = {
    'android': './KAZ/SERVERLOCAL/mqtt_logs_andro.csv',
    'arduinolocal': './KAZ/SERVERLOCAL/local_logs_ardu.csv',
    'mqtt_ardu': './KAZ/SERVERUP/mqtt_logs_ardu.csv'
}

# Pengaturan koneksi basis data MySQL
DB_SETTINGS = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flightestdb',
    'pool_name': 'mypool',
    'pool_size': 5
}

def create_connection():
    return connection_pool.get_connection()

def insert_data_to_table(connection, table_name, data):
    android_query = (
        "INSERT INTO android (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, pitch, roll, yaw, latitude, longitude, altitude, counter) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    arduino_query = (
        "INSERT INTO arduino (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, pitch, roll, yaw, counter) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
    cursor = connection.cursor()
    query = android_query if table_name == 'android' else arduino_query

    try:
        for item in data:
            values = [float(value) for value in item[:10]]  # Mengubah dari [:9] menjadi [:10]
            cursor.execute(query, tuple(values))
        connection.commit()
    except Exception as e:
        print(f"Kesalahan saat memasukkan data ke tabel '{table_name}': {e}")

def normalize_degrees(degrees):
    while degrees > 180:
        degrees -= 360
    while degrees < -180:
        degrees += 360
    return degrees

def receive_broadcasts(port, csv_path):
    client_ip = ''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind((client_ip, port))
    print(f"Mendengarkan pesan siaran pada port {port}...")
    while True:
        data, server_address = client_socket.recvfrom(1024)
        received_list = json.loads(data.decode('utf-8'))
        
        if port == 50000 or port == 52222:
            received_list[8] = normalize_degrees(float(received_list[8]))

        with create_connection() as connection:
            with open(csv_path, 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(received_list)

            if port == 50000:
                insert_data_to_table(connection, 'android', [received_list])
            elif port == 52222:
                insert_data_to_table(connection, 'arduinolocal', [received_list])
            elif port == 53333:
                insert_data_to_table(connection, 'arduino', [received_list])

# Main execution
if __name__ == "__main__":
    try:
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_SETTINGS)

        port_50000_thread = threading.Thread(target=receive_broadcasts, args=(50000, CSV_PATHS['android']))
        port_52222_thread = threading.Thread(target=receive_broadcasts, args=(52222, CSV_PATHS['arduinolocal']))
        port_53333_thread = threading.Thread(target=receive_broadcasts, args=(53333, CSV_PATHS['mqtt_ardu']))

        port_50000_thread.start()
        port_52222_thread.start()
        port_53333_thread.start()

        port_50000_thread.join()
        port_52222_thread.join()
        port_53333_thread.join()
    except Exception as e:
        print(f"Kesalahan utama: {e}")
