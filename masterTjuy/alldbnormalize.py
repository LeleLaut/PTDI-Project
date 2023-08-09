import socket
import json
import csv
import threading
import os
import mysql.connector

if os.path.exists('./masterTjuy/local_logs_ardu.csv'):
    os.remove('./masterTjuy/local_logs_ardu.csv')
if os.path.exists('./masterTjuy/mqtt_logs_andro.csv'):
    os.remove('./masterTjuy/mqtt_logs_andro.csv')

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='flightestdb'
    )

# Fungsi untuk mengirim data ke tabel 'android'
def insert_data_to_android(connection, data):
    query = "INSERT INTO android (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, pitch, roll, yaw, latitude, longitude, altitude, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        for item in data:
            values = [float(value) for value in item]
            cursor.execute(query, tuple(values))
        connection.commit()
    except Exception as e:
        print(f"Error saat memasukkan data ke tabel 'android': {e}")

# Fungsi untuk mengirim data ke tabel 'arduinolocal'
def insert_data_to_arduinolocal(connection, data):
    query = "INSERT INTO arduinolocal (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, pitch, roll, yaw, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        for item in data:
            values = [float(value) for value in item[:9]]
            values.append(item[9])
            cursor.execute(query, tuple(values))
        connection.commit()
    except Exception as e:
        print(f"Error saat memasukkan data ke tabel 'arduinolocal': {e}")

# Fungsi untuk mengolah data sudut agar nilainya berada dalam rentang -180 hingga 180
def normalize_degrees(degrees):
    while degrees > 180:
        degrees -= 360
    while degrees < -180:
        degrees += 360
    return degrees

# Fungsi untuk menerima data dari server dan menulisnya ke file CSV
def receive_broadcasts(port, connection):
    client_ip = ''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind((client_ip, port))
    print(f"Mendengarkan pesan broadcast di port {port}...")
    try:
        while True:
            try:
                # Terima data dari server
                data, server_address = client_socket.recvfrom(1024)
                received_list = json.loads(data.decode('utf-8'))

                # Olah data yaw agar nilainya dalam rentang -180 hingga 180
                received_list[8] = normalize_degrees(received_list[8])

                if port == 50000:
                    with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        # Tulis data yang sudah di-normalisasi ke file CSV
                        normalized_data = received_list.copy()
                        normalized_data[8] = normalize_degrees(normalized_data[8])
                        csv_writer.writerow(normalized_data)
                    insert_data_to_android(connection, [received_list])  # Masukkan data ke tabel 'android'
                elif port == 52222:
                    with open('./masterTjuy/local_logs_ardu.csv', 'a', newline='') as csvfile:
                        csv_writer = csv.writer(csvfile)
                        # Tulis data yang sudah di-normalisasi ke file CSV
                        normalized_data = received_list.copy()
                        normalized_data[8] = normalize_degrees(normalized_data[8])
                        csv_writer.writerow(normalized_data)
                    insert_data_to_arduinolocal(connection, [received_list])  # Masukkan data ke tabel 'arduinolocal'
            except Exception as e:
                print(f"Error saat menerima dan menulis data: {e}")
    except KeyboardInterrupt:
        print("Menerima data dihentikan.")

# Main execution
if __name__ == "__main__":
    # Buat koneksi ke database
    connection = create_connection()

    # Port untuk menerima data dari server
    port_mqtt_logs_andro = 50000
    port_local_logs_ardu = 52222

    # Thread untuk menerima dan menyimpan data dari server ke file CSV
    thread_port_mqtt = threading.Thread(target=receive_broadcasts, args=(port_mqtt_logs_andro, connection))
    thread_port_local = threading.Thread(target=receive_broadcasts, args=(port_local_logs_ardu, connection))
    
    thread_port_mqtt.start()
    thread_port_local.start()
    
    # Tunggu sampai kedua thread selesai
    thread_port_mqtt.join()
    thread_port_local.join()

    # Tutup koneksi database setelah selesai memasukkan data
    connection.close()
