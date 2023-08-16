import threading
import socket
import csv
import os
import json
import paho.mqtt.client as mqtt

def udp_server_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    ip_components = local_ip.split('.')
    modified_ip = '.'.join(ip_components[:-1] + ['255'])
    broadcast_address = modified_ip

    BROADCAST_IP = local_ip
    PORT = 51111

    if os.path.exists('./KAZ/SERVERLOCAL/local_logs_ardu.csv'):
        os.remove('./KAZ/SERVERLOCAL/local_logs_ardu.csv')
    ininambah = 0

    receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    receive_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    receive_socket.bind((BROADCAST_IP, PORT))

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_ip = local_ip
    server_port = 52222
    server_socket.bind((server_ip, server_port))

    print(f"Listening for broadcasts from ESP8266 on port {PORT}")

    while True:
        try:
            data, esp8266_address = receive_socket.recvfrom(1024)
            decoded_data = data.decode('utf-8')
            float_list = [float(number) for number in decoded_data.split(',')]
            float_list.append(ininambah)
            ininambah += 1
            with open('./KAZ/SERVERLOCAL/local_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(float_list)
                serialized_data = json.dumps(float_list)
                server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
                print(f"Received data from ESP8266: {decoded_data} from {esp8266_address[0]} on port {esp8266_address[1]}")
        except socket.timeout:
            pass
    receive_socket.close()

def mqtt_client_thread():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    ip_components = local_ip.split('.')
    modified_ip = '.'.join(ip_components[:-1] + ['255'])
    broadcast_address = modified_ip
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_ip = local_ip
    server_port = 50000
    server_socket.bind((server_ip, server_port))
    broadcast_address = modified_ip

    if os.path.exists('./KAZ/SERVERLOCAL/mqtt_logs_android.csv'):
        os.remove('./KAZ/SERVERLOCAL/mqtt_logs_android.csv')

    mqtt_port = 17149
    ininambah = 0
    list_akhir = []

    def on_message(client, userdata, message):
        nonlocal ininambah
        topic = message.topic
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
                    serialized_data = json.dumps(list_terakhir)
                    server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
                    print(f"Broadcasted: {serialized_data}")
            list_akhir.clear()

    client = mqtt.Client()
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

if __name__ == "__main__":
    udp_thread = threading.Thread(target=udp_server_thread)
    mqtt_thread = threading.Thread(target=mqtt_client_thread)

    udp_thread.start()
    mqtt_thread.start()

    udp_thread.join()
    mqtt_thread.join()
