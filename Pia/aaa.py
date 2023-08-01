import csv
import paho.mqtt.client as mqtt
import os
import ssl
if os.path.exists('./PIA/mqtt_logs_android.csv'):
    os.remove('./PIA/mqtt_logs_android.csv')

mqtt_port=19716
ininambah=0

list_akhir=[]
# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah
    topic = message.topic
    payload = message.payload.decode('utf-8')
    payload2=payload.strip('[]')
    new_payload=payload2.replace('"','')
    # list_akhir = [float(item) for item in new_payload.split(',')]
    list_akhir=eval(payload)

    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(list_akhir) == 5:
        # list_akhir.append(ininambah)
        for i, sublist in enumerate(list_akhir):
            list_akhir[i].append(ininambah)
            ininambah+=1
            with open('./PIA/mqtt_logs_android.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(list_akhir[i])
 
        list_akhir.clear()
        
# Create an MQTT client instance
client = mqtt.Client()


# Set the callback for message reception
client.on_message = on_message

# Connect to the MQTT broker
client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

# Subscribe to the desired MQTT topic
client.subscribe([('android',2),])

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
