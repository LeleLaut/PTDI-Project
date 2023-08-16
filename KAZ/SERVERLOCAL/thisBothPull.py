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

    mqtt_port = 1883
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
    client.connect('test.mosquitto.org', mqtt_port, 60)
    client.subscribe([('android', 2)])

    client.loop_start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()

def third_thread():
    if os.path.exists('./KAZ/SERVERUP/mqtt_logs_ardu.csv'):
        os.remove('./KAZ/SERVERUP/mqtt_logs_ardu.csv')

    mqtt_port = 1883
    udp_broadcast_port = 53333  # New UDP broadcast port
    ininambah = 0

    subscribed_data = []

    def on_message(client, userdata, message):
        nonlocal ininambah
        topic = message.topic
        payload = message.payload.decode('utf-8')
        subscribed_data.append(payload)
        if len(subscribed_data) == 9:
            subscribed_data.sort()
            processed_data = [ast.literal_eval(s.split(' ', 1)[1]) for s in subscribed_data]

            num_rows = len(processed_data)
            num_columns = len(processed_data[0])

            result_lists = [[] for _ in range(num_columns)]

            for i in range(num_rows):
                for j in range(num_columns):
                    result_lists[j].append(processed_data[i][j])

            if len(subscribed_data) == 9:
                with open('./KAZ/SERVERUP/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    for result_list in result_lists:
                        result_list.append(ininambah)
                        ininambah += 1
                        csv_writer.writerow(result_list)

                # Broadcasting using UDP
                serialized_data = json.dumps(result_lists)
                udp_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                udp_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
                udp_broadcast_socket.sendto(serialized_data.encode('utf-8'), ('<broadcast>', udp_broadcast_port))
                udp_broadcast_socket.close()

                subscribed_data.clear()

    client = mqtt.Client()

    client.on_message = on_message

    client.connect('test.mosquitto.org', mqtt_port, 60)

    client.subscribe([
        ('Telkom/Arduino/GYRO X |', 2),
        ('Telkom/Arduino/GYRO Y |', 2),
        ('Telkom/Arduino/GYRO Z |', 2),
        ('Telkom/Arduino/ACC X |', 2),
        ('Telkom/Arduino/ACC Y |', 2),
        ('Telkom/Arduino/ACC Z |', 2),
        ('Telkom/Arduino/P |', 2),
        ('Telkom/Arduino/R |', 2),
        ('Telkom/Arduino/Y |', 2),
    ])

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
    third_thread = threading.Thread(target=third_thread)  # New thread

    udp_thread.start()
    mqtt_thread.start()
    third_thread.start()  # Start the new thread

    udp_thread.join()
    mqtt_thread.join()
    third_thread.join()  # Wait for the new thread to complete