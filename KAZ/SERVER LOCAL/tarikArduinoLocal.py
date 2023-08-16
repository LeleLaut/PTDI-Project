import csv
import paho.mqtt.client as mqtt
import os
import ast
import socket
import pickle
import time
import json

if os.path.exists('./KAZ/SERVER LOCAL/mqtt_logs_ardu.csv'):
    os.remove('./KAZ/SERVER LOCAL/mqtt_logs_ardu.csv')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
server_ip = '192.168.168.191'
server_port = 50000
server_socket.bind((server_ip, server_port))
broadcast_address = '192.168.168.255'
mqtt_port=10153
ininambah=0
subscribed_data = []
def on_message(client, userdata, message):
    global ininambah
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    if len(subscribed_data)==9:
        subscribed_data.sort()
        processed_data = [ast.literal_eval(s.split(' ', 1)[1]) for s in subscribed_data]
        num_rows = len(processed_data)
        num_columns = len(processed_data[0])
        result_lists = [[] for _ in range(num_columns)]
        for i in range(num_rows):
            for j in range(num_columns):
                result_lists[j].append(processed_data[i][j])

        if len(subscribed_data) == 9:
            with open('./KAZ/SERVER LOCAL/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for result_list in result_lists:
                    result_list.append(ininambah)
                    ininambah+=1
                    csv_writer.writerow(result_list)
                    serialized_data = json.dumps(result_list)

                    # Broadcast the serialized data to the client
                    server_socket.sendto(serialized_data.encode('utf-8'), (broadcast_address, server_port))
                    print(f"Broadcasted: {result_list}")

            subscribed_data.clear()
        
client = mqtt.Client()

client.on_message = on_message

client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

client.subscribe([('Arduino/GYRO X |',2),
                  ('Arduino/GYRO Y |',2),
                  ('Arduino/GYRO Z |',2),
                  ('Arduino/ACC X |',2),
                  ('Arduino/ACC Y |',2),
                  ('Arduino/ACC Z |',2),
                  ('Arduino/P |',2),
                  ('Arduino/R |',2),
                  ('Arduino/Y |',2),
                  ])

client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
