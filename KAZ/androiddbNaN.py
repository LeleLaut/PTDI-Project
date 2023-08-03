import csv
import paho.mqtt.client as mqtt
import os
import json
import mysql.connector

if os.path.exists('./KAZ/SERVER LOCAL/mqtt_logs_android.csv'):
    os.remove('./KAZ/SERVER LOCAL/mqtt_logs_android.csv')

mqtt_port = 10153
ininambah = 0

def insert_data_to_database(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='flightestdb'
        )
        cursor = connection.cursor()

        query = "INSERT INTO arduino1 (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, pitch, roll, yaw, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 

        for item in data:
            values = [float(value) for value in item[:12]]  # Mengambil hanya 9 nilai pertama
            cursor.execute(query, tuple(values))
            connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while saving data to the database: {e}")

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah, list_akhir
    topic = message.topic
    payload = message.payload.decode('utf-8')

    formatted_data = f'[{payload.replace("][", "], [")}]'
    list_akhir = json.loads(formatted_data)
    print(list_akhir)

    if len(list_akhir) == 5:
        with open('./KAZ/SERVER LOCAL/mqtt_logs_android.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for list_terakhir in list_akhir:
                list_terakhir.append(ininambah)
                ininambah += 1
                # Replace NaN with 0
                list_terakhir = [float(value) if str(value) != 'nan' else 0.0 for value in list_terakhir]
                csv_writer.writerow(list_terakhir)

        # Replace NaN with 0 in the list_akhir before inserting to the database
        list_akhir = [[float(value) if str(value) != 'nan' else 0.0 for value in item] for item in list_akhir]

        # Insert the received data to the MySQL database
        insert_data_to_database(list_akhir)

        list_akhir.clear()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

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