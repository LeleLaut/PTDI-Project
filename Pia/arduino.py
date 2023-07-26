import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

if os.path.exists('mqtt_logs.csv'):
    os.remove('mqtt_logs.csv')

subscribed_data = []

# Fungsi untuk menyimpan data ke database MySQL (PHPMyAdmin)
def insert_data_to_database(data):
    connection = mysql.connector.connect(
        host='localhost',  # alamat host MySQL
        user='root',       # username MySQL
        password='',       # password MySQL
        database='flightestdb'  # nama database di PHPMyAdmin
    )
    cursor = connection.cursor()

    # query INSERT sesuai dengan struktur tabel di database
    query = "INSERT INTO arduino (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, degree_x, degree_y, degree_z) " \
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # Konversi data ke tipe float sepanjang 16
    values = tuple(map(float, data))

    cursor.execute(query, values)
    connection.commit()

    cursor.close()
    connection.close()

# Callback saat klien menerima pesan dari broker
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')

    # Data cleaning: Remove first two digits from each value and split the payload by comma
    cleaned_payload = [value[2:] for value in payload.split(',')]

    # Convert the values to float
    try:
        cleaned_payload = [float(value) for value in cleaned_payload]
    except ValueError as e:
        print(f"Error converting data to float: {e}")
        return

    subscribed_data.extend(cleaned_payload)

    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(subscribed_data) == 9:
        with open('mqtt_logs.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(subscribed_data)

        # Kirim data yang berhasil didapat ke database MySQL (PHPMyAdmin)
        insert_data_to_database(subscribed_data)

        subscribed_data.clear()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', 14731, 60)

# Subscribe to the desired MQTT topic
client.subscribe([
    ('Arduino/GYRO X |', 2),
    ('Arduino/GYRO Y |', 2),
    ('Arduino/GYRO Z |', 2),
    ('Arduino/ACC X |', 2),
    ('Arduino/ACC Y |', 2),
    ('Arduino/ACC Z |', 2),
    ('Arduino/6 Degree Freedom X |', 2),
    ('Arduino/6 Degree Freedom Y |', 2),
    ('Arduino/6 Degree Freedom Z |', 2),
])

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