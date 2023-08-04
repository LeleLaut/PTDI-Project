import socket
import csv
import os
import json
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Connect to a public IP address (e.g., Google's DNS server) to get the local IP
s.connect(("8.8.8.8", 80))
# Get the local IP address
local_ip = s.getsockname()[0]
# Replace 'BROADCAST_IP' and 'PORT' with the appropriate values
BROADCAST_IP = local_ip
PORT = 51111

if os.path.exists('./KAZ/SERVERLOCAL/local_logs_ardu.csv'):
    os.remove('./KAZ/SERVERLOCAL/local_logs_ardu.csv')
ininambah=0

receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

receive_socket.bind((BROADCAST_IP, PORT))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

server_ip = local_ip
server_port = 52222
server_socket.bind((server_ip, server_port))

ip_components = local_ip.split('.')
# Change the last three digits to '255'
modified_ip = '.'.join(ip_components[:-1] + ['255'])
broadcast_address = modified_ip

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
        with open('./KAZ/SERVERLOCAL/local_logs_ardu.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(float_list)
            serialized_data = json.dumps(float_list)
            server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
            print(f"Broadcasted: {serialized_data}")
    
    except socket.timeout:
        # Timeout occurred, no data received
        pass

# Close the socket (usually not reached in this example)
receive_socket.close()
