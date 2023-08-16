import socket
import json
import csv
import threading
import os
import mysql.connector.pooling

# Path untuk berkas CSV
PATH_CSV = {
    'android': './masterTjuy/mqtt_logs_andro.csv',
    'arduinolocal': './masterTjuy/local_logs_ardu.csv'
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
            values = [float(value) for value in item[:9]]
            if table_name == 'android':
                values.extend(item[9:])
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

def receive_broadcasts(port):
    client_ip = ''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind((client_ip, port))
    print(f"Mendengarkan pesan siaran pada port {port}...")
    try:
        while True:
            try:
                data, server_address = client_socket.recvfrom(1024)
                received_list = json.loads(data.decode('utf-8'))

                received_list[8] = normalize_degrees(float(received_list[8]))

                with create_connection() as connection:
                    with open(PATH_CSV['android' if port == 50000 else 'arduinolocal'], 'a', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        normalized_data = received_list.copy()
                        normalized_data[8] = normalize_degrees(float(normalized_data[8]))
                        csv_writer.writerow(normalized_data)

                    insert_data_to_table(connection, 'android' if port == 50000 else 'arduinolocal', [received_list])

            except Exception as e:
                print(f"Kesalahan saat menerima dan menulis data: {e}")
    except KeyboardInterrupt:
        print("Penerimaan data dihentikan")

if __name__ == "__main__":
    try:
        connection_pool = mysql.connector.pooling.MySQLConnectionPool(**DB_SETTINGS)

        port_mqtt_logs_andro = 50000
        port_local_logs_ardu = 52222

        thread_port_mqtt = threading.Thread(target=receive_broadcasts, args=(port_mqtt_logs_andro,))
        thread_port_local = threading.Thread(target=receive_broadcasts, args=(port_local_logs_ardu,))
        
        thread_port_mqtt.start()
        thread_port_local.start()
        
        thread_port_mqtt.join()
        thread_port_local.join()
    except Exception as e:
        print(f"Kesalahan utama: {e}")
