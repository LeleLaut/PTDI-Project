import socket
import json
import csv
import os
import mysql.connector

if os.path.exists('./KAZ/SERVERLOCAL/mqtt_logs_ardu.csv'):
    os.remove('./KAZ/SERVERLOCAL/mqtt_logs_ardu.csv')

client_ip = ''  # Bind to all available network interfaces for receiving broadcast messages
client_port = 50000  # Replace with the desired port number

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enable broadcasting mode for the socket
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the broadcast address and port number
client_socket.bind((client_ip, client_port))

# Function to save data to MySQL database
def insert_data_to_database(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',  # MySQL host address
            user='root',       # MySQL username
            password='',       # MySQL password
            database='flightestdb'  # The name of the database 
        )
        cursor = connection.cursor()

        # Adjust the INSERT query according to the table structure in your database
        query = "INSERT INTO arduino (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, pitch, roll, yaw, counter) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 

        for item in data:
            # Convert each value from string to float before inserting into the database
            values = [float(value) for value in item]

            cursor.execute(query, tuple(values))
            connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while saving data to the database: {e}")

print("Listening for broadcast messages...")
while True:
    # Receive data from the server
    data, server_address = client_socket.recvfrom(1024)
    received_list = json.loads(data.decode('utf-8'))

    # Save the received data to the CSV file
    with open('./KAZ/SERVER LOCAL/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(received_list)

    # Insert the received data to the MySQL database
    insert_data_to_database([received_list])
