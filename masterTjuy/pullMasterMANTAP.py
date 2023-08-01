import csv
import paho.mqtt.client as mqtt
import os
import ast

if os.path.exists('./masterTjuy/mqtt_logs_ardu.csv'):
    os.remove('./masterTjuy/mqtt_logs_ardu.csv')
if os.path.exists('./masterTjuy/mqtt_logs_andro.csv'):
    os.remove('./masterTjuy/mqtt_logs_andro.csv')

mqtt_port=19716
ininambahandro=0
ininambahardu=0

subscribed_data = []

def on_message(client, userdata, message):
    global ininambahandro
    global ininambahardu
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    if len(subscribed_data) == 10:
        subscribed_data.sort()

        list_akhir=eval(subscribed_data[9])
        subscribed_data.pop()

        processed_data = [ast.literal_eval(s.split(' ', 1)[1]) for s in subscribed_data]
        num_rows = len(processed_data)
        num_columns = len(processed_data[0])
        result_lists = [[] for _ in range(num_columns)]

        for i in range(num_rows):
            for j in range(num_columns):
                result_lists[j].append(processed_data[i][j])
        
        if (len(subscribed_data)==9) and (len(list_akhir)==5):
            with open('./masterTjuy/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                for result_list in result_lists:
                    result_list.append(ininambahardu)
                    ininambahardu+=1
                    csv_writer.writerow(result_list)

            for i, sublist in enumerate(list_akhir):
                list_akhir[i].append(ininambahandro)
                ininambahandro+=1
                with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(list_akhir[i])

            list_akhir.clear()
            subscribed_data.clear()


            list_akhir.clear()

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
                  ('android',2),
                  ])

client.loop_start()

try:
    while True:
        pass
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
