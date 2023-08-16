import socket
import csv
import os
import json

if os.path.exists('./KAZ/SERVERLOCAL/local_logs_ardu.csv'):
    os.remove('./KAZ/SERVERLOCAL/local_logs_ardu.csv')

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
local_ip = s.getsockname()[0]
ip_components = local_ip.split('.')
modified_ip = '.'.join(ip_components[:-1] + ['255'])
broadcast_address = modified_ip
BROADCAST_IP = local_ip
PORT = 51111

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

while True:
    try:
        data, esp8266_address = receive_socket.recvfrom(1024)
        decoded_data = data.decode('utf-8')
        float_list = [float(number) for number in decoded_data.split(',')]
        float_list.append(ininambah)
        ininambah+=1
        with open('./KAZ/SERVERLOCAL/local_logs_ardu.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(float_list)
            serialized_data = json.dumps(float_list)
            server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
            print(f"Received data from ESP8266: {decoded_data} from {esp8266_address[0]} on port {esp8266_address[1]}")
    except socket.timeout:
        pass
receive_socket.close()
