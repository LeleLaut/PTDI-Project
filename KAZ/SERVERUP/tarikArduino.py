import csv
import paho.mqtt.client as mqtt
import os
import ast

if os.path.exists('./KAZ/SERVERUP/mqtt_logs_ardu.csv'):
    os.remove('./KAZ/SERVERUP/mqtt_logs_ardu.csv')

mqtt_port=14897
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
            with open('./KAZ/SERVERUP/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for result_list in result_lists:
                    result_list.append(ininambah)
                    ininambah+=1
                    csv_writer.writerow(result_list)

            subscribed_data.clear()
        
client = mqtt.Client()

client.on_message = on_message

client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

client.subscribe([('Arduino/Telkom/GYRO X |',2),
                  ('Arduino/Telkom/GYRO Y |',2),
                  ('Arduino/Telkom/GYRO Z |',2),
                  ('Arduino/Telkom/ACC X |',2),
                  ('Arduino/Telkom/ACC Y |',2),
                  ('Arduino/Telkom/ACC Z |',2),
                  ('Arduino/Telkom/P |',2),
                  ('Arduino/Telkom/R |',2),
                  ('Arduino/Telkom/Y |',2),
                  ])

client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
