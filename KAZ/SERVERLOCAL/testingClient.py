import socket
import json
import csv 

client_ip = ''  # Bind to all available network interfaces for receiving broadcast messages
client_port = 50000  # Replace with the desired port number

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Enable broadcasting mode for the socket
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the broadcast address and port number
client_socket.bind((client_ip, client_port))

print("Listening for broadcast messages...")
while True:
    # Receive data from the server
    data, server_address = client_socket.recvfrom(1024)
    received_list=json.loads(data.decode('utf-8'))
    with open('./KAZ/SERVERLOCAL/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(received_list)