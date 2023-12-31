import socket
import json
import csv
import threading
import os
import mysql.connector

# Fungsi untuk membuat koneksi baru ke database
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='flightestdb'
    )

# Fungsi untuk membuat tabel 'android' jika belum ada
def create_table_android1(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS android1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gyro_x FLOAT,
            gyro_y FLOAT,
            gyro_z FLOAT,
            accel_x FLOAT,
            accel_y FLOAT,
            accel_z FLOAT,
            pitch FLOAT,
            roll FLOAT,
            yaw FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            altitude FLOAT,
            counter INT
        )
        '''
        cursor.execute(create_table_query)
        print("Table 'android1' created successfully.")
    except Exception as e:
        print(f"Error while creating table 'android1': {e}")

# Fungsi untuk membuat tabel 'arduinolocal' jika belum ada
def create_table_arduino1(connection):
    try:
        cursor = connection.cursor()
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS arduino1 (
            id INT AUTO_INCREMENT PRIMARY KEY,
            gyro_x FLOAT,
            gyro_y FLOAT,
            gyro_z FLOAT,
            acc_x FLOAT,
            acc_y FLOAT,
            acc_z FLOAT,
            pitch FLOAT,
            roll FLOAT,
            yaw FLOAT,
            counter INT
        )
        '''
        cursor.execute(create_table_query)
        print("Table 'arduino1' created successfully.")
    except Exception as e:
        print(f"Error while creating table 'arduino1': {e}")

# Fungsi untuk mengirim data ke tabel 'android'
def insert_data_to_android1(connection, data):
    query = "INSERT INTO android1 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, pitch, roll, yaw, latitude, longitude, altitude, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        for item in data:
            values = [float(value) for value in item]
            cursor.execute(query, tuple(values))
        connection.commit()
        print("Data inserted to 'android1' table successfully.")
    except Exception as e:
        print(f"Error while inserting data to Android1 table: {e}")
        # Print the data being inserted to check if it's in the expected format
        print("Data being inserted:", data)

# Fungsi untuk mengirim data ke tabel 'arduinolocal'
def insert_data_to_arduino1(connection, data):
    query = "INSERT INTO arduino1 (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, pitch, roll, yaw, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor = connection.cursor()
    try:
        for item in data:
            values = [float(value) for value in item[:9]]
            values.append(item[9])
            cursor.execute(query, tuple(values))
        connection.commit()
        print("Data inserted to 'arduino1' table successfully.")
    except Exception as e:
        print(f"Error while inserting data to arduino1 table: {e}")
        # Print the data being inserted to check if it's in the expected format
        print("Data being inserted:", data)

# Fungsi untuk menerima data dari server dan menyimpannya ke file CSV
def receive_broadcasts(port):
    client_ip = ''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind((client_ip, port))
    print(f"Listening for broadcast messages on port {port}...")

    try:
        while True:
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
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

# Fungsi untuk memproses data dari file CSV ke database
def process_csv_and_insert_to_database(connection):
    try:
        with open('./masterTjuy/mqtt_logs_andro.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = list(csv_reader)
            insert_data_to_android1(connection, data)

        with open('./masterTjuy/local_logs_ardu.csv', 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            data = list(csv_reader)
            insert_data_to_arduino1(connection, data)

    except Exception as e:
        print(f"Error while processing CSV and inserting to database: {e}")

# Panggil fungsi create_connection untuk membuat koneksi ke database
connection = create_connection()

# Panggil fungsi untuk membuat tabel baru 'android' dan 'arduinolocal' jika belum ada
create_table_android1(connection)
create_table_arduino1(connection)

# Buat thread untuk menerima data dari server dan menulisnya ke file CSV
receive_thread_50000 = threading.Thread(target=receive_broadcasts, args=(50000,))
receive_thread_52222 = threading.Thread(target=receive_broadcasts, args=(52222,))

# Buat thread untuk memproses data dari file CSV dan memasukkan ke database
process_thread = threading.Thread(target=process_csv_and_insert_to_database, args=(connection,))

# Start thread untuk menerima data
receive_thread_50000.start()
receive_thread_52222.start()

# Tunggu hingga thread menerima data selesai
receive_thread_50000.join()
receive_thread_52222.join()

# Start thread untuk memproses data dan memasukkan ke database
process_thread.start()

# Tunggu hingga thread memproses data dan memasukkan ke database selesai
process_thread.join()

# Tutup koneksi ke database
connection.close()