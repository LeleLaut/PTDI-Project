import mysql.connector

# Fungsi untuk membuat database
def create_database():
    connection = mysql.connector.connect(
        host='localhost',  # Alamat host MySQL
        user='root',       # Username MySQL
        password=''        # Password MySQL
    )
    cursor = connection.cursor()

    # Buat database jika belum ada
    cursor.execute("CREATE DATABASE IF NOT EXISTS flightestdb")

    cursor.close()
    connection.close()

# Fungsi untuk membuat tabel
def create_table():
    connection = mysql.connector.connect(
        host='localhost',  # Alamat host MySQL
        user='root',       # Username MySQL
        password='',       # Password MySQL
        database='flightestdb'  # Nama database yang telah dibuat
    )
    cursor = connection.cursor()

    # Buat tabel jika belum ada
    cursor.execute("CREATE TABLE IF NOT EXISTS android3 ("
                   "id INT AUTO_INCREMENT PRIMARY KEY,"
                   "gyro_x FLOAT,"
                   "gyro_y FLOAT,"
                   "gyro_z FLOAT,"
                   "accel_x FLOAT,"
                   "accel_y FLOAT,"
                   "accel_z FLOAT,"
                   "sumbu_x FLOAT,"
                   "sumbu_y FLOAT,"
                   "sumbu_z FLOAT,"
                   "latitude FLOAT,"
                   "longitude FLOAT"
                   ")")

    cursor.close()
    connection.close()

# Panggil fungsi untuk membuat database dan tabel
create_database()
create_table()
