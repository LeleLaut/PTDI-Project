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

def process_data(data):
    # Pembersihan data dari karakter yang tidak diinginkan
    cleaned_data = data.strip('[]').replace('"', '')
    # Pembagian data berdasarkan tanda koma
    data_list = cleaned_data.split(',')
    
    # Inisialisasi list untuk menyimpan data numerik
    numeric_data = []
    
    # Loop melalui data_list untuk mengambil nilai float yang benar
    for item in data_list:
        try:
            # Pisahkan nilai float dari teks tambahan seperti '1 ', '2 ', dll.
            numeric_value = float(item.split()[1])
            numeric_data.append(numeric_value)
        except ValueError as e:
            print(f"Error converting data to float: {e}")
            return None

    return numeric_data

def on_message(client, userdata, message):
    global ininambah, subscribed_data  # Tambahkan subscribed_data ke daftar variabel global
    topic = message.topic
    payload = message.payload.decode('utf-8')
    subscribed_data.append(payload)

    if len(subscribed_data) == 10:
        # Membuat list_akhir untuk data dari subscribed_data
        list_akhir = process_data(subscribed_data[9])
        if list_akhir is None:
            # Jika data tidak valid, hapus semua data yang diterima
            subscribed_data.clear()
            return

        subscribed_data = subscribed_data[:9]  # Hapus data terakhir dari subscribed_data

        # Proses subscribed_data lebih lanjut jika diperlukan...

        # Menyimpan data ke dalam file CSV
        with open('./masterTjuy/mqtt_logs_ardu.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(subscribed_data)
        print(subscribed_data)

        with open('./masterTjuy/mqtt_logs_andro.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(list_akhir)
        print(list_akhir)

        # Increment nilai ininambah
        ininambah += 1

        # Panggil fungsi insert_data_to_database di sini, setelah data sudah siap
        # Periksa topik untuk menentukan tabel yang sesuai
        if "arduino" in topic:
            # Pastikan subscribed_data memiliki 9 elemen untuk tabel "arduino"
            if len(subscribed_data) == 9:
                insert_data_to_database(subscribed_data, table_name="arduino")
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

# Inisialisasi MQTT client
client = mqtt.Client()

# Set callback untuk menerima pesan
client.on_message = on_message

# Koneksi ke broker MQTT
client.connect('0.tcp.ap.ngrok.io', mqtt_port, 60)

# Subscribe ke topik-topik yang diinginkan
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
    ('android', 0),  # Ganti QoS level dari 2 menjadi 0
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