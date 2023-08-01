import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

if os.path.exists('./KAZ/mqtt_logs_andro.csv'):
    os.remove('./KAZ/mqtt_logs_andro.csv')

mqtt_port = 19716
ininambah = 0

list_akhir = []

# Function to save data to MySQL database (PHPMyAdmin)
def insert_data_to_database(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',   # MySQL host address
            user='root',        # MySQL username
            password='',        # MySQL password
            database='flightestdb'  # Replace with the name of the database you created in PHPMyAdmin
        )
        cursor = connection.cursor()

        # Adjust the INSERT query according to the table structure in your database
        query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Convert data to float with precision 2
        data_float = [[round(float(value), 2) for value in sublist] for sublist in data]

        cursor.executemany(query, data_float)
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
    payload2 = payload.strip('[]')
    new_payload = payload2.replace('"', '')
    # list_akhir = [float(item) for item in new_payload.split(',')]
    list_akhir = eval(payload)

    if len(list_akhir) == 5:
        for i, sublist in enumerate(list_akhir):
            # Check if all elements in sublist are numbers
            if all(isinstance(value, (int, float)) for value in sublist):
                list_akhir[i].append(ininambah)
                ininambah += 1
                with open('./KAZ/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(list_akhir[i])
                
        # Send the successfully received data to the MySQL database (PHPMyAdmin)
        # Filter data to only include numeric values before sending to the database
        numeric_data = [sublist for sublist in list_akhir if all(isinstance(value, (int, float)) for value in sublist)]
        insert_data_to_database(numeric_data)

        # Clear the list after sending data to the database
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
