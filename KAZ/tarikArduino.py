import csv
import paho.mqtt.client as mqtt
import os
if os.path.exists('./KAZ/mqtt_logs_ardu.csv'):
    os.remove('./KAZ/mqtt_logs_ardu.csv')

mqtt_port=18080
ininambah=0

subscribed_data = []
# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    
    # You can process or filter the data here before saving it to the CSV file
    
    # For simplicity, we'll save the topic and payload as-is
    if len(subscribed_data)==9:
        subscribed_data.sort()
        cleaned_payload = [value[2:] for value in subscribed_data]
        try:
            cleaned_payload = [value for value in cleaned_payload]
            subscribed_data.clear()
        except ValueError as e:
            print(f"Error converting data to float: {e}")
            return
        subscribed_data.extend(cleaned_payload)
        if len(subscribed_data) == 9:
            subscribed_data.append(ininambah)
            with open('./KAZ/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(subscribed_data)
            ininambah+=1
            subscribed_data.clear()
        
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
                  ('Arduino/6 Degree Freedom X |',2),
                  ('Arduino/6 Degree Freedom Y |',2),
                  ('Arduino/6 Degree Freedom Z |',2),
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
