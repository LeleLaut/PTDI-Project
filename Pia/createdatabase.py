import mysql.connector

def create_database():
    connection = mysql.connector.connect(
        host='localhost',  # Alamat host MySQL
        user='root',       # Username MySQL
        password=''        # Password MySQL
    )
    cursor = connection.cursor()

def create_table():
    connection = mysql.connector.connect(
        host='localhost',  # Alamat host MySQL
        user='root',       # Username MySQL
        password='',       # Password MySQL
        database='flightestdb'  # Nama database
    )
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS arduino ("
                   "id INT AUTO_INCREMENT PRIMARY KEY,"
                   "gyro_x FLOAT,"
                   "gyro_y FLOAT,"
                   "gyro_z FLOAT,"
                   "acc_x FLOAT,"
                   "acc_y FLOAT,"
                   "acc_z FLOAT,"
                   "pitch FLOAT,"
                   "roll FLOAT,"
                   "yaw FLOAT,"
                   "counter FLOAT,"
                   "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"
                   ")")

    cursor.close()
    connection.close()

    print("Tabel berhasil dibuat")

create_database()
create_table()