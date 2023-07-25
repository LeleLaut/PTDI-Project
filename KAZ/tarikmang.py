import csv
import paho.mqtt.client as mqtt
import os
if os.path.exists('mqtt_logs.csv'):
    os.remove('mqtt_logs.csv')

subscribed_data = []
# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(subscribed_data) == 3:
        with open('mqtt_logs.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(subscribed_data)
        subscribed_data.clear()
# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', 10968, 60)

# Subscribe to the desired MQTT topic
client.subscribe([('Arduino/6 Degree Freedom X | P : ',0),('Arduino/6 Degree Freedom Y | R : ',1),('Arduino/6 Degree Freedom Z | Y : ',2)])

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
