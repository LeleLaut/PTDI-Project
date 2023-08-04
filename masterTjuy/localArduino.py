import socket
import csv
import os

# Replace 'BROADCAST_IP' and 'PORT' with the appropriate values
BROADCAST_IP = '192.168.168.191'
PORT = 51111

if os.path.exists('mqtt_logs_ardu.csv'):
    os.remove('mqtt_logs_ardu.csv')
ininambah=0
# Create a UDP socket
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set socket options to allow broadcasting and reuse the address
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to the local address and port to receive messages
receive_socket.bind((BROADCAST_IP, PORT))

print(f"Listening for broadcasts from ESP8266 on port {PORT}")

while True:
    try:
        # Receive data from the broadcast
        data, esp8266_address = receive_socket.recvfrom(1024)  # 1024 is the buffer size

        # Decode the received data as UTF-8
        decoded_data = data.decode('utf-8')
        float_list = [float(number) for number in decoded_data.split(',')]
        # print(type(float_list))
        # print(float_list)
        # Process and display the received data
        # print(f"Received data from ESP8266: {decoded_data} from {esp8266_address[0]}")
        float_list.append(ininambah)
        ininambah+=1
        with open('mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(float_list)
    
    except socket.timeout:
        # Timeout occurred, no data received
        pass

# Close the socket (usually not reached in this example)
receive_socket.close()
