import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector
if os.path.exists('./PIA/mqtt_logs_android.csv'):
    os.remove('./PIA/mqtt_logs_android.csv')

mqtt_port=19716
ininambah=0

list_akhir=[]

def insert_data_to_database(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',   # MySQL host address
            user='root',        # MySQL username
            password='',        # MySQL password
            database='flightestdb'  # Replace with the name of the database you created in PHPMyAdmin
        )
        cursor = connection.cursor()

        # Adjust the INSERT query according to the table structure in your database
        query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.executemany(query, data)
        connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Error while saving data to the database: {e}")

# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah
    global list_akhir
    topic = message.topic
    payload = message.payload.decode('utf-8')
    payload_values = payload.strip('[]').split(',')
    
    # Remove double quotes from each item in the payload
    payload_values = [item.replace('"', '') for item in payload_values]

    # Convert payload_values to float
    list_akhir = [float(item) for item in payload_values]

    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(list_akhir) == 5:
        list_akhir.append(ininambah)
        ininambah += 1
        with open('./PIA/mqtt_logs_android.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(list_akhir)

        # Convert the sublist to a tuple before inserting into the database
        data_to_insert = tuple(list_akhir)

        # Send the successfully received data to the MySQL database (PHPMyAdmin)
        insert_data_to_database([data_to_insert])

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
