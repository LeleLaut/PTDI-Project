import csv
import socket
import json
import threading
import paho.mqtt.client as mqtt
import os


ininambah=0
list_akhir=[]
# Function for handling the MQTT communication
def mqtt_communication():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to a specific IP address and port
    server_ip = '192.168.168.191'  # Bind to all available network interfaces
    server_port = 50000  # Replace with the desired port number
    server_socket.bind((server_ip, server_port))

    # Get the broadcast address
    broadcast_address = '192.168.168.255'

    if os.path.exists('./KAZ/SERVERLOCAL/mqtt_logs_android.csv'):
        os.remove('./KAZ/SERVERLOCAL/mqtt_logs_android.csv')

    mqtt_port=10153
    

    
    def on_message(client, userdata, message):
        global ininambah
        topic = message.topic
        payload = message.payload.decode('utf-8')

        formatted_data = f'[{payload.replace("][", "], [")}]'
        list_akhir = json.loads(formatted_data)

        if len(list_akhir) == 5:
            # list_akhir.append(ininambah)
            with open('./KAZ/SERVERLOCAL/mqtt_logs_android.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for list_terakhir in list_akhir:
                    csv_writer.writerow(list_terakhir)
                    list_terakhir.append(ininambah)
                    ininambah+=1
                    serialized_data = json.dumps(list_terakhir)
                    # Broadcast the serialized data to the client
                    server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
                    print(f"Broadcasted: {serialized_data}")


            list_akhir.clear()

    # Create an MQTT client instance
    client = mqtt.Client()

    # Set the callback for message reception
    client.on_message = on_message

    # Connect to the MQTT broker
    client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

    # Subscribe to the desired MQTT topics
    client.subscribe([('android', 2)])

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


# Function for handling the UDP broadcasting and receiving
def udp_communication():
    BROADCAST_IP = '192.168.168.191'
    PORT = 51111

    if os.path.exists('./KAZ/SERVERLOCAL/local_logs_ardu.csv'):
        os.remove('./KAZ/SERVERLOCAL/local_logs_ardu.csv')

    # Create a UDP socket
    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set socket options to allow broadcasting and reuse the address
    receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind the socket to the local address and port to receive messages
    receive_socket.bind((BROADCAST_IP, PORT))

    print(f"Listening for broadcasts from ESP8266 on port {PORT}")

    ininambah = 0
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

        except socket.timeout:
            pass

    # Close the socket (usually not reached in this example)
    receive_socket.close()


# Create and start the threads for both functions
mqtt_thread = threading.Thread(target=mqtt_communication)
udp_thread = threading.Thread(target=udp_communication)

mqtt_thread.start()
udp_thread.start()
