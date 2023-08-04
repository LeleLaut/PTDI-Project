import csv
import socket
import json
import threading
import paho.mqtt.client as mqtt
import os

ininambah = 0
list_akhir = []

# Function for handling the MQTT communication
def mqtt_communication():
    mqtt_port = 10153
    client = mqtt.Client()

    def on_message(client, userdata, message):
        global ininambah
        payload = message.payload.decode('utf-8')
        formatted_data = f'[{payload.replace("][", "], [")}]'
        list_akhir = json.loads(formatted_data)

        if len(list_akhir) == 5:
            with open('./KAZ/SERVERLOCAL/mqtt_logs_android.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for list_terakhir in list_akhir:
                    csv_writer.writerow(list_terakhir)
                    list_terakhir.append(ininambah)
                    ininambah += 1
                    # serialized_data = json.dumps(list_terakhir)
                    # # Broadcast the serialized data to the client
                    # server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
                    # print(f"Broadcasted MQTT: {serialized_data}")

        list_akhir.clear()

    client.on_message = on_message
    client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)
    client.subscribe([('android', 2)])
    client.loop_start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()


# Function for handling the UDP broadcasting and receiving from ESP8266
def udp_communication():
    global ininambah
    BROADCAST_IP = '192.168.168.191'
    PORT = 51111

    if os.path.exists('./KAZ/SERVERLOCAL/local_logs_ardu.csv'):
        os.remove('./KAZ/SERVERLOCAL/local_logs_ardu.csv')

    # Create a UDP socket for receiving data from ESP8266
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
            decoded_data = data.decode('utf-8')
            float_list = [float(number) for number in decoded_data.split(',')]
            float_list.append(ininambah)
            ininambah += 1
            with open('./KAZ/SERVERLOCAL/local_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(float_list)

            # Broadcast both the received message and MQTT data using UDP
            # Combine the MQTT and ESP8266 data into a single message
            mqtt_data = "your mqtt message here"  # Replace with the actual MQTT message
            combined_data = f"{mqtt_data},{decoded_data}"
            receive_socket.sendto(combined_data.encode('utf-8'), (broadcast_address, server_port))

        except socket.timeout:
            pass

    # Close the socket (usually not reached in this example)
    receive_socket.close()


# Function for handling the UDP broadcasting of both MQTT and ESP8266 data
def broadcast_data():
    # Create a UDP socket for broadcasting
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to a specific IP address and port
    server_ip = '192.168.168.191'  # Bind to all available network interfaces
    server_port = 50000  # Replace with the desired port number
    server_socket.bind((server_ip, server_port))

    # Get the broadcast address
    broadcast_address = '192.168.168.255'

    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass


# Create and start the threads for all functions
mqtt_thread = threading.Thread(target=mqtt_communication)
udp_receive_thread = threading.Thread(target=udp_communication)
broadcast_thread = threading.Thread(target=broadcast_data)

mqtt_thread.start()
udp_receive_thread.start()
broadcast_thread.start()

# Wait for all threads to finish
mqtt_thread.join()
udp_receive_thread.join()
broadcast_thread.join()
