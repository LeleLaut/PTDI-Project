import csv
import paho.mqtt.client as mqtt
import os

if os.path.exists('./masterTjuy/mqtt_logs_ardu.csv'):
    os.remove('./masterTjuy/mqtt_logs_ardu.csv')
if os.path.exists('./masterTjuy/mqtt_logs_andro.csv'):
    os.remove('./masterTjuy/mqtt_logs_andro.csv')

mqtt_port = 14731
ininambah = 0

subscribed_data = []
list_akhir = []
check9 = []

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah, subscribed_data, list_akhir, check9
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)

    if topic == 'android':
        # For the android topic, we directly append the data to list_akhir
        payload2 = subscribed_data[-1].strip('[]')
        new_payload = payload2.replace('"', '')
        list_akhir = [item for item in new_payload.split(',')]
        check9 = list_akhir[8].split()
        subscribed_data.clear()
    else:
        # For other topics, we check if the length of subscribed_data is 10 before processing
        if len(subscribed_data) == 10:
            payload2 = subscribed_data[-1].strip('[]')
            new_payload = payload2.replace('"', '')
            list_akhir = [item for item in new_payload.split(',')]
            check9 = subscribed_data[8].split()
            subscribed_data.pop()

            # Data cleaning: Remove first two digits from each value and split the payload by comma
            cleaned_payload = [value[2:] for value in subscribed_data]

            # Convert the values to float
            try:
                cleaned_payload = [float(value) for value in cleaned_payload]
            except ValueError as e:
                print(f"Error converting data to float: {e}")
                return

            subscribed_data.extend(cleaned_payload)

    if len(subscribed_data) == 9 and len(list_akhir) == 11 and check9[0] != '9':
        subscribed_data.append(ininambah)
        with open('./masterTjuy/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(subscribed_data)

        list_akhir.append(ininambah)
        with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(list_akhir)

        ininambah += 1

        subscribed_data.clear()
        list_akhir.clear()

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

# Subscribe to the desired MQTT topic
client.subscribe([
    ('Arduino/GYRO X |', 0),
    ('Arduino/GYRO Y |', 0),
    ('Arduino/GYRO Z |', 0),
    ('Arduino/ACC X |', 0),
    ('Arduino/ACC Y |', 0),
    ('Arduino/ACC Z |', 0),
    ('Arduino/6 Degree Freedom X |', 0),
    ('Arduino/6 Degree Freedom Y |', 0),
    ('Arduino/6 Degree Freedom Z |', 0),
    ('android', 2),
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