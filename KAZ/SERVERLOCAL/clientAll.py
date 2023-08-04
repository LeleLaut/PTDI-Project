import socket
import json
import csv 
import threading

# Function to receive broadcasts on port 50000
def receive_broadcasts(port):
    client_ip = ''  # Bind to all available network interfaces for receiving broadcast messages

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcasting mode for the socket
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to the broadcast address and port number
    client_socket.bind((client_ip, port))

    print(f"Listening for broadcast messages on port {port}...")
    while True:
        # Receive data from the server
        data, server_address = client_socket.recvfrom(1024)
        received_list = json.loads(data.decode('utf-8'))
        if port==50000:
            with open('./KAZ/SERVERLOCAL/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(received_list)
        
        if port==52222:
            with open('./KAZ/SERVERLOCAL/local_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(received_list)


# Create and start the threads for both ports
port_50000_thread = threading.Thread(target=receive_broadcasts, args=(50000,))
port_51111_thread = threading.Thread(target=receive_broadcasts, args=(52222,))

port_50000_thread.start()
port_51111_thread.start()

# Wait for both threads to finish
port_50000_thread.join()
port_51111_thread.join()
