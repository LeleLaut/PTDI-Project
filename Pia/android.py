import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

mqtt_broker = '0.tcp.ap.ngrok.io'
mqtt_port = 10208
ininambah = 0
csv_file_path = './PIA/mqtt_logs_android.csv'
list_akhir = []

if os.path.exists(csv_file_path):
    os.remove(csv_file_path)

# Function to save data to MySQL database (PHPMyAdmin)
def insert_data_to_database(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',  # MySQL host address
            user='root',       # MySQL username
            password='',       # MySQL password
            database='flightestdb'  # Replace with the name of the database you created in PHPMyAdmin
        )
        cursor = connection.cursor()

        # Adjust the INSERT query according to the table structure in your database
        query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Convert data to float with precision 16
        values = tuple(float(value) for value in data)

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while saving data to the database: {e}")

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah, list_akhir  # Add global declarations for the ininambah and list_akhir variables
    topic = message.topic
    payload = message.payload.decode('utf-8')
    payload2 = payload.strip('[]')
    new_payload = payload2.replace('"', '')
    list_akhir = [float(item) for item in new_payload.split(',')]

    if len(list_akhir) == 11:
        with open(csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(list_akhir)
        ininambah += 1

        # Send the successfully received data to the MySQL database (PHPMyAdmin)
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