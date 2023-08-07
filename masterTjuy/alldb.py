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
        print(f"Error while inserting data to Android table: {e}")

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
        print(f"Error while inserting data to arduinolocal table: {e}")

# Fungsi untuk menerima data dari server dan menulisnya ke file CSV
def receive_broadcasts(port):
    client_ip = ''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind((client_ip, port))
    print(f"Listening for broadcast messages on port {port}...")

    while True:
        try:
            # Terima data dari server
            data, server_address = client_socket.recvfrom(1024)
            received_list = json.loads(data.decode('utf-8'))
            if port == 50000:
                with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(received_list)
            elif port == 52222:
                with open('./masterTjuy/local_logs_ardu.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(received_list)

        except KeyboardInterrupt:
            print("Broadcast listener terminated.")
            break

        except Exception as e:
            print(f"Error: {e}")

    # Tutup socket ketika keluar dari loop
    client_socket.close()

# Fungsi untuk menerima data dan memprosesnya ke tabel 'android' dan 'arduinolocal'
def receive_and_insert_data(connection, port):
    # Thread untuk menerima data dari server dan menulisnya ke file CSV
    data_receive_thread = threading.Thread(target=receive_broadcasts, args=(port,))
    data_receive_thread.start()

    while True:
        try:
            # Di sini, Anda dapat memproses pesan atau melakukan tindakan lain sesuai kebutuhan
            # Misalnya, Anda dapat memanggil fungsi untuk menyimpan data ke database
            if port == 50000:
                with open('./masterTjuy/mqtt_logs_andro.csv', 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    data = list(csv_reader)
                    insert_data_to_android(connection, data)
            elif port == 52222:
                with open('./masterTjuy/local_logs_ardu.csv', 'r') as csvfile:
                    csv_reader = csv.reader(csvfile)
                    data = list(csv_reader)
                    insert_data_to_arduinolocal(connection, data)
        except KeyboardInterrupt:
            print("Broadcast listener terminated.")
            break

        except Exception as e:
            print(f"Error: {e}")

    # Tutup koneksi ke database ketika keluar dari loop
    connection.close()

# Panggil fungsi create_connection untuk membuat koneksi ke database
connection = create_connection()

# Panggil fungsi receive_and_insert_data dengan port yang diinginkan
port_50000_thread = threading.Thread(target=receive_and_insert_data, args=(connection, 50000))
port_52222_thread = threading.Thread(target=receive_and_insert_data, args=(connection, 52222))

port_50000_thread.start()
port_52222_thread.start()

# Tunggu kedua thread selesai
port_50000_thread.join()
port_52222_thread.join()
