import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

if os.path.exists('mqtt_logs_andro.csv'):
    os.remove('mqtt_logs_andro.csv')

list_akhir = []  # Tambahkan variabel global list_akhir

# Fungsi untuk menyimpan data ke database MySQL (PHPMyAdmin)
def insert_data_to_database(data):
    connection = mysql.connector.connect(
        host='localhost',  # Alamat host MySQL
        user='root',       # Username MySQL
        password='',       # Password MySQL
        database='flightestdb'  # Ganti dengan nama database yang telah Anda buat di PHPMyAdmin
    )
    cursor = connection.cursor()

    # Sesuaikan query INSERT sesuai dengan struktur tabel di database Anda
    query = "INSERT INTO android2 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    
    # Konversi data ke tipe float sepanjang 16
    values = tuple(float(value) for value in data)

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global list_akhir  # Tambahkan deklarasi global untuk variabel list_akhir
    topic = message.topic
    payload = message.payload.decode('utf-8')
    payload2 = payload.strip('[]')
    new_payload = payload2.replace('"', '')
    list_akhir = [float(item) for item in new_payload.split(',')]

    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(list_akhir) == 11:
        with open('mqtt_logs_andro.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(list_akhir)

        # Kirim data yang berhasil didapat ke database MySQL (PHPMyAdmin)
        insert_data_to_database(list_akhir)

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', 14731, 60)

# Subscribe to the desired MQTT topic
client.subscribe([('android', 2)])

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
