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
# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambahandro
    global ininambahardu
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
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
        
        
        # payload2=subscribed_data[9].strip('[]')
        # new_payload=payload2.replace('"','')
        # list_akhir = [item for item in new_payload.split(',')]
        # del subscribed_data[9] 
        # check9=subscribed_data[8].split()
        # if (check9[0]!='9'):
        #     subscribed_data.clear()
        #     list_akhir.clear()

        # cleaned_payload = [value[2:] for value in subscribed_data]
        # try:
        #     cleaned_payload = [value for value in cleaned_payload]
        #     subscribed_data.clear()
        # except ValueError as e:
        #     print(f"Error converting data to float: {e}")
        #     return
        # subscribed_data.extend(cleaned_payload)
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
        #     subscribed_data.append(ininambah)
        #     with open('./masterTjuy/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
        #         csv_writer = csv.writer(csvfile)
        #         csv_writer.writerow(subscribed_data)
        #     list_akhir.append(ininambah)
        #     with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
        #         csv_writer = csv.writer(csvfile)
        #         csv_writer.writerow(list_akhir)
        #     ininambah+=1
        
        # subscribed_data.clear()
        # list_akhir.clear()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

# Subscribe to the desired MQTT topic
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
