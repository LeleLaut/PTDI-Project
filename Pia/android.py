import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

mqtt_broker = '0.tcp.ap.ngrok.io'
mqtt_port = 18080
ininambah = 0
csv_file_path = './PIA/mqtt_logs_android.csv'
list_akhir = []

if os.path.exists(csv_file_path):
    os.remove(csv_file_path)

# Fungsi untuk menyimpan data ke database MySQL (PHPMyAdmin)
def insert_data_to_database(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',  # Alamat host MySQL
            user='root',       # Username MySQL
            password='',       # Password MySQL
            database='flightestdb'  # Ganti dengan nama database yang telah Anda buat di PHPMyAdmin
        )
        cursor = connection.cursor()

        # Sesuaikan query INSERT sesuai dengan struktur tabel di database Anda
        query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Konversi data ke tipe float sepanjang 16
        values = tuple(float(value) for value in data)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error saat menyimpan data ke database: {e}")

# Callback saat klien menerima pesan dari broker
def on_message(client, userdata, message):
    global ininambah, list_akhir  # Tambahkan deklarasi global untuk variabel ininambah dan list_akhir
    topic = message.topic
    payload = message.payload.decode('utf-8')
    payload2 = payload.strip('[]')
    new_payload = payload2.replace('"', '')
    list_akhir = [float(item) for item in new_payload.split(',')]
    print(list_akhir)

    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(list_akhir) == 11:
        with open(csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(list_akhir)
        ininambah += 1

        # Kirim data yang berhasil didapat ke database MySQL (PHPMyAdmin)
        insert_data_to_database(list_akhir)

        list_akhir.clear()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

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
