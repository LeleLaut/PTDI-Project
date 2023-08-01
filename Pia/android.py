import csv
import paho.mqtt.client as mqtt
import os
import ssl
import mysql.connector

if os.path.exists('./PIA/mqtt_logs_android.csv'):
    os.remove('./PIA/mqtt_logs_android.csv')

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
        query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude, ininambah) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        # Convert data to float with precision 2
        data_float = [[round(float(value), 2) for value in sublist] for sublist in data]

        cursor.executemany(query, data_float)
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while saving data to the database: {e}")

def on_message(client, userdata, message):
    global ininambah, list_akhir
    topic = message.topic
    payload = message.payload.decode('utf-8')
    
    try:
        data = eval(payload)  # Convert the payload to a Python list
        if len(data) == 11 and all(isinstance(value, (int, float)) for value in data):
            data = [float(value) for value in data]  # Convert elements to float
            data.append(ininambah)
            ininambah += 1
            with open('./PIA/mqtt_logs_android.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(data)
            insert_data_to_database([data])  # Send the data to the database as a list of lists

            # Log pesan masuk dan data ditulis ke file CSV
            print(f"Received MQTT message: {data}")
            print("Data written to CSV file.")
        else:
            print("Received MQTT message does not meet the condition for writing to CSV.")

    except Exception as e:
        print(f"Error while processing message: {e}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

# Subscribe to the desired MQTT topic
client.subscribe('android')

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