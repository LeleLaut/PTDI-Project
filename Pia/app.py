from flask import Flask, request, jsonify
import paho.mqtt.client as mqtt
import mysql.connector

app = Flask(__name__)

# Konfigurasi koneksi MySQL
mysql_host = "localhost"
mysql_user = "db_user"
mysql_password = "db_password"
mysql_database = "db_name"

# Fungsi untuk memasukkan data ke database MySQL
def insert_data_to_mysql(data):
    try:
        connection = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_database
        )

        cursor = connection.cursor()
        sql_query = "INSERT INTO data_sensor (sensor_name, value) VALUES (%s, %s)"
        cursor.execute(sql_query, (data['sensor_name'], data['value']))
        connection.commit()
        cursor.close()

    except mysql.connector.Error as error:
        print("Error: {}".format(error))

    finally:
        if connection.is_connected():
            connection.close()

# Fungsi callback ketika pesan MQTT diterima
def on_message(client, userdata, message):
    payload = str(message.payload.decode("utf-8"))
    # Parsing data dari payload (contoh: JSON)
    data = {
        "sensor_name": "sensor1",
        "value": payload,
    }
    insert_data_to_mysql(data)

# Konfigurasi koneksi MQTT dan subscribe ke topik
client = mqtt.Client()
client.connect("0.tcp.ap.ngrok.io", 19636)
client.subscribe("sensor_topic")
client.on_message = on_message

# Callback untuk rute API menerima data dari subscriber MQTT
@app.route('/mqtt-data', methods=['POST'])
def receive_mqtt_data():
    try:
        data = request.get_json()
        sensor_name = data['sensor_name']
        value = data['value']
        # Lakukan operasi apa pun dengan data yang diterima dari subscriber MQTT
        # (opsional: validasi, olah data, dan sebagainya)
        # Misalnya, Anda bisa langsung menyimpannya ke database atau melakukan pengolahan lain.

        # Mengirimkan data ke subscriber MQTT (opsional, jika diperlukan oleh aplikasi)
        # client.publish("response_topic", "Data berhasil diterima")
        
        return jsonify({"message": "Data berhasil diterima"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    client.loop_start() # Mulai thread untuk menangani koneksi MQTT
    app.run(debug=True) # Menjalankan aplikasi Flask
