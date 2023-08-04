import csv
import paho.mqtt.client as mqtt
import os
import ssl
import socket
import pickle
import time
import json
import mysql.connector

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to a specific IP address and port
server_ip = '192.168.233.237'  # Bind to all available network interfaces
server_port = 50000  # Replace with the desired port number
server_socket.bind((server_ip, server_port))

# Get the broadcast address
broadcast_address = '192.168.168.255'

if os.path.exists('./KAZ/SERVERLOCAL/mqtt_logs_andro.csv'):
    os.remove('./KAZ/SERVERLOCAL/mqtt_logs_andro.csv')

mqtt_port=10153
ininambah=0

list_akhir=[]

# Open the database connection outside of the loop
def insert_data_to_database(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='flightestdb'
        )
        cursor = connection.cursor()

        query = "INSERT INTO android (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, pitch, roll, yaw, latitude, longitude, altitude, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 

        for item in data:
            values = [float(value) for value in item[:13]]
            cursor.execute(query, tuple(values))
            connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while saving data to the database: {e}")

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah
    topic = message.topic
    payload = message.payload.decode('utf-8')

    formatted_data = f'[{payload.replace("][", "], [")}]'
    list_akhir = json.loads(formatted_data)

    if len(list_akhir) == 5:
        # list_akhir.append(ininambah)
        with open('./KAZ/SERVERLOCAL/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for list_terakhir in list_akhir:
                csv_writer.writerow(list_terakhir)
                list_terakhir.append(ininambah)
                ininambah+=1
                serialized_data = json.dumps(list_terakhir)
                # Broadcast the serialized data to the client
                server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
                print(f"Broadcasted: {serialized_data}")

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
client.subscribe([('android',2),
                  
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
