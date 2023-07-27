import csv
import paho.mqtt.client as mqtt
import os
import mysql.connector

if os.path.exists('./masterTjuy/mqtt_logs_ardu.csv'):
    os.remove('./masterTjuy/mqtt_logs_ardu.csv')
if os.path.exists('./masterTjuy/mqtt_logs_andro.csv'):
    os.remove('./masterTjuy/mqtt_logs_andro.csv')

mqtt_port = 13533
ininambah = 0

subscribed_data = []

def insert_data_to_database(data, table_name):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='flightestdb'
        )
        cursor = connection.cursor()

        if table_name == "arduino":
            query = "INSERT INTO arduino (gyro_x, gyro_y, gyro_z, acc_x, acc_y, acc_z, degree_x, degree_y, degree_z) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        elif table_name == "android3":
            query = "INSERT INTO android3 (gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, sumbu_x, sumbu_y, sumbu_z, latitude, longitude) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        else:
            print(f"Nama tabel tidak valid: {table_name}")
            return

        cursor.executemany(query, data)
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Terjadi kesalahan saat menyisipkan data ke dalam database: {err}")

    finally:
        cursor.close()
        connection.close()

def on_message(client, userdata, message):
    global ininambah
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)
    
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
                  ('android',0),  # Ganti QoS level dari 2 menjadi 0
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