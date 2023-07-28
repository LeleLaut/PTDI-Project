import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

# ... (existing code)

# Fungsi untuk menyimpan data ke database MySQL (PHPMyAdmin)
def insert_data_to_database(data, table_name):
    connection = mysql.connector.connect(
        host='localhost',  # alamat host MySQL
        user='root',       # username MySQL
        password='',       # password MySQL
        database='flightestdb'  # nama database di PHPMyAdmin
    )
    cursor = connection.cursor()

    if table_name == "arduino3":
        # query INSERT sesuai dengan struktur tabel "arduino3" di database
        query = "INSERT INTO arduino3 (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, degree_x, degree_y, degree_z) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    elif table_name == "android3":
        # query INSERT sesuai dengan struktur tabel "android3" di database
        query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    else:
        # Jika nama tabel tidak valid, tampilkan pesan kesalahan
        print(f"Invalid table name: {table_name}")
        return

    # Konversi data ke tipe float sepanjang jumlah kolom di tabel yang sesuai
    values = tuple(float(value) for value in data)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# ... (existing code)

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    # ... (existing code)

        # Kirim data yang berhasil didapat ke database MySQL (PHPMyAdmin)
        insert_data_to_database(list_akhir, table_name="arduino3")
        insert_data_to_database(list_akhir, table_name="android3")
        
        subscribed_data.clear()
        list_akhir.clear()

# ... (existing code)

# Start the MQTT network loop to process incoming messages
client.loop_start()

try:
    # Keep the script running until interrupted
    while True:
        pass
except KeyboardInterrupt:
    # Stop the MQTT network loop and disconnect from the broker when interrupted
    client.loop_stop()
    client.disconnect()
