import csv
import paho.mqtt.client as mqtt
import os
if os.path.exists('./masterTjuy/mqtt_logs_ardu.csv'):
    os.remove('./masterTjuy/mqtt_logs_ardu.csv')
if os.path.exists('./masterTjuy/mqtt_logs_andro.csv'):
    os.remove('./masterTjuy/mqtt_logs_andro.csv')


mqtt_port=14731

subscribed_data = []
# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(subscribed_data) == 10:
        subscribed_data.sort()
        print("\n AWIKWOK \n")
        print(subscribed_data)
        payload2=subscribed_data[9].strip('[]')
        new_payload=payload2.replace('"','')
        list_akhir = [item for item in new_payload.split(',')]
        del subscribed_data[9]
        print("\n DELWED \n")
        print(subscribed_data)
        with open('./masterTjuy/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(subscribed_data)
        with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(list_akhir)
        
        subscribed_data.clear()
        list_akhir.clear()
        print("\n NYEDOT \n")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

# Subscribe to the desired MQTT topic
client.subscribe([('Arduino/GYRO X |',0),
                  ('Arduino/GYRO Y |',0),
                  ('Arduino/GYRO Z |',0),
                  ('Arduino/ACC X |',0),
                  ('Arduino/ACC Y |',0),
                  ('Arduino/ACC Z |',0),
                  ('Arduino/6 Degree Freedom X |',0),
                  ('Arduino/6 Degree Freedom Y |',0),
                  ('Arduino/6 Degree Freedom Z |',0),
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
