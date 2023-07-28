import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

if os.path.exists('./masterTjuy/mqtt_logs_ardu.csv'):
    os.remove('./masterTjuy/mqtt_logs_ardu.csv')
if os.path.exists('./masterTjuy/mqtt_logs_andro.csv'):
    os.remove('./masterTjuy/mqtt_logs_andro.csv')

mqtt_port=13533
ininambah=0

subscribed_data = []

def insert_data_to_database(data, table_name):
    connection = mysql.connector.connect(
        host='localhost',  # alamat host MySQL
        user='root',       # username MySQL
        password='',       # password MySQL
        database='flightestdb'  # nama database di PHPMyAdmin
    )
    cursor = connection.cursor()

    if table_name == "arduino":
        # kueri INSERT sesuai dengan struktur tabel "arduino3" di database
        query = "INSERT INTO arduino (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, degree_x, degree_y, degree_z) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    elif table_name == "android3":
        # kueri INSERT sesuai dengan struktur tabel "android3" di database
        query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    else:
        # Jika nama tabel tidak valid, tampilkan pesan kesalahan
        print(f"Nama tabel tidak valid: {table_name}")
        return

    # Eksekusi kueri dengan menggunakan placeholder dan tupel nilai numerik
    cursor.execute(query, data)
    connection.commit()

    cursor.close()
    connection.close()


# Callback when the client receives a message from the broker
# Callback when the client receives a message from the broker
def on_message(client, userdata, message):
    global ininambah
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    
    # You can process or filter the data here before saving it to the CSV file
    # For simplicity, we'll save the topic and payload as-is
    if len(subscribed_data) == 10:
        subscribed_data.sort()
        payload2 = subscribed_data[9].strip('[]')
        new_payload = payload2.replace('"', '')
        list_akhir = [item for item in new_payload.split(',')]
        del subscribed_data[9]
        check9 = subscribed_data[8].split()
        if check9[0] != '9':
            subscribed_data.clear()
            list_akhir.clear()

        cleaned_payload = [value[2:] for value in subscribed_data]
        try:
            cleaned_payload = [value for value in cleaned_payload]
            subscribed_data.clear()
        except ValueError as e:
            print(f"Error converting data to float: {e}")
            return
        subscribed_data.extend(cleaned_payload)
        print(subscribed_data)
        if len(subscribed_data) == 9 and len(list_akhir) == 11:
            subscribed_data.append(ininambah)
            with open('./masterTjuy/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(subscribed_data)
            print(subscribed_data)
            list_akhir.append(ininambah)
            with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(list_akhir)
            # print(list_akhir)
            ininambah += 1

            # Panggil fungsi insert_data_to_database di sini, setelah data sudah siap
            # Periksa topik untuk menentukan tabel yang sesuai
            if "arduino" in topic:
                # Pastikan list_akhir memiliki 9 elemen untuk tabel "arduino"
                if len(list_akhir) == 9:
                    insert_data_to_database(list_akhir, table_name="arduino")
                else:
                    print("Jumlah elemen tidak sesuai dengan tabel 'arduino'")
            elif "android" in topic:
                # Pastikan list_akhir memiliki 11 elemen untuk tabel "android3"
                if len(list_akhir) == 11:
                    insert_data_to_database(list_akhir, table_name="android3")
                else:
                    print("Jumlah elemen tidak sesuai dengan tabel 'android3'")

            # Bersihkan daftar setelah menyimpan data
            subscribed_data.clear()
            list_akhir.clear()

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

    client.loop_start()