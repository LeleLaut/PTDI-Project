import socket
import json
import csv 
import threading
import os

if os.path.exists('./KAZ/SERVERLOCAL/local_logs_ardu.csv'):
    os.remove('./KAZ/SERVERLOCAL/local_logs_ardu.csv')
if os.path.exists('./KAZ/SERVERLOCAL/mqtt_logs_andro.csv'):
    os.remove('./KAZ/SERVERLOCAL/mqtt_logs_andro.csv')
if os.path.exists('./KAZ/SERVERUP/mqtt_logs_ardu.csv'):
    os.remove('./KAZ/SERVERUP/mqtt_logs_ardu.csv')

def receive_broadcasts(port, csv_path):
    client_ip = ''
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    client_socket.bind((client_ip, port))
    print(f"Listening for broadcast messages on port {port}...")
    while True:
        data, server_address = client_socket.recvfrom(1024)
        received_list = json.loads(data.decode('utf-8'))
        with open(csv_path, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(received_list)

port_50000_thread = threading.Thread(target=receive_broadcasts, args=(50000, './KAZ/SERVERLOCAL/mqtt_logs_andro.csv'))
port_52222_thread = threading.Thread(target=receive_broadcasts, args=(52222, './KAZ/SERVERLOCAL/local_logs_ardu.csv'))
port_53333_thread = threading.Thread(target=receive_broadcasts, args=(53333, './KAZ/SERVERUP/mqtt_logs_ardu.csv'))

port_50000_thread.start()
port_52222_thread.start()
port_53333_thread.start()

port_50000_thread.join()
port_52222_thread.join()
port_53333_thread.join()
