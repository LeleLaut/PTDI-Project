import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

mqtt_broker = '0.tcp.ap.ngrok.io'
mqtt_port = 19716
csv_file_path = './PIA/mqtt_logs_arduino.csv'
subscribed_data = []

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
        query = "INSERT INTO arduino (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, degree_x, degree_y, degree_z) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # Convert data to float with precision 16
        values = tuple(map(float, data))

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error inserting data into the database: {e}")

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global subscribed_data
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)

    if len(subscribed_data) == 9:
        try:
            subscribed_data.sort()
            cleaned_payload = [value[2:] for value in subscribed_data]
            cleaned_payload = [float(value) for value in cleaned_payload]
        except ValueError as e:
            print(f"Error converting data to float: {e}")
            subscribed_data.clear()
            return

        # Send the successfully received data to the MySQL database (PHPMyAdmin)
        insert_data_to_database(cleaned_payload)

        # Save data to the CSV file
        with open(csv_file_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(cleaned_payload)

        subscribed_data.clear()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker, mqtt_port, 60)

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